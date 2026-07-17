<#
.SYNOPSIS
  Scheduled PostgreSQL backup for the CERA Tariff app (local dev environment).

.DESCRIPTION
  Runs pg_dump against the local tariff_app database in custom (-Fc) format,
  writes it into a OneDrive-synced folder (so it lands off this machine
  automatically), and keeps a rolling window of daily + weekly copies so a
  single overwrite or a problem discovered days later is still recoverable.

  This is temporary insurance for the local dev environment only. Once the
  application moves to Azure Database for PostgreSQL Flexible Server, this
  script is superseded by Azure's built-in automated backups (see
  AZURE_DEPLOYMENT_BRIEF_v2.md, Section 8) and can be retired.

  Credentials are read from %APPDATA%\postgresql\pgpass.conf, not embedded
  here or passed on the command line.
#>

$ErrorActionPreference = "Stop"

$PgDump = "C:\Program Files\PostgreSQL\17\bin\pg_dump.exe"
$DbHost = "127.0.0.1"
$DbPort = "5433"
$DbName = "tariff_app"
$DbUser = "postgres"

$BackupRoot = "C:\Users\pkoussi\OneDrive - Cyprus Energy Regulatory Authority\Tariff-App-DB-Backups"
$DailyDir   = Join-Path $BackupRoot "daily"
$WeeklyDir  = Join-Path $BackupRoot "weekly"
$LogFile    = Join-Path $BackupRoot "backup.log"

New-Item -ItemType Directory -Force -Path $DailyDir  | Out-Null
New-Item -ItemType Directory -Force -Path $WeeklyDir | Out-Null

function Write-Log($msg) {
    $line = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')  $msg"
    Write-Output $line
    Add-Content -Path $LogFile -Value $line
}

$Timestamp = Get-Date -Format "yyyy-MM-dd_HHmm"
$FileName  = "tariff_app_$Timestamp.dump"
$DailyPath = Join-Path $DailyDir $FileName

Write-Log "Starting backup -> $DailyPath"

& $PgDump -h $DbHost -p $DbPort -U $DbUser -Fc -f $DailyPath $DbName 2>&1 | ForEach-Object { Write-Log $_ }

if ($LASTEXITCODE -ne 0) {
    Write-Log "ERROR: pg_dump failed with exit code $LASTEXITCODE"
    exit 1
}

$size = (Get-Item $DailyPath).Length
if ($size -eq 0) {
    Write-Log "ERROR: backup file is empty, treating as failed"
    Remove-Item $DailyPath -Force
    exit 1
}
Write-Log "pg_dump succeeded ($size bytes)"

# Keep one copy per week (the first successful run each Monday) in the weekly folder
if ((Get-Date).DayOfWeek -eq 'Monday') {
    Copy-Item -Path $DailyPath -Destination (Join-Path $WeeklyDir $FileName) -Force
    Write-Log "Copied to weekly retention (Monday run)"
}

# Rotate: keep the 14 most recent daily dumps, 8 most recent weekly dumps
$removedDaily = Get-ChildItem $DailyDir -Filter "*.dump" | Sort-Object LastWriteTime -Descending | Select-Object -Skip 14
$removedDaily | Remove-Item -Force
if ($removedDaily) { Write-Log "Pruned $($removedDaily.Count) old daily backup(s)" }

$removedWeekly = Get-ChildItem $WeeklyDir -Filter "*.dump" | Sort-Object LastWriteTime -Descending | Select-Object -Skip 8
$removedWeekly | Remove-Item -Force
if ($removedWeekly) { Write-Log "Pruned $($removedWeekly.Count) old weekly backup(s)" }

Write-Log "Backup complete."

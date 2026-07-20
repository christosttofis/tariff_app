-- Follow-up migration: drop the legacy supplier_name string columns from
-- users and message_reads, now that supplier_id (added by
-- migrate_supplier_fk.sql) is verified working and no code reads the old
-- columns anymore.
--
-- BACK UP THE DATABASE BEFORE RUNNING THIS (tariff-api\scripts\backup_db.ps1).

ALTER TABLE users DROP COLUMN IF EXISTS supplier_name;
ALTER TABLE message_reads DROP COLUMN IF EXISTS supplier_name;

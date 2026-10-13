function esc(s){ return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;'); }
/* ── Language system ── */
const LANG = {
  en: {
    ERR_FIELDS_SUMMARY:'Please correct the highlighted fields ({N}).',
    ERR_F_REQUIRED:'Please enter a value.', ERR_F_MIN:'This cannot be less than {N}.',
    ERR_F_ABOVE:'This must be more than {N}.', ERR_F_MAX:'This cannot be more than {N}.',
    ERR_F_WHOLE:'Please enter a whole number.', ERR_F_TOO_LONG:'Too long: at most {N} characters.',
    ERR_F_NAME:'Please provide the tariff name.', ERR_F_SUPPLIER:'Please choose the supplier.',
    ERR_F_TIER_ORDER:'The limit of each tier must be higher than the one before it.',
    ERR_F_TIER_OPEN:'Only the last tier may be left without a limit (∞).',
    ERR_F_TIER_NEEDED:'A Variable tariff needs at least one tier.',
    ERR_F_DISC_PCT:'Enter a percentage (more than 0, up to 100), or remove this discount.',
    PAGE_TITLE:'CERA Admin',
    // Login
    LOGIN_TITLE:'CERA Admin', LOGIN_SUB:'Sign in to continue',
    LBL_EMAIL:'Email', LBL_PASSWORD:'Password', BTN_SIGNIN:'Sign in',
    LNK_FORGOT:'Forgot password?',
    OTP_TITLE:'Verify your identity', OTP_SUB:'A 6-digit code was sent to your email. Enter it below to continue.',
    OTP_LBL:'Verification code', OTP_BTN:'Verify',
    OTP_RESEND:'Resend code', OTP_RESEND_WAIT:'Resend in {s}s', OTP_RESEND_SENT:'Code resent — check your email.',
    RESET_TITLE:'Reset password', RESET_SUB:'Enter your email to receive a reset link.',
    BTN_SEND_RESET:'Send reset link', LNK_BACK_SIGNIN:'← Back to sign in',
    IDLE_TITLE:'Still there?', IDLE_SUB:"You've been inactive for a while. For security, you'll be signed out soon.", IDLE_STAY:'Stay signed in',
    // Sidebar
    BRAND_LABEL:'Admin Panel', BRAND_TITLE:'Tariff Manager', BRAND_SUB:'Electricity comparison tool',
    NAV_DASHBOARD:'Dashboard',
    NAV_CONFIGURATION:'Configuration', NAV_ADMINISTRATION:'Administration',
    NAV_MARKET_DATA:'Market data', NAV_DEPLOY:'Deploy',
    NAV_SUPPLIERS:'Suppliers', NAV_PROFILES:'Consumption profiles', NAV_TARIFFS:'Tariffs',
    NAV_USERS:'Users', NAV_LOGIN_ACTIVITY:'Login activity', NAV_MESSAGES:'Notifications', NAV_DAM:'DAM price data', NAV_REGULATED:'Regulated tariffs',
    NAV_AUDIT:'Audit calculator', NAV_NOTICES:'Notices', NAV_CHANGELOG:'Changelog', NAV_REPORTS:'Reported issues',
    BTN_MY_ACCOUNT:'My Account', BTN_SIGNOUT:'Sign out',
    // Dashboard pane
    PANE_DASH_TITLE:'Dashboard', PANE_DASH_DESC:'Overview of what needs your attention.',
    DASH_ALL_CAUGHT_UP:'All caught up', DASH_AWAITING_REVIEW:'awaiting your review',
    DASH_NOTHING_PENDING:'Nothing pending — all tariff submissions are reviewed.',
    DASH_FRESHNESS_TITLE:'Regulated charges and FPA',
    DASH_REG_UPDATED:'Regulated charges last updated', DASH_FPA_UPDATED:'FPA prices last updated',
    DASH_NEVER_UPDATED:'never', DASH_UNUSUAL_TITLE:'Unusual activity',
    DASH_FPA_EXPIRED:'Expired, please update from',
    DASH_REG_YEARLY_NOTE:'New year — please review grid usage and universal charges',
    // Suppliers pane
    PANE_SUP_TITLE:'Suppliers', PANE_SUP_DESC:'Manage electricity suppliers in the comparison tool.',
    CARD_SUP_LIST:'Supplier list', BTN_ADD:'+ Add',
    EMPTY_SUPPLIERS:'No suppliers yet.',
    SUP_TARIFFS:'tariff(s)', SUP_NO_CONTACT:'⚠ No contact details', BADGE_REGULATED:'Regulated',
    BTN_EDIT_DETAILS:'✏ Edit details', BTN_REMOVE:'Remove',
    // Profiles pane
    PANE_PROF_TITLE:'Consumption profiles',
    PANE_PROF_DESC:'Paste the DSO profile CSV directly — the transposed format with time rows and month/day-type columns is accepted as-is. Values are normalised automatically.',
    CARD_EAC_FORMAT:'Expected DSO format',
    CARD_ADD_PROF:'Add / replace profile', LBL_PROF_NAME:'Profile name',
    LBL_PROF_DESC:'Description (optional)',
    LBL_PASTE_EAC:'Paste DSO CSV here (copy straight from the spreadsheet)',
    BTN_PARSE_SAVE:'⚡ Parse & save profile', CARD_SAVED_PROF:'Saved profiles',
    EMPTY_PROFILES:'No profiles yet. Paste DSO data above.',
    BTN_RENAME:'✏ Rename', BTN_DELETE:'Delete',
    // Tariffs pane
    PANE_TAR_TITLE:'Tariffs',
    PANE_TAR_DESC:'Each tariff belongs to a supplier, has a contract type, voltage, pricing structure, and an assigned consumption profile.',
    BTN_ADD_TARIFF:'+ Add tariff', CARD_ALL_TARIFFS:'All tariffs',
    LBL_GROUP_BY:'Group by:', BTN_NONE:'None', BTN_SUPPLIER_GRP:'Supplier',
    BTN_PRICING_GRP:'Pricing', BTN_CONTRACT_GRP:'Contract',
    OPT_ALL_SUPPLIERS:'All suppliers', OPT_ALL_PRICING:'All pricing', OPT_ALL_CONTRACTS:'All contracts',
    BTN_CLEAR:'✕ Clear',
    EMPTY_TARIFFS:'No tariffs yet. Click "+ Add tariff".',
    EMPTY_TARIFFS_FILTER:'No tariffs match the current filters.',
    STATUS_LIVE:'● Live', STATUS_PENDING:'⏳ Pending review', STATUS_REJECTED:'✕ Rejected',
    STATUS_DRAFT:'◌ Draft', STATUS_SUSPENDED:'⏸ Suspended', STATUS_ARCHIVED:'▣ Archived by supplier',
    BTN_REVIEW:'🔍 Review', BTN_SUSPEND:'⏸ Suspend', BTN_RESTORE:'▶ Restore', BTN_VIEW:'View',
    // Users pane
    PANE_USERS_TITLE:'User management',
    PANE_USERS_DESC:'Manage supplier portal accounts. Invited users receive an email with a link to set their password.',
    LBL_INVITE_HEADING:'Invite new supplier user', BTN_INVITE:'+ Invite user',
    LBL_ADMINS_HEADING:'Admins', LBL_SUPPLIERS_HEADING:'Suppliers',
    LBL_EMAIL_ADDR:'Email address', LBL_SUPPLIER_SEL:'Supplier', BTN_SEND_INV:'Send invitation',
    TH_EMAIL:'Email', TH_SUPPLIER:'Supplier', TH_STATUS:'Status', TH_2FA:'2FA', TH_ACTIONS:'Actions',
    USERS_LOADING:'Loading…', USERS_EMPTY:'No users yet.', USERS_FAILED:'Failed to load users.',
    // Login activity pane
    PANE_LA_TITLE:'Login activity',
    PANE_LA_DESC:'Recent sign-in attempts across the admin and supplier portals, most recent first.',
    OPT_ALL_RESULTS:'All results', OPT_SUCCESS:'Successful', OPT_FAILED:'Failed', BTN_REFRESH:'↻ Refresh',
    TH_RESULT:'Result', TH_REASON:'Reason', TH_IP:'IP address', TH_USER_AGENT:'Device / browser',
    LA_SUCCESS:'Success', LA_FAILED:'Failed', LA_EMPTY:'No login activity yet.',
    USER_ACTIVE:'Active', USER_INACTIVE:'Inactive',
    BTN_DEACTIVATE:'Deactivate', BTN_ACTIVATE:'Activate', BTN_RESEND_INV:'Resend invite', BTN_DELETE_USER:'Delete',
    OTP_ON_HINT:'2FA enabled — user must enter a code from email at login', OTP_OFF_HINT:'2FA disabled — user logs in with password only',
    // Notifications pane
    PANE_MESSAGES_TITLE:'Notifications',
    PANE_MESSAGES_DESC:'Send a notification to all suppliers or a selected group. Notifications are emailed and shown in the Supplier Portal.',
    MSG_COMPOSE_TITLE:'Compose notification', LBL_SUBJECT:'Subject', LBL_MESSAGE_BODY:'Message', LBL_AUDIENCE:'Audience',
    AUDIENCE_ALL:'All suppliers', AUDIENCE_SELECTED:'Selected suppliers', BTN_SEND_MESSAGE:'Send notification',
    MSG_HISTORY_TITLE:'Notification history', MSG_LOADING:'Loading…',
    SCHED_TITLE:'Scheduled notifications', SCHED_DESC:'Repeats automatically every N months — e.g. remind suppliers to review their tariffs twice a year.',
    BTN_NEW_SCHEDULE:'+ New schedule', LBL_INTERVAL:'Repeat every (months)', LBL_START_DATE:'Start date',
    BTN_SAVE_SCHEDULE:'Save schedule',
    // DAM pane
    PANE_DAM_TITLE:'DAM price data',
    PANE_DAM_DESC:'Shared half-hourly market prices used by all dynamic tariffs.',
    CARD_FORMAT:'Format', CARD_PASTE_DATA:'Paste data',
    LBL_DATA_YEAR:'Data year', LBL_PRICE_UNIT:'Price unit',
    DZ_TITLE:'Drop CSV files here', DZ_SUB:'or click to browse — multiple files supported', BTN_PARSE:'⚡ Parse', BTN_CLEAR_DAM:'Clear', BTN_SAVE_DAM:'💾 Save DAM data',
    COV_NEW:'New — not saved yet', DAM_MISSING:'missing', 
    BTN_DAM_CSV:'⬇ Download CSV (re-uploadable)', BTN_DAM_RESTORE:'Restore', BTN_OPEN_DAM:'Open DAM prices',
    CARD_DAM_HISTORY:'Saved versions (backups)', CARD_DAM_LOG:'Change log',
    DAM_HISTORY_HINT:'Every save is kept. Restore makes an earlier version live again; the current one stays in this list.',
    TH_DAM_VERSION:'Version', TH_DAM_SOURCE:'Source', TH_DAM_RANGE:'Dates', TH_DAM_ROWS:'Half-hours',
    DAM_SRC_INITIAL:'Before versioning', DAM_SRC_UPLOAD:'CSV upload', DAM_SRC_TSOC:'TSOC fetch', DAM_SRC_ROLLBACK:'Restored',
    DAM_ACT_SAVED_UPLOAD:'Saved (CSV upload)', DAM_ACT_SAVED_TSOC:'Saved (TSOC fetch)', DAM_ACT_ROLLBACK:'Restored version',
    DAM_ACT_FETCH_OK:'Fetched (not saved yet)', DAM_ACT_FETCH_CANCELLED:'Fetch cancelled', DAM_ACT_STALE:'Reminder emailed',
    DAM_LIVE:'live', DAM_SYSTEM:'system', DAM_NO_VERSIONS:'No saved versions yet. The current data is backed up automatically on the next save.', DAM_NO_LOG:'No changes recorded yet.',
    
    DAM_HALF_HOURS:'half-hours', 
    DAM_NO_DATA:'No DAM data to download.',
    DAM_CONFIRM_DROP:'This will remove {N} day(s) that are in the saved data ({FROM} to {TO}).\n\nThe current data stays available as a backup version. Save anyway?',
    DAM_CONFIRM_RESTORE:'Make version {V} ({FROM} to {TO}) live again?\n\nThe current data is kept as a version and can be restored later.',
    DAM_RESTORED:'Version {V} restored ✓ — now live as version {N}.',
    DASH_DAM_TITLE:'DAM prices', DASH_DAM_UNTIL:'Prices up to', DASH_DAM_SAVED:'Last change', DASH_DAM_COVERAGE:'Days stored',
    DASH_DAM_NONE:'No data', DASH_DAM_DAYS_OLD:'days old', DASH_DAM_STALE:'more than {N} days old — fetch or upload',
    DASH_DAM_ATTENTION:'DAM prices end on {D} ({N} days ago). Dynamic tariffs use older data.',
    DASH_DAM_ATTENTION_NONE:'No DAM prices are stored. Dynamic tariffs cannot be priced properly.',
    CARD_COV_TITLE:'Data coverage', COV_FULL:'Full', COV_PARTIAL:'Partial', COV_NONE:'No data', COV_BACK:'Back',
    CARD_MONTHLY_AVG:'Monthly averages (€/kWh)',
    BTN_EXP_DAILY:'⬇ Export daily CSV', BTN_EXP_SLOT:'⬇ Export slot averages', BTN_EXP_MONTHLY:'⬇ Export monthly averages',
    CARD_PRICE_EXPLORER:'Price explorer',
    // Regulated pane
    PANE_REG_TITLE:'Regulated tariffs',
    PANE_REG_DESC:'Regulated charges set by CERA that apply on top of all supplier tariffs. Grid usage is voltage-specific; all other charges apply to every tariff.',
    REG_LAST_UPDATED:'Last updated: {dt}',
    CARD_HOW_APPLIED:'ℹ How these are applied',
    CARD_GRID_USAGE:'⚡ Grid usage charges (€/kWh) — voltage specific',
    CARD_FPA:'🛢 Fuel Price Adjustment — FPA reference rates (€/kWh)',
    CARD_FPA_UPDATE_FROM:'Update from:',
    CARD_UNIVERSAL:'🌐 Universal charges — all tariffs & voltage levels',
    CARD_REG_PREVIEW:'🔍 Preview — regulated cost for reference consumption',
    LBL_LV_GRID:'LV grid usage (€/kWh)', LBL_MV_GRID:'MV grid usage (€/kWh)', LBL_HV_GRID:'HV grid usage (€/kWh)',
    LBL_LV_FPA:'LV — FPA (€/kWh)', LBL_MV_FPA:'MV — FPA (€/kWh)', LBL_HV_FPA:'HV — FPA (€/kWh)',
    LBL_PSO:'Public Service Obligations — PSO (€/kWh)',
    LBL_RES:'RES and Energy Conservation Fund (€/kWh)',
    LBL_REG_MDM:'Meter Data Management — MDM (€ per invoice)',
    HINT_REG_MDM:"Fixed MDM rate for regulated suppliers' tariffs (e.g. EAC) — charged once per invoice. Each tariff's own invoicing frequency (Tariffs tab) sets the annual total.",
    LBL_REF_KWH:'Reference annual consumption (kWh)', LBL_VOLTAGE_LVL:'Voltage level',
    // Audit pane
    PANE_AUDIT_TITLE:'Audit calculator',
    PANE_AUDIT_DESC:'Step-by-step cost breakdown for any tariff, using the same rules as the customer page: the first 12 months after switching (from next month), with discounts. Fixed/ToU/Dynamic: half-hourly for the selected month. Variable: all billing periods. Each run is checked against the customer page.',
    CARD_INPUTS:'Inputs', LBL_TARIFF_SEL:'Tariff', LBL_ANNUAL_KWH:'Annual consumption (kWh)', LBL_MONTH:'Month',
    BTN_RUN_AUDIT:'▶ Run audit', CARD_MONTH_SUMMARY:'Month summary',
    MONTH_0:'January', MONTH_1:'February', MONTH_2:'March', MONTH_3:'April',
    MONTH_4:'May', MONTH_5:'June', MONTH_6:'July', MONTH_7:'August',
    MONTH_8:'September', MONTH_9:'October', MONTH_10:'November', MONTH_11:'December',
    // Notices pane
    PANE_NOTICES_TITLE:'Assumptions & Notices',
    PANE_NOTICES_DESC:'This content appears as a popup on the customer calculator. Use it to document calculation assumptions and provide legal notices. Click "Save notices" below to publish changes.',
    BTN_SAVE_NOTICES:'💾 Save notices',
    CARD_SAMPLE_INVOICE:'Sample invoice',
    LBL_SAMPLE_INVOICE_ENABLE:'Enable sample invoice on customer calculator',
    DESC_SAMPLE_INVOICE_ENABLE:"Shows a bill-styled cost breakdown with explanations for each tariff, based on the customer's own inputs. Disable if it causes display issues.",
    CARD_FMT_TOOLBAR:'Formatting toolbar',
    CARD_ASSUMPTIONS:'Assumptions', CARD_LEGAL:'Legal notices',
    CARD_VULNERABLE:'🛡 Vulnerable consumer / social tariff — eligible cases',
    // Changelog pane
    PANE_CHANGELOG_TITLE:'Changelog',
    PANE_CHANGELOG_DESC:'Full audit log of all tariff creates, updates, and deletes. Timestamps are local time.',
    OPT_ALL_ACTIONS:'All actions', OPT_CREATED:'Created', OPT_UPDATED:'Updated', OPT_DELETED:'Deleted',
    OPT_ALL_SUPPLIERS:'All suppliers',
    BTN_EXPORT_CSV:'⬇ Export CSV',
    TH_TIMESTAMP:'Timestamp', TH_TARIFF_CL:'Tariff', TH_SUPPLIER_CL:'User', TH_ACTOR:'Made by', TH_ACTION:'Action', TH_CHANGES:'Changes',
    CL_ACTOR_ADMIN:'CERA Admin', CL_ACTOR_SUPPLIER:'Supplier',
    CL_EMPTY:'No changelog entries yet. Changes to tariffs will appear here.',
    // Reports pane
    PANE_REPORTS_TITLE:'Reported issues',
    PANE_REPORTS_DESC:'Issues customers have flagged about published tariff information, via the "Report an issue" link on the comparison tool.',
    OPT_ALL_STATUSES:'All statuses', OPT_STATUS_OPEN:'Open', OPT_STATUS_REVIEWED:'Reviewed', OPT_STATUS_RESOLVED:'Resolved', OPT_STATUS_DISMISSED:'Dismissed',
    TH_REPORTED_AT:'Reported', TH_TARIFF_RP:'Tariff', TH_SUPPLIER_RP:'Supplier', TH_CATEGORY_RP:'Category', TH_NOTE:'Note', TH_STATUS:'Status', TH_ACTIONS:'Actions',
    BTN_MARK_REVIEWED:'Mark reviewed', BTN_MARK_RESOLVED:'Mark resolved', BTN_DISMISS:'Dismiss', BTN_REOPEN:'Reopen',
    RP_CAT_INCORRECT_PRICE:'Incorrect price', RP_CAT_TERMS_MISMATCH:'Terms mismatch', RP_CAT_BROKEN_LINK:'Broken link', RP_CAT_OTHER:'Other',
    RP_LBL_REPORTER:'Reporter', RP_LBL_RESOLUTION:'Resolution', RP_OVERDUE:'⚠ Overdue', RP_ADMIN_NOTE_PROMPT:'Add a resolution note (optional):',
    RP_GENERAL_ISSUE:'General site issue',
    RP_EMPTY:'No reported issues yet.',
    // Publish pane
    BTN_SAVE_REG:'💾 Save regulated charges', BTN_REG_HISTORY:'📈 History',
    MODAL_REG_HISTORY_FPA:'Regulated charges history — FPA trend',
    MODAL_REG_HISTORY_GRID:'Regulated charges history — Grid usage trend',
    MODAL_REG_HISTORY_UNIVERSAL:'Regulated charges history — Universal charges trend',
    REG_HIST_SHOW_ALL:'Show all history (instead of last 12 months)',
    REG_HIST_COL_MONTH:'Month', REG_HIST_COL_FPA_LV:'FPA — LV', REG_HIST_COL_FPA_MV:'FPA — MV', REG_HIST_COL_FPA_HV:'FPA — HV',
    REG_HIST_COL_LV:'LV grid usage', REG_HIST_COL_MV:'MV grid usage', REG_HIST_COL_HV:'HV grid usage',
    REG_HIST_COL_PSO:'PSO', REG_HIST_COL_RES:'RES & Energy Conservation Fund',
    // Tariff editor modal
    MODAL_ADD_TARIFF:'Add tariff', MODAL_EDIT_TARIFF:'Edit tariff', MODAL_VIEW_TARIFF:'View tariff',
    BTN_SAVE_TARIFF:'Save tariff', BTN_EDIT_TARIFF_BTN:'Edit tariff', BTN_DELETE_TARIFF:'Delete tariff',
    BTN_CANCEL:'Cancel', BTN_CLOSE:'Close',
    // Review modal
    MODAL_REVIEW_TARIFF:'Review tariff',
    BTN_APPROVE:'✓ Approve', BTN_REJECT:'✕ Reject',
    BTN_CONFIRM_REJECT:'Confirm Rejection', BTN_CANCEL_REJECT:'Cancel',
    LBL_REJECT_REASON:'Select a reason for rejection:',
    // Account modal
    ACCT_TITLE:'My Account', ACCT_CHANGE_EMAIL:'Change email',
    LBL_CURRENT_EMAIL:'Current email', LBL_NEW_EMAIL:'New email', BTN_UPDATE_EMAIL:'Update email',
    ACCT_CHANGE_PW:'Change password', LBL_CURRENT_PW:'Current password',
    LBL_NEW_PW:'New password', LBL_CONFIRM_PW:'Confirm new password', BTN_UPDATE_PW:'Update password',
    // Supplier detail modal
    SUP_MODAL_TITLE:'Supplier details', LBL_COMPANY_NAME:'Company / Supplier name',
    LBL_LICENCE:'CERA Licence No.', LBL_ADDRESS:'Company address',
    LBL_WEBSITE:'Website', LBL_TEL_NO:'Telephone',
    LBL_SUP_REGULATED:'Regulated supplier',
    BTN_SAVE_DETAILS:'Save details',
    REG_CONFIRM_TITLE:'Change regulated status?', BTN_CONFIRM_CHANGE:'Confirm change',
    REG_CHANGE_TITLE:'Please check these values', REG_CHANGE_QUESTION:'Is this correct?', BTN_CONFIRM:'Confirm',
    REG_CHANGE_PCT:'The {F} value is now {P}% {D} than the previous one ({OLD} → {NEW}).',
    REG_CHANGE_HIGHER:'higher', REG_CHANGE_LOWER:'lower',
    REG_CHANGE_FROM_ZERO:'The {F} value was 0 and is now {NEW}.',
    REG_FPA_ORDER:'The FPA rates are not in the usual order LV > MV > HV (LV {LV}, MV {MV}, HV {HV}).',
    REG_NOT_SAVED:'Not saved.',
    ERR_REG_GRID_ORDER:'Grid usage must fall with voltage: LV > MV > HV.',
    REG_F_lv:'LV grid usage', REG_F_mv:'MV grid usage', REG_F_hv:'HV grid usage',
    REG_F_fpaLV:'LV FPA', REG_F_fpaMV:'MV FPA', REG_F_fpaHV:'HV FPA',
    REG_F_pso:'PSO', REG_F_res:'RES', REG_F_mdm:'MDM',
    // Admin docs modal
    ADOCS_TITLE_PREFIX:'Documents — ',
  },
  el: {
    ERR_FIELDS_SUMMARY:'Παρακαλώ διορθώστε τα επισημασμένα πεδία ({N}).',
    ERR_F_REQUIRED:'Παρακαλώ συμπληρώστε τιμή.', ERR_F_MIN:'Η τιμή δεν μπορεί να είναι μικρότερη από {N}.',
    ERR_F_ABOVE:'Η τιμή πρέπει να είναι μεγαλύτερη από {N}.', ERR_F_MAX:'Η τιμή δεν μπορεί να είναι μεγαλύτερη από {N}.',
    ERR_F_WHOLE:'Παρακαλώ εισάγετε ακέραιο αριθμό.', ERR_F_TOO_LONG:'Πολύ μεγάλο κείμενο: έως {N} χαρακτήρες.',
    ERR_F_NAME:'Παρακαλώ δώστε το όνομα της διατίμησης.', ERR_F_SUPPLIER:'Παρακαλώ επιλέξτε προμηθευτή.',
    ERR_F_TIER_ORDER:'Το όριο κάθε κλίμακας πρέπει να είναι μεγαλύτερο από το προηγούμενο.',
    ERR_F_TIER_OPEN:'Μόνο η τελευταία κλίμακα μπορεί να μείνει χωρίς όριο (∞).',
    ERR_F_TIER_NEEDED:'Η κλιμακωτή διατίμηση χρειάζεται τουλάχιστον μία κλίμακα.',
    ERR_F_DISC_PCT:'Εισάγετε ποσοστό (πάνω από 0, έως 100) ή αφαιρέστε αυτή την έκπτωση.',
    PAGE_TITLE:'ΡΑΕΚ Admin',
    // Login
    LOGIN_TITLE:'ΡΑΕΚ Admin', LOGIN_SUB:'Εισέλθετε για να συνεχίσετε',
    LBL_EMAIL:'Email', LBL_PASSWORD:'Κωδικός', BTN_SIGNIN:'Είσοδος',
    LNK_FORGOT:'Ξεχάσατε τον κωδικό;',
    OTP_TITLE:'Επαλήθευση ταυτότητας', OTP_SUB:'Στάλθηκε εξαψήφιος κωδικός στο email σας. Εισαγάγετέ τον παρακάτω.',
    OTP_LBL:'Κωδικός επαλήθευσης', OTP_BTN:'Επαλήθευση',
    OTP_RESEND:'Επαναποστολή κωδικού', OTP_RESEND_WAIT:'Επαναποστολή σε {s}δ', OTP_RESEND_SENT:'Ο κωδικός εστάλη ξανά — ελέγξτε το email σας.',
    RESET_TITLE:'Επαναφορά κωδικού', RESET_SUB:'Εισάγετε το email σας για να λάβετε σύνδεσμο επαναφοράς.',
    BTN_SEND_RESET:'Αποστολή συνδέσμου', LNK_BACK_SIGNIN:'← Επιστροφή στην είσοδο',
    IDLE_TITLE:'Είστε ακόμα εκεί;', IDLE_SUB:'Δεν έχετε δραστηριότητα για λίγη ώρα. Για λόγους ασφαλείας, θα αποσυνδεθείτε σύντομα.', IDLE_STAY:'Παραμονή συνδεδεμένος',
    // Sidebar
    BRAND_LABEL:'Πίνακας Διαχείρισης', BRAND_TITLE:'Διαχείριση Διατιμήσεων', BRAND_SUB:'Εργαλείο σύγκρισης διατιμήσεων ηλεκτρισμού',
    NAV_DASHBOARD:'Πίνακας ελέγχου',
    NAV_CONFIGURATION:'Διαμόρφωση', NAV_ADMINISTRATION:'Διαχείριση',
    NAV_MARKET_DATA:'Δεδομένα αγοράς', NAV_DEPLOY:'Ανάπτυξη',
    NAV_SUPPLIERS:'Προμηθευτές', NAV_PROFILES:'Προφίλ κατανάλωσης', NAV_TARIFFS:'Διατιμήσεις',
    NAV_USERS:'Χρήστες', NAV_LOGIN_ACTIVITY:'Δραστηριότητα σύνδεσης', NAV_MESSAGES:'Ειδοποιήσεις', NAV_DAM:'Δεδομένα ΠΗΑ', NAV_REGULATED:'Ρυθμιζόμενες διατιμήσεις',
    NAV_AUDIT:'Έλεγχος υπολογισμού διατιμήσεων', NAV_NOTICES:'Ανακοινώσεις', NAV_CHANGELOG:'Ιστορικό αλλαγών', NAV_REPORTS:'Αναφορές προβλημάτων',
    BTN_MY_ACCOUNT:'Ο λογαριασμός μου', BTN_SIGNOUT:'Αποσύνδεση',
    // Dashboard pane
    PANE_DASH_TITLE:'Πίνακας ελέγχου', PANE_DASH_DESC:'Επισκόπηση όσων απαιτούν την προσοχή σας.',
    DASH_ALL_CAUGHT_UP:'Όλα ενημερωμένα', DASH_AWAITING_REVIEW:'εκκρεμούν προς έλεγχο',
    DASH_NOTHING_PENDING:'Καμία εκκρεμότητα — όλες οι υποβολές διατιμήσεων έχουν ελεγχθεί.',
    DASH_FRESHNESS_TITLE:'Ρυθμιζόμενες χρεώσεις και FPA',
    DASH_REG_UPDATED:'Τελευταία ενημέρωση ρυθμιζόμενων χρεώσεων', DASH_FPA_UPDATED:'Τελευταία ενημέρωση τιμών FPA',
    DASH_NEVER_UPDATED:'ποτέ', DASH_UNUSUAL_TITLE:'Ασυνήθιστη δραστηριότητα',
    DASH_FPA_EXPIRED:'Έληξε, παρακαλώ ενημερώστε από',
    DASH_REG_YEARLY_NOTE:'Νέος χρόνος — παρακαλώ ελέγξτε τις χρεώσεις δικτύου και τις οικουμενικές χρεώσεις',
    // Suppliers pane
    PANE_SUP_TITLE:'Προμηθευτές', PANE_SUP_DESC:'Διαχείριση προμηθευτών ηλεκτρισμού στο εργαλείο σύγκρισης.',
    CARD_SUP_LIST:'Λίστα προμηθευτών', BTN_ADD:'+ Προσθήκη',
    EMPTY_SUPPLIERS:'Δεν υπάρχουν προμηθευτές ακόμα.',
    SUP_TARIFFS:'τιμολόγιο(-α)', SUP_NO_CONTACT:'⚠ Χωρίς στοιχεία επικοινωνίας', BADGE_REGULATED:'Ρυθμιζόμενος',
    BTN_EDIT_DETAILS:'✏ Επεξεργασία', BTN_REMOVE:'Αφαίρεση',
    // Profiles pane
    PANE_PROF_TITLE:'Προφίλ κατανάλωσης',
    PANE_PROF_DESC:'Επικολλήστε το CSV προφίλ ΔΣΔ απευθείας — η μεταφερμένη μορφή με χρονικές γραμμές και στήλες μήνα/ημερότυπου γίνεται αποδεκτή ως έχει. Οι τιμές κανονικοποιούνται αυτόματα.',
    CARD_EAC_FORMAT:'Αναμενόμενη μορφή ΔΣΔ',
    CARD_ADD_PROF:'Προσθήκη / αντικατάσταση προφίλ', LBL_PROF_NAME:'Όνομα προφίλ',
    LBL_PROF_DESC:'Περιγραφή (προαιρετικό)',
    LBL_PASTE_EAC:'Επικολλήστε το CSV του ΔΣΔ εδώ',
    BTN_PARSE_SAVE:'⚡ Ανάλυση & αποθήκευση', CARD_SAVED_PROF:'Αποθηκευμένα προφίλ',
    EMPTY_PROFILES:'Δεν υπάρχουν προφίλ ακόμα. Επικολλήστε δεδομένα ΔΣΔ παραπάνω.',
    BTN_RENAME:'✏ Μετονομασία', BTN_DELETE:'Διαγραφή',
    // Tariffs pane
    PANE_TAR_TITLE:'Διατιμήσεις',
    PANE_TAR_DESC:'Κάθε διατίμηση ανήκει σε προμηθευτή, έχει τύπο σύμβασης, τάση, δομή τιμολόγησης και ανατεθειμένο προφίλ κατανάλωσης.',
    BTN_ADD_TARIFF:'+ Προσθήκη διατίμησης', CARD_ALL_TARIFFS:'Όλες οι διατιμήσεις',
    LBL_GROUP_BY:'Ομαδοποίηση:', BTN_NONE:'Καμία', BTN_SUPPLIER_GRP:'Προμηθευτής',
    BTN_PRICING_GRP:'Διατίμηση', BTN_CONTRACT_GRP:'Σύμβαση',
    OPT_ALL_SUPPLIERS:'Όλοι οι προμηθευτές', OPT_ALL_PRICING:'Όλες οι διατιμήσεις', OPT_ALL_CONTRACTS:'Όλες οι συμβάσεις',
    BTN_CLEAR:'✕ Εκκαθάριση',
    EMPTY_TARIFFS:'Δεν υπάρχουν διατιμήσεις ακόμα. Κάντε κλικ στο "+ Προσθήκη διατίμησης".',
    EMPTY_TARIFFS_FILTER:'Καμία διατίμηση δεν ταιριάζει με τα τρέχοντα φίλτρα.',
    STATUS_LIVE:'● Ενεργό', STATUS_PENDING:'⏳ Σε αναμονή αξιολόγησης', STATUS_REJECTED:'✕ Απορρίφθηκε',
    STATUS_DRAFT:'◌ Πρόχειρο', STATUS_SUSPENDED:'⏸ Ανεσταλμένο', STATUS_ARCHIVED:'▣ Αρχειοθετήθηκε από προμηθευτή',
    BTN_REVIEW:'🔍 Αξιολόγηση', BTN_SUSPEND:'⏸ Αναστολή', BTN_RESTORE:'▶ Επαναφορά', BTN_VIEW:'Προβολή',
    // Users pane
    PANE_USERS_TITLE:'Διαχείριση χρηστών',
    PANE_USERS_DESC:'Διαχείριση λογαριασμών πύλης προμηθευτών. Οι προσκεκλημένοι χρήστες λαμβάνουν email με σύνδεσμο ορισμού κωδικού.',
    LBL_INVITE_HEADING:'Πρόσκληση νέου χρήστη προμηθευτή', BTN_INVITE:'+ Πρόσκληση',
    LBL_ADMINS_HEADING:'Διαχειριστές', LBL_SUPPLIERS_HEADING:'Προμηθευτές',
    LBL_EMAIL_ADDR:'Διεύθυνση email', LBL_SUPPLIER_SEL:'Προμηθευτής', BTN_SEND_INV:'Αποστολή πρόσκλησης',
    TH_EMAIL:'Email', TH_SUPPLIER:'Προμηθευτής', TH_STATUS:'Κατάσταση', TH_2FA:'2FA', TH_ACTIONS:'Ενέργειες',
    USERS_LOADING:'Φόρτωση…', USERS_EMPTY:'Δεν υπάρχουν χρήστες ακόμα.', USERS_FAILED:'Αποτυχία φόρτωσης χρηστών.',
    // Login activity pane
    PANE_LA_TITLE:'Δραστηριότητα σύνδεσης',
    PANE_LA_DESC:'Πρόσφατες προσπάθειες σύνδεσης στις πύλες διαχειριστών και προμηθευτών, με την πιο πρόσφατη πρώτη.',
    OPT_ALL_RESULTS:'Όλα τα αποτελέσματα', OPT_SUCCESS:'Επιτυχείς', OPT_FAILED:'Αποτυχημένες', BTN_REFRESH:'↻ Ανανέωση',
    TH_RESULT:'Αποτέλεσμα', TH_REASON:'Αιτία', TH_IP:'Διεύθυνση IP', TH_USER_AGENT:'Συσκευή / πρόγραμμα περιήγησης',
    LA_SUCCESS:'Επιτυχία', LA_FAILED:'Αποτυχία', LA_EMPTY:'Δεν υπάρχει δραστηριότητα σύνδεσης ακόμα.',
    USER_ACTIVE:'Ενεργός', USER_INACTIVE:'Ανενεργός',
    BTN_DEACTIVATE:'Απενεργοποίηση', BTN_ACTIVATE:'Ενεργοποίηση', BTN_RESEND_INV:'Επαναποστολή', BTN_DELETE_USER:'Διαγραφή',
    OTP_ON_HINT:'2FA ενεργό — ο χρήστης πρέπει να εισαγάγει κωδικό email κατά τη σύνδεση', OTP_OFF_HINT:'2FA ανενεργό — ο χρήστης συνδέεται μόνο με κωδικό πρόσβασης',
    // Notifications pane
    PANE_MESSAGES_TITLE:'Ειδοποιήσεις',
    PANE_MESSAGES_DESC:'Στείλτε ειδοποίηση σε όλους τους προμηθευτές ή σε επιλεγμένη ομάδα. Οι ειδοποιήσεις αποστέλλονται με email και εμφανίζονται στην Πύλη Προμηθευτών.',
    MSG_COMPOSE_TITLE:'Σύνταξη ειδοποίησης', LBL_SUBJECT:'Θέμα', LBL_MESSAGE_BODY:'Μήνυμα', LBL_AUDIENCE:'Αποδέκτες',
    AUDIENCE_ALL:'Όλοι οι προμηθευτές', AUDIENCE_SELECTED:'Επιλεγμένοι προμηθευτές', BTN_SEND_MESSAGE:'Αποστολή ειδοποίησης',
    MSG_HISTORY_TITLE:'Ιστορικό ειδοποιήσεων', MSG_LOADING:'Φόρτωση…',
    SCHED_TITLE:'Προγραμματισμένες ειδοποιήσεις', SCHED_DESC:'Επαναλαμβάνεται αυτόματα κάθε Ν μήνες — π.χ. υπενθύμιση στους προμηθευτές να επανεξετάσουν τις διατιμήσεις τους δύο φορές τον χρόνο.',
    BTN_NEW_SCHEDULE:'+ Νέο πρόγραμμα', LBL_INTERVAL:'Επανάληψη κάθε (μήνες)', LBL_START_DATE:'Ημερομηνία έναρξης',
    BTN_SAVE_SCHEDULE:'Αποθήκευση προγράμματος',
    // DAM pane
    PANE_DAM_TITLE:'Δεδομένα τιμών ΠΗΑ',
    PANE_DAM_DESC:'Κοινές τιμές αγοράς ανά μισάωρο που χρησιμοποιούνται από όλα τις δυναμικές διατιμήσεις.',
    CARD_FORMAT:'Μορφή', CARD_PASTE_DATA:'Επικόλληση δεδομένων',
    LBL_DATA_YEAR:'Έτος δεδομένων', LBL_PRICE_UNIT:'Μονάδα τιμής',
    DZ_TITLE:'Σύρτε αρχεία CSV εδώ', DZ_SUB:'ή κάντε κλικ για αναζήτηση — υποστηρίζονται πολλαπλά αρχεία', BTN_PARSE:'⚡ Ανάλυση', BTN_CLEAR_DAM:'Εκκαθάριση', BTN_SAVE_DAM:'💾 Αποθήκευση δεδομένων ΠΗΑ',
    COV_NEW:'Νέα — δεν έχει αποθηκευτεί', DAM_MISSING:'λείπει', 
    BTN_DAM_CSV:'⬇ Λήψη CSV (για επαναφόρτωση)', BTN_DAM_RESTORE:'Επαναφορά', BTN_OPEN_DAM:'Άνοιγμα τιμών ΠΗΑ',
    CARD_DAM_HISTORY:'Αποθηκευμένες εκδόσεις (αντίγραφα ασφαλείας)', CARD_DAM_LOG:'Αρχείο αλλαγών',
    DAM_HISTORY_HINT:'Κάθε αποθήκευση διατηρείται. Η επαναφορά κάνει ενεργή μια παλαιότερη έκδοση· η τρέχουσα παραμένει στη λίστα.',
    TH_DAM_VERSION:'Έκδοση', TH_DAM_SOURCE:'Προέλευση', TH_DAM_RANGE:'Ημερομηνίες', TH_DAM_ROWS:'Ημίωρα',
    DAM_SRC_INITIAL:'Πριν τις εκδόσεις', DAM_SRC_UPLOAD:'Φόρτωση CSV', DAM_SRC_TSOC:'Ανάκτηση ΔΣΜΚ', DAM_SRC_ROLLBACK:'Επαναφορά',
    DAM_ACT_SAVED_UPLOAD:'Αποθήκευση (φόρτωση CSV)', DAM_ACT_SAVED_TSOC:'Αποθήκευση (ανάκτηση ΔΣΜΚ)', DAM_ACT_ROLLBACK:'Επαναφορά έκδοσης',
    DAM_ACT_FETCH_OK:'Ανάκτηση (χωρίς αποθήκευση)', DAM_ACT_FETCH_CANCELLED:'Ακύρωση ανάκτησης', DAM_ACT_STALE:'Στάλθηκε υπενθύμιση',
    DAM_LIVE:'ενεργή', DAM_SYSTEM:'σύστημα', DAM_NO_VERSIONS:'Δεν υπάρχουν ακόμη εκδόσεις. Τα τρέχοντα δεδομένα θα αποθηκευτούν αυτόματα ως αντίγραφο στην επόμενη αποθήκευση.', DAM_NO_LOG:'Δεν έχουν καταγραφεί αλλαγές.',
    
    DAM_HALF_HOURS:'ημίωρα', 
    DAM_NO_DATA:'Δεν υπάρχουν δεδομένα ΠΗΑ για λήψη.',
    DAM_CONFIRM_DROP:'Θα αφαιρεθούν {N} ημέρα(ες) που υπάρχουν στα αποθηκευμένα δεδομένα ({FROM} έως {TO}).\n\nΤα τρέχοντα δεδομένα παραμένουν ως αντίγραφο ασφαλείας. Αποθήκευση;',
    DAM_CONFIRM_RESTORE:'Να γίνει ξανά ενεργή η έκδοση {V} ({FROM} έως {TO});\n\nΤα τρέχοντα δεδομένα διατηρούνται ως έκδοση και μπορούν να επανέλθουν.',
    DAM_RESTORED:'Η έκδοση {V} επανήλθε ✓ — ενεργή ως έκδοση {N}.',
    DASH_DAM_TITLE:'Τιμές ΠΗΑ', DASH_DAM_UNTIL:'Τιμές έως', DASH_DAM_SAVED:'Τελευταία αλλαγή', DASH_DAM_COVERAGE:'Αποθηκευμένες ημέρες',
    DASH_DAM_NONE:'Χωρίς δεδομένα', DASH_DAM_DAYS_OLD:'ημέρες πριν', DASH_DAM_STALE:'παλαιότερες από {N} ημέρες — ανάκτηση ή φόρτωση',
    DASH_DAM_ATTENTION:'Οι τιμές ΠΗΑ φτάνουν έως {D} ({N} ημέρες πριν). Οι δυναμικές χρεώσεις χρησιμοποιούν παλαιότερα δεδομένα.',
    DASH_DAM_ATTENTION_NONE:'Δεν υπάρχουν αποθηκευμένες τιμές ΠΗΑ. Οι δυναμικές χρεώσεις δεν μπορούν να υπολογιστούν σωστά.',
    CARD_COV_TITLE:'Κάλυψη δεδομένων', COV_FULL:'Πλήρης', COV_PARTIAL:'Μερική', COV_NONE:'Κανένα δεδομένο', COV_BACK:'Πίσω',
    CARD_MONTHLY_AVG:'Μηνιαίοι μέσοι όροι (€/kWh)',
    BTN_EXP_DAILY:'⬇ Εξαγωγή ημερήσιο CSV', BTN_EXP_SLOT:'⬇ Εξαγωγή μέσους ανά slot', BTN_EXP_MONTHLY:'⬇ Εξαγωγή μηνιαίους μέσους',
    CARD_PRICE_EXPLORER:'Εξερεύνηση τιμών',
    // Regulated pane
    PANE_REG_TITLE:'Ρυθμιζόμενες διατιμήσεις',
    PANE_REG_DESC:'Ρυθμιζόμενες χρεώσεις από τη ΡΑΕΚ που εφαρμόζονται επιπλέον όλων των διατιμήσεων των προμηθευτών. Η χρήση δικτύου εξαρτάται από την τάση· οι υπόλοιπες χρεώσεις ισχύουν για κάθε διατίμηση.',
    REG_LAST_UPDATED:'Τελευταία ενημέρωση: {dt}',
    CARD_HOW_APPLIED:'ℹ Πώς εφαρμόζονται',
    CARD_GRID_USAGE:'⚡ Χρεώσεις χρήσης δικτύου (€/kWh) — ανά τάση',
    CARD_FPA:'🛢 Αναπροσαρμογή καυσίμου — τιμές αναφοράς (€/kWh)',
    CARD_FPA_UPDATE_FROM:'Ενημέρωση από:',
    CARD_UNIVERSAL:'🌐 Καθολικές χρεώσεις — όλα τα τιμολόγια & επίπεδα τάσης',
    CARD_REG_PREVIEW:'🔍 Προεπισκόπηση — ρυθμιζόμενο κόστος για κατανάλωση αναφοράς',
    LBL_LV_GRID:'Χρήση δικτύου ΧΤ (€/kWh)', LBL_MV_GRID:'Χρήση δικτύου ΜΤ (€/kWh)', LBL_HV_GRID:'Χρήση δικτύου ΥΤ (€/kWh)',
    LBL_LV_FPA:'ΧΤ — FPA (€/kWh)', LBL_MV_FPA:'ΜΤ — FPA (€/kWh)', LBL_HV_FPA:'ΥΤ — FPA (€/kWh)',
    LBL_PSO:'Υποχρεώσεις Παροχής Υπηρεσιών — ΥΠΥ (€/kWh)',
    LBL_RES:'Ταμείο ΑΠΕ & ΕΞΕ (€/kWh)',
    LBL_REG_MDM:'Διαχείριση Μετρητικών Δεδομένων — MDM (€ ανά λογαριασμό)',
    HINT_REG_MDM:'Σταθερή χρέωση MDM για διατιμήσεις ρυθμιζόμενων προμηθευτών (π.χ. ΑΗΚ) — χρεώνεται μία φορά ανά λογαριασμό. Η συχνότητα τιμολόγησης κάθε διατίμησης (καρτέλα Τιμολόγια) καθορίζει το ετήσιο σύνολο.',
    LBL_REF_KWH:'Κατανάλωση αναφοράς (kWh/έτος)', LBL_VOLTAGE_LVL:'Επίπεδο τάσης',
    // Audit pane
    PANE_AUDIT_TITLE:'Ελεγχος υπολογισμού διατιμήσεων',
    PANE_AUDIT_DESC:'Αναλυτική κατανομή κόστους για οποιαδήποτε διατίμηση, με τους ίδιους κανόνες όπως η σελίδα πελατών: οι πρώτοι 12 μήνες μετά την αλλαγή (από τον επόμενο μήνα), με εκπτώσεις. Κάθε υπολογισμός ελέγχεται έναντι της σελίδας πελατών.',
    CARD_INPUTS:'Δεδομένα εισόδου', LBL_TARIFF_SEL:'Διατίμηση', LBL_ANNUAL_KWH:'Ετήσια κατανάλωση (kWh)', LBL_MONTH:'Μήνας',
    BTN_RUN_AUDIT:'▶ Εκτέλεση ελέγχου', CARD_MONTH_SUMMARY:'Σύνοψη μήνα',
    MONTH_0:'Ιανουάριος', MONTH_1:'Φεβρουάριος', MONTH_2:'Μάρτιος', MONTH_3:'Απρίλιος',
    MONTH_4:'Μάιος', MONTH_5:'Ιούνιος', MONTH_6:'Ιούλιος', MONTH_7:'Αύγουστος',
    MONTH_8:'Σεπτέμβριος', MONTH_9:'Οκτώβριος', MONTH_10:'Νοέμβριος', MONTH_11:'Δεκέμβριος',
    // Notices pane
    PANE_NOTICES_TITLE:'Σημειώσεις & Αποποιήσεις Ευθυνών',
    PANE_NOTICES_DESC:'Αυτό το περιεχόμενο εμφανίζεται ως αναδυόμενο παράθυρο στην αριθμομηχανή. Χρησιμοποιήστε το για να τεκμηριώσετε υπολογιστικές παραδοχές και νομικές ανακοινώσεις. Πατήστε «Αποθήκευση ανακοινώσεων» παρακάτω για δημοσίευση.',
    BTN_SAVE_NOTICES:'💾 Αποθήκευση ανακοινώσεων',
    CARD_SAMPLE_INVOICE:'Δείγμα λογαριασμού',
    LBL_SAMPLE_INVOICE_ENABLE:'Ενεργοποίηση δείγματος λογαριασμού στην αριθμομηχανή πελατών',
    DESC_SAMPLE_INVOICE_ENABLE:'Εμφανίζει ανάλυση κόστους σε μορφή λογαριασμού με επεξηγήσεις για κάθε τιμολόγιο, βάσει των στοιχείων που εισήγαγε ο πελάτης. Απενεργοποιήστε το αν προκαλεί προβλήματα εμφάνισης.',
    CARD_FMT_TOOLBAR:'Γραμμή μορφοποίησης',
    CARD_ASSUMPTIONS:'Σημειώσεις', CARD_LEGAL:'Αποποιήσεις Ευθυνών',
    CARD_VULNERABLE:'🛡 Ευάλωτοι καταναλωτές / κοινωνικό τιμολόγιο',
    // Changelog pane
    PANE_CHANGELOG_TITLE:'Ιστορικό αλλαγών',
    PANE_CHANGELOG_DESC:'Πλήρες αρχείο καταγραφής δημιουργιών, ενημερώσεων και διαγραφών τιμολογίων. Οι χρονοσφραγίδες είναι τοπικής ώρας.',
    OPT_ALL_ACTIONS:'Όλες οι ενέργειες', OPT_CREATED:'Δημιουργήθηκε', OPT_UPDATED:'Ενημερώθηκε', OPT_DELETED:'Διαγράφηκε',
    OPT_ALL_SUPPLIERS:'Όλοι οι προμηθευτές',
    BTN_EXPORT_CSV:'⬇ Εξαγωγή CSV',
    TH_TIMESTAMP:'Χρόνος', TH_TARIFF_CL:'Τιμολόγιο', TH_SUPPLIER_CL:'Χρήστης', TH_ACTOR:'Έγινε από', TH_ACTION:'Ενέργεια', TH_CHANGES:'Αλλαγές',
    CL_ACTOR_ADMIN:'Διαχειριστής CERA', CL_ACTOR_SUPPLIER:'Προμηθευτής',
    CL_EMPTY:'Δεν υπάρχουν καταχωρήσεις ακόμα. Οι αλλαγές στα τιμολόγια θα εμφανίζονται εδώ.',
    // Reports pane
    PANE_REPORTS_TITLE:'Αναφορές προβλημάτων',
    PANE_REPORTS_DESC:'Προβλήματα που ανέφεραν πελάτες σχετικά με δημοσιευμένες πληροφορίες διατιμήσεων, μέσω του συνδέσμου «Αναφορά προβλήματος» στο εργαλείο σύγκρισης.',
    OPT_ALL_STATUSES:'Όλες οι καταστάσεις', OPT_STATUS_OPEN:'Ανοιχτή', OPT_STATUS_REVIEWED:'Ελέγχθηκε', OPT_STATUS_RESOLVED:'Επιλύθηκε', OPT_STATUS_DISMISSED:'Απορρίφθηκε',
    TH_REPORTED_AT:'Αναφέρθηκε', TH_TARIFF_RP:'Διατίμηση', TH_SUPPLIER_RP:'Προμηθευτής', TH_CATEGORY_RP:'Κατηγορία', TH_NOTE:'Σημείωση', TH_STATUS:'Κατάσταση', TH_ACTIONS:'Ενέργειες',
    BTN_MARK_REVIEWED:'Σήμανση ως ελέγχθηκε', BTN_MARK_RESOLVED:'Σήμανση ως επιλύθηκε', BTN_DISMISS:'Απόρριψη', BTN_REOPEN:'Άνοιγμα ξανά',
    RP_CAT_INCORRECT_PRICE:'Λανθασμένη τιμή', RP_CAT_TERMS_MISMATCH:'Ασυμφωνία όρων', RP_CAT_BROKEN_LINK:'Κατεστραμμένος σύνδεσμος', RP_CAT_OTHER:'Άλλο',
    RP_LBL_REPORTER:'Αναφέρων', RP_LBL_RESOLUTION:'Επίλυση', RP_OVERDUE:'⚠ Εκπρόθεσμη', RP_ADMIN_NOTE_PROMPT:'Προσθήκη σημείωσης επίλυσης (προαιρετικό):',
    RP_GENERAL_ISSUE:'Γενικό πρόβλημα ιστοσελίδας',
    RP_EMPTY:'Δεν υπάρχουν αναφορές προβλημάτων ακόμα.',
    // Publish pane
    BTN_SAVE_REG:'💾 Αποθήκευση ρυθμιζόμενων χρεώσεων', BTN_REG_HISTORY:'📈 Ιστορικό',
    MODAL_REG_HISTORY_FPA:'Ιστορικό ρυθμιζόμενων χρεώσεων — τάση FPA',
    MODAL_REG_HISTORY_GRID:'Ιστορικό ρυθμιζόμενων χρεώσεων — τάση χρεώσεων δικτύου',
    MODAL_REG_HISTORY_UNIVERSAL:'Ιστορικό ρυθμιζόμενων χρεώσεων — τάση οικουμενικών χρεώσεων',
    REG_HIST_SHOW_ALL:'Εμφάνιση όλου του ιστορικού (αντί για τους τελευταίους 12 μήνες)',
    REG_HIST_COL_MONTH:'Μήνας', REG_HIST_COL_FPA_LV:'FPA — LV', REG_HIST_COL_FPA_MV:'FPA — MV', REG_HIST_COL_FPA_HV:'FPA — HV',
    REG_HIST_COL_LV:'Χρέωση δικτύου LV', REG_HIST_COL_MV:'Χρέωση δικτύου MV', REG_HIST_COL_HV:'Χρέωση δικτύου HV',
    REG_HIST_COL_PSO:'PSO', REG_HIST_COL_RES:'RES & Ταμείο Εξοικονόμησης Ενέργειας',
    // Tariff editor modal
    MODAL_ADD_TARIFF:'Προσθήκη τιμολογίου', MODAL_EDIT_TARIFF:'Επεξεργασία τιμολογίου', MODAL_VIEW_TARIFF:'Προβολή τιμολογίου',
    BTN_SAVE_TARIFF:'Αποθήκευση τιμολογίου', BTN_EDIT_TARIFF_BTN:'Επεξεργασία τιμολογίου', BTN_DELETE_TARIFF:'Διαγραφή τιμολογίου',
    BTN_CANCEL:'Ακύρωση', BTN_CLOSE:'Κλείσιμο',
    // Review modal
    MODAL_REVIEW_TARIFF:'Αξιολόγηση τιμολογίου',
    BTN_APPROVE:'✓ Έγκριση', BTN_REJECT:'✕ Απόρριψη',
    BTN_CONFIRM_REJECT:'Επιβεβαίωση Απόρριψης', BTN_CANCEL_REJECT:'Ακύρωση',
    LBL_REJECT_REASON:'Επιλέξτε λόγο απόρριψης:',
    // Account modal
    ACCT_TITLE:'Ο λογαριασμός μου', ACCT_CHANGE_EMAIL:'Αλλαγή email',
    LBL_CURRENT_EMAIL:'Τρέχον email', LBL_NEW_EMAIL:'Νέο email', BTN_UPDATE_EMAIL:'Ενημέρωση email',
    ACCT_CHANGE_PW:'Αλλαγή κωδικού', LBL_CURRENT_PW:'Τρέχων κωδικός',
    LBL_NEW_PW:'Νέος κωδικός', LBL_CONFIRM_PW:'Επιβεβαίωση νέου κωδικού', BTN_UPDATE_PW:'Ενημέρωση κωδικού',
    // Supplier detail modal
    SUP_MODAL_TITLE:'Στοιχεία προμηθευτή', LBL_COMPANY_NAME:'Εταιρεία / Όνομα προμηθευτή',
    LBL_LICENCE:'Αριθμός άδειας ΡΑΕΚ', LBL_ADDRESS:'Διεύθυνση εταιρείας',
    LBL_WEBSITE:'Ιστοσελίδα', LBL_TEL_NO:'Τηλέφωνο',
    LBL_SUP_REGULATED:'Ρυθμιζόμενος προμηθευτής',
    BTN_SAVE_DETAILS:'Αποθήκευση στοιχείων',
    REG_CONFIRM_TITLE:'Αλλαγή καθεστώτος ρύθμισης;', BTN_CONFIRM_CHANGE:'Επιβεβαίωση αλλαγής',
    REG_CHANGE_TITLE:'Παρακαλώ ελέγξτε αυτές τις τιμές', REG_CHANGE_QUESTION:'Είναι σωστό;', BTN_CONFIRM:'Επιβεβαίωση',
    REG_CHANGE_PCT:'Η τιμή {F} είναι τώρα {P}% {D} από την προηγούμενη ({OLD} → {NEW}).',
    REG_CHANGE_HIGHER:'υψηλότερη', REG_CHANGE_LOWER:'χαμηλότερη',
    REG_CHANGE_FROM_ZERO:'Η τιμή {F} ήταν 0 και είναι τώρα {NEW}.',
    REG_FPA_ORDER:'Οι συντελεστές FPA δεν είναι στη συνήθη σειρά ΧΤ > ΜΤ > ΥΤ (ΧΤ {LV}, ΜΤ {MV}, ΥΤ {HV}).',
    REG_NOT_SAVED:'Δεν αποθηκεύτηκε.',
    ERR_REG_GRID_ORDER:'Η χρήση δικτύου πρέπει να μειώνεται με την τάση: ΧΤ > ΜΤ > ΥΤ.',
    REG_F_lv:'χρήσης δικτύου ΧΤ', REG_F_mv:'χρήσης δικτύου ΜΤ', REG_F_hv:'χρήσης δικτύου ΥΤ',
    REG_F_fpaLV:'FPA ΧΤ', REG_F_fpaMV:'FPA ΜΤ', REG_F_fpaHV:'FPA ΥΤ',
    REG_F_pso:'ΥΠΥ', REG_F_res:'ΑΠΕ & ΕΞΕ', REG_F_mdm:'MDM',
    // Admin docs modal
    ADOCS_TITLE_PREFIX:'Έγγραφα — ',
  }
};
let _lang = localStorage.getItem('cera_admin_lang') || 'en';
function T(k){ return (LANG[_lang]&&LANG[_lang][k]) || LANG.en[k] || k; }
function setLang(l){ _lang=l; localStorage.setItem('cera_admin_lang',l); renderPage(); }
function renderPage(){
  document.getElementById('html-root').lang = _lang;
  document.title = T('PAGE_TITLE');
  document.querySelectorAll('[data-t]').forEach(el => { el.textContent = T(el.dataset.t); });
  document.querySelectorAll('[data-th]').forEach(el => { el.innerHTML = T(el.dataset.th); });
  document.querySelectorAll('.btn-lang-admin').forEach(b => {
    b.classList.toggle('active', b.dataset.lang === _lang);
  });
  // Update audit month options
  const auditMonthSel = document.getElementById('audit-month');
  if(auditMonthSel) auditMonthSel.querySelectorAll('option').forEach(o => {
    if(o.dataset.t) o.textContent = T(o.dataset.t);
  });
  // Update changelog filter options
  const clAction = document.getElementById('cl-filter-action');
  if(clAction) clAction.querySelectorAll('option[data-t]').forEach(o => { o.textContent = T(o.dataset.t); });
  // Re-render dynamic lists so translated strings appear
  renderSuppliers();
  renderProfiles();
  renderTariffs();
  renderChangelog();
}

const MONTHS_SHORT=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];

let suppliers=[], profiles=[], tariffs=[], changelog=[], loginActivity=[], reports=[];
let docTariffIds=new Set();
// suppliers is an array of objects: {name, tradingName, licence, address, website, email, tel}
// For backwards compat, string entries are treated as {name: entry}
function supObj(s){ return typeof s==='string'?{name:s}:s; }
function supName(s){ return supObj(s).name; }
// Note: tradingName removed — name is the single company identifier
let damMonthly=new Array(12).fill(null);
let damBySlot=[];
let damRowCount=0;

function uid(){return Date.now().toString(36)+Math.random().toString(36).slice(2,6);}
function fv(id){return parseFloat(document.getElementById(id)?.value)||0;}
function sv(id){return document.getElementById(id)?.value||'';}
function showStatus(el,type,msg){if(!el)return;el.className='status show '+type;el.textContent=msg;}

/* ── Nav ── */
/* ── Unsaved-changes guard ──
   Forms whose edits are held on the page until their own Save button is
   clicked. Typing in one marks it unsaved: its menu item gets a ● marker,
   leaving its page / closing its window / signing out asks first, and
   reloading or closing the tab triggers the browser's "Leave site?" prompt.
   A successful save (or re-opening the form fresh) marks it clean again.
   Forms that save instantly (e.g. the sample-invoice checkbox) aren't listed. */
const _UNSAVED_FORMS={
  tariff:         {label:'the tariff editor',          pane:null,        sel:'#editor-overlay'},
  supplierDetails:{label:'supplier details',           pane:null,        sel:'#sup-modal-overlay'},
  supplierNew:    {label:'the new supplier name',      pane:'suppliers', sel:'#sup-name'},
  profile:        {label:'the load profile form',      pane:'profiles',  sel:'#prof-name,#prof-desc,#prof-raw'},
  invite:         {label:'the user invitation form',   pane:'users',     sel:'#inv-email,#inv-supplier'},
  message:        {label:'the notification being written', pane:'messages', sel:'#msg-subject,#msg-body'},
  schedule:       {label:'the recurring notification form', pane:'messages', sel:'#sched-form'},
  dam:            {label:'DAM price data',             pane:'dam',       sel:'#dam-year,#dam-unit,#dam-file-input,#dam-raw'},
  regulated:      {label:'regulated charges',          pane:'regulated', sel:'#reg-lv,#reg-mv,#reg-hv,#reg-fpa-lv,#reg-fpa-mv,#reg-fpa-hv,#reg-pso,#reg-res,#reg-mdm'},
  notices:        {label:'notices',                    pane:'notices',   sel:'#assumptions-en,#assumptions-el,#legal-en,#legal-el,#vulnerable-en,#vulnerable-el'},
};
const _unsaved=new Set();
function _refreshUnsavedMarkers(){
  document.querySelectorAll('.nav-item.nav-unsaved').forEach(n=>n.classList.remove('nav-unsaved'));
  _unsaved.forEach(k=>{
    const pane=_UNSAVED_FORMS[k].pane;
    const nav=pane&&document.querySelector(`.nav-item[data-action="showPane"][data-arg="${pane}"]`);
    if(nav) nav.classList.add('nav-unsaved');
  });
}
function markUnsaved(key){_unsaved.add(key);_refreshUnsavedMarkers();}
function markClean(key){_unsaved.delete(key);_refreshUnsavedMarkers();}
function _unsavedLabels(keys){return keys.map(k=>'• '+_UNSAVED_FORMS[k].label).join('\n');}
// true = OK to discard (nothing unsaved, or the admin confirmed); clears the flag
function confirmDiscard(key){
  if(!_unsaved.has(key)) return true;
  if(!confirm('You have unsaved changes in '+_UNSAVED_FORMS[key].label+'.\n\nDiscard them?')) return false;
  markClean(key); return true;
}
['input','change'].forEach(evt=>document.addEventListener(evt,e=>{
  if(!e.isTrusted||!(e.target instanceof Element)) return;   // only real user edits
  // A field that lost focus after its form was saved and hidden can still fire
  // a late "change" event; ignore anything not currently on screen.
  if(!e.target.getClientRects().length) return;
  for(const [k,f] of Object.entries(_UNSAVED_FORMS)){
    if(e.target.closest(f.sel)){markUnsaved(k);break;}
  }
},true));
// Adding/removing discount or tier rows in the tariff editor changes the
// tariff without any typing, so count those clicks as edits too.
document.addEventListener('click',e=>{
  if(!e.isTrusted||!(e.target instanceof Element)) return;
  const b=e.target.closest('#editor-overlay [data-action]');
  if(b&&/^(addDiscount|addTierRow|removeTierRow|removeDiscountRow)$/.test(b.dataset.action)) markUnsaved('tariff');
},true);
window.addEventListener('beforeunload',e=>{
  if(_unsaved.size){e.preventDefault();e.returnValue='';}
});

function showPane(id){
  // Leaving a page with unsaved edits: they stay in the form, but aren't live.
  const current=document.querySelector('.pane.active')?.id?.replace(/^pane-/,'');
  if(current&&current!==id){
    const pending=[..._unsaved].filter(k=>_UNSAVED_FORMS[k].pane===current);
    if(pending.length&&!confirm('You have unsaved changes in:\n'+_unsavedLabels(pending)
        +'\n\nThey are NOT saved and NOT live yet. Leave this page anyway?\n(Your edits stay in the form, marked ● in the menu, until you save them or reload.)')) return;
  }
  document.querySelectorAll('.pane').forEach(p=>p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n=>n.classList.remove('active'));
  document.getElementById('pane-'+id).classList.add('active');
  const keys=['dashboard','suppliers','profiles','tariffs','users','login-activity','messages','dam','regulated','audit','notices','changelog','reports'];
  const idx=keys.indexOf(id);
  if(idx>=0) document.querySelectorAll('.nav-item')[idx].classList.add('active');
  if(id==='dashboard') buildDashboard();
  if(id==='regulated') updateRegPreview();
  if(id==='audit') auditPopulateTariffs();
  if(id==='changelog') renderChangelog();
  if(id==='reports') renderReports();
  if(id==='users') usersLoad();
  if(id==='login-activity') loginActivityLoad();
  if(id==='messages'){ messagesLoad(); schedulesLoad(); }
}

/* ── Suppliers ── */
async function addSupplier(){
  const name=document.getElementById('sup-name').value.trim();
  if(!name||suppliers.some(s=>supName(s)===name)) return;
  const st=document.getElementById('sup-status');
  showStatus(st,'ok','Saving…');
  try{
    const resp=await fetch(_adminApiBase+'/api/admin/suppliers',{method:'POST',headers:authHeaders(),body:JSON.stringify({name})});
    if(resp.status===401){showLogin('Session expired.');return;}
    if(!resp.ok){const e=await resp.json().catch(()=>({}));showStatus(st,'err','Save failed: '+(e.detail||resp.status));return;}
    const saved=await resp.json();
    suppliers.push(saved);
    document.getElementById('sup-name').value='';
    markClean('supplierNew');
    renderSuppliers();
    showStatus(st,'ok',`Saved — "${name}" added.`);
  } catch(e){showStatus(st,'err','Save failed: '+e.message);}
}
function openSupModal(name){
  const s=suppliers.find(x=>supName(x)===name);
  if(!s) return;
  const o=supObj(s);
  document.getElementById('sup-modal-orig-name').value=o.name; // original key for lookup
  document.getElementById('sup-modal-name').value=o.name;      // editable
  document.getElementById('sup-modal-title').textContent='Edit supplier';
  document.getElementById('sup-licence').value=o.licence||'';
  document.getElementById('sup-address').value=o.address||'';
  document.getElementById('sup-website').value=o.website||'';
  document.getElementById('sup-email').value=o.email||'';
  document.getElementById('sup-tel').value=o.tel||'';
  document.getElementById('sup-regulated').checked=!!o.regulated;
  _supModalOrigRegulated=!!o.regulated;
  markClean('supplierDetails');
  document.getElementById('sup-modal-overlay').style.display='flex';
}
function closeSupModal(){
  if(!confirmDiscard('supplierDetails')) return;
  document.getElementById('sup-modal-overlay').style.display='none';
}

/* Toggling "regulated" changes how MDM is calculated for every tariff under
   this supplier, so it goes through two deliberate confirmation steps rather
   than a plain checkbox click — a details pop-out here, then a second
   confirmation when the change is actually saved (see saveSupplierDetails). */
let _supModalOrigRegulated=false;
let _pendingRegulatedState=null;
function onRegulatedCheckboxClick(){
  const cb=document.getElementById('sup-regulated');
  // The browser has already flipped the box when the click handler runs, so its
  // current state is the one the click asks for (this used to read !cb.checked,
  // which made confirming a no-op: the setting could never be changed).
  _pendingRegulatedState=cb.checked;
  document.getElementById('regulated-confirm-body').textContent=_pendingRegulatedState
    ?'Marking this supplier as regulated means their tariffs will automatically use the CERA-set regulated MDM rate (Regulated tariffs tab), instead of a value set per tariff.'
    :'Removing the regulated flag means this supplier\'s tariffs will stop automatically following the CERA-set regulated MDM rate — each tariff will need its own MDM value (or an explicit opt-in to the regulated rate) instead.';
  document.getElementById('regulated-confirm-overlay').style.display='flex';
  return false; // cancels the checkbox's own toggle; confirmRegulatedToggle() applies it explicitly
}
function closeRegulatedConfirm(){
  document.getElementById('regulated-confirm-overlay').style.display='none';
  _pendingRegulatedState=null;
}
function confirmRegulatedToggle(){
  if(_pendingRegulatedState!==null){
    document.getElementById('sup-regulated').checked=_pendingRegulatedState;
    markUnsaved('supplierDetails'); // set programmatically, so the input listener doesn't see it
  }
  closeRegulatedConfirm();
}
async function saveSupplierDetails(){
  const origName=document.getElementById('sup-modal-orig-name').value;
  const newName=document.getElementById('sup-modal-name').value.trim();
  if(!newName) return;
  const idx=suppliers.findIndex(s=>supName(s)===origName);
  if(idx<0) return;
  const body={
    name:newName,
    licence:document.getElementById('sup-licence').value.trim(),
    address:document.getElementById('sup-address').value.trim(),
    website:document.getElementById('sup-website').value.trim(),
    email:document.getElementById('sup-email').value.trim(),
    tel:document.getElementById('sup-tel').value.trim(),
    regulated:document.getElementById('sup-regulated').checked
  };
  if(body.regulated!==_supModalOrigRegulated){
    const msg=body.regulated
      ?`Confirm: mark "${newName}" as a regulated supplier? This changes how MDM is calculated for all of their tariffs.`
      :`Confirm: remove "${newName}" from regulated suppliers? This changes how MDM is calculated for all of their tariffs.`;
    if(!confirm(msg)) return;
  }
  const st=document.getElementById('sup-status');
  showStatus(st,'ok','Saving…');
  try{
    const resp=await fetch(_adminApiBase+'/api/admin/suppliers/'+encodeURIComponent(origName),{method:'PUT',headers:authHeaders(),body:JSON.stringify(body)});
    if(resp.status===401){showLogin('Session expired.');return;}
    if(!resp.ok){const e=await resp.json().catch(()=>({}));showStatus(st,'err','Save failed: '+(e.detail||resp.status));return;}
    const saved=await resp.json();
    // Server already renamed this supplier on any referencing tariffs — mirror that locally
    if(newName!==origName){
      tariffs.forEach(t=>{if(t.supplier===origName) t.supplier=newName;});
    }
    if(body.regulated!==_supModalOrigRegulated){
      // Mirrors the changelog row the server just wrote (see update_supplier in admin.py)
      // so the change shows up immediately without waiting for a changelog reload.
      addChangelogEntry({action:'updated',tariffId:null,tariffName:'Supplier settings',supplier:newName,
        changes:[{field:'regulated',from:_supModalOrigRegulated?'yes':'no',to:body.regulated?'yes':'no'}],
        ts:new Date().toISOString(),actorRole:'admin'});
    }
    suppliers[idx]=saved;
    markClean('supplierDetails');
    closeSupModal();
    renderSuppliers();
    renderTariffs(); // refresh tariff list in case supplier name changed
    showStatus(st,'ok',`Saved — "${newName}" updated.`);
  } catch(e){showStatus(st,'err','Save failed: '+e.message);}
}
async function removeSupplier(name){
  if(tariffs.some(t=>t.supplier===name)){alert(`Remove tariffs under "${name}" first.`);return;}
  if(!confirm(`Remove supplier "${name}"?\n\nThis cannot be undone.`)) return;
  const st=document.getElementById('sup-status');
  showStatus(st,'ok','Saving…');
  try{
    const resp=await fetch(_adminApiBase+'/api/admin/suppliers/'+encodeURIComponent(name),{method:'DELETE',headers:authHeaders()});
    if(resp.status===401){showLogin('Session expired.');return;}
    if(!resp.ok){const e=await resp.json().catch(()=>({}));showStatus(st,'err','Delete failed: '+(e.detail||resp.status));return;}
    suppliers=suppliers.filter(s=>supName(s)!==name);
    renderSuppliers();
    showStatus(st,'ok',`Saved — "${name}" removed.`);
  } catch(e){showStatus(st,'err','Delete failed: '+e.message);}
}
function renderSuppliers(){
  const el=document.getElementById('supplier-list');
  if(!suppliers.length){el.innerHTML='<div class="empty-state">'+T('EMPTY_SUPPLIERS')+'</div>';return;}
  el.innerHTML='<div class="list-wrap">'+suppliers.map(s=>{
    const o=supObj(s);
    const n=o.name;
    const tCount=tariffs.filter(t=>t.supplier===n).length;
    const hasDetails=o.licence||o.address||o.website||o.email||o.tel;
    return `<div class="item-row" style="flex-wrap:wrap;gap:10px">
      <div class="item-row-info" style="flex:1;min-width:0">
        <div class="item-name">${esc(n)}</div>
        <div class="item-meta">
          <span class="badge badge-type">${tCount} ${T('SUP_TARIFFS')}</span>
          ${o.regulated?`<span class="badge" style="background:rgba(188,108,37,.12);color:var(--yellow)">⚖ ${T('BADGE_REGULATED')}</span>`:''}
          ${o.licence?`<span class="badge badge-voltage">Lic: ${esc(o.licence)}</span>`:''}
          ${o.tel?`<span class="badge" style="background:var(--bg3);color:var(--text2)">${esc(o.tel)}</span>`:''}
          ${o.email?`<span class="badge" style="background:var(--bg3);color:var(--text2)">${esc(o.email)}</span>`:''}
          ${o.website?`<span class="badge" style="background:var(--bg3);color:var(--accent)">${esc(o.website)}</span>`:''}
          ${!hasDetails?`<span class="badge" style="background:rgba(245,158,11,.1);color:#d97706">${T('SUP_NO_CONTACT')}</span>`:''}
        </div>
        ${o.address?`<div style="font-size:11px;color:var(--text3);font-family:var(--mono);margin-top:3px">📍 ${esc(o.address)}</div>`:''}
      </div>
      <div class="item-row-actions">
        <button class="btn btn-sm" data-sup="${n.replace(/&/g,'&amp;').replace(/"/g,'&quot;')}" data-action="openSupModal">${T('BTN_EDIT_DETAILS')}</button>
        <button class="btn btn-danger btn-sm" data-sup="${n.replace(/&/g,'&amp;').replace(/"/g,'&quot;')}" data-action="removeSupplier">${T('BTN_REMOVE')}</button>
      </div>
    </div>`;
  }).join('')+'</div>';
}

/* ─────────────────────────────────────────
   PROFILE PARSER — DSO transposed format
   ───────────────────────────────────────── */
const _PROF_MONTHS=['January','February','March','April','May','June','July','August','September','October','November','December'];
const _PROF_DT={W:'working days',NW:'non-working days'};

// Server-side profile validation errors (the safety net behind the parser's own
// checks) point at e.g. months › 2 › W › 5; say "March, working days, 03:00" instead.
function profileErrorText(detail,fallback){
  if(!Array.isArray(detail)) return apiErrorText(detail,fallback);
  return detail.map(d=>{
    const loc=(d.loc||[]).filter(x=>x!=='body');
    const msg=String(d.msg||'').replace(/^Value error, /,'');
    if(loc[0]==='months'&&Number.isInteger(loc[1])){
      let where=_PROF_MONTHS[loc[1]]||('month '+(loc[1]+1));
      if(loc[2]==='W'||loc[2]==='NW') where+=', '+_PROF_DT[loc[2]];
      if(Number.isInteger(loc[3])){
        const endMin=(loc[3]+1)*30;
        where+=', '+String(Math.floor(endMin/60)%24).padStart(2,'0')+':'+String(endMin%60).padStart(2,'0');
      }
      return where+': '+msg;
    }
    return (loc.length?loc.join(' › ')+': ':'')+msg;
  }).join('; ');
}

async function parseAndAddProfile(){
  const name=document.getElementById('prof-name').value.trim();
  const desc=document.getElementById('prof-desc').value.trim();
  const raw=document.getElementById('prof-raw').value.trim();
  const status=document.getElementById('prof-status');

  if(!name){showStatus(status,'err','Profile name is required.');return;}
  if(!raw){showStatus(status,'err','No data pasted.');return;}

  // Keep each non-blank line's original line number (1-based) for error messages
  const lines=[], lineNos=[];
  document.getElementById('prof-raw').value.split(/\r?\n/).forEach((l,i)=>{
    l=l.trim(); if(l){lines.push(l);lineNos.push(i+1);}
  });

  // Find header row (contains TIME or Jan_WD etc.)
  let headerIdx=-1;
  for(let i=0;i<Math.min(5,lines.length);i++){
    if(lines[i].toUpperCase().includes('TIME')||lines[i].toUpperCase().includes('JAN')){
      headerIdx=i; break;
    }
  }
  if(headerIdx<0){showStatus(status,'err','Could not find header row (expected TIME, Jan_WD, Jan_NWD, …).');return;}

  // Parse header to get column → {month, dayType} mapping
  const headerParts=lines[headerIdx].split(/[,;\t]/).map(s=>s.trim());
  // Build column map: colIdx → {mi: 0..11, dt: 'W'|'NW'}
  const colMap=[];
  for(let c=1;c<headerParts.length;c++){
    const h=headerParts[c].toUpperCase();
    if(!h) continue;
    const mMatch=h.match(/^(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)/);
    if(!mMatch) continue;
    const mNames=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'];
    const mi=mNames.indexOf(mMatch[1]);
    const dt=h.includes('NWD')||h.includes('NW')?'NW':'W';
    colMap.push({c,mi,dt,label:headerParts[c]});
  }

  if(colMap.length===0){showStatus(status,'err','Could not parse column headers. Expected Jan_WD, Jan_NWD format.');return;}

  // Correct slot order: slot s covers [s*30, (s+1)*30) minutes from midnight
  // Label = end of slot: slot 0 covers 00:00-00:30 → label '00:30'
  //                      slot 1 covers 00:30-01:00 → label '01:00'
  //                      slot 47 covers 23:30-00:00 → label '00:00'
  const slotOrder=[];
  for(let s=0;s<48;s++){
    const endMin=(s+1)*30;
    const endH=Math.floor(endMin/60)%24;
    const endM=endMin%60;
    slotOrder.push(`${String(endH).padStart(2,'0')}:${String(endM).padStart(2,'0')}`);
  }
  // slotOrder[0]='00:30', slotOrder[1]='01:00', ..., slotOrder[46]='23:30', slotOrder[47]='00:00'

  // data[mi][dt][slot 0..47] = raw value
  const raw_data=Array.from({length:12},()=>({W:new Array(48).fill(0),NW:new Array(48).fill(0)}));
  let parsed=0, skipped=0;

  // Check the whole file before saving. Problems that would silently corrupt the
  // profile (text/empty/negative cells, duplicate or missing time rows, duplicate
  // columns) refuse the save, with the exact place in the file. Unusual-but-possible
  // things (a month with no column or no usage, very high values) only warn.
  const errors=[], warnings=[];
  const where=(lineNo,label,time)=>`Line ${lineNo}, ${label} at ${time}`;
  const seenCol={};
  colMap.forEach(({mi,dt,label})=>{
    const k=mi+dt;
    if(seenCol[k]) errors.push(`Columns ${seenCol[k]} and ${label} are both ${_PROF_MONTHS[mi]} ${_PROF_DT[dt]}`);
    else seenCol[k]=label;
  });
  const slotLine={};
  lines.slice(headerIdx+1).forEach((line,i)=>{
    const lineNo=lineNos[headerIdx+1+i];
    const parts=line.split(/[,;\t]/).map(s=>s.trim());
    if(!parts[0]) return;
    let timeLabel=parts[0]; // e.g. "00:30"
    if(/^\d:\d\d$/.test(timeLabel)) timeLabel='0'+timeLabel;   // 0:30 → 00:30
    if(timeLabel==='24:00') timeLabel='00:00';                   // end of day, either way
    const slotIdx=slotOrder.indexOf(timeLabel);
    if(slotIdx<0){
      // A time-like label that isn't a half-hour slot is a data error; other rows
      // (e.g. a "Total" line) are just skipped, as before.
      if(/^\d{1,2}:\d{2}/.test(timeLabel)) errors.push(`Line ${lineNo}: "${parts[0]}" is not a half-hour time (expected 00:30, 01:00 … 23:30, 00:00)`);
      else skipped++;
      return;
    }
    if(slotLine[slotIdx]!==undefined){errors.push(`Time ${timeLabel} appears twice (lines ${slotLine[slotIdx]} and ${lineNo})`);return;}
    slotLine[slotIdx]=lineNo;
    colMap.forEach(({c,mi,dt,label})=>{
      const cell=parts[c]===undefined?'':parts[c];
      if(cell===''){errors.push(`${where(lineNo,label,timeLabel)}: empty cell`);return;}
      const val=Number(cell);
      if(!Number.isFinite(val)){errors.push(`${where(lineNo,label,timeLabel)}: "${cell}" is not a number`);return;}
      if(val<0){errors.push(`${where(lineNo,label,timeLabel)}: negative value ${cell}`);return;}
      raw_data[mi][dt][slotIdx]+=val;
    });
    parsed++;
  });

  if(!parsed&&!errors.length){showStatus(status,'err','No valid data rows found. Check time labels (expected HH:MM format like 00:30).');return;}
  const missingSlots=slotOrder.filter((t,s)=>slotLine[s]===undefined);
  if(parsed&&missingSlots.length) errors.push(`Missing time rows: ${missingSlots.join(', ')}`);
  if(errors.length){
    const shown=errors.slice(0,10);
    if(errors.length>10) shown.push(`…and ${errors.length-10} more`);
    showStatus(status,'err',`Profile not saved: ${errors.length} problem${errors.length>1?'s':''} found:\n• `+shown.join('\n• '));
    return;
  }

  // Warnings: months/day types with no column or no usage at all, and values far
  // above this profile's typical level (median of its non-zero values).
  const noData=[];
  for(let mi=0;mi<12;mi++) for(const dt of ['W','NW']){
    if(!raw_data[mi][dt].some(v=>v>0)) noData.push(`${_PROF_MONTHS[mi]} ${_PROF_DT[dt]}`);
  }
  if(noData.length) warnings.push(`No data for: ${noData.join(', ')}`);
  const nonZero=raw_data.flatMap(m=>[...m.W,...m.NW]).filter(v=>v>0).sort((a,b)=>a-b);
  const median=nonZero.length?nonZero[Math.floor(nonZero.length/2)]:0;
  if(median>0){
    const high=[];
    raw_data.forEach((m,mi)=>['W','NW'].forEach(dt=>m[dt].forEach((v,s)=>{
      if(v>10*median) high.push(`${_PROF_MONTHS[mi]} ${_PROF_DT[dt]} at ${slotOrder[s]}: ${v}`);
    })));
    if(high.length){
      const shownHigh=high.slice(0,10).concat(high.length>10?[`…and ${high.length-10} more`]:[]);
      warnings.push(`Unusually high values (over 10× this profile's typical value of ${median}):\n  - `+shownHigh.join('\n  - '));
    }
  }
  if(warnings.length&&!confirm(`Please check this profile before saving:\n\n• ${warnings.join('\n• ')}\n\nSave anyway?`)){
    showStatus(status,'err','Not saved. Correct the CSV and try again.');
    return;
  }

  // Store raw unnormalised HHFFs.
  // Normalisation uses actual calendar day counts at runtime (year 2026)
  // so the full annual weighting across months and day-types is correct.
  const months=raw_data.map(m=>({
    W: [...m.W],
    NW:[...m.NW],
    hasW:  m.W.some(v=>v>0),
    hasNW: m.NW.some(v=>v>0)
  }));

  const covW =months.filter(m=>m.hasW).length;
  const covNW=months.filter(m=>m.hasNW).length;

  const ex=profiles.findIndex(p=>p.name===name);
  if(ex>=0&&!confirm(`Overwrite profile "${name}"?`))return;
  // Reuse the existing profile's id on overwrite so tariffs referencing it via
  // profileId keep pointing at the same row — only brand-new profiles get a new id.
  const profile={id:ex>=0?profiles[ex].id:uid(),name,desc,months,covW,covNW,rows:parsed,colCount:colMap.length};

  showStatus(status,'ok','Saving…');
  try{
    const url=ex>=0
      ?_adminApiBase+'/api/admin/profiles/'+encodeURIComponent(profile.id)
      :_adminApiBase+'/api/admin/profiles';
    const resp=await fetch(url,{method:ex>=0?'PUT':'POST',headers:authHeaders(),body:JSON.stringify(profile)});
    if(resp.status===401){showLogin('Session expired.');return;}
    if(!resp.ok){const e=await resp.json().catch(()=>({}));showStatus(status,'err','Save failed: '+profileErrorText(e.detail,resp.status));return;}
    const saved=await resp.json();
    if(ex>=0) profiles[ex]=saved; else profiles.push(saved);
    document.getElementById('prof-name').value='';
    document.getElementById('prof-raw').value='';
    markClean('profile');
    renderProfiles();
    refreshProfileDropdowns();
    showStatus(status,'ok',
      `✓ Profile "${name}" saved — ${parsed} time slots, ${colMap.length} columns (W:${covW}/12 months, NW:${covNW}/12 months), ${skipped} skipped rows.`
    );
  } catch(e){showStatus(status,'err','Save failed: '+e.message);}
}

async function editProfileName(id){
  const p=profiles.find(x=>x.id===id);
  if(!p) return;
  const newName=prompt('Rename profile:', p.name);
  if(!newName||!newName.trim()||newName.trim()===p.name) return;
  const st=document.getElementById('profile-list-status');
  showStatus(st,'ok','Saving…');
  const body={...p,name:newName.trim()};
  try{
    const resp=await fetch(_adminApiBase+'/api/admin/profiles/'+encodeURIComponent(id),{method:'PUT',headers:authHeaders(),body:JSON.stringify(body)});
    if(resp.status===401){showLogin('Session expired.');return;}
    if(!resp.ok){const e=await resp.json().catch(()=>({}));showStatus(st,'err','Save failed: '+profileErrorText(e.detail,resp.status));return;}
    const saved=await resp.json();
    const idx=profiles.findIndex(x=>x.id===id);
    if(idx>=0) profiles[idx]=saved;
    renderProfiles();
    refreshProfileDropdowns();
    showStatus(st,'ok',`Saved — renamed to "${saved.name}".`);
  } catch(e){showStatus(st,'err','Save failed: '+e.message);}
}

async function deleteProfile(id){
  if(tariffs.some(t=>t.profileId===id)){alert('Unassign from tariffs first.');return;}
  if(!confirm('Delete this profile?'))return;
  const st=document.getElementById('profile-list-status');
  showStatus(st,'ok','Saving…');
  try{
    const resp=await fetch(_adminApiBase+'/api/admin/profiles/'+encodeURIComponent(id),{method:'DELETE',headers:authHeaders()});
    if(resp.status===401){showLogin('Session expired.');return;}
    if(!resp.ok){const e=await resp.json().catch(()=>({}));showStatus(st,'err','Delete failed: '+(e.detail||resp.status));return;}
    profiles=profiles.filter(p=>p.id!==id);
    renderProfiles();refreshProfileDropdowns();
    showStatus(st,'ok','Saved — profile deleted.');
  } catch(e){showStatus(st,'err','Delete failed: '+e.message);}
}

function renderProfiles(){
  const el=document.getElementById('profile-list');
  if(!profiles.length){el.innerHTML='<div class="empty-state">'+T('EMPTY_PROFILES')+'</div>';return;}
  el.innerHTML='<div class="list-wrap">'+profiles.map(p=>{
    const assigned=tariffs.filter(t=>t.profileId===p.id).length;
    const covCells=p.months.map((m,i)=>{
      const cls=m.hasW&&m.hasNW?'cov-ok':m.hasW||m.hasNW?'cov-partial':'cov-miss';
      const lbl=m.hasW&&m.hasNW?'✓':m.hasW?'W':m.hasNW?'NW':'–';
      return `<div class="cov-cell ${cls}" title="${MONTHS_SHORT[i]}: ${lbl}">${MONTHS_SHORT[i].slice(0,1)}</div>`;
    }).join('');
    // Month tabs
    const tabCls=p.months.map(m=>m.hasW&&m.hasNW?'has-both':m.hasW||m.hasNW?'has-one':'missing');
    const tabs=MONTHS_SHORT.map((m,i)=>
      `<button class="prof-month-tab ${tabCls[i]} ${i===0?'active':''}"
        data-action="selectProfileMonth" data-arg="${esc(p.id)}" data-arg2="${i}">${m}</button>`
    ).join('');
    // Initial sparklines (January)
    const m0=p.months[0];
    const sharedMax0=Math.max(...m0.W,...m0.NW,0.001); // shared scale for WD+NWD
    const wBars=m0.W.map(v=>`<div class="spark-bar-lg spark-wd" style="height:${Math.round((v/sharedMax0)*78)+2}px" title="${v.toFixed(4)}"></div>`).join('');
    const nwBars=m0.NW.map(v=>`<div class="spark-bar-lg spark-nwd" style="height:${Math.round((v/sharedMax0)*78)+2}px" title="${v.toFixed(4)}"></div>`).join('');
    const timeLabels='<span>00:00</span><span>06:00</span><span>12:00</span><span>18:00</span><span>00:00</span>';
    return `<div class="item-row" style="flex-direction:column;align-items:flex-start;gap:10px">
      <div style="display:flex;align-items:center;gap:10px;width:100%;flex-wrap:wrap">
        <div class="item-row-info">
          <div class="item-name">${esc(p.name)}</div>
          <div class="item-meta">
            <span class="badge badge-type">${p.rows} slots</span>
            <span class="badge badge-voltage">W: ${p.covW}/12</span>
            <span class="badge badge-voltage">NW: ${p.covNW}/12</span>
            ${assigned?`<span class="badge badge-profile">${assigned} tariff(s)</span>`:'<span class="badge badge-no-profile">unassigned</span>'}
          </div>
          ${p.desc?`<div style="font-size:11px;color:var(--text3);margin-top:3px;font-family:var(--mono)">${esc(p.desc)}</div>`:''}
        </div>
        <div class="item-row-actions" style="margin-left:auto">
          <button class="btn btn-sm" data-action="editProfileName" data-arg="${esc(p.id)}">${T('BTN_RENAME')}</button>
          <button class="btn btn-danger btn-sm" data-action="deleteProfile" data-arg="${esc(p.id)}">${T('BTN_DELETE')}</button>
        </div>
      </div>
      <div style="width:100%">
        <div style="font-size:10px;color:var(--text3);font-family:var(--mono);margin-bottom:4px">Month coverage — click to view profile shape</div>
        <div class="prof-month-tabs" id="tabs-${p.id}">${tabs}</div>
        <div id="spark-${p.id}" style="width:100%">
          <div class="sparkline-wrap">
            <div>
              <div class="spark-label" id="wlabel-${p.id}">🔵 Jan — working day (00:00–00:00)</div>
              <div class="sparkline-lg" id="wbars-${p.id}">${wBars}</div>
              <div class="spark-time-labels">${timeLabels}</div>
            </div>
            <div>
              <div class="spark-label" id="nwlabel-${p.id}">🟣 Jan — non-working day (00:00–00:00)</div>
              <div class="sparkline-lg" id="nwbars-${p.id}">${nwBars}</div>
              <div class="spark-time-labels">${timeLabels}</div>
            </div>
          </div>
          ${p.monthlyFractions?`<div style="margin-top:8px">
            <div style="font-size:10px;color:var(--text3);font-family:var(--mono);margin-bottom:4px">Annual consumption distribution by month</div>
            <div style="display:grid;grid-template-columns:repeat(12,1fr);gap:4px">
              ${p.monthlyFractions.map((f,i)=>`<div style="background:var(--bg);border:1px solid var(--border);border-radius:2px;padding:5px 2px;text-align:center">
                <div style="font-size:9px;font-family:var(--mono);color:var(--text3)">${MONTHS_SHORT[i]}</div>
                <div style="font-size:10px;font-family:var(--mono);color:var(--green);font-weight:500">${(f*100).toFixed(1)}%</div>
              </div>`).join('')}
            </div>
          </div>`:''}
        </div>
      </div>
    </div>`;
  }).join('')+ '</div>';
}

function selectProfileMonth(profileId, monthIdx){
  const p=profiles.find(x=>x.id===profileId);
  if(!p) return;
  // Update tab active states
  const tabs=document.querySelectorAll(`#tabs-${profileId} .prof-month-tab`);
  tabs.forEach((t,i)=>t.classList.toggle('active',i===monthIdx));
  // Update sparklines
  const m=p.months[monthIdx];
  const sharedMax=Math.max(...m.W,...m.NW,0.001); // same scale for both
  const timeLabels='<span>00:00</span><span>06:00</span><span>12:00</span><span>18:00</span><span>00:00</span>';
  const wBars=m.W.map(v=>`<div class="spark-bar-lg spark-wd" style="height:${Math.round((v/sharedMax)*78)+2}px" title="${v.toFixed(4)}"></div>`).join('');
  const nwBars=m.NW.map(v=>`<div class="spark-bar-lg spark-nwd" style="height:${Math.round((v/sharedMax)*78)+2}px" title="${v.toFixed(4)}"></div>`).join('');
  const mn=MONTHS_SHORT[monthIdx];
  document.getElementById(`wlabel-${profileId}`).textContent=`🔵 ${mn} — working day (00:00–00:00)`;
  document.getElementById(`nwlabel-${profileId}`).textContent=`🟣 ${mn} — non-working day (00:00–00:00)`;
  document.getElementById(`wbars-${profileId}`).innerHTML=wBars;
  document.getElementById(`nwbars-${profileId}`).innerHTML=nwBars;
}


function refreshProfileDropdowns(){
  const sel=document.getElementById('edit-profile');
  if(!sel) return;
  const cur=sel.value;
  sel.innerHTML='<option value="">— None (hour-fraction fallback) —</option>'
    +profiles.map(p=>`<option value="${esc(p.id)}">${esc(p.name)}</option>`).join('');
  if(profiles.find(p=>p.id===cur)) sel.value=cur;
}

/* ── Users ── */
let _usersFormOpen = false;
function usersToggleForm(){
  _usersFormOpen = !_usersFormOpen;
  document.getElementById('users-form').style.display = _usersFormOpen ? 'block' : 'none';
  if(_usersFormOpen){
    // populate supplier dropdown
    const sel = document.getElementById('inv-supplier');
    sel.innerHTML = suppliers.map(s=>`<option value="${esc(s.name)}">${esc(s.name)}</option>`).join('');
    document.getElementById('inv-email').value = '';
    document.getElementById('users-form-msg').textContent = '';
    markClean('invite');
  }
}

let _usersCache = [];
function _usersOtpToggle(u){
  const otpOn = u.otp_enabled !== false;
  return `<button data-action="usersToggleOtp" data-arg="${u.id}" data-arg2="${!otpOn}"
    title="${otpOn ? T('OTP_ON_HINT') : T('OTP_OFF_HINT')}"
    style="border:none;cursor:pointer;padding:0;background:none;display:inline-block;width:36px;height:20px;position:relative;vertical-align:middle">
    <span style="position:absolute;inset:0;border-radius:10px;background:${otpOn?'var(--accent)':'#d1d5db'}"></span>
    <span style="position:absolute;top:3px;left:${otpOn?'19':'3'}px;width:14px;height:14px;border-radius:50%;background:#fff"></span>
  </button>`;
}
function _usersStatusBadge(u){
  const lockedBadge = u.is_locked
    ? `<span style="background:#fef3c7;color:#92400e;font-size:11px;padding:2px 8px;border-radius:10px;font-weight:500;margin-left:4px">🔒 Locked</span>`
    : '';
  return (u.is_active
    ? `<span style="background:#d1fae5;color:#065f46;font-size:11px;padding:2px 8px;border-radius:10px;font-weight:500">${T('USER_ACTIVE')}</span>`
    : `<span style="background:#fee2e2;color:#991b1b;font-size:11px;padding:2px 8px;border-radius:10px;font-weight:500">${T('USER_INACTIVE')}</span>`) + lockedBadge;
}
async function usersLoad(){
  const adminTbody = document.getElementById('users-tbody-admin');
  const supplierTbody = document.getElementById('users-tbody-supplier');
  adminTbody.innerHTML = '<tr><td colspan="3" style="padding:24px;text-align:center;color:var(--text3);font-size:13px">'+T('USERS_LOADING')+'</td></tr>';
  supplierTbody.innerHTML = '<tr><td colspan="5" style="padding:24px;text-align:center;color:var(--text3);font-size:13px">'+T('USERS_LOADING')+'</td></tr>';
  try{
    const resp = await fetch(_adminApiBase+'/api/admin/users',{headers:authHeaders()});
    const list = await resp.json();
    _usersCache = list;
    const admins = list.filter(u=>u.role==='admin');
    const supplierUsers = list.filter(u=>u.role!=='admin');

    adminTbody.innerHTML = admins.length ? admins.map(u => `<tr style="border-bottom:1px solid var(--border)">
        <td style="padding:10px;font-size:13px">${esc(u.email)}</td>
        <td style="padding:10px">${_usersStatusBadge(u)}</td>
        <td style="padding:10px;text-align:center">${_usersOtpToggle(u)}</td>
      </tr>`).join('')
      : `<tr><td colspan="3" style="padding:24px;text-align:center;color:var(--text3);font-size:13px">${T('USERS_EMPTY')}</td></tr>`;

    supplierTbody.innerHTML = supplierUsers.length ? supplierUsers.map(u => {
      const unlockBtn = u.is_locked
        ? `<button class="btn-sm" style="margin-right:4px;background:#fef3c7;color:#92400e;border-color:#fcd34d" data-action="usersUnlock" data-arg="${u.id}">🔓 Unlock</button>`
        : '';
      const toggleBtn = u.is_active
        ? `<button class="btn-sm" style="margin-right:4px" data-action="usersSetStatus" data-arg="${u.id}" data-arg2="false">${T('BTN_DEACTIVATE')}</button>`
        : `<button class="btn-sm" style="margin-right:4px" data-action="usersSetStatus" data-arg="${u.id}" data-arg2="true">${T('BTN_ACTIVATE')}</button>`;
      const reinviteBtn = `<button class="btn-sm" style="margin-right:4px" data-action="usersReinvite" data-arg="${u.id}">${T('BTN_RESEND_INV')}</button>`;
      const deleteBtn = `<button class="btn-sm" style="background:#fee2e2;color:#991b1b;border-color:#fca5a5" data-action="usersDelete" data-arg="${u.id}">${T('BTN_DELETE_USER')}</button>`;
      return `<tr style="border-bottom:1px solid var(--border)">
        <td style="padding:10px;font-size:13px">${esc(u.email)}</td>
        <td style="padding:10px;font-size:13px;color:var(--text2)">${esc(u.supplier_name)||'—'}</td>
        <td style="padding:10px">${_usersStatusBadge(u)}</td>
        <td style="padding:10px;text-align:center">${_usersOtpToggle(u)}</td>
        <td style="padding:10px;text-align:right">${unlockBtn}${toggleBtn}${reinviteBtn}${deleteBtn}</td>
      </tr>`;
    }).join('')
      : `<tr><td colspan="5" style="padding:24px;text-align:center;color:var(--text3);font-size:13px">${T('USERS_EMPTY')}</td></tr>`;
  }catch(e){
    adminTbody.innerHTML = `<tr><td colspan="3" style="padding:24px;text-align:center;color:var(--red);font-size:13px">${T('USERS_FAILED')}</td></tr>`;
    supplierTbody.innerHTML = `<tr><td colspan="5" style="padding:24px;text-align:center;color:var(--red);font-size:13px">${T('USERS_FAILED')}</td></tr>`;
  }
}

async function usersInvite(){
  const email = document.getElementById('inv-email').value.trim();
  const supplier_name = document.getElementById('inv-supplier').value;
  const msgEl = document.getElementById('users-form-msg');
  msgEl.style.color = 'var(--text3)'; msgEl.textContent = '';
  if(!email){ msgEl.style.color='var(--red)'; msgEl.textContent='Email is required.'; return; }
  if(!supplier_name){ msgEl.style.color='var(--red)'; msgEl.textContent='Please select a supplier.'; return; }
  try{
    const resp = await fetch(_adminApiBase+'/api/admin/users',{method:'POST',headers:authHeaders(),body:JSON.stringify({email,supplier_name})});
    const data = await resp.json().catch(()=>({}));
    if(resp.ok){
      msgEl.style.color='var(--green)';
      msgEl.textContent = 'Invitation sent to ' + email + '.';
      document.getElementById('inv-email').value = '';
      markClean('invite');
      usersLoad();
    } else {
      msgEl.style.color='var(--red)';
      msgEl.textContent = apiErrorText(data.detail, 'Failed to create user.');
    }
  }catch(e){
    msgEl.style.color='var(--red)'; msgEl.textContent='Network error.';
  }
}

async function usersSetStatus(id, active){
  const label = active ? 'activate' : 'deactivate';
  if(!confirm(`Are you sure you want to ${label} this account?`)) return;
  try{
    const resp = await fetch(_adminApiBase+`/api/admin/users/${id}/status`,{method:'PATCH',headers:authHeaders(),body:JSON.stringify({is_active:active})});
    if(resp.ok) usersLoad(); else alert('Failed to update user status.');
  }catch(e){ alert('Network error.'); }
}

async function usersUnlock(id){
  const email = _usersCache.find(u=>u.id===id)?.email || '';
  if(!confirm(`Unlock account "${email}" and clear the failed attempt counter?`)) return;
  try{
    const resp = await fetch(_adminApiBase+`/api/admin/users/${id}/unlock`,{method:'POST',headers:authHeaders()});
    if(resp.ok) usersLoad(); else alert('Failed to unlock account.');
  }catch(e){ alert('Network error.'); }
}

async function usersToggleOtp(id, enabled){
  try{
    const resp = await fetch(_adminApiBase+`/api/admin/users/${id}/otp`,{method:'PATCH',headers:authHeaders(),body:JSON.stringify({otp_enabled:enabled})});
    if(resp.ok) usersLoad(); else alert('Failed to update 2FA setting.');
  }catch(e){ alert('Network error.'); }
}

/* ── Login activity ── */
async function loginActivityLoad(){
  const tbody = document.getElementById('la-tbody');
  tbody.innerHTML = '<tr><td colspan="6" style="padding:24px;text-align:center;color:var(--text3);font-size:13px">'+T('USERS_LOADING')+'</td></tr>';
  try{
    const resp = await fetch(_adminApiBase+'/api/admin/login-activity',{headers:authHeaders()});
    loginActivity = await resp.json();
    renderLoginActivity();
  }catch(e){
    tbody.innerHTML = `<tr><td colspan="6" style="padding:24px;text-align:center;color:var(--red);font-size:13px">${T('USERS_FAILED')}</td></tr>`;
  }
}

function renderLoginActivity(){
  const tbody = document.getElementById('la-tbody');
  const emptyEl = document.getElementById('la-empty');
  const countEl = document.getElementById('la-count');
  const resultFilter = document.getElementById('la-filter-result').value;
  const emailFilter = document.getElementById('la-filter-email').value.trim().toLowerCase();
  const filtered = loginActivity.filter(r => {
    if(resultFilter==='success' && !r.success) return false;
    if(resultFilter==='failed' && r.success) return false;
    if(emailFilter && !(r.email||'').toLowerCase().includes(emailFilter)) return false;
    return true;
  });
  countEl.textContent = '('+filtered.length+' of '+loginActivity.length+' entries)';
  if(!filtered.length){
    tbody.replaceChildren();
    document.getElementById('la-table').style.display = 'none';
    emptyEl.style.display = 'block';
    return;
  }
  document.getElementById('la-table').style.display = '';
  emptyEl.style.display = 'none';

  const rows = filtered.map(r => {
    const tr = document.createElement('tr');
    tr.style.borderBottom = '1px solid var(--border)';

    const tdTs = document.createElement('td');
    tdTs.style.cssText = 'padding:10px;font-size:13px;font-family:var(--mono)';
    tdTs.textContent = r.ts ? new Date(r.ts).toLocaleString() : '—';

    const tdEmail = document.createElement('td');
    tdEmail.style.cssText = 'padding:10px;font-size:13px';
    tdEmail.textContent = r.email || '—';

    const tdResult = document.createElement('td');
    tdResult.style.padding = '10px';
    const badge = document.createElement('span');
    badge.style.cssText = r.success
      ? 'background:#d1fae5;color:#065f46;font-size:11px;padding:2px 8px;border-radius:10px;font-weight:500'
      : 'background:#fee2e2;color:#991b1b;font-size:11px;padding:2px 8px;border-radius:10px;font-weight:500';
    badge.textContent = T(r.success ? 'LA_SUCCESS' : 'LA_FAILED');
    tdResult.appendChild(badge);

    const tdReason = document.createElement('td');
    tdReason.style.cssText = 'padding:10px;font-size:12px;color:var(--text2)';
    tdReason.textContent = r.reason || '—';

    const tdIp = document.createElement('td');
    tdIp.style.cssText = 'padding:10px;font-size:12px;color:var(--text2);font-family:var(--mono)';
    tdIp.textContent = r.ip_address || '—';

    const tdUa = document.createElement('td');
    tdUa.style.cssText = 'padding:10px;font-size:12px;color:var(--text2);max-width:260px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap';
    tdUa.title = r.user_agent || '';
    tdUa.textContent = r.user_agent || '—';

    tr.append(tdTs, tdEmail, tdResult, tdReason, tdIp, tdUa);
    return tr;
  });
  tbody.replaceChildren(...rows);
}

async function usersDelete(id){
  const email = _usersCache.find(u=>u.id===id)?.email || '';
  if(!confirm(`Permanently delete account "${email}"? This cannot be undone.`)) return;
  try{
    const resp = await fetch(_adminApiBase+`/api/admin/users/${id}`,{method:'DELETE',headers:authHeaders()});
    if(resp.ok || resp.status===204) usersLoad(); else { const d=await resp.json().catch(()=>({})); alert(d.detail||'Failed to delete user.'); }
  }catch(e){ alert('Network error.'); }
}

async function usersReinvite(id){
  const email = _usersCache.find(u=>u.id===id)?.email || '';
  if(!confirm(`Resend invitation email to ${email}?`)) return;
  try{
    const resp = await fetch(_adminApiBase+`/api/admin/users/${id}/reinvite`,{method:'POST',headers:authHeaders()});
    const data = await resp.json().catch(()=>({}));
    if(resp.ok) alert('Invitation sent to ' + email + '.');
    else alert(apiErrorText(data.detail, 'Failed to resend invitation.'));
  }catch(e){ alert('Network error.'); }
}

/* ── Communications ── */
function _esc(s){
  const d = document.createElement('div');
  d.textContent = s ?? '';
  return d.innerHTML;
}

function toggleAudienceMode(){
  const selected = document.querySelector('input[name="msg-audience"]:checked').value === 'selected';
  const box = document.getElementById('msg-supplier-list');
  box.style.display = selected ? 'block' : 'none';
  if(selected && !box.innerHTML){
    box.innerHTML = suppliers.map(s => {
      const n = supName(s);
      return `<label style="display:flex;align-items:center;gap:8px;font-size:13px;font-family:var(--font);color:var(--text);padding:4px 0;cursor:pointer">
        <input type="checkbox" class="msg-sup-check" value="${_esc(n)}"><span>${_esc(n)}</span></label>`;
    }).join('') || '<p class="hint">No suppliers found.</p>';
  }
}

async function sendMessage(){
  const subject = document.getElementById('msg-subject').value.trim();
  const bodyText = document.getElementById('msg-body').value.trim();
  const audience = document.querySelector('input[name="msg-audience"]:checked').value;
  const statusEl = document.getElementById('msg-compose-status');
  statusEl.textContent=''; statusEl.style.color='';
  if(!subject || !bodyText){ statusEl.style.color='var(--red)'; statusEl.textContent='Subject and message are required.'; return; }
  let target_suppliers = [];
  if(audience === 'selected'){
    target_suppliers = Array.from(document.querySelectorAll('.msg-sup-check:checked')).map(c=>c.value);
    if(!target_suppliers.length){ statusEl.style.color='var(--red)'; statusEl.textContent='Select at least one supplier.'; return; }
  }
  const audienceLabel = audience === 'all' ? 'all suppliers' : `${target_suppliers.length} selected supplier(s)`;
  if(!confirm(`Send this notification to ${audienceLabel}? This will email them immediately.`)) return;
  try{
    const resp = await fetch(_adminApiBase+'/api/admin/messages',{
      method:'POST', headers:authHeaders(),
      body: JSON.stringify({subject, body: bodyText, audience, target_suppliers})
    });
    const data = await resp.json().catch(()=>({}));
    if(resp.ok){
      statusEl.style.color='var(--green)'; statusEl.textContent='Notification sent.';
      document.getElementById('msg-subject').value='';
      document.getElementById('msg-body').value='';
      markClean('message');
      messagesLoad();
    } else {
      statusEl.style.color='var(--red)'; statusEl.textContent=apiErrorText(data.detail, 'Failed to send notification.');
    }
  }catch(e){ statusEl.style.color='var(--red)'; statusEl.textContent='Network error.'; }
}

let _messagesCache = [];

async function messagesLoad(){
  const box = document.getElementById('msg-history');
  box.innerHTML = '<p class="hint">Loading…</p>';
  try{
    const resp = await fetch(_adminApiBase+'/api/admin/messages',{headers:authHeaders()});
    const list = await resp.json();
    if(!list.length){ box.innerHTML = '<p class="hint">No notifications sent yet.</p>'; _messagesCache = []; return; }
    // Active messages first, archived at the bottom
    list.sort((a,b) => (a.archived - b.archived));
    _messagesCache = list;
    box.innerHTML = list.map(m => {
      const audienceLabel = m.audience === 'all' ? 'All suppliers' : `${m.targetSuppliers.length} suppliers: ${_esc(m.targetSuppliers.join(', '))}`;
      const date = new Date(m.createdAt).toLocaleString();
      const archivedBadge = m.archived
        ? '<span style="font-size:11px;background:#fef3c7;color:#92400e;padding:2px 8px;border-radius:10px;font-weight:500">📦 Archived</span>'
        : '';
      const archiveBtn = m.archived
        ? `<button class="btn-sm" data-action="archiveMessage" data-arg="${esc(m.id)}" data-arg2="false">Restore</button>`
        : `<button class="btn-sm" data-action="archiveMessage" data-arg="${esc(m.id)}" data-arg2="true">Archive</button>`;
      return `<div style="border-bottom:1px solid var(--border);padding:12px 0${m.archived ? ';opacity:.65' : ''}">
        <div style="display:flex;justify-content:space-between;align-items:start;gap:12px">
          <div>
            <strong style="font-size:13px">${_esc(m.subject)}</strong> ${archivedBadge}
            <div style="font-size:11px;color:var(--text3);margin-top:2px">${date} · ${audienceLabel} · by ${_esc(m.createdBy)}</div>
          </div>
          <div style="display:flex;align-items:center;gap:8px;white-space:nowrap">
            <span style="font-size:11px;background:var(--bg3);padding:2px 8px;border-radius:10px;cursor:pointer" title="Click for details" data-action="openMsgStatusModal" data-arg="${esc(m.id)}">${m.readCount}/${m.totalTargets} read</span>
            <span style="font-size:11px;background:#d1fae5;color:#065f46;padding:2px 8px;border-radius:10px;cursor:pointer" title="Click for details" data-action="openMsgStatusModal" data-arg="${esc(m.id)}">${m.ackCount||0}/${m.totalTargets} acknowledged</span>
            ${archiveBtn}
            <button class="btn-sm" data-action="deleteMessageEntry" data-arg="${esc(m.id)}">Delete</button>
          </div>
        </div>
        <div style="font-size:13px;margin-top:8px;white-space:pre-wrap">${_esc(m.body)}</div>
      </div>`;
    }).join('');
  }catch(e){ box.innerHTML = '<p class="hint">Failed to load notifications.</p>'; }
}

async function archiveMessage(id, archived){
  if(archived && !confirm('Archive this notification? It will be hidden from the Supplier Portal but kept here with its read history.')) return;
  try{
    const resp = await fetch(_adminApiBase+'/api/admin/messages/'+id+'/archive',{
      method:'PATCH', headers:authHeaders(), body:JSON.stringify({archived})
    });
    if(resp.ok) messagesLoad(); else alert('Failed to update notification.');
  }catch(e){ alert('Network error.'); }
}

async function deleteMessageEntry(id){
  if(!confirm('Delete this notification? It will be removed from the Supplier Portal (already-sent emails cannot be recalled).')) return;
  try{
    const resp = await fetch(_adminApiBase+'/api/admin/messages/'+id,{method:'DELETE',headers:authHeaders()});
    if(resp.ok) messagesLoad(); else alert('Failed to delete notification.');
  }catch(e){ alert('Network error.'); }
}

function openMsgStatusModal(id){
  const m = _messagesCache.find(x => x.id === id);
  if(!m) return;
  document.getElementById('msg-status-title').textContent = m.subject;
  const rows = (m.recipients || []).map(r => {
    const readLabel = r.read ? new Date(r.readAt).toLocaleString() : '—';
    const ackLabel = r.acknowledged ? new Date(r.ackAt).toLocaleString() : '—';
    const statusBadge = r.acknowledged
      ? '<span style="background:#d1fae5;color:#065f46;font-size:11px;padding:2px 8px;border-radius:10px;font-weight:500">Acknowledged</span>'
      : (r.read
        ? '<span style="background:#dbeafe;color:#1e40af;font-size:11px;padding:2px 8px;border-radius:10px;font-weight:500">Read</span>'
        : '<span style="background:var(--bg3);color:var(--text3);font-size:11px;padding:2px 8px;border-radius:10px;font-weight:500">Unread</span>');
    return `<tr>
      <td style="padding:8px 10px;font-size:13px">${_esc(r.supplier)}</td>
      <td style="padding:8px 10px;text-align:center">${statusBadge}</td>
      <td style="padding:8px 10px;font-size:12px;color:var(--text3)">${readLabel}</td>
      <td style="padding:8px 10px;font-size:12px;color:var(--text3)">${ackLabel}</td>
    </tr>`;
  }).join('');
  document.getElementById('msg-status-body').innerHTML = `
    <table style="width:100%;border-collapse:collapse">
      <thead>
        <tr style="border-bottom:2px solid var(--border)">
          <th style="text-align:left;padding:8px 10px;font-size:12px;color:var(--text3);font-weight:500">Supplier</th>
          <th style="text-align:center;padding:8px 10px;font-size:12px;color:var(--text3);font-weight:500">Status</th>
          <th style="text-align:left;padding:8px 10px;font-size:12px;color:var(--text3);font-weight:500">Read at</th>
          <th style="text-align:left;padding:8px 10px;font-size:12px;color:var(--text3);font-weight:500">Acknowledged at</th>
        </tr>
      </thead>
      <tbody>${rows || '<tr><td colspan="4" style="padding:16px;text-align:center;color:var(--text3)">No recipients.</td></tr>'}</tbody>
    </table>`;
  document.getElementById('msg-status-overlay').style.display = 'flex';
}

function closeMsgStatusModal(){
  document.getElementById('msg-status-overlay').style.display = 'none';
}

/* ── Scheduled notifications ── */
let _schedulesCache = [];
let _editingScheduleId = null;

function schedToggleAudienceMode(){
  const selected = document.querySelector('input[name="sched-audience"]:checked').value === 'selected';
  const box = document.getElementById('sched-supplier-list');
  box.style.display = selected ? 'block' : 'none';
  if(selected && !box.innerHTML){
    box.innerHTML = suppliers.map(s => {
      const n = supName(s);
      return `<label style="display:flex;align-items:center;gap:8px;font-size:13px;font-family:var(--font);color:var(--text);padding:4px 0;cursor:pointer">
        <input type="checkbox" class="sched-sup-check" value="${_esc(n)}"><span>${_esc(n)}</span></label>`;
    }).join('') || '<p class="hint">No suppliers found.</p>';
  }
}

function schedToggleForm(){
  const form = document.getElementById('sched-form');
  const opening = form.style.display === 'none';
  if(!opening && !confirmDiscard('schedule')) return;
  form.style.display = opening ? 'block' : 'none';
  if(!opening){ _editingScheduleId = null; return; }
  markClean('schedule');
  if(_editingScheduleId === null){
    // Fresh "new schedule" open (not triggered via editSchedule) — reset the form
    document.getElementById('sched-subject').value = '';
    document.getElementById('sched-body').value = '';
    document.getElementById('sched-interval').value = 6;
    document.getElementById('sched-start-date').value = new Date().toISOString().slice(0,10);
    document.querySelector('input[name="sched-audience"][value="all"]').checked = true;
    document.getElementById('sched-supplier-list').innerHTML = '';
    schedToggleAudienceMode();
    document.getElementById('sched-form-status').textContent = '';
  }
}

async function saveSchedule(){
  const subject = document.getElementById('sched-subject').value.trim();
  const bodyText = document.getElementById('sched-body').value.trim();
  const audience = document.querySelector('input[name="sched-audience"]:checked').value;
  const interval_months = parseInt(document.getElementById('sched-interval').value, 10);
  const start_date = document.getElementById('sched-start-date').value;
  const statusEl = document.getElementById('sched-form-status');
  statusEl.textContent=''; statusEl.style.color='';
  if(!subject || !bodyText){ statusEl.style.color='var(--red)'; statusEl.textContent='Subject and message are required.'; return; }
  if(!interval_months || interval_months < 1){ statusEl.style.color='var(--red)'; statusEl.textContent='Enter a valid interval (1 or more months).'; return; }
  let target_suppliers = [];
  if(audience === 'selected'){
    target_suppliers = Array.from(document.querySelectorAll('.sched-sup-check:checked')).map(c=>c.value);
    if(!target_suppliers.length){ statusEl.style.color='var(--red)'; statusEl.textContent='Select at least one supplier.'; return; }
  }
  const payload = {subject, body: bodyText, audience, target_suppliers, interval_months, start_date: start_date || undefined};
  try{
    const url = _editingScheduleId
      ? _adminApiBase+'/api/admin/scheduled-notifications/'+_editingScheduleId
      : _adminApiBase+'/api/admin/scheduled-notifications';
    const resp = await fetch(url, {method: _editingScheduleId ? 'PUT' : 'POST', headers:authHeaders(), body:JSON.stringify(payload)});
    const data = await resp.json().catch(()=>({}));
    if(resp.ok){
      _editingScheduleId = null;
      markClean('schedule');
      document.getElementById('sched-form').style.display = 'none';
      schedulesLoad();
    } else {
      statusEl.style.color='var(--red)'; statusEl.textContent=apiErrorText(data.detail, 'Failed to save schedule.');
    }
  }catch(e){ statusEl.style.color='var(--red)'; statusEl.textContent='Network error.'; }
}

function editSchedule(id){
  const s = _schedulesCache.find(x => x.id === id);
  if(!s) return;
  if(_editingScheduleId !== id && !confirmDiscard('schedule')) return;
  _editingScheduleId = id;
  markClean('schedule');
  document.getElementById('sched-form').style.display = 'block';
  document.getElementById('sched-subject').value = s.subject;
  document.getElementById('sched-body').value = s.body;
  document.getElementById('sched-interval').value = s.intervalMonths;
  document.getElementById('sched-start-date').value = s.nextSendAt;
  document.querySelector(`input[name="sched-audience"][value="${s.audience}"]`).checked = true;
  document.getElementById('sched-supplier-list').innerHTML = '';
  schedToggleAudienceMode();
  if(s.audience === 'selected'){
    document.querySelectorAll('.sched-sup-check').forEach(c => { c.checked = s.targetSuppliers.includes(c.value); });
  }
  document.getElementById('sched-form-status').textContent = '';
  document.getElementById('sched-form').scrollIntoView({behavior:'smooth', block:'nearest'});
}

async function toggleScheduleEnabled(id, enabled){
  try{
    const resp = await fetch(_adminApiBase+'/api/admin/scheduled-notifications/'+id+'/enabled',{
      method:'PATCH', headers:authHeaders(), body:JSON.stringify({enabled})
    });
    if(resp.ok) schedulesLoad(); else alert('Failed to update schedule.');
  }catch(e){ alert('Network error.'); }
}

async function deleteSchedule(id){
  if(!confirm('Delete this schedule? Notifications already sent from it are kept in the history.')) return;
  try{
    const resp = await fetch(_adminApiBase+'/api/admin/scheduled-notifications/'+id,{method:'DELETE',headers:authHeaders()});
    if(resp.ok) schedulesLoad(); else alert('Failed to delete schedule.');
  }catch(e){ alert('Network error.'); }
}

async function schedulesLoad(){
  const box = document.getElementById('sched-list');
  try{
    const resp = await fetch(_adminApiBase+'/api/admin/scheduled-notifications',{headers:authHeaders()});
    const list = await resp.json();
    _schedulesCache = list;
    if(!list.length){ box.innerHTML = '<p class="hint">No scheduled notifications.</p>'; return; }
    box.innerHTML = list.map(s => {
      const audienceLabel = s.audience === 'all' ? 'All suppliers' : `${s.targetSuppliers.length} suppliers: ${_esc(s.targetSuppliers.join(', '))}`;
      const pauseBtn = s.enabled
        ? `<button class="btn-sm" data-action="toggleScheduleEnabled" data-arg="${esc(s.id)}" data-arg2="false">Pause</button>`
        : `<button class="btn-sm" data-action="toggleScheduleEnabled" data-arg="${esc(s.id)}" data-arg2="true">Resume</button>`;
      const pausedBadge = s.enabled ? '' : '<span style="font-size:11px;background:var(--bg3);color:var(--text3);padding:2px 8px;border-radius:10px;font-weight:500">Paused</span>';
      return `<div style="border-bottom:1px solid var(--border);padding:12px 0${s.enabled ? '' : ';opacity:.65'}">
        <div style="display:flex;justify-content:space-between;align-items:start;gap:12px">
          <div>
            <strong style="font-size:13px">${_esc(s.subject)}</strong> ${pausedBadge}
            <div style="font-size:11px;color:var(--text3);margin-top:2px">Every ${s.intervalMonths} month(s) · Next: ${s.nextSendAt} · ${audienceLabel}</div>
          </div>
          <div style="display:flex;align-items:center;gap:8px;white-space:nowrap">
            ${pauseBtn}
            <button class="btn-sm" data-action="editSchedule" data-arg="${esc(s.id)}">Edit</button>
            <button class="btn-sm" data-action="deleteSchedule" data-arg="${esc(s.id)}">Delete</button>
          </div>
        </div>
      </div>`;
    }).join('');
  }catch(e){ box.innerHTML = '<p class="hint">Failed to load scheduled notifications.</p>'; }
}

/* ── Tariff editor ── */
// Regulated suppliers (e.g. EAC) always use the CERA-set regulated MDM rate —
// no choice, field locked. Other suppliers always use their own value; there
// is no option for them to opt into the regulated rate.
function onEditSupplierChange(){
  const name=document.getElementById('edit-supplier').value;
  const s=suppliers.find(x=>supName(x)===name);
  const regulated=!!(s&&supObj(s).regulated);
  const mdmEl=document.getElementById('edit-mdm');
  const hintEl=document.getElementById('edit-mdm-hint');
  if(regulated){
    mdmEl.value=getRegulated().mdm||0;
    mdmEl.disabled=true;
    hintEl.textContent='🔒 Fixed by the CERA regulated MDM charge — this supplier is marked regulated (Suppliers tab).';
    hintEl.style.display='block';
  } else {
    mdmEl.disabled=false;
    hintEl.style.display='none';
  }
}
function openEditor(id){
  markClean('tariff'); // fields are reloaded below
  _clearFieldErrors();
  const t=id!=null?tariffs.find(x=>x.id===id):null;
  document.getElementById('edit-id').value=id??'';
  document.getElementById('editor-title').textContent=t?T('MODAL_EDIT_TARIFF'):T('MODAL_ADD_TARIFF');
  const supSel=document.getElementById('edit-supplier');
  supSel.innerHTML=suppliers.length
    ?suppliers.map(s=>{const n=supName(s);return `<option value="${esc(n)}">${esc(n)}</option>`;}).join('')
    :'<option value="">— add suppliers first —</option>';
  refreshProfileDropdowns();
  if(t){
    document.getElementById('edit-name').value=t.name;
    supSel.value=t.supplier;
    document.getElementById('edit-contract').value=t.contract;
    document.getElementById('edit-voltage').value=t.voltage;
    document.getElementById('edit-pricing').value=t.pricing;
    document.getElementById('edit-standing').value=t.standing;
    document.getElementById('edit-mdm').value=t.mdm||0;
    document.getElementById('edit-mdm-invoice-months').value=t.mdmInvoiceMonths||2;
    onEditSupplierChange();
    document.getElementById('edit-profile').value=t.profileId||'';
    // Load entitlement
    document.getElementById('edit-le').value=t.loadEntitlement||'any';
    updateLoadEntitlementField();
    // Discounts
    setDiscounts(t.discounts||[]);
    // Duration
    const durType=t.durationMonths?'fixed':'indefinite';
    document.getElementById('edit-duration-type').value=durType;
    document.getElementById('edit-duration-months').value=t.durationMonths||12;
    updateDurationType();
    // FPA
    const fpaSource=t.fpaSource||'global';
    document.getElementById('edit-fpa-source').value=fpaSource;
    document.getElementById('edit-fpa-custom').value=t.fpaCustom||0;
    updateFpaSource();
    // Vulnerable
    document.getElementById('edit-vulnerable').checked=t.vulnerable||false;
    const r=t.rates;
    if(t.pricing==='Fixed') document.getElementById('fix-rate').value=r.rate;
    else if(t.pricing==='ToU'){
      document.getElementById('tou-hi-start').value=r.hiStart;
      document.getElementById('tou-hi-end').value=r.hiEnd;
      document.getElementById('tou-hi-ps').value=r.hiPeakStart;
      document.getElementById('tou-hi-pe').value=r.hiPeakEnd;
      document.getElementById('tou-lo-ps').value=r.loPeakStart;
      document.getElementById('tou-lo-pe').value=r.loPeakEnd;
      document.getElementById('tou-hi-pr').value=r.hiPeakRate;
      document.getElementById('tou-hi-or').value=r.hiOffRate;
      document.getElementById('tou-lo-pr').value=r.loPeakRate;
      document.getElementById('tou-lo-or').value=r.loOffRate;
    } else if(t.pricing==='Dynamic'){
      document.getElementById('var-mult').value=r.mult;
      document.getElementById('var-adder').value=r.adder;
      document.getElementById('var-dam-floor').value=r.damFloor||'';
    } else if(t.pricing==='Variable'){
      document.getElementById('var-reset-months').value=r.resetMonths||2;
      renderTierRows(r.tiers||[{upTo:null,rate:0}]);
    }
  } else {
    document.getElementById('edit-name').value='';
    document.getElementById('edit-standing').value='5.50';
    document.getElementById('edit-mdm').value='0';
    document.getElementById('edit-mdm-invoice-months').value='2';
    onEditSupplierChange();
    document.getElementById('edit-pricing').value='Fixed';
    document.getElementById('edit-profile').value='';
    document.getElementById('edit-fpa-source').value='global';
    document.getElementById('edit-fpa-custom').value='0.0000';
    updateFpaSource();
    document.getElementById('edit-duration-type').value='indefinite';
    document.getElementById('edit-duration-months').value=12;
    updateDurationType();
    document.getElementById('edit-le').value='any';
    updateLoadEntitlementField();
    setDiscounts([]);
    document.getElementById('edit-vulnerable').checked=false;
    renderTierRows([{upTo:100,rate:0.08},{upTo:null,rate:0.13}]);
  }
  updatePricingFields();
  document.getElementById('editor-status').className='status';
  document.getElementById('editor-overlay').style.display='flex';
}
function closeEditor(){
  if(!confirmDiscard('tariff')) return;
  document.getElementById('editor-overlay').style.display='none';
  setEditorLocked(false); // reset for next open
}

function openViewer(id){
  openEditor(id);
  setEditorLocked(true);
}

function setEditorLocked(locked){
  const overlay=document.getElementById('editor-overlay');
  overlay.querySelectorAll('input,select,textarea').forEach(el=>{el.disabled=locked;});
  overlay.querySelectorAll('button:not(.editor-action-btn)').forEach(el=>{el.disabled=locked;});
  document.getElementById('editor-lock-banner').style.display=locked?'flex':'none';
  document.getElementById('editor-edit-btns').style.display=locked?'none':'flex';
  document.getElementById('editor-view-btns').style.display=locked?'flex':'none';
  if(locked){
    document.getElementById('editor-title').textContent=T('MODAL_VIEW_TARIFF');
  }
}

function editorStartEdit(){
  if(!confirm('Are you sure you want to edit this tariff?')) return;
  setEditorLocked(false);
  const id=document.getElementById('edit-id').value;
  const t=tariffs.find(x=>x.id===id);
  document.getElementById('editor-title').textContent=t?T('MODAL_EDIT_TARIFF'):T('MODAL_ADD_TARIFF');
}

async function editorDeleteFromViewer(){
  const id=document.getElementById('edit-id').value;
  const t=tariffs.find(x=>x.id===id);
  if(!t) return;
  if(!confirm('Are you sure you want to delete "'+t.name+'"?\n\nThis cannot be undone.')) return;
  const before=tariffs.length;
  await deleteTariff(id);   // server first; only updates the page if the delete succeeded
  if(tariffs.length<before) closeEditor();
}

function updateFpaSource(){
  const src=document.getElementById('edit-fpa-source').value;
  const customField=document.getElementById('fpa-custom-field');
  const hint=document.getElementById('fpa-hint');
  customField.style.display=src==='custom'?'':'none';
  const r=getRegulated();
  const voltageEl=document.getElementById('edit-voltage');
  const vol=voltageEl?voltageEl.value:'LV';
  const globalRate=vol==='LV'?r.fpaLV:vol==='MV'?r.fpaMV:r.fpaHV;
  if(src==='global') hint.textContent=`This tariff uses the global ${vol} FPA rate (currently €${globalRate.toFixed(4)}/kWh). Change the global value in the Regulated tab to update all linked tariffs at once.`;
  else if(src==='custom') hint.textContent='Enter a specific FPA rate for this tariff only.';
  else hint.textContent='No FPA applied to this tariff.';
  const preview=document.getElementById('fpa-global-preview');
  if(preview) preview.textContent='€'+globalRate.toFixed(4);
}
/* ── Discount management ── */
function addDiscount(type){
  const container=document.getElementById(type+'-discounts');
  if(!container) return;
  const id='disc-'+Date.now();
  const row=document.createElement('div');
  row.className='discount-row';
  row.id=id;
  row.innerHTML=`
    <div class="field">
      <label>Conditions / description</label>
      <input type="text" placeholder="e.g. Direct debit payment" style="width:100%">
    </div>
    <div class="field">
      <label>Discount %</label>
      <input type="number" value="10" min="0.01" max="100" step="0.01">
    </div>
    <div class="field">
      <label>Duration (months)</label>
      <input type="number" value="" min="1" step="1" placeholder="∞">
    </div>
    <div class="field" style="grid-column:span 1">
      <label>Type</label>
      <input type="hidden" value="${type}">
      <span style="font-size:12px;font-family:var(--mono);color:var(--text2);padding-top:8px;display:block">${type==='standing'?'Standing charge':'Energy cost'}</span>
    </div>
    <div style="padding-top:18px">
      <button class="btn btn-danger btn-sm" data-action="removeDiscountRow" data-arg="${id}">✕</button>
    </div>`;
  container.appendChild(row);
}

function getDiscounts(){
  const discounts=[];
  ['standing','energy'].forEach(type=>{
    const container=document.getElementById(type+'-discounts');
    if(!container) return;
    container.querySelectorAll('.discount-row').forEach(row=>{
      const inputs=row.querySelectorAll('input');
      const conditions=inputs[0].value.trim();
      const pct=parseFloat(inputs[1].value)||0;
      const dur=parseInt(inputs[2].value)||null;
      if(pct>0) discounts.push({type,percentage:pct,durationMonths:dur,conditions});
    });
  });
  return discounts;
}

function setDiscounts(discounts){
  ['standing','energy'].forEach(type=>{
    const container=document.getElementById(type+'-discounts');
    if(container) container.innerHTML='';
  });
  if(!discounts||!discounts.length) return;
  discounts.forEach(d=>{
    addDiscount(d.type);
    const container=document.getElementById(d.type+'-discounts');
    const row=container.lastElementChild;
    const inputs=row.querySelectorAll('input');
    inputs[0].value=d.conditions||'';
    inputs[1].value=d.percentage||0;
    inputs[2].value=d.durationMonths||'';
  });
}

function updateDurationType(){
  const t=document.getElementById('edit-duration-type').value;
  document.getElementById('duration-months-field').style.display=t==='fixed'?'':'none';
}

function updateLoadEntitlementField(){
  const contract=document.getElementById('edit-contract').value;
  const voltage=document.getElementById('edit-voltage').value;
  const show=(contract==='Commercial'||contract==='Industrial')&&(voltage==='LV'||voltage==='MV');
  document.getElementById('le-admin-field').style.display=show?'':'none';
  const isDomestic=contract==='Domestic';
  document.getElementById('vulnerable-field').style.display=isDomestic?'':'none';
  if(!isDomestic) document.getElementById('edit-vulnerable').checked=false;
}
function renderTierRows(tiers){
  const container=document.getElementById('tier-rows');
  if(!container) return;
  container.innerHTML='';
  (tiers||[{upTo:null,rate:0}]).forEach((_,i)=>addTierRow(i<(tiers||[]).length?tiers[i]:null));
}
function addTierRow(existing){
  const container=document.getElementById('tier-rows');
  if(!container) return;
  const idx=container.children.length;
  const row=document.createElement('div');
  row.className='tier-row';
  row.style.cssText='display:flex;gap:8px;align-items:center;flex-wrap:wrap;background:var(--bg3);border:1px solid var(--border);border-radius:2px;padding:8px 10px';
  const upToVal=existing&&existing.upTo!=null?existing.upTo:'';
  const rateVal=existing?existing.rate:'';
  const fixedVal=existing&&existing.fixedCharge!=null?existing.fixedCharge:'';
  row.innerHTML=''
    +'<span style="font-size:11px;font-family:var(--mono);color:var(--text3);white-space:nowrap;min-width:28px">Tier '+(idx+1)+'</span>'
    +'<div style="display:flex;align-items:center;gap:4px">'
    +'<span style="font-size:11px;color:var(--text3)">up to</span>'
    +'<input type="number" class="tier-upto" value="'+esc(upToVal)+'" placeholder="∞" min="1" step="1"'
    +' style="width:80px;padding:4px 6px;border:1px solid var(--border);border-radius:2px;background:var(--bg);color:var(--text);font-size:12px;font-family:var(--mono)">'
    +'<span style="font-size:11px;color:var(--text3)">kWh</span>'
    +'</div>'
    +'<div style="display:flex;align-items:center;gap:4px">'
    +'<span style="font-size:11px;color:var(--text3)">rate</span>'
    +'<input type="number" class="tier-rate" value="'+esc(rateVal)+'" placeholder="€/kWh" min="0" step="0.0001"'
    +' style="width:80px;padding:4px 6px;border:1px solid var(--border);border-radius:2px;background:var(--bg);color:var(--text);font-size:12px;font-family:var(--mono)">'
    +'<span style="font-size:11px;color:var(--text3)">€/kWh</span>'
    +'</div>'
    +'<div style="display:flex;align-items:center;gap:4px">'
    +'<span style="font-size:11px;color:var(--text3)">fixed</span>'
    +'<input type="number" class="tier-fixed" value="'+esc(fixedVal)+'" placeholder="0.00" min="0" step="0.01"'
    +' style="width:72px;padding:4px 6px;border:1px solid var(--border);border-radius:2px;background:var(--bg);color:var(--text);font-size:12px;font-family:var(--mono)">'
    +'<span style="font-size:11px;color:var(--text3)">€/period</span>'
    +'</div>'
    +'<button data-action="removeTierRow" style="background:none;border:none;cursor:pointer;color:var(--red);font-size:14px;padding:2px 4px" title="Remove tier">✕</button>';
  container.appendChild(row);
  updateTierLabels();
}
function removeTierRow(btn){
  const container=document.getElementById('tier-rows');
  if(container.children.length<=1){alert('A Variable tariff needs at least one tier.');return;}
  btn.closest('.tier-row').remove();
  updateTierLabels();
}
function updateTierLabels(){
  const rows=document.querySelectorAll('#tier-rows .tier-row');
  rows.forEach((row,i)=>{
    const lbl=row.querySelector('span');
    if(lbl) lbl.textContent='Tier '+(i+1);
  });
}
function getTiers(){
  const rows=document.querySelectorAll('#tier-rows .tier-row');
  const tiers=[];
  rows.forEach((row,i)=>{
    const upToInput=row.querySelector('.tier-upto');
    const rateInput=row.querySelector('.tier-rate');
    const fixedInput=row.querySelector('.tier-fixed');
    const upToVal=parseFloat(upToInput.value);
    const rate=parseFloat(rateInput.value)||0;
    const fixedCharge=fixedInput&&fixedInput.value!==''?parseFloat(fixedInput.value)||0:0;
    const upTo=(isNaN(upToVal)||upToInput.value==='')?null:upToVal;
    tiers.push({upTo,rate,fixedCharge});
  });
  // Ensure last tier has upTo:null
  if(tiers.length>0) tiers[tiers.length-1].upTo=null;
  return tiers;
}

function updatePricingFields(){
  const p=document.getElementById('edit-pricing').value;
  document.getElementById('fields-fixed').style.display=p==='Fixed'?'':'none';
  document.getElementById('fields-tou').style.display=p==='ToU'?'':'none';
  document.getElementById('fields-dynamic').style.display=p==='Dynamic'?'':'none';
  document.getElementById('fields-variable').style.display=p==='Variable'?'':'none';
}

// ── Field-level errors in the tariff editor ───────────────────────────────────
// Each problem is shown next to its own field (red outline + message), not only
// in the status line. The page checks first, using the server's limits
// (schemas.TariffIn); anything the server still refuses is mapped back to its
// field where possible. Same approach as supplier.js.
const _MAX_RATE = 5;        // €/kWh — config.TARIFF_MAX_ENERGY_RATE default
const _MAX_MONTHLY = 1000;  // €/month — config.TARIFF_MAX_MONTHLY_CHARGE default
const _RATE_FIELDS = {rate:'fix-rate', hiStart:'tou-hi-start', hiEnd:'tou-hi-end', hiPeakStart:'tou-hi-ps',
  hiPeakEnd:'tou-hi-pe', loPeakStart:'tou-lo-ps', loPeakEnd:'tou-lo-pe', hiPeakRate:'tou-hi-pr',
  hiOffRate:'tou-hi-or', loPeakRate:'tou-lo-pr', loOffRate:'tou-lo-or', mult:'var-mult', adder:'var-adder',
  damFloor:'var-dam-floor', resetMonths:'var-reset-months'};
const _BODY_FIELDS = {name:'edit-name', supplier:'edit-supplier', standing:'edit-standing', mdm:'edit-mdm',
  fpaCustom:'edit-fpa-custom', durationMonths:'edit-duration-months', profileId:'edit-profile',
  loadEntitlement:'edit-le', mdmInvoiceMonths:'edit-mdm-invoice-months'};
const _TIER_FIELDS = {upTo:'.tier-upto', rate:'.tier-rate', fixedCharge:'.tier-fixed'};
const _DISC_INPUT = {conditions:0, percentage:1, durationMonths:2};   // order of a discount row's inputs

function _tn(key, n){ return T(key).replace('{N}', n); }
function _discountRows(){
  // Same order as getDiscounts(): standing rows, then energy rows.
  return ['standing','energy'].flatMap(t => [...document.querySelectorAll('#'+t+'-discounts .discount-row')]);
}
function _clearFieldErrors(){
  document.querySelectorAll('#editor-overlay .field-invalid').forEach(el => { el.classList.remove('field-invalid'); el.removeAttribute('aria-invalid'); });
  document.querySelectorAll('#editor-overlay .field-err-msg').forEach(el => el.remove());
}
// Mark one input (or the tier list) as wrong and put the message right under it.
function _fieldError(el, msg){
  if(!el || el.classList.contains('field-invalid')) return false;   // first problem per field wins
  el.classList.add('field-invalid');
  el.setAttribute('aria-invalid', 'true');
  const m = document.createElement('div');
  m.className = 'field-err-msg';
  m.textContent = msg;
  const host = el.closest('.field') || el.closest('.tier-row');
  if(host && host.classList.contains('field')) host.appendChild(m);
  else (host || el).insertAdjacentElement('afterend', m);
  el._errMsg = m;
  return true;
}
// Typing in a highlighted field clears its highlight.
['input','change'].forEach(evt => document.addEventListener(evt, e => {
  const el = e.target;
  if(!(el instanceof Element) || !el.classList.contains('field-invalid')) return;
  el.classList.remove('field-invalid'); el.removeAttribute('aria-invalid');
  if(el._errMsg){ el._errMsg.remove(); el._errMsg = null; }
}));
// Check one number box. opts: required, min, above (exclusive min), max, whole.
function _checkNumber(el, opts){
  const raw = (el.value || '').trim();
  if(raw === ''){ return opts.required ? _fieldError(el, T('ERR_F_REQUIRED')) : false; }
  const v = Number(raw);
  if(!Number.isFinite(v)) return _fieldError(el, T('ERR_F_REQUIRED'));
  if(opts.whole && !Number.isInteger(v)) return _fieldError(el, T('ERR_F_WHOLE'));
  if(opts.above != null && !(v > opts.above)) return _fieldError(el, _tn('ERR_F_ABOVE', opts.above));
  if(opts.min != null && v < opts.min) return _fieldError(el, _tn('ERR_F_MIN', opts.min));
  if(opts.max != null && v > opts.max) return _fieldError(el, _tn('ERR_F_MAX', opts.max));
  return false;
}
// Returns the number of problems found (0 = OK to save).
function _validateTariffForm(){
  _clearFieldErrors();
  const $ = id => document.getElementById(id);
  const RATE = {required:true, min:0, max:_MAX_RATE};
  const MONTHLY = {required:true, min:0, max:_MAX_MONTHLY};
  if(!sv('edit-name')) _fieldError($('edit-name'), T('ERR_F_NAME'));
  else if(sv('edit-name').length > 200) _fieldError($('edit-name'), _tn('ERR_F_TOO_LONG', 200));
  if(!sv('edit-supplier')) _fieldError($('edit-supplier'), T('ERR_F_SUPPLIER'));
  if(sv('edit-duration-type') === 'fixed') _checkNumber($('edit-duration-months'), {required:true, whole:true, min:1, max:120});
  _checkNumber($('edit-standing'), MONTHLY);
  _checkNumber($('edit-mdm'), MONTHLY);
  if(sv('edit-fpa-source') === 'custom') _checkNumber($('edit-fpa-custom'), {required:true, min:-_MAX_RATE, max:_MAX_RATE});
  const pricing = sv('edit-pricing');
  if(pricing === 'Fixed') _checkNumber($('fix-rate'), RATE);
  if(pricing === 'ToU'){
    ['tou-hi-start','tou-hi-end'].forEach(id => _checkNumber($(id), {required:true, whole:true, min:0, max:12}));
    ['tou-hi-ps','tou-hi-pe','tou-lo-ps','tou-lo-pe'].forEach(id => _checkNumber($(id), {required:true, min:0, max:24}));
    ['tou-hi-pr','tou-hi-or','tou-lo-pr','tou-lo-or'].forEach(id => _checkNumber($(id), RATE));
  }
  if(pricing === 'Dynamic'){
    _checkNumber($('var-mult'), {required:true, above:0, max:10});
    _checkNumber($('var-adder'), {required:true, min:-_MAX_RATE, max:_MAX_RATE});
    _checkNumber($('var-dam-floor'), {min:0, max:_MAX_RATE});
  }
  if(pricing === 'Variable'){
    const rows = [...document.querySelectorAll('#tier-rows .tier-row')];
    if(!rows.length) _fieldError($('tier-rows'), T('ERR_F_TIER_NEEDED'));
    let prev = 0;
    rows.forEach((row, i) => {
      const upTo = row.querySelector('.tier-upto');
      if(i < rows.length - 1){                     // the last tier is always "no limit" (getTiers)
        if(upTo.value.trim() === '') _fieldError(upTo, T('ERR_F_TIER_OPEN'));
        else if(!_checkNumber(upTo, {above:0, max:10000000})){
          if(+upTo.value <= prev) _fieldError(upTo, T('ERR_F_TIER_ORDER'));
          prev = +upTo.value;
        }
      }
      _checkNumber(row.querySelector('.tier-rate'), RATE);
      _checkNumber(row.querySelector('.tier-fixed'), {min:0, max:_MAX_MONTHLY});
    });
  }
  _discountRows().forEach(row => {
    const inputs = row.querySelectorAll('input');
    const pct = inputs[_DISC_INPUT.percentage], v = Number(pct.value);
    if(pct.value.trim() === '' || !(v > 0) || v > 100) _fieldError(pct, T('ERR_F_DISC_PCT'));
    _checkNumber(inputs[_DISC_INPUT.durationMonths], {whole:true, min:1, max:120});
  });
  return _showErrorSummary();
}
function _showErrorSummary(extra){
  const bad = document.querySelectorAll('#editor-overlay .field-invalid');
  if(!bad.length && !extra) return 0;
  const parts = [];
  if(bad.length) parts.push(_tn('ERR_FIELDS_SUMMARY', bad.length));
  if(extra) parts.push(extra);
  showStatus(document.getElementById('editor-status'), 'err', parts.join(' '));
  if(bad.length){ bad[0].scrollIntoView({block:'center', behavior:'smooth'}); bad[0].focus({preventScroll:true}); }
  return bad.length || 1;
}
// Server-side message ("Input should be greater than or equal to 0") → the page's wording.
function _friendlyMsg(type, ctx, msg){
  msg = String(msg || '').replace(/^Value error, /, '');
  const n = ctx && (ctx.ge ?? ctx.gt ?? ctx.le ?? ctx.lt ?? ctx.max_length);
  if(type === 'missing') return T('ERR_F_REQUIRED');
  if(type === 'greater_than_equal') return _tn('ERR_F_MIN', n);
  if(type === 'greater_than') return _tn('ERR_F_ABOVE', n);
  if(type === 'less_than_equal') return _tn('ERR_F_MAX', n);
  if(type === 'string_too_long') return _tn('ERR_F_TOO_LONG', n);
  let m;
  if((m = msg.match(/greater than or equal to (-?\d+(?:\.\d+)?)/))) return _tn('ERR_F_MIN', m[1]);
  if((m = msg.match(/greater than (-?\d+(?:\.\d+)?)/))) return _tn('ERR_F_ABOVE', m[1]);
  if((m = msg.match(/less than or equal to (-?\d+(?:\.\d+)?)/))) return _tn('ERR_F_MAX', m[1]);
  if(/strictly increasing/.test(msg)) return T('ERR_F_TIER_ORDER');
  if(/no upper limit/.test(msg)) return T('ERR_F_TIER_OPEN');
  return msg;
}
// Map a 422 from the server onto the editor's fields; anything unplaceable stays in the summary.
function _showServerErrors(detail){
  if(!Array.isArray(detail)) return false;
  _clearFieldErrors();
  const discRows = _discountRows();
  const tierRows = [...document.querySelectorAll('#tier-rows .tier-row')];
  const unplaced = [];
  detail.forEach(d => {
    const loc = (d.loc || []).filter(x => x !== 'body');
    let el = null;
    if(loc.length === 1 && _BODY_FIELDS[loc[0]]) el = document.getElementById(_BODY_FIELDS[loc[0]]);
    else if(loc[0] === 'discounts' && discRows[loc[1]] && _DISC_INPUT[loc[2]] != null) el = discRows[loc[1]].querySelectorAll('input')[_DISC_INPUT[loc[2]]];
    if(el){ _fieldError(el, _friendlyMsg(d.type, d.ctx, d.msg)); return; }
    // The rates check reports "invalid <pricing> rates — path: message; path: message".
    const text = String(d.msg || '');
    const dash = text.indexOf(' — ');
    if(loc.length === 0 && dash > 0 && /rates/.test(text)){
      text.slice(dash + 3).split('; ').forEach(part => {
        const i = part.indexOf(': ');
        const path = (i > 0 ? part.slice(0, i) : '').split('.');
        const msg = i > 0 ? part.slice(i + 2) : part;
        let rel = null;
        if(path.length === 1 && _RATE_FIELDS[path[0]]) rel = document.getElementById(_RATE_FIELDS[path[0]]);
        else if(path[0] === 'tiers' && tierRows[path[1]] && _TIER_FIELDS[path[2]]) rel = tierRows[path[1]].querySelector(_TIER_FIELDS[path[2]]);
        if(rel) _fieldError(rel, _friendlyMsg(null, null, msg)); else unplaced.push(part);
      });
      return;
    }
    unplaced.push((loc.length ? loc.join(' › ') + ': ' : '') + _friendlyMsg(d.type, d.ctx, d.msg));
  });
  _showErrorSummary(unplaced.join('; '));
  return true;
}

async function saveTariff(){
  if(_validateTariffForm()) return;
  const name=sv('edit-name'),supplier=sv('edit-supplier');
  if(!name||!supplier){showStatus(document.getElementById('editor-status'),'err','Name and supplier required.');return;}
  const pricing=sv('edit-pricing');
  let rates={};
  if(pricing==='Fixed') rates={rate:fv('fix-rate')};
  else if(pricing==='ToU') rates={
    hiStart:fv('tou-hi-start'),hiEnd:fv('tou-hi-end'),
    hiPeakStart:fv('tou-hi-ps'),hiPeakEnd:fv('tou-hi-pe'),
    loPeakStart:fv('tou-lo-ps'),loPeakEnd:fv('tou-lo-pe'),
    hiPeakRate:fv('tou-hi-pr'),hiOffRate:fv('tou-hi-or'),
    loPeakRate:fv('tou-lo-pr'),loOffRate:fv('tou-lo-or'),
  };
  else if(pricing==='Variable'){
    const tiers=getTiers();
    if(tiers.length<1){showStatus(document.getElementById('editor-status'),'err','Variable tariff needs at least one tier.');return;}
    rates={resetMonths:parseInt(document.getElementById('var-reset-months').value)||2,tiers};
  }
  else {
    const floorVal=parseFloat(document.getElementById('var-dam-floor')?.value);
    rates={
      mult:fv('var-mult'),
      adder:fv('var-adder'),
      damFloor:isNaN(floorVal)||floorVal<=0?null:floorVal
    };
  }
  const editId=document.getElementById('edit-id').value;
  const fpaSource=sv('edit-fpa-source');
  const fpaCustom=fpaSource==='custom'?fv('edit-fpa-custom'):0;
  const durationType=sv('edit-duration-type');
  const durationMonths=durationType==='fixed'?fv('edit-duration-months'):null;
  const contractVal=sv('edit-contract');
  const voltageVal=sv('edit-voltage');
  const leApplies=(contractVal==='Commercial'||contractVal==='Industrial')&&(voltageVal==='LV'||voltageVal==='MV');
  const now=new Date().toISOString();
  const oldTariff=editId?tariffs.find(t=>t.id===editId):null;
  const tariff={
    id:editId||uid(),name,supplier,
    contract:contractVal,
    voltage:voltageVal,
    pricing,standing:fv('edit-standing'),mdm:fv('edit-mdm'),
    mdmSource:(suppliers.find(x=>supName(x)===supplier)&&supObj(suppliers.find(x=>supName(x)===supplier)).regulated)?'global':'custom',
    mdmInvoiceMonths:parseInt(sv('edit-mdm-invoice-months'))||2,rates,
    profileId:sv('edit-profile')||null,
    fpaSource,fpaCustom,
    durationMonths,
    loadEntitlement:leApplies?(sv('edit-le')||'any'):null,
    discounts:getDiscounts(),
    vulnerable:document.getElementById('edit-vulnerable').checked||false,
    createdAt:oldTariff?oldTariff.createdAt:now,
    updatedAt:now
  };

  const editorStatus=document.getElementById('editor-status');
  showStatus(editorStatus,'ok','Saving…');
  try {
    const url=editId
      ?_adminApiBase+'/api/admin/tariffs/'+encodeURIComponent(editId)
      :_adminApiBase+'/api/admin/tariffs';
    const resp=await fetch(url,{method:editId?'PUT':'POST',headers:authHeaders(),body:JSON.stringify(tariff)});
    if(resp.status===401){showLogin('Session expired.');return;}
    if(!resp.ok){
      const e=await resp.json().catch(()=>({}));
      if(!(resp.status===422&&_showServerErrors(e.detail))) showStatus(editorStatus,'err','Save failed: '+apiErrorText(e.detail,resp.status));
      return;
    }
    const saved=await resp.json();
    if(editId){
      const i=tariffs.findIndex(t=>t.id===editId);
      if(i>=0){
        const changes=diffTariff(tariffs[i],saved);
        addChangelogEntry({action:'updated',tariffId:saved.id,tariffName:saved.name,supplier:saved.supplier,changes,ts:now});
        tariffs[i]=saved;
      }
    } else {
      const changes=tariffToChangeFields(saved);
      addChangelogEntry({action:'created',tariffId:saved.id,tariffName:saved.name,supplier:saved.supplier,changes,ts:now});
      tariffs.push(saved);
    }
    markClean('tariff');renderTariffs();closeEditor();
  } catch(e){showStatus(editorStatus,'err','Save failed: '+e.message);}
}
async function deleteTariff(id){
  try {
    const resp=await fetch(_adminApiBase+'/api/admin/tariffs/'+encodeURIComponent(id),{method:'DELETE',headers:authHeaders()});
    if(resp.status===401){showLogin('Session expired.');return;}
    if(!resp.ok){const e=await resp.json().catch(()=>({}));alert('Delete failed: '+(e.detail||resp.status));return;}
  } catch(e){alert('Delete failed: '+e.message);return;}
  const t=tariffs.find(x=>x.id===id);
  if(t) addChangelogEntry({action:'deleted',tariffId:t.id,tariffName:t.name,supplier:t.supplier,changes:[],ts:new Date().toISOString()});
  tariffs=tariffs.filter(x=>x.id!==id);renderTariffs();
}
async function setTariffStatus(id,status,reason=''){
  const body={status};
  if(reason) body.reason=reason;
  const resp=await fetch(_adminApiBase+'/api/admin/tariffs/'+encodeURIComponent(id)+'/status',{
    method:'PATCH',headers:authHeaders(),body:JSON.stringify(body)
  });
  if(resp.status===401){showLogin('Session expired.');return;}
  if(!resp.ok){const e=await resp.json().catch(()=>({}));alert('Status update failed: '+(e.detail||resp.status));return;}
  const t=tariffs.find(x=>x.id===id);
  if(t){t.status=status;if(status==='rejected')t.rejectionReason=reason;else t.rejectionReason=null;}
  closeReview();
  renderTariffs();
}
async function suspendTariff(id){
  const name=tariffs.find(t=>t.id===id)?.name||'';
  if(!confirm(`Suspend "${name}"?\n\nIt will be taken offline immediately and hidden from the public calculator until restored.`)) return;
  await setTariffStatus(id,'suspended');
}
let _rejectTargetId=null;
function showRejectPanel(id){
  _rejectTargetId=id;
  document.getElementById('review-approve-btn').style.display='none';
  document.getElementById('review-reject-btn').style.display='none';
  document.getElementById('reject-reason-panel').style.display='block';
  document.querySelectorAll('input[name="reject-preset"]').forEach(r=>r.checked=false);
  document.getElementById('reject-custom-text').style.display='none';
  document.getElementById('reject-custom-text').value='';
}
function cancelReject(){
  document.getElementById('review-approve-btn').style.display='';
  document.getElementById('review-reject-btn').style.display='';
  document.getElementById('reject-reason-panel').style.display='none';
}
async function confirmReject(){
  const selected=document.querySelector('input[name="reject-preset"]:checked');
  if(!selected){alert('Please select a reason for rejection.');return;}
  let reason=selected.value;
  if(reason==='__custom__'){
    reason=document.getElementById('reject-custom-text').value.trim();
    if(!reason){alert('Please enter a rejection reason.');return;}
  }
  await setTariffStatus(_rejectTargetId,'rejected',reason);
  cancelReject();
}

function formatRatesSummary(pricing,rates){
  if(!rates) return '—';
  if(pricing==='Fixed') return '€'+(rates.rate||0).toFixed(4)+'/kWh (flat)';
  if(pricing==='ToU'){
    return 'Hi-season peak €'+(rates.hiPeakRate||0).toFixed(4)+' / off-peak €'+(rates.hiOffRate||0).toFixed(4)
      +'\nLo-season peak €'+(rates.loPeakRate||0).toFixed(4)+' / off-peak €'+(rates.loOffRate||0).toFixed(4)
      +'\nHi season: month '+(rates.hiStart||'?')+' – '+(rates.hiEnd||'?');
  }
  if(pricing==='Dynamic'){
    return '×'+(rates.mult||1)+' DAM + €'+(rates.adder||0).toFixed(4)+'/kWh'
      +(rates.damFloor?' (floor €'+rates.damFloor.toFixed(4)+')':'');
  }
  if(pricing==='Variable'){
    const ts=(rates.tiers||[]).map((t,i)=>
      'Tier '+(i+1)+': '+(t.upTo!=null?'up to '+t.upTo+' kWh':'∞')+' @ €'+(Number(t.rate)||0).toFixed(4)+'/kWh'
    ).join('\n');
    return 'Reset every '+(rates.resetMonths||2)+' month(s)\n'+ts;
  }
  return JSON.stringify(rates);
}

function openReview(id){
  const t=tariffs.find(x=>x.id===id);
  if(!t) return;

  // Find the most recent changelog entry for this tariff
  const log=(changelog||[]).filter(c=>c.tariffId===id).sort((a,b)=>b.ts.localeCompare(a.ts));
  const latest=log[0]||null;
  const action=latest?.action||'created';
  const changes=latest?.changes||[];
  const changedFields=new Set(changes.map(c=>c.field));
  const isNew=action==='created';

  const prof=profiles.find(p=>p.id===t.profileId);

  // Builds a <span> whose text is line-broken on '\n' using real <br> elements,
  // instead of a raw HTML string with '\n'.replace(/\n/g,'<br>').
  function multilineSpan(cls,text){
    const span=document.createElement('span');
    if(cls) span.className=cls;
    String(text).split('\n').forEach((line,i)=>{
      if(i>0) span.appendChild(document.createElement('br'));
      span.appendChild(document.createTextNode(line));
    });
    return span;
  }

  function row(field,label,val){
    const isChanged=changedFields.has(field);
    const ch=changes.find(c=>c.field===field);

    const rowEl=document.createElement('div');
    rowEl.className='review-row'+(isNew||isChanged?' changed':'');
    const lblEl=document.createElement('span');
    lblEl.className='review-lbl';
    lblEl.textContent=label;
    const valEl=document.createElement('span');
    valEl.className='review-val';
    rowEl.append(lblEl,valEl);

    if(isNew){
      const newSpan=document.createElement('span');
      newSpan.className='new-val';
      newSpan.textContent=val;
      valEl.appendChild(newSpan);
    } else if(isChanged && ch){
      if(field==='rates'){
        const oldRates=(()=>{try{return JSON.parse(ch.from)}catch(e){return {}}})();
        const newRates=(()=>{try{return JSON.parse(ch.to)}catch(e){return {}}})();
        const arrow=document.createElement('span'); arrow.className='change-arrow'; arrow.textContent='→';
        valEl.append(
          multilineSpan('prev-val',formatRatesSummary(t.pricing,oldRates)),
          arrow,
          multilineSpan('new-val',formatRatesSummary(t.pricing,newRates)),
        );
      } else {
        const prevSpan=document.createElement('span'); prevSpan.className='prev-val'; prevSpan.textContent=ch.from||'—';
        const arrow=document.createElement('span'); arrow.className='change-arrow'; arrow.textContent='→';
        const newSpan=document.createElement('span'); newSpan.className='new-val'; newSpan.textContent=ch.to||'—';
        valEl.append(prevSpan,arrow,newSpan);
      }
    } else {
      if(field==='rates'){
        valEl.appendChild(multilineSpan('rates-detail',val));
      } else {
        valEl.appendChild(document.createTextNode(val));
      }
    }
    return rowEl;
  }

  const leVal=t.loadEntitlement==='lt70'?'< 70 kVA':t.loadEntitlement==='gt70'?'> 70 kVA':t.loadEntitlement==='any'?'Any':'—';
  const ts=latest?.ts?new Date(latest.ts).toLocaleString():'unknown';

  const bodyEl=document.createElement('div');

  const banner=document.createElement('div');
  banner.className='submission-banner';
  const bannerLabel=document.createElement('strong');
  bannerLabel.textContent=isNew?'New tariff submission':'Edited tariff';
  const supplierStrong=document.createElement('strong');
  supplierStrong.textContent=t.supplier;
  banner.append(bannerLabel,' ·  Submitted by ',supplierStrong,' ·  '+ts);
  bodyEl.appendChild(banner);

  const sectionLine=document.createElement('div');
  sectionLine.className='review-section';
  sectionLine.textContent=changes.length&&!isNew?`${changes.length} field(s) changed — highlighted below`
    :isNew?'All fields — new submission'
    :'No field changes recorded';
  bodyEl.appendChild(sectionLine);

  const detailsHeader=document.createElement('div');
  detailsHeader.className='review-section';
  detailsHeader.style.marginTop=changes.length?'12px':'4px';
  detailsHeader.textContent='Tariff details';
  bodyEl.appendChild(detailsHeader);

  bodyEl.append(
    row('name','Name',t.name||'—'),
    row('contract','Contract type',t.contract||'—'),
    row('voltage','Voltage',t.voltage||'—'),
    row('pricing','Pricing type',t.pricing||'—'),
    row('standing','Standing charge','€'+(t.standing||0).toFixed(2)+'/month'),
  );
  if((t.mdm||0)>0) bodyEl.appendChild(row('mdm','MDM (Meter Data Management)','€'+(t.mdm||0).toFixed(2)+'/invoice, '+(t.mdmInvoiceMonths===1?'monthly':'bimonthly')+(t.mdmSource==='global'?' (regulated rate)':'')));
  bodyEl.append(
    row('rates','Rates',formatRatesSummary(t.pricing,t.rates)),
    row('fpaSource','FPA source',t.fpaSource==='global'?'Global (regulated)'
        :t.fpaSource==='custom'?'Custom — €'+(t.fpaCustom||0).toFixed(4)+'/kWh':'None'),
    row('durationMonths','Duration',t.durationMonths?t.durationMonths+' months (fixed term)':'Indefinite'),
    row('loadEntitlement','Load entitlement',leVal||'—'),
    row('profileId','Profile',prof?prof.name+' ('+prof.id+')':'None assigned'),
    row('vulnerable','Vulnerable tariff',t.vulnerable?'Yes — eligible customers only':'No'),
    row('discounts','Discounts',(t.discounts||[]).length
      ?(t.discounts||[]).map(d=>(d.type==='standing'?'Standing':'Energy')+' −'+d.percentage+'%'
          +(d.durationMonths?' for '+d.durationMonths+' months':' (permanent)')
          +(d.conditions?' — '+d.conditions:'')).join('; ')
      :'None'),
  );

  const docsHeader=document.createElement('div');
  docsHeader.className='review-section';
  docsHeader.style.marginTop='16px';
  docsHeader.textContent='Supporting documents';
  bodyEl.appendChild(docsHeader);

  const docsListWrap=document.createElement('div');
  docsListWrap.id='review-docs-list';
  docsListWrap.style.cssText='padding:0 0 8px';
  const loadingSpan=document.createElement('span');
  loadingSpan.style.cssText='font-size:13px;color:var(--text3)';
  loadingSpan.textContent='Loading…';
  docsListWrap.appendChild(loadingSpan);
  bodyEl.appendChild(docsListWrap);

  document.getElementById('review-title').textContent='Review: '+t.name;
  document.getElementById('review-body').replaceChildren(bodyEl);
  document.getElementById('review-approve-btn').onclick=()=>setTariffStatus(id,'approved');
  document.getElementById('review-reject-btn').onclick=()=>showRejectPanel(id);
  cancelReject();
  document.getElementById('review-overlay').style.display='flex';
  loadReviewDocs(id);
}
function closeReview(){
  cancelReject();
  document.getElementById('review-overlay').style.display='none';
}

let _docsCache = {};

async function loadReviewDocs(tariffId){
  const el=document.getElementById('review-docs-list');
  if(!el) return;
  try{
    const resp=await fetch(_adminApiBase+'/api/admin/tariffs/'+encodeURIComponent(tariffId)+'/documents',{headers:authHeaders()});
    const docs=await resp.json();
    if(!docs.length){
      el.innerHTML='<span style="font-size:13px;color:var(--text3)">No documents uploaded.</span>';
      return;
    }
    docs.forEach(d=>{ _docsCache[d.id]=d.original_name; });
    el.innerHTML=docs.map(d=>{
      const ts=new Date(d.uploaded_at).toLocaleString();
      return `<div style="display:flex;align-items:center;justify-content:space-between;padding:6px 0;border-bottom:1px solid var(--border)">
        <div>
          <div style="font-size:13px;font-weight:500">${esc(d.original_name)}</div>
          <div style="font-size:11px;color:var(--text3)">${ts} &nbsp;·&nbsp; ${esc(d.uploaded_by)}</div>
        </div>
        <a href="#" data-action="downloadDoc" data-arg="${d.id}" style="font-size:12px;color:var(--accent);font-weight:500;text-decoration:none">↓ Download</a>
      </div>`;
    }).join('');
  }catch(e){
    if(el) el.innerHTML='<span style="font-size:13px;color:var(--red)">Failed to load documents.</span>';
  }
}

// ── Admin docs-only modal (no approve/reject) ─────────────────────────────────
async function openAdminDocs(tariffId){
  const tariffName=tariffs.find(t=>t.id===tariffId)?.name||'';
  document.getElementById('adocs-title').textContent=T('ADOCS_TITLE_PREFIX')+tariffName;
  document.getElementById('adocs-list').innerHTML='<span style="font-size:13px;color:var(--text3)">Loading…</span>';
  document.getElementById('adocs-overlay').style.display='flex';
  try{
    const resp=await fetch(_adminApiBase+'/api/admin/tariffs/'+encodeURIComponent(tariffId)+'/documents',{headers:authHeaders()});
    const docs=await resp.json();
    const el=document.getElementById('adocs-list');
    if(!docs.length){el.innerHTML='<span style="font-size:13px;color:var(--text3)">No documents uploaded yet.</span>';return;}
    docs.forEach(d=>{ _docsCache[d.id]=d.original_name; });
    el.innerHTML=docs.map(d=>{
      const ts=new Date(d.uploaded_at).toLocaleString();
      return `<div style="display:flex;align-items:center;justify-content:space-between;padding:8px 0;border-bottom:1px solid var(--border)">
        <div>
          <div style="font-size:13px;font-weight:500">${esc(d.original_name)}</div>
          <div style="font-size:11px;color:var(--text3)">${ts} &nbsp;·&nbsp; ${esc(d.uploaded_by)}</div>
        </div>
        <a href="#" data-action="downloadDoc" data-arg="${d.id}" style="font-size:12px;color:var(--accent);font-weight:500;text-decoration:none">↓ Download</a>
      </div>`;
    }).join('');
  }catch(e){document.getElementById('adocs-list').innerHTML='<span style="font-size:13px;color:var(--red)">Failed to load.</span>';}
}
function closeAdminDocs(){document.getElementById('adocs-overlay').style.display='none';}

async function downloadDoc(docId){
  const filename=_docsCache[docId]||'document.pdf';
  try{
    const resp=await fetch(_adminApiBase+'/api/admin/documents/'+docId+'/download',{headers:authHeaders()});
    if(!resp.ok){alert('Download failed — please try again.');return;}
    const blob=await resp.blob();
    const url=URL.createObjectURL(blob);
    const a=document.createElement('a');
    a.href=url; a.download=filename;
    document.body.appendChild(a); a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }catch(e){alert('Download error: '+e.message);}
}
let tariffGroupBy='none';

function setTariffGroup(g){
  tariffGroupBy=g;
  ['none','supplier','pricing','contract'].forEach(k=>{
    const el=document.getElementById('grp-'+k);
    if(el) el.classList.toggle('active',k===g);
  });
  renderTariffs();
}

/* ── Changelog helpers ── */
function fmtDiscounts(discounts){
  if(!discounts||!discounts.length) return 'none';
  return discounts.map(d=>
    d.type+':'+d.percentage+'%'+(d.durationMonths?'('+d.durationMonths+'mo)':'(permanent)')+(d.conditions?' "'+d.conditions+'"':'')
  ).join(', ');
}
function fmtTariffRates(t){
  if(t.pricing==='Fixed') return 'rate:€'+t.rates.rate;
  if(t.pricing==='ToU') return 'hiPeak:€'+t.rates.hiPeakRate+' hiOff:€'+t.rates.hiOffRate+' loPeak:€'+t.rates.loPeakRate+' loOff:€'+t.rates.loOffRate;
  if(t.pricing==='Variable'){
    const tiersStr=(t.rates.tiers||[]).map(tier=>
      (tier.upTo!=null?'≤'+tier.upTo:'∞')+':€'+tier.rate+(tier.fixedCharge?'+€'+tier.fixedCharge+'fix':'')
    ).join(',');
    return 'reset:'+t.rates.resetMonths+'mo ['+tiersStr+']';
  }
  return 'mult:×'+t.rates.mult+' adder:€'+t.rates.adder+' floor:'+(t.rates.damFloor?'€'+t.rates.damFloor:'none');
}
function tariffToChangeFields(t){
  return [
    {field:'name',       to:t.name},
    {field:'supplier',   to:t.supplier},
    {field:'contract',   to:t.contract},
    {field:'voltage',    to:t.voltage},
    {field:'pricing',    to:t.pricing},
    {field:'standing',   to:'€'+t.standing.toFixed(2)+'/mo'},
    {field:'fpaSource',  to:t.fpaSource},
    {field:'duration',   to:t.durationMonths?t.durationMonths+'mo':'indefinite'},
    {field:'loadEntitlement', to:t.loadEntitlement||'n/a'},
    {field:'vulnerable', to:t.vulnerable?'yes':'no'},
    {field:'rates',      to:fmtTariffRates(t)},
    {field:'discounts',  to:fmtDiscounts(t.discounts)}
  ];
}
function diffTariff(old,neo){
  const changes=[];
  const track=(field,from,to)=>{
    const fs=String(from??''),ts=String(to??'');
    if(fs!==ts) changes.push({field,from:fs,to:ts});
  };
  track('name',old.name,neo.name);
  track('supplier',old.supplier,neo.supplier);
  track('contract',old.contract,neo.contract);
  track('voltage',old.voltage,neo.voltage);
  track('pricing',old.pricing,neo.pricing);
  track('standing','€'+(old.standing||0).toFixed(2)+'/mo','€'+(neo.standing||0).toFixed(2)+'/mo');
  track('fpaSource',old.fpaSource,neo.fpaSource);
  if(neo.fpaSource==='custom'||old.fpaSource==='custom') track('fpaCustom',old.fpaCustom,neo.fpaCustom);
  track('duration',old.durationMonths?old.durationMonths+'mo':'indefinite',neo.durationMonths?neo.durationMonths+'mo':'indefinite');
  track('loadEntitlement',old.loadEntitlement||'n/a',neo.loadEntitlement||'n/a');
  track('vulnerable',old.vulnerable?'yes':'no',neo.vulnerable?'yes':'no');
  track('rates',fmtTariffRates(old),fmtTariffRates(neo));
  track('discounts',fmtDiscounts(old.discounts),fmtDiscounts(neo.discounts));
  return changes;
}
function addChangelogEntry(entry){
  changelog.unshift({id:uid(),...entry}); // newest first
  if(changelog.length>500) changelog.length=500; // cap at 500 entries
}
function fmtLocalTs(isoStr){
  try{
    const d=new Date(isoStr);
    return d.toLocaleDateString('en-GB',{day:'2-digit',month:'short',year:'numeric'})+
      ' '+d.toLocaleTimeString('en-GB',{hour:'2-digit',minute:'2-digit',second:'2-digit'});
  } catch(e){return isoStr||'—';}
}
const CL_FIELD_LABELS={
  name:'Name', contract:'Contract', voltage:'Voltage', pricing:'Pricing type',
  standing:'Standing charge', fpaSource:'FPA source', fpaCustom:'FPA custom rate',
  durationMonths:'Duration (months)', loadEntitlement:'Load entitlement',
  vulnerable:'Vulnerable-consumer flag', profileId:'Load profile',
  rates:'Rates', discounts:'Discounts', regulated:'Regulated supplier'
};
function clFieldLabel(field){ return CL_FIELD_LABELS[field]||field; }
function renderChangelogRow(entry){
  const actionCls='cl-action-'+entry.action;
  const actionLabel=entry.action.charAt(0).toUpperCase()+entry.action.slice(1);
  let changesHtml='<div class="cl-changes">';
  if(entry.action==='deleted'){
    changesHtml+='<span class="cl-change">Tariff removed</span>';
  } else if(entry.changes&&entry.changes.length){
    entry.changes.forEach(function(c){
      const label=clFieldLabel(c.field);
      if(c.from===undefined||c.from===null||c.from===''){
        changesHtml+='<span class="cl-change"><span class="field-name">'+esc(label)+':</span> <span class="to-val">'+esc(c.to)+'</span></span>';
      } else {
        changesHtml+='<span class="cl-change"><span class="field-name">'+esc(label)+':</span> <span class="from-val">'+esc(c.from)+'</span> → <span class="to-val">'+esc(c.to)+'</span></span>';
      }
    });
  } else {
    changesHtml+='<span class="cl-change" style="color:var(--text3)">No tracked changes</span>';
  }
  changesHtml+='</div>';
  let actorHtml='<span style="color:var(--text3)">—</span>';
  if(entry.actorRole==='admin'){
    actorHtml='<span style="font-weight:600;color:var(--accent)">'+T('CL_ACTOR_ADMIN')+'</span>';
  } else if(entry.actorRole==='supplier'){
    actorHtml='<span>'+T('CL_ACTOR_SUPPLIER')+(entry.actorEmail?' <span style="color:var(--text3)">('+esc(entry.actorEmail)+')</span>':'')+'</span>';
  }
  return '<tr>'
    +'<td style="white-space:nowrap;color:var(--text3)">'+fmtLocalTs(entry.ts)+'</td>'
    +'<td style="color:var(--text);font-weight:500">'+esc(entry.tariffName)+'</td>'
    +'<td>'+esc(entry.supplier)+'</td>'
    +'<td>'+actorHtml+'</td>'
    +'<td class="'+actionCls+'">'+actionLabel+'</td>'
    +'<td>'+changesHtml+'</td>'
    +'</tr>';
}
function renderChangelog(){
  const fAction=document.getElementById('cl-filter-action')?.value||'';
  const fSup=document.getElementById('cl-filter-supplier')?.value||'';
  // Populate supplier filter
  const supSel=document.getElementById('cl-filter-supplier');
  if(supSel){
    const cur=supSel.value;
    const uniqSups=[...new Set(changelog.map(e=>e.supplier))].sort();
    supSel.innerHTML='<option value="">'+T('OPT_ALL_SUPPLIERS')+'</option>'+uniqSups.map(s=>'<option value="'+esc(s)+'"'+(s===cur?' selected':'')+'>'+esc(s)+'</option>').join('');
  }
  const filtered=changelog.filter(function(e){
    return (!fAction||e.action===fAction)&&(!fSup||e.supplier===fSup);
  });
  const tbody=document.getElementById('cl-tbody');
  const empty=document.getElementById('cl-empty');
  const table=document.getElementById('cl-table');
  const countEl=document.getElementById('cl-count');
  if(!filtered.length){
    if(tbody) tbody.innerHTML='';
    if(table) table.style.display='none';
    if(empty) empty.style.display='';
    if(countEl) countEl.textContent='';
  } else {
    if(table) table.style.display='';
    if(empty) empty.style.display='none';
    if(tbody) tbody.innerHTML=filtered.map(renderChangelogRow).join('');
    if(countEl) countEl.textContent='('+filtered.length+' of '+changelog.length+' entries)';
  }
}

/* ── Tariff reports (Article 121(ζ)) ── */
const RP_OVERDUE_DAYS=5;   // reports left "open" past this many days are flagged for follow-up
function renderReportRow(r){
  const statusCls='rp-status-'+r.status;
  const statusLabel=T('OPT_STATUS_'+r.status.toUpperCase());
  const categoryLabel=T('RP_CAT_'+(r.category||'other').toUpperCase());
  let noteHtml=r.note?esc(r.note):'<span style="color:var(--text3)">—</span>';
  if(r.reporterEmail) noteHtml+=`<div style="font-size:10.5px;color:var(--text3);margin-top:3px">${esc(T('RP_LBL_REPORTER'))}: ${esc(r.reporterEmail)}</div>`;
  if(r.adminNote) noteHtml+=`<div style="font-size:10.5px;color:var(--text3);margin-top:3px">${esc(T('RP_LBL_RESOLUTION'))}: ${esc(r.adminNote)}</div>`;
  const ageDays=(Date.now()-new Date(r.createdAt).getTime())/86400000;
  const overdueBadge=(r.status==='open'&&ageDays>RP_OVERDUE_DAYS)
    ?`<span style="display:block;color:#b45309;font-size:10.5px;font-weight:600;margin-top:2px">${esc(T('RP_OVERDUE'))}</span>`
    :'';
  const actions=r.status==='open'
    ?`<button class="btn-sm" data-action="setReportStatus" data-arg="${esc(r.id)}" data-arg2="reviewed">${T('BTN_MARK_REVIEWED')}</button>
      <button class="btn-sm" data-action="setReportStatus" data-arg="${esc(r.id)}" data-arg2="resolved">${T('BTN_MARK_RESOLVED')}</button>
      <button class="btn-sm" data-action="setReportStatus" data-arg="${esc(r.id)}" data-arg2="dismissed">${T('BTN_DISMISS')}</button>`
    :`<button class="btn-sm" data-action="setReportStatus" data-arg="${esc(r.id)}" data-arg2="open">${T('BTN_REOPEN')}</button>`;
  const tariffCell=r.tariffName?esc(r.tariffName):`<em style="color:var(--text3);font-style:italic">${esc(T('RP_GENERAL_ISSUE'))}</em>`;
  const supplierCell=r.supplier?esc(r.supplier):'<span style="color:var(--text3)">—</span>';
  return '<tr>'
    +'<td style="white-space:nowrap;color:var(--text3)">'+fmtLocalTs(r.createdAt)+overdueBadge+'</td>'
    +'<td style="color:var(--text);font-weight:500">'+tariffCell+'</td>'
    +'<td>'+supplierCell+'</td>'
    +'<td>'+esc(categoryLabel)+'</td>'
    +'<td>'+noteHtml+'</td>'
    +'<td class="'+statusCls+'">'+esc(statusLabel)+'</td>'
    +'<td>'+actions+'</td>'
    +'</tr>';
}
function renderReports(){
  const fStatus=document.getElementById('rp-filter-status')?.value||'';
  const filtered=reports.filter(r=>!fStatus||r.status===fStatus);
  const tbody=document.getElementById('rp-tbody');
  const empty=document.getElementById('rp-empty');
  const table=document.getElementById('rp-table');
  const countEl=document.getElementById('rp-count');
  if(!filtered.length){
    if(tbody) tbody.innerHTML='';
    if(table) table.style.display='none';
    if(empty) empty.style.display='';
    if(countEl) countEl.textContent='';
  } else {
    if(table) table.style.display='';
    if(empty) empty.style.display='none';
    if(tbody) tbody.innerHTML=filtered.map(renderReportRow).join('');
    if(countEl) countEl.textContent='('+filtered.length+' of '+reports.length+' entries)';
  }
}
async function setReportStatus(id,status){
  let admin_note;
  if(status==='resolved'||status==='dismissed'){
    const entered=prompt(T('RP_ADMIN_NOTE_PROMPT'),'');
    if(entered===null) return; // user cancelled — leave the report untouched
    if(entered.trim()) admin_note=entered.trim();
  }
  try{
    const body={status};
    if(admin_note!==undefined) body.admin_note=admin_note;
    const resp=await fetch(_adminApiBase+'/api/admin/reports/'+id,{method:'PATCH',headers:authHeaders(),body:JSON.stringify(body)});
    if(resp.status===401){showLogin('Session expired.');return;}
    if(!resp.ok){alert('Failed to update report.');return;}
    const updated=await resp.json();
    const i=reports.findIndex(r=>r.id===id);
    if(i>=0) reports[i]=updated;
    renderReports();
    updateReportsBubble();
  }catch(e){ alert('Network error.'); }
}
function updateReportsBubble(){
  const n=reports.filter(r=>r.status==='open').length;
  const b=document.getElementById('nav-reports-bubble');
  if(b){ b.style.display=n?'':'none'; b.textContent=n; }
}
// Quotes a CSV cell (RFC4180 — doubles embedded quotes) and, if the value starts with
// a character a spreadsheet app (Excel/Sheets/LibreOffice) would interpret as the start
// of a formula (=, +, -, @, tab, CR), prefixes a leading ' so it's forced to plain text.
// Tariff/supplier names and changelog diff values are attacker-controllable (via the
// supplier portal), so this matters for exports containing them.
function csvCell(v){
  let s=String(v==null?'':v);
  if(/^[=+\-@\t\r]/.test(s)) s="'"+s;
  return '"'+s.replace(/"/g,'""')+'"';
}
function exportChangelog(){
  if(!changelog.length){alert('No changelog entries to export.');return;}
  let csv='Timestamp,Tariff,Supplier,Made by,Action,Field,From,To\n';
  changelog.forEach(function(e){
    const actor=e.actorRole==='admin'?'CERA Admin':(e.actorRole==='supplier'?'Supplier'+(e.actorEmail?' ('+e.actorEmail+')':''):'');
    if(!e.changes||!e.changes.length){
      csv+=[fmtLocalTs(e.ts),e.tariffName,e.supplier,actor,e.action,'','',''].map(csvCell).join(',')+'\n';
    } else {
      e.changes.forEach(function(c){
        csv+=[fmtLocalTs(e.ts),e.tariffName,e.supplier,actor,e.action,c.field,c.from||'',c.to].map(csvCell).join(',')+'\n';
      });
    }
  });
  const blob=new Blob([csv],{type:'text/csv;charset=utf-8;'});
  const a=document.createElement('a');
  a.href=URL.createObjectURL(blob);
  a.download='tariff_changelog_'+new Date().toISOString().slice(0,10)+'.csv';
  document.body.appendChild(a);a.click();document.body.removeChild(a);
}
function renderTariffMiniLog(tariffId){
  const entries=changelog.filter(function(e){return e.tariffId===tariffId;}).slice(0,5);
  if(!entries.length) return '';
  let html='<details class="tariff-log"><summary>🕓 History ('+entries.length+' entries)</summary><div class="tariff-log-entries">';
  entries.forEach(function(e){
    const actionCls='tl-action-'+e.action;
    const actionLabel=e.action.charAt(0).toUpperCase()+e.action.slice(1);
    let detail='';
    if(e.action==='updated'&&e.changes&&e.changes.length){
      detail=' — '+e.changes.map(function(c){return c.field;}).join(', ');
    }
    html+='<div class="tariff-log-entry"><span class="tl-ts">'+fmtLocalTs(e.ts)+'</span> <span class="'+actionCls+'">'+actionLabel+'</span>'+detail+'</div>';
  });
  html+='</div></details>';
  return html;
}

function renderTariffItem(t){
  const prof=profiles.find(p=>p.id===t.profileId);
  const supOK=suppliers.some(s=>supName(s)===t.supplier);
  const tsLine=t.updatedAt
    ? '<div style="font-size:10px;font-family:var(--mono);color:var(--text3);margin-top:4px">'
      +(t.createdAt&&t.createdAt!==t.updatedAt?'Created: '+fmtLocalTs(t.createdAt)+' · ':'')
      +'Updated: '+fmtLocalTs(t.updatedAt)+'</div>'
    : '';
  const miniLog=renderTariffMiniLog(t.id);
  const status=t.status||'approved';
  const statusLabel={approved:T('STATUS_LIVE'),pending:T('STATUS_PENDING'),rejected:T('STATUS_REJECTED'),draft:T('STATUS_DRAFT'),suspended:T('STATUS_SUSPENDED'),archived:T('STATUS_ARCHIVED')};
  const statusBadge='<span class="badge badge-status-'+status+'">'+(statusLabel[status]||status)+'</span>';
  const isPending=status==='pending';
  const isSuspended=status==='suspended';
  const isArchived=status==='archived';
  const rowExtra=isPending?'border-left:3px solid var(--yellow);padding-left:10px;background:rgba(188,108,37,.025)'
    :isSuspended?'border-left:3px solid #4338ca;padding-left:10px;background:rgba(99,102,241,.025)'
    :isArchived?'border-left:3px dashed var(--border);padding-left:10px;opacity:.7':'';
  const reviewBtn=isPending
    ?'<button class="btn btn-sm btn-review" data-action="openReview" data-arg="'+esc(t.id)+'">'+T('BTN_REVIEW')+'</button>'
    :'';
  const suspendBtn=status==='approved'
    ?'<button class="btn btn-sm btn-suspend" data-action="suspendTariff" data-arg="'+esc(t.id)+'" title="Temporarily take offline">'+T('BTN_SUSPEND')+'</button>'
    :(isSuspended||isArchived)
    ?'<button class="btn btn-sm btn-approve" data-action="setTariffStatus" data-arg="'+esc(t.id)+'" data-arg2="approved" title="Put back online">'+T('BTN_RESTORE')+'</button>'
    :'';
  return '<div class="item-row" style="flex-direction:column;align-items:stretch;gap:0;'+rowExtra+'">'
    +'<div style="display:flex;align-items:flex-start;gap:10px">'
    +'<div class="item-row-info">'
    +'<div class="item-name">'+esc(t.name)+(!supOK?' <span class="badge badge-no-profile">⚠ supplier missing</span>':'')+'</div>'
    +'<div class="item-meta">'
    +'<span class="badge badge-type">'+esc(t.supplier)+'</span>'
    +'<span class="badge badge-voltage">'+esc(t.voltage)+'</span>'
    +'<span class="badge badge-pricing-'+esc(t.pricing)+'">'+esc(t.pricing)+'</span>'
    +'<span class="badge">'+esc(t.contract)+'</span>'
    +(prof?'<span class="badge badge-profile">📊 '+esc(prof.name)+'</span>':'<span class="badge badge-no-profile">⚠ No profile</span>')
    +(t.fpaSource==='global'?'<span class="badge" style="background:rgba(47,111,78,.1);color:#1f4d36">FPA:global</span>'
      :t.fpaSource==='custom'?'<span class="badge" style="background:rgba(188,108,37,.1);color:#7a4a18">FPA:€'+(t.fpaCustom||0).toFixed(4)+'</span>'
      :'<span class="badge" style="background:var(--bg3);color:var(--text3)">FPA:none</span>')
    +(t.durationMonths?'<span class="badge" style="background:rgba(166,64,58,.1);color:#7a3530">⏱ '+t.durationMonths+'mo min</span>'
      :'<span class="badge" style="background:var(--bg3);color:var(--text3)">Indefinite</span>')
    +(t.loadEntitlement&&t.loadEntitlement!=='any'
      ?'<span class="badge" style="background:rgba(47,111,78,.1);color:#1f4d36">'+(t.loadEntitlement==='lt70'?'<70kVA':'>70kVA')+'</span>'
      :t.loadEntitlement==='any'?'<span class="badge" style="background:var(--bg3);color:var(--text3)">Any kVA</span>':'')
    +(t.vulnerable?'<span class="badge" style="background:rgba(236,72,153,.12);color:#ec4899">🛡 Vulnerable</span>':'')
    +statusBadge
    +'</div>'
    +tsLine
    +'</div>'
    +'<div class="item-row-actions" style="flex-shrink:0;display:flex;gap:4px;align-items:center">'
    +reviewBtn
    +(isPending?'<span style="width:4px"></span>':'')
    +suspendBtn
+(docTariffIds.has(t.id)?'<button class="btn btn-sm" data-action="openAdminDocs" data-arg="'+esc(t.id)+'" title="View documents">📎</button>':'')
    +'<button class="btn btn-sm" data-action="openViewer" data-arg="'+esc(t.id)+'">'+T('BTN_VIEW')+'</button>'
    +'</div>'
    +'</div>'
    +miniLog
    +'</div>';
}


function renderTariffs(){
  const el=document.getElementById('tariff-list');
  const countEl=document.getElementById('tariff-count');
  if(!tariffs.length){
    el.innerHTML='<div class="empty-state">'+T('EMPTY_TARIFFS')+'</div>';
    if(countEl) countEl.textContent='';
    return;
  }

  // Update supplier dropdown options
  const supSel=document.getElementById('tf-sup');
  if(supSel){
    const cur=supSel.value;
    supSel.innerHTML='<option value="">'+T('OPT_ALL_SUPPLIERS')+'</option>'+
      [...new Set(tariffs.map(t=>t.supplier))].sort()
        .map(s=>`<option value="${esc(s)}"${cur===s?' selected':''}>${esc(s)}</option>`).join('');
  }

  // Apply filters
  const fSup=document.getElementById('tf-sup')?.value||'';
  const fPricing=document.getElementById('tf-pricing')?.value||'';
  const fContract=document.getElementById('tf-contract')?.value||'';
  const filtered=tariffs.filter(t=>
    (!fSup||t.supplier===fSup)&&
    (!fPricing||t.pricing===fPricing)&&
    (!fContract||t.contract===fContract)
  );

  if(countEl) countEl.textContent=`(${filtered.length} of ${tariffs.length})`;
  const pendingCount=tariffs.filter(t=>t.status==='pending').length;
  const bubble=document.getElementById('nav-pending-bubble');
  if(bubble){bubble.textContent=pendingCount;bubble.style.display=pendingCount?'':'none';}

  if(!filtered.length){
    el.innerHTML='<div class="empty-state">'+T('EMPTY_TARIFFS_FILTER')+'</div>';
    return;
  }

  let html='<div class="list-wrap">';

  if(tariffGroupBy==='none'){
    html+=filtered.map(t=>renderTariffItem(t)).join('');
  } else {
    const keyFn=tariffGroupBy==='supplier'?t=>t.supplier
      :tariffGroupBy==='pricing'?t=>t.pricing
      :t=>t.contract;
    const groups=[...new Set(filtered.map(keyFn))].sort();
    groups.forEach(g=>{
      const gt=filtered.filter(t=>keyFn(t)===g);
      html+=`<div style="margin-bottom:18px">
        <div style="font-size:10px;font-family:var(--mono);color:var(--text3);text-transform:uppercase;letter-spacing:.1em;padding:5px 2px 6px;border-bottom:1px solid var(--border);margin-bottom:6px">
          ${esc(g)} <span style="font-weight:400">(${gt.length})</span>
        </div>
        ${gt.map(t=>renderTariffItem(t)).join('')}
      </div>`;
    });
  }

  html+='</div>';
  el.innerHTML=html;
}

/* ── DAM parser ── */
// damDailyData[monthIdx] = array of day objects {dateStr, dow, slots:[48 prices]}
let damDailyData=Array.from({length:12},()=>[]);
let damViewerState={month:0,week:0};
let damWeekChart=null;

function damLoadFiles(files){
  if(!files||!files.length) return;
  const fileList=Array.from(files);
  const readers=fileList.map(f=>new Promise((res,rej)=>{
    const r=new FileReader();
    r.onload=e=>res(e.target.result);
    r.onerror=rej;
    r.readAsText(f);
  }));
  Promise.all(readers).then(texts=>{
    const existing=document.getElementById('dam-raw').value.trim();
    const combined=[existing,...texts].filter(Boolean).join('\n');
    document.getElementById('dam-raw').value=combined;
    document.getElementById('dam-file-input').value='';
    const names=fileList.map(f=>f.name).join(', ');
    document.getElementById('dam-dz-label').innerHTML=`<span style="font-size:20px">✅</span><div style="margin-top:6px;font-weight:600">${names}</div><div style="margin-top:2px;font-size:11px;opacity:.7">Drop more files to append</div>`;
    parseDAM();
  });
}

function parseDAM(){
  const raw=document.getElementById('dam-raw').value.trim();
  const unit=document.getElementById('dam-unit').value;
  const toKwh=unit==='mwh'?v=>v/1000:v=>v;
  const status=document.getElementById('dam-status');
  if(!raw){showStatus(status,'err','No data.');return;}

  const lines=raw.split(/\r?\n/).filter(l=>l.trim());
  const slotBuckets=Array.from({length:12},()=>Array.from({length:48},()=>[]));
  const monthBuckets=Array.from({length:12},()=>[]);
  // Daily data: dayMap[dateStr] = {month, dow, slots:[48]}
  const dayMap=new Map();
  let parsed=0,skipped=0;

  lines.forEach(line=>{
    const parts=line.split(/[,;]/);
    if(parts.length<2){skipped++;return;}
    const dtStr=parts[0].trim(),priceStr=parts[1].trim();
    if(isNaN(parseFloat(priceStr))){skipped++;return;}
    const price=toKwh(parseFloat(priceStr));
    const m=dtStr.match(/^(\d{4})-(\d{2})-(\d{2})\s+(\d{2}):(\d{2})/);
    if(!m){skipped++;return;}
    const dateStr=`${m[1]}-${m[2]}-${m[3]}`;
    const month=parseInt(m[2],10)-1;
    const hour=parseInt(m[4],10);
    const minute=parseInt(m[5],10);
    if(month<0||month>11){skipped++;return;}
    const slot=hour*2+(minute>=30?1:0);
    slotBuckets[month][slot].push(price);
    monthBuckets[month].push(price);
    if(!dayMap.has(dateStr)){
      const d=new Date(dateStr);
      dayMap.set(dateStr,{dateStr,month,dow:d.getDay(),slots:new Array(48).fill(null)});
    }
    dayMap.get(dateStr).slots[slot]=price;
    parsed++;
  });

  damMonthly=monthBuckets.map(b=>b.length?b.reduce((a,x)=>a+x,0)/b.length:null);
  damBySlot=slotBuckets.map(month=>month.map(s=>s.length?s.reduce((a,x)=>a+x,0)/s.length:null));
  damRowCount=parsed;
  damPendingSource='upload';
  _damHideReport();

  // Build sorted daily arrays per month
  damDailyData=Array.from({length:12},()=>[]);
  dayMap.forEach(day=>damDailyData[day.month].push(day));
  damDailyData.forEach(arr=>arr.sort((a,b)=>a.dateStr.localeCompare(b.dateStr)));

  showStatus(status,'ok',`Parsed ${parsed} rows · ${monthBuckets.filter(b=>b.length).length}/12 months · ${dayMap.size} days.`);
  renderMonthGrid();
  renderDamCoverage();
  renderDamViewer();
}
function renderMonthGrid(){
  const g=document.getElementById('month-grid');g.innerHTML='';
  damMonthly.forEach((v,i)=>{
    const d=document.createElement('div');
    d.className='month-cell'+(v!==null?' has-data':'');
    d.innerHTML=`<div class="month-cell-lbl">${MONTHS_SHORT[i]}</div><div class="month-cell-val">${v!==null?v.toFixed(5):'—'}</div>`;
    g.appendChild(d);
  });
  document.getElementById('dam-preview-card').style.display='';
}

function renderDamCoverage(){
  const card=document.getElementById('dam-coverage-card');
  if(!damDailyData.some(m=>m.length>0)){card.style.display='none';return;}
  card.style.display='';
  document.getElementById('dam-cal-month-view').style.display='';
  document.getElementById('dam-cal-day-view').style.display='none';

  // Build a sorted list of {year, mi, days} — one entry per unique year+month in the data
  const entries=[];
  damDailyData.forEach((days,mi)=>{
    if(!days||!days.length) return;
    const byYear={};
    days.forEach(d=>{
      const yr=parseInt(d.dateStr.slice(0,4));
      if(!byYear[yr]) byYear[yr]=[];
      byYear[yr].push(d);
    });
    Object.entries(byYear).forEach(([yr,yrDays])=>{
      entries.push({year:parseInt(yr),mi,days:yrDays});
    });
  });
  entries.sort((a,b)=>a.year!==b.year?a.year-b.year:a.mi-b.mi);

  document.getElementById('dam-cal-mon-grid').innerHTML=entries.map(e=>{
    const expDays=new Date(e.year,e.mi+1,0).getDate();
    const slotCounts=e.days.map(d=>Array.isArray(d.slots)?d.slots.filter(s=>s!==null).length:0);
    const maxSlots=Math.max(...slotCounts,1);
    const thresh=Math.max(1,Math.round(maxSlots*0.9));
    const fullDays=slotCounts.filter(n=>n>=thresh).length;
    const cls=(fullDays===expDays&&e.days.length===expDays?'dcal-full':'dcal-part')
      +(e.days.some(d=>!damSavedDates.has(d.dateStr))?' dcal-new':'');
    return `<div class="dcal-mon ${cls}" data-action="damOpenMonth" data-arg="${e.mi}" data-arg2="${e.year}" title="${MONTHS_SHORT[e.mi]} ${e.year}: ${e.days.length}/${expDays} days">
      <div style="font-size:11px;font-weight:600">${MONTHS_SHORT[e.mi]}</div>
      <div style="font-size:9px;margin-top:1px;opacity:.85">${e.year}</div>
    </div>`;
  }).join('');
}

function damOpenMonth(mi,year){
  const days=(damDailyData[mi]||[]).filter(d=>parseInt(d.dateStr.slice(0,4))===year);
  const expDays=new Date(year,mi+1,0).getDate();
  // Count non-null slots per day, guarding against non-array slots
  const slotCount={};
  let maxSlots=48;
  days.forEach(d=>{
    const n=Array.isArray(d.slots)?d.slots.filter(s=>s!==null).length:0;
    slotCount[d.dateStr]=n;
    if(n>maxSlots) maxSlots=n;
  });
  if(days.length) maxSlots=Math.max(...days.map(d=>Array.isArray(d.slots)?d.slots.filter(s=>s!==null).length:0));
  const thresh=Math.max(1,Math.round(maxSlots*0.9));
  const DOW=['Mo','Tu','We','Th','Fr','Sa','Su'];
  let html=DOW.map(d=>`<div class="dcal-hdr">${d}</div>`).join('');
  const firstDow=(new Date(year,mi,1).getDay()+6)%7;
  for(let i=0;i<firstDow;i++) html+=`<div class="dcal-cell dcal-empty"></div>`;
  for(let day=1;day<=expDays;day++){
    const ds=`${year}-${String(mi+1).padStart(2,'0')}-${String(day).padStart(2,'0')}`;
    const sc=slotCount[ds]||0;
    const cls=sc===0?'dcal-none':(sc>=thresh?'dcal-full':'dcal-part')+' has-data'+(damSavedDates.has(ds)?'':' dcal-new');
    const tip=sc===0?'No data':`${sc}/48 half-hours`;
    html+=sc===0?`<div class="dcal-cell ${cls}" title="${ds}: ${tip}">${day}</div>`
      :`<div class="dcal-cell ${cls}" data-action="damShowDay" data-arg="${ds}" title="${ds}: ${tip}">${day}</div>`;
  }
  document.getElementById('dam-cal-day-grid').innerHTML=html;
  document.getElementById('dam-cal-day-title').textContent=`${MONTHS_SHORT[mi]} ${year}`;
  document.getElementById('dam-cal-month-view').style.display='none';
  document.getElementById('dam-cal-day-view').style.display='';
  document.getElementById('dam-day-detail').style.display='none';
}

// One day's 48 half-hourly prices, to check them (e.g. a TSOC fetch) before saving.
function damShowDay(ds){
  const mi=parseInt(ds.slice(5,7),10)-1, year=parseInt(ds.slice(0,4),10);
  if(document.getElementById('dam-cal-day-view').style.display==='none'
     ||document.getElementById('dam-cal-day-title').textContent!==`${MONTHS_SHORT[mi]} ${year}`){
    damOpenMonth(mi,year);
  }
  const day=(damDailyData[mi]||[]).find(d=>d.dateStr===ds);
  const box=document.getElementById('dam-day-detail');
  document.querySelectorAll('#dam-cal-day-grid .dcal-sel').forEach(c=>c.classList.remove('dcal-sel'));
  const cell=document.querySelector(`#dam-cal-day-grid [data-arg="${ds}"]`);
  if(cell) cell.classList.add('dcal-sel');
  if(!day){box.style.display='none';return;}
  const vals=day.slots.filter(v=>v!==null).map(v=>v*1000);
  const head=document.createElement('div');
  head.className='dam-day-head';
  const title=document.createElement('strong');
  title.textContent=new Date(ds+'T12:00:00').toLocaleDateString(undefined,{weekday:'long',year:'numeric',month:'long',day:'numeric'});
  head.appendChild(title);
  const info=document.createElement('span');
  info.textContent=`${vals.length}/48 ${T('DAM_HALF_HOURS')} · €/MWh`+(vals.length
    ?` · min ${Math.min(...vals).toFixed(2)} · max ${Math.max(...vals).toFixed(2)} · avg ${(vals.reduce((a,x)=>a+x,0)/vals.length).toFixed(2)}`:'');
  head.appendChild(info);
  if(!damSavedDates.has(ds)){
    const nw=document.createElement('span');
    nw.className='dam-day-new';
    nw.textContent='● '+T('COV_NEW');
    head.appendChild(nw);
  }
  const grid=document.createElement('div');
  grid.className='dam-day-slots';
  day.slots.forEach((p,s)=>{
    const c=document.createElement('div');
    c.className='dam-day-slot'+(p===null?' missing':'');
    const t=document.createElement('span');
    t.textContent=`${String(Math.floor(s/2)).padStart(2,'0')}:${s%2?'30':'00'}`;
    const v=document.createElement('span');
    v.textContent=p===null?T('DAM_MISSING'):(p*1000).toFixed(2);
    c.append(t,v);
    grid.appendChild(c);
  });
  box.replaceChildren(head,grid);
  box.style.display='';
  box.scrollIntoView({behavior:'smooth',block:'nearest'});
}

function damBackToMonths(){
  document.getElementById('dam-cal-day-view').style.display='none';
  document.getElementById('dam-cal-month-view').style.display='';
}

function renderDamViewer(){
  const card=document.getElementById('dam-viewer-card');
  if(!damDailyData.some(m=>m.length>0)){card.style.display='none';return;}
  card.style.display='';

  // Build month tabs
  const tabsEl=document.getElementById('dam-month-tabs');
  tabsEl.innerHTML=MONTHS_SHORT.map((m,i)=>{
    const hasData=damDailyData[i]&&damDailyData[i].length>0;
    const cls='dam-month-tab'+(hasData?' has-data':' no-data')+(i===damViewerState.month&&hasData?' active':'');
    return `<button class="${cls}" ${hasData?`data-action="selectDamMonth" data-arg="${i}"`:'disabled'}>${m}</button>`;
  }).join('');

  // Find first month with data if current has none
  if(!damDailyData[damViewerState.month]||!damDailyData[damViewerState.month].length){
    const first=damDailyData.findIndex(m=>m.length>0);
    if(first>=0) damViewerState.month=first;
    else return;
  }
  renderDamWeek();
}

function selectDamMonth(mi){
  damViewerState.month=mi;
  damViewerState.week=0;
  // Update tab highlights
  document.querySelectorAll('.dam-month-tab').forEach((t,i)=>{
    t.classList.toggle('active',i===mi);
  });
  renderDamWeek();
}

function damNavWeek(dir){
  const days=damDailyData[damViewerState.month];
  const totalWeeks=Math.ceil(days.length/7);
  damViewerState.week=Math.max(0,Math.min(totalWeeks-1,damViewerState.week+dir));
  renderDamWeek();
}

function renderDamWeek(){
  const mi=damViewerState.month;
  const wi=damViewerState.week;
  const days=damDailyData[mi];
  if(!days||!days.length) return;

  const totalWeeks=Math.ceil(days.length/7);
  const weekDays=days.slice(wi*7,wi*7+7);

  // Nav labels
  const firstDay=weekDays[0].dateStr;
  const lastDay=weekDays[weekDays.length-1].dateStr;
  document.getElementById('dam-week-label').textContent=
    `${MONTHS_SHORT[mi]} · Week ${wi+1} of ${totalWeeks} · ${firstDay} → ${lastDay}`;
  document.getElementById('dam-prev-week').disabled=wi===0;
  document.getElementById('dam-next-week').disabled=wi>=totalWeeks-1;

  // Build chart data: 48 slots per day, labelled by time
  const labels=[];
  const prices=[];
  const bgColors=[];
  const holidays=getCyprusHolidays2026();

  weekDays.forEach(day=>{
    const isWeekend=day.dow===0||day.dow===6;
    const isHoliday=holidays.has(day.dateStr.replace(/-/g,''));
    const isNonWork=isWeekend||isHoliday;
    day.slots.forEach((price,s)=>{
      const endMin=(s+1)*30;
      const hh=Math.floor(endMin/60)%24;
      const mm=endMin%60;
      // Only label midnight of each day to avoid clutter
      labels.push(s===0?day.dateStr.slice(5):''); // MM-DD at midnight
      prices.push(price!==null?+(price*1000).toFixed(3):null); // show in €/MWh for readability
      bgColors.push(isNonWork?'rgba(139,92,246,.55)':'rgba(59,130,246,.55)');
    });
  });

  // Stats for week and month
  const weekPrices=prices.filter(v=>v!==null);
  const monthPrices=days.flatMap(d=>d.slots).filter(v=>v!==null).map(v=>v*1000);
  const stats=(arr)=>{
    if(!arr.length) return {min:0,max:0,avg:0,std:0};
    const avg=arr.reduce((a,x)=>a+x,0)/arr.length;
    const std=Math.sqrt(arr.reduce((a,x)=>a+(x-avg)**2,0)/arr.length);
    return {min:Math.min(...arr),max:Math.max(...arr),avg,std};
  };
  const ws=stats(weekPrices);
  const ms=stats(monthPrices);

  // Render stats
  document.getElementById('dam-stats-grid').innerHTML=`
    <div style="grid-column:1/-1;font-size:10px;font-family:var(--mono);color:var(--text3);margin-bottom:4px;text-transform:uppercase;letter-spacing:.07em">
      Week stats &nbsp;·&nbsp; <span style="color:var(--text2)">prices in €/MWh</span> &nbsp;·&nbsp;
      <span style="color:rgba(59,130,246,.9)">■ working day</span> &nbsp;
      <span style="color:rgba(139,92,246,.9)">■ non-working day</span>
    </div>
    ${statTile('Week peak',ws.max.toFixed(2),'€/MWh')}
    ${statTile('Week low',ws.min.toFixed(2),'€/MWh')}
    ${statTile('Week avg',ws.avg.toFixed(2),'€/MWh')}
    ${statTile('Week std dev',ws.std.toFixed(2),'€/MWh')}
    <div style="grid-column:1/-1;font-size:10px;font-family:var(--mono);color:var(--text3);margin-top:6px;margin-bottom:4px;text-transform:uppercase;letter-spacing:.07em">
      ${MONTHS_SHORT[mi]} full month stats
    </div>
    ${statTile('Month peak',ms.max.toFixed(2),'€/MWh')}
    ${statTile('Month low',ms.min.toFixed(2),'€/MWh')}
    ${statTile('Month avg',ms.avg.toFixed(2),'€/MWh')}
    ${statTile('Month std dev',ms.std.toFixed(2),'€/MWh')}`;

  // Draw chart
  if(damWeekChart) damWeekChart.destroy();
  damWeekChart=new Chart(document.getElementById('dam-week-chart'),{
    type:'bar',
    data:{labels,datasets:[{
      label:'DAM price (€/MWh)',
      data:prices,
      backgroundColor:bgColors,
      borderWidth:0,
      borderRadius:1,
      categoryPercentage:1.0,
      barPercentage:1.0
    }]},
    options:{
      responsive:true,maintainAspectRatio:false,
      animation:{duration:200},
      plugins:{
        legend:{display:false},
        tooltip:{callbacks:{
          title:ctx=>{
            const idx=ctx[0].dataIndex;
            const dayIdx=Math.floor(idx/48);
            const slotIdx=idx%48;
            const d=weekDays[dayIdx];
            const startMin=slotIdx*30;
            const sh=Math.floor(startMin/60).toString().padStart(2,'0');
            const sm=(startMin%60).toString().padStart(2,'0');
            const em=startMin+30;
            const eh=Math.floor(em/60)%24;
            const emm=em%60;
            return `${d.dateStr}  ${sh}:${sm}–${eh.toString().padStart(2,'0')}:${emm.toString().padStart(2,'0')}`;
          },
          label:ctx=>`€${ctx.parsed.y.toFixed(3)}/MWh`
        }}
      },
      scales:{
        x:{
          ticks:{
            font:{family:"'Consolas','Liberation Mono','Menlo',monospace",size:9},
            maxRotation:0,
            callback:(val,idx)=>labels[idx]||null
          },
          grid:{display:false}
        },
        y:{
          ticks:{callback:v=>v.toFixed(0),font:{family:"'Consolas','Liberation Mono','Menlo',monospace",size:10}},
          grid:{color:'rgba(28,37,48,.06)'},
          title:{display:true,text:'€/MWh',font:{family:"'Consolas','Liberation Mono','Menlo',monospace",size:10},color:'#4a5568'}
        }
      }
    }
  });
}

function statTile(label,val,unit){
  return `<div class="dam-stat">
    <div class="dam-stat-lbl">${label}</div>
    <div class="dam-stat-val">${val}</div>
    <div class="dam-stat-sub">${unit}</div>
  </div>`;
}

// Cyprus holidays helper for DAM viewer (uses the stored DAM year)
function getCyprusHolidays2026(){
  return getCyprusHolidaysAdmin(parseInt(document.getElementById('dam-year')?.value)||2026);
}
function exportDAM(type){
  if(!damRowCount){alert('No DAM data loaded.');return;}
  const MONTHS_FULL=['January','February','March','April','May','June',
    'July','August','September','October','November','December'];
  let csv='',filename='';

  if(type==='monthly'){
    // One row per month — monthly average €/kWh
    csv='Month,Month_No,Average_EUR_per_kWh\n';
    damMonthly.forEach((v,i)=>{
      if(v!==null) csv+=`${MONTHS_FULL[i]},${i+1},${v.toFixed(6)}
`;
    });
    filename=`DAM_monthly_averages.csv`;

  } else if(type==='slot_avg'){
    // 48 rows per month — slot-position averages
    csv='Month,Month_No,Slot,Time_Start,Time_End,Average_EUR_per_kWh\n';
    damBySlot.forEach((month,mi)=>{
      if(!month||!month.some(v=>v!==null)) return;
      month.forEach((v,s)=>{
        if(v===null) return;
        const startMin=s*30;
        const sh=Math.floor(startMin/60).toString().padStart(2,'0');
        const sm=(startMin%60).toString().padStart(2,'0');
        const endMin=(s+1)*30;
        const eh=(Math.floor(endMin/60)%24).toString().padStart(2,'0');
        const em=(endMin%60).toString().padStart(2,'0');
        csv+=`${MONTHS_FULL[mi]},${mi+1},${s},${sh}:${sm},${eh}:${em},${v.toFixed(6)}
`;
      });
    });
    filename=`DAM_slot_averages.csv`;

  } else if(type==='daily'){
    // Full daily data — one row per datetime
    csv='Date,Month,Day_of_Week,Slot,Time_Start,Time_End,Price_EUR_per_kWh\n';
    const dayNames=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
    damDailyData.forEach((monthData,mi)=>{
      if(!monthData||!monthData.length) return;
      monthData.forEach(day=>{
        day.slots.forEach((price,s)=>{
          if(price===null) return;
          const startMin=s*30;
          const sh=Math.floor(startMin/60).toString().padStart(2,'0');
          const sm=(startMin%60).toString().padStart(2,'0');
          const endMin=(s+1)*30;
          const eh=(Math.floor(endMin/60)%24).toString().padStart(2,'0');
          const em=(endMin%60).toString().padStart(2,'0');
          csv+=`${day.dateStr},${MONTHS_FULL[mi]},${dayNames[day.dow]},${s},${sh}:${sm},${eh}:${em},${price.toFixed(6)}
`;
        });
      });
    });
    filename=`DAM_daily_prices.csv`;
  }

  if(!csv){alert('No data to export for this format.');return;}
  const blob=new Blob([csv],{type:'text/csv;charset=utf-8;'});
  const a=document.createElement('a');
  a.href=URL.createObjectURL(blob);
  a.download=filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}

function clearDAM(){
  document.getElementById('dam-raw').value='';
  document.getElementById('dam-dz-label').innerHTML=`<span style="font-size:24px">📂</span><div style="margin-top:6px;font-weight:600">${T('DZ_TITLE')}</div><div style="margin-top:2px;font-size:11px;opacity:.7">${T('DZ_SUB')}</div>`;
  const s=document.getElementById('dam-status');s.className='status';s.textContent='';
  document.getElementById('dam-preview-card').style.display='none';
  document.getElementById('dam-viewer-card').style.display='none';
  document.getElementById('dam-coverage-card').style.display='none';
  damMonthly=new Array(12).fill(null);damBySlot=[];
  damDailyData=Array.from({length:12},()=>[]);
  if(damWeekChart){damWeekChart.destroy();damWeekChart=null;}
  _damHideReport();
}
async function saveDamData(){
  const st=document.getElementById('dam-status');
  // A file holding only part of the history would replace all of it: ask first.
  const now=new Set(_damDates(damDailyData));
  const dropped=[...damSavedDates].filter(d=>!now.has(d)).sort();
  if(dropped.length&&!confirm(T('DAM_CONFIRM_DROP').replace('{N}',dropped.length)
      .replace('{FROM}',dropped[0]).replace('{TO}',dropped[dropped.length-1]))) return;
  showStatus(st,'ok','Saving…');
  try{
    const body={damMonthly,damBySlot,damDailyData,damRowCount,damYear:fv('dam-year'),source:damPendingSource};
    const resp=await fetch(_adminApiBase+'/api/admin/dam',{method:'PUT',headers:authHeaders(),body:JSON.stringify(body)});
    if(resp.status===401){showLogin('Session expired.');return;}
    if(!resp.ok){const e=await resp.json().catch(()=>({}));showStatus(st,'err','Save failed: '+apiErrorText(e.detail,resp.status));return;}
    const r=await resp.json().catch(()=>({}));
    showStatus(st,'ok',`Saved ✓ — DAM data now live (version ${r.versionId}).`);
    damSavedDates=now;
    damPendingSource='upload';
    markClean('dam');
    renderDamCoverage();
    loadDamHistory();
    buildDamStatus();
  } catch(e){showStatus(st,'err','Save failed: '+e.message);}
}

/* ── DAM: CSV download, versions and change log ── */
let damPendingSource='upload';   // where the data on screen came from: 'upload' | 'tsoc'
let damSavedDates=new Set();     // dates in the stored (live) dataset

function _damDates(daily){
  const out=new Set();
  (daily||[]).forEach(m=>(m||[]).forEach(d=>{ if(d&&d.slots&&d.slots.some(v=>v!==null)) out.add(d.dateStr); }));
  return [...out].sort();
}
function _damApplyPayload(p){
  damMonthly=p.damMonthly||new Array(12).fill(null);
  damBySlot=p.damBySlot||[];
  damDailyData=p.damDailyData||Array.from({length:12},()=>[]);
  damRowCount=p.damRowCount||0;
  renderMonthGrid();
  renderDamCoverage();
  renderDamViewer();
}
function _damHideReport(){
  const box=document.getElementById('dam-fetch-report');
  box.style.display='none'; box.replaceChildren();
}
// Same format the upload box reads (unit €/MWh): "YYYY-MM-DD HH:MM,price".
function damToCsv(daily){
  const rows=[];
  (daily||[]).forEach(m=>(m||[]).forEach(d=>(d.slots||[]).forEach((p,s)=>{
    if(p===null||p===undefined) return;
    let v=(p*1000).toFixed(6).replace(/\.?0+$/,'');
    if(v==='-0') v='0';
    rows.push(`${d.dateStr} ${String(Math.floor(s/2)).padStart(2,'0')}:${s%2?'30':'00'},${v}`);
  })));
  rows.sort();
  return 'timestamp,price_eur_mwh\n'+rows.join('\n')+(rows.length?'\n':'');
}
function _damSaveFile(csv,name){
  const a=document.createElement('a');
  a.href=URL.createObjectURL(new Blob([csv],{type:'text/csv;charset=utf-8;'}));
  a.download=name;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}
function downloadDamCsv(){
  const dates=_damDates(damDailyData);
  if(!dates.length){alert(T('DAM_NO_DATA'));return;}
  _damSaveFile(damToCsv(damDailyData),`dam_prices_${dates[0]}_to_${dates[dates.length-1]}.csv`);
}
async function damDownloadVersion(id){
  const resp=await fetch(_adminApiBase+'/api/admin/dam/versions/'+encodeURIComponent(id),{headers:authHeaders()});
  if(resp.status===401){showLogin('Session expired.');return;}
  if(!resp.ok){alert('Download failed: '+resp.status);return;}
  const v=await resp.json();
  _damSaveFile(damToCsv(v.payload.damDailyData),`dam_prices_version_${v.id}_${v.firstDate||''}_to_${v.lastDate||''}.csv`);
}
async function damRestoreVersion(id){
  const v=_damVersions.find(x=>String(x.id)===String(id));
  if(!v) return;
  const msg=T('DAM_CONFIRM_RESTORE').replace('{V}',v.id).replace('{FROM}',v.firstDate||'—').replace('{TO}',v.lastDate||'—');
  if(!confirm(msg)) return;
  const st=document.getElementById('dam-status');
  const resp=await fetch(_adminApiBase+`/api/admin/dam/versions/${encodeURIComponent(id)}/restore`,{method:'POST',headers:authHeaders()});
  if(resp.status===401){showLogin('Session expired.');return;}
  const r=await resp.json().catch(()=>({}));
  if(!resp.ok){showStatus(st,'err','Restore failed: '+apiErrorText(r.detail,resp.status));return;}
  await reloadDamFromServer();
  _damHideReport();
  showStatus(st,'ok',T('DAM_RESTORED').replace('{V}',r.restoredFrom).replace('{N}',r.versionId));
}
async function reloadDamFromServer(){
  const resp=await fetch(_adminApiBase+'/api/admin/dam',{headers:authHeaders()});
  if(!resp.ok) return;
  const p=await resp.json();
  if(p.damYear) document.getElementById('dam-year').value=p.damYear;
  damSavedDates=new Set(_damDates(p.damDailyData));
  _damApplyPayload(p);
  damPendingSource='upload';
  markClean('dam');
  loadDamHistory();
  buildDamStatus();
}

let _damVersions=[];
const _DAM_SOURCES={initial:'DAM_SRC_INITIAL',upload:'DAM_SRC_UPLOAD',tsoc:'DAM_SRC_TSOC',rollback:'DAM_SRC_ROLLBACK'};
const _DAM_ACTIONS={saved_upload:'DAM_ACT_SAVED_UPLOAD',saved_tsoc:'DAM_ACT_SAVED_TSOC',rollback:'DAM_ACT_ROLLBACK',
  fetch_ok:'DAM_ACT_FETCH_OK',fetch_cancelled:'DAM_ACT_FETCH_CANCELLED',stale_alert_sent:'DAM_ACT_STALE'};
function _fmtTs(iso){
  if(!iso) return '—';
  return new Date(iso).toLocaleString(undefined,{year:'numeric',month:'short',day:'numeric',hour:'2-digit',minute:'2-digit'});
}
function _td(text){ const td=document.createElement('td'); td.textContent=text; return td; }
function _damBtn(label,action,id){
  const b=document.createElement('button');
  b.className='btn btn-sm';
  b.textContent=label;
  b.dataset.action=action;
  b.dataset.arg=id;
  return b;
}
async function loadDamHistory(){
  try{
    const [vr,lr]=await Promise.all([
      fetch(_adminApiBase+'/api/admin/dam/versions',{headers:authHeaders()}),
      fetch(_adminApiBase+'/api/admin/dam/log?limit=200',{headers:authHeaders()}),
    ]);
    if(!vr.ok||!lr.ok) return;
    _damVersions=await vr.json();
    const log=await lr.json();
    const vt=document.getElementById('dam-versions-tbody');
    if(!_damVersions.length){
      const tr=document.createElement('tr'); const td=_td(T('DAM_NO_VERSIONS')); td.colSpan=7; tr.appendChild(td);
      vt.replaceChildren(tr);
    }else{
      vt.replaceChildren(..._damVersions.map((v,i)=>{
        const tr=document.createElement('tr');
        const src=T(_DAM_SOURCES[v.source]||v.source)+(v.restoredFrom?` (v${v.restoredFrom})`:'');
        tr.append(_td('v'+v.id+(i===0?' · '+T('DAM_LIVE'):'')),_td(_fmtTs(v.createdAt)),_td(v.createdBy||'—'),_td(src),
          _td(v.firstDate?`${v.firstDate} → ${v.lastDate} (${v.dayCount})`:'—'),_td(String(v.rowCount||0)));
        const act=document.createElement('td');
        act.style.whiteSpace='nowrap';
        act.appendChild(_damBtn('⬇ CSV','damDownloadVersion',v.id));
        if(i>0){ act.append(' '); act.appendChild(_damBtn('↩ '+T('BTN_DAM_RESTORE'),'damRestoreVersion',v.id)); }
        tr.appendChild(act);
        return tr;
      }));
    }
    const lt=document.getElementById('dam-log-tbody');
    if(!log.length){
      const tr=document.createElement('tr'); const td=_td(T('DAM_NO_LOG')); td.colSpan=4; tr.appendChild(td);
      lt.replaceChildren(tr);
    }else{
      lt.replaceChildren(...log.map(l=>{
        const tr=document.createElement('tr');
        const what=_td(l.summary||'');
        const reasons=(l.details&&l.details.reasons)||[];
        if(reasons.length>1){
          const ul=document.createElement('ul');
          ul.style.margin='4px 0 0 16px';
          reasons.slice(0,50).forEach(x=>{ const li=document.createElement('li'); li.textContent=x; ul.appendChild(li); });
          what.appendChild(ul);
        }
        const act=_td(T(_DAM_ACTIONS[l.action]||l.action));
        if(l.action==='fetch_cancelled'||l.action==='stale_alert_sent') act.style.color='var(--red)';
        tr.append(_td(_fmtTs(l.ts)),_td(l.actor||T('DAM_SYSTEM')),act,what);
        return tr;
      }));
    }
  }catch(e){ console.warn('DAM history:',e); }
}

// Dashboard card, "needs attention" line and the menu marker.
async function buildDamStatus(){
  try{
    const resp=await fetch(_adminApiBase+'/api/admin/dam/status',{headers:authHeaders()});
    if(!resp.ok) return;
    const s=await resp.json();
    const until=document.getElementById('dash-dam-until');
    if(!s.lastDate){
      until.textContent=T('DASH_DAM_NONE');
    }else{
      until.textContent=`${s.lastDate} (${s.ageDays} ${T('DASH_DAM_DAYS_OLD')})`;
    }
    if(s.stale){
      const warn=document.createElement('span');
      warn.className='dash-expired';
      warn.textContent=' ('+T('DASH_DAM_STALE').replace('{N}',s.staleAfterDays)+')';
      until.appendChild(warn);
    }
    const lv=s.lastVersion;
    document.getElementById('dash-dam-saved').textContent=lv
      ?`${_fmtTs(lv.createdAt)} · ${lv.createdBy||T('DAM_SYSTEM')} · ${T(_DAM_SOURCES[lv.source]||lv.source)}`:'—';
    document.getElementById('dash-dam-days').textContent=s.dayCount?`${s.dayCount} (${s.firstDate} → ${s.lastDate})`:'0';
    const att=document.getElementById('dash-dam-attention');
    att.style.display=s.stale?'':'none';
    document.getElementById('dash-dam-attention-text').textContent=s.lastDate
      ?T('DASH_DAM_ATTENTION').replace('{D}',s.lastDate).replace('{N}',s.ageDays)
      :T('DASH_DAM_ATTENTION_NONE');
    document.getElementById('nav-dam-bubble').style.display=s.stale?'':'none';
  }catch(e){ console.warn('DAM status:',e); }
}

/* ── Regulated tariffs ── */
function getRegulated(){
  return {
    lv:     parseFloat(document.getElementById('reg-lv')?.value)||0,
    mv:     parseFloat(document.getElementById('reg-mv')?.value)||0,
    hv:     parseFloat(document.getElementById('reg-hv')?.value)||0,
    fpaLV:  parseFloat(document.getElementById('reg-fpa-lv')?.value)||0,
    fpaMV:  parseFloat(document.getElementById('reg-fpa-mv')?.value)||0,
    fpaHV:  parseFloat(document.getElementById('reg-fpa-hv')?.value)||0,
    pso:    parseFloat(document.getElementById('reg-pso')?.value)||0,
    res:    parseFloat(document.getElementById('reg-res')?.value)||0,
    mdm:    parseFloat(document.getElementById('reg-mdm')?.value)||0,
  };
}

function setRegulated(r){
  if(!r) return;
  const set=(id,v)=>{const el=document.getElementById(id);if(el&&v!==undefined)el.value=v;};
  set('reg-lv',r.lv);set('reg-mv',r.mv);set('reg-hv',r.hv);
  set('reg-fpa-lv',r.fpaLV||r.fpa||0);  // backwards compat with old single fpa
  set('reg-fpa-mv',r.fpaMV||r.fpa||0);
  set('reg-fpa-hv',r.fpaHV||r.fpa||0);
  set('reg-pso',r.pso);
  set('reg-res',r.res||0);
  set('reg-mdm',r.mdm||0);
  const setTs=(cls,iso)=>{
    const els=document.querySelectorAll(cls);
    if(iso){
      const dt=new Date(iso);
      const fmt=dt.toLocaleString(undefined,{year:'numeric',month:'short',day:'numeric',hour:'2-digit',minute:'2-digit'});
      const label=T('REG_LAST_UPDATED').replace('{dt}',fmt);
      els.forEach(el=>{el.textContent=label;el.style.display='block';});
    } else {
      els.forEach(el=>{el.style.display='none';});
    }
  };
  setTs('.reg-ts-grid',r.grid_updated_at);
  setTs('.reg-ts-fpa',r.fpa_updated_at);
  setTs('.reg-ts-universal',r.universal_updated_at);
  _regSaved=getRegulated();
}

// Values as last loaded/saved, so a new entry can be compared with the previous one.
let _regSaved=null;
// One line per changed value, plus a note if FPA is out of its usual LV > MV > HV order
// (only a note: a negative FPA reverses that order, so it can't be a hard rule).
function _regChangeLines(body){
  const lines=[];
  const fmt=v=>String(+v.toFixed(6));
  if(_regSaved) Object.keys(_REG_FIELDS).forEach(k=>{
    const was=_regSaved[k], now=body[k];
    if(Math.abs(now-was)<1e-12) return;
    const F=T('REG_F_'+k);
    if(was===0){lines.push(T('REG_CHANGE_FROM_ZERO').replace('{F}',F).replace('{NEW}',fmt(now)));return;}
    const pct=(now-was)/Math.abs(was)*100;
    lines.push(T('REG_CHANGE_PCT').replace('{F}',F)
      .replace('{P}',Math.abs(pct)<0.05?Math.abs(pct).toPrecision(1):Math.abs(pct).toFixed(1))
      .replace('{D}',T(pct>0?'REG_CHANGE_HIGHER':'REG_CHANGE_LOWER'))
      .replace('{OLD}',fmt(was)).replace('{NEW}',fmt(now)));
  });
  const fpaChanged=['fpaLV','fpaMV','fpaHV'].some(k=>!_regSaved||Math.abs(body[k]-_regSaved[k])>=1e-12);
  if(fpaChanged&&!(body.fpaLV>body.fpaMV&&body.fpaMV>body.fpaHV))
    lines.push(T('REG_FPA_ORDER').replace('{LV}',fmt(body.fpaLV)).replace('{MV}',fmt(body.fpaMV)).replace('{HV}',fmt(body.fpaHV)));
  return lines;
}
let _regChangeResolve=null;
function _askRegChange(lines){
  const ul=document.getElementById('reg-change-list');
  ul.replaceChildren(...lines.map(t=>{const li=document.createElement('li');li.textContent=t;return li;}));
  document.getElementById('reg-change-overlay').style.display='flex';
  return new Promise(res=>{_regChangeResolve=res;});
}
function _closeRegChange(ok){
  document.getElementById('reg-change-overlay').style.display='none';
  const res=_regChangeResolve;_regChangeResolve=null;
  if(res) res(ok);
}

// Server field → box on the Regulated tariffs page, for placing a refusal on its field.
const _REG_FIELDS={lv:'reg-lv',mv:'reg-mv',hv:'reg-hv',fpaLV:'reg-fpa-lv',fpaMV:'reg-fpa-mv',fpaHV:'reg-fpa-hv',pso:'reg-pso',res:'reg-res',mdm:'reg-mdm'};
async function saveRegulated(){
  const body=getRegulated();
  const st=document.getElementById('reg-save-status');
  document.querySelectorAll('#pane-regulated .field-invalid').forEach(el=>{el.classList.remove('field-invalid');if(el._errMsg){el._errMsg.remove();el._errMsg=null;}});
  // Grid usage always falls with voltage (the server enforces the same rule).
  let bad=0;
  if(!(body.mv<body.lv)&&_fieldError(document.getElementById('reg-mv'),T('ERR_REG_GRID_ORDER'))) bad++;
  if(!(body.hv<body.mv)&&_fieldError(document.getElementById('reg-hv'),T('ERR_REG_GRID_ORDER'))) bad++;
  if(bad){showStatus(st,'err',_tn('ERR_FIELDS_SUMMARY',bad));return;}
  const lines=_regChangeLines(body);
  if(lines.length&&!(await _askRegChange(lines))){showStatus(st,'err',T('REG_NOT_SAVED'));return;}
  showStatus(st,'ok','Saving…');
  try {
    const resp=await fetch(_adminApiBase+'/api/admin/regulated',{method:'PUT',headers:authHeaders(),body:JSON.stringify(body)});
    if(resp.status===401){showLogin('Session expired.');return;}
    if(!resp.ok){
      const e=await resp.json().catch(()=>({}));
      let placed=0;
      if(resp.status===422&&Array.isArray(e.detail)) e.detail.forEach(d=>{
        const id=_REG_FIELDS[(d.loc||[]).filter(x=>x!=='body')[0]];
        if(id&&_fieldError(document.getElementById(id),_friendlyMsg(d.type,d.ctx,d.msg))) placed++;
      });
      showStatus(st,'err',placed?_tn('ERR_FIELDS_SUMMARY',placed):'Save failed: '+apiErrorText(e.detail,resp.status));
      return;
    }
    const saved=await resp.json();
    setRegulated(saved);
    markClean('regulated');
    // Refresh local changelog from server so the new entry is visible
    try {
      const cfgResp=await fetch(_adminApiBase+'/api/admin/config',{headers:authHeaders()});
      if(cfgResp.ok){const cfg=await cfgResp.json();if(cfg.changelog) changelog=cfg.changelog;if(cfg.reports){reports=cfg.reports;updateReportsBubble();}}
    } catch {}
    showStatus(st,'ok','Saved ✓');
  } catch(e){showStatus(st,'err','Save failed: '+e.message);}
}

let _regHistoryCache=null;
let _regHistoryChart=null;
let _regHistoryMode='fpa';

const _REG_HISTORY_MODES={
  fpa:{
    titleKey:'MODAL_REG_HISTORY_FPA',
    series:[
      {field:'fpaLV',labelKey:'REG_HIST_COL_FPA_LV',color:'#1e3a5f'},
      {field:'fpaMV',labelKey:'REG_HIST_COL_FPA_MV',color:'#bc6c25'},
      {field:'fpaHV',labelKey:'REG_HIST_COL_FPA_HV',color:'#a6403a'},
    ],
  },
  grid:{
    titleKey:'MODAL_REG_HISTORY_GRID',
    series:[
      {field:'lv',labelKey:'REG_HIST_COL_LV',color:'#1e3a5f'},
      {field:'mv',labelKey:'REG_HIST_COL_MV',color:'#bc6c25'},
      {field:'hv',labelKey:'REG_HIST_COL_HV',color:'#a6403a'},
    ],
  },
  universal:{
    titleKey:'MODAL_REG_HISTORY_UNIVERSAL',
    series:[
      {field:'pso',labelKey:'REG_HIST_COL_PSO',color:'#1e3a5f'},
      {field:'res',labelKey:'REG_HIST_COL_RES',color:'#6b5b95'},
    ],
  },
};

async function openRegHistory(mode){
  _regHistoryMode=mode||'fpa';
  document.getElementById('reg-history-overlay').style.display='flex';
  document.getElementById('reg-history-showall').checked=false;
  try{
    const resp=await fetch(_adminApiBase+'/api/admin/regulated/history',{headers:authHeaders()});
    _regHistoryCache=resp.ok?await resp.json():[];
  }catch(e){
    _regHistoryCache=[];
  }
  renderRegHistory();
}
function closeRegHistory(){
  document.getElementById('reg-history-overlay').style.display='none';
  if(_regHistoryChart){_regHistoryChart.destroy();_regHistoryChart=null;}
}
function _regFmtRate(v){
  return (Math.round((v||0)*100000)/100000).toString();
}
function _regMonthKey(iso){
  const d=new Date(iso);
  return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0');
}
function renderRegHistory(){
  const cfg=_REG_HISTORY_MODES[_regHistoryMode]||_REG_HISTORY_MODES.fpa;
  document.getElementById('reg-history-title').textContent=T(cfg.titleKey);

  const showAll=document.getElementById('reg-history-showall').checked;
  const rows=_regHistoryCache||[];
  // rows arrive newest-first; group by month and keep only the latest snapshot per month
  const byMonth=new Map();
  for(const r of rows){
    const key=_regMonthKey(r.recordedAt);
    if(!byMonth.has(key)) byMonth.set(key,r);
  }
  let monthly=[...byMonth.entries()].map(([key,r])=>({key,...r})).sort((a,b)=>a.key.localeCompare(b.key));
  if(!showAll) monthly=monthly.slice(-12);

  const theadRow=document.getElementById('reg-history-thead-row');
  theadRow.innerHTML='<th style="padding:6px 8px">'+T('REG_HIST_COL_MONTH')+'</th>'+
    cfg.series.map(s=>'<th style="padding:6px 8px">'+T(s.labelKey)+'</th>').join('');

  const tbody=document.getElementById('reg-history-tbody');
  if(!monthly.length){
    tbody.innerHTML=`<tr><td colspan="${cfg.series.length+1}" class="empty-state" style="padding:16px">No history recorded yet.</td></tr>`;
  }else{
    tbody.innerHTML=[...monthly].reverse().map(r=>
      `<tr style="border-bottom:1px solid var(--border)">`+
      `<td style="padding:6px 8px">${r.key}</td>`+
      cfg.series.map(s=>`<td style="padding:6px 8px">${_regFmtRate(r[s.field])}</td>`).join('')+
      `</tr>`
    ).join('');
  }

  const ctx=document.getElementById('reg-history-chart');
  if(_regHistoryChart) _regHistoryChart.destroy();
  _regHistoryChart=new Chart(ctx,{
    type:'line',
    data:{
      labels:monthly.map(r=>r.key),
      datasets:cfg.series.map(s=>({
        label:T(s.labelKey),data:monthly.map(r=>r[s.field]),borderColor:s.color,backgroundColor:'transparent',tension:.2,
      })),
    },
    options:{responsive:true,maintainAspectRatio:false,scales:{y:{beginAtZero:false}}}
  });
}

function updateRegPreview(){
  const kwh=parseFloat(document.getElementById('reg-preview-kwh')?.value)||0;
  const voltage=document.getElementById('reg-preview-voltage')?.value||'LV';
  const r=getRegulated();
  const gridRate=voltage==='LV'?r.lv:voltage==='MV'?r.mv:r.hv;
  const gridCost=kwh*gridRate;
  const fpaRate=voltage==='LV'?r.fpaLV:voltage==='MV'?r.fpaMV:r.fpaHV;
  const fpaCost=kwh*fpaRate;
  const psoCost=kwh*r.pso;
  const resCost=kwh*(r.res||0);
  const total=gridCost+fpaCost+psoCost+resCost;
  const out=document.getElementById('reg-preview-output');
  if(!out) return;
  out.innerHTML=`
    <span style="color:var(--text3)">${voltage} Grid usage:</span> €${gridCost.toFixed(4)}  <span style="color:var(--text3)">(${kwh.toLocaleString()} kWh × €${gridRate.toFixed(4)})</span><br>
    <span style="color:var(--text3)">${voltage} FPA:</span>         €${fpaCost.toFixed(4)}  <span style="color:var(--text3)">(${kwh.toLocaleString()} kWh × €${fpaRate.toFixed(4)})</span><br>
    <span style="color:var(--text3)">PSO:</span>                    €${psoCost.toFixed(4)}  <span style="color:var(--text3)">(${kwh.toLocaleString()} kWh × €${r.pso.toFixed(4)})</span><br>
    ${r.res?`<span style="color:var(--text3)">RES Fund:</span>       €${resCost.toFixed(4)}  <span style="color:var(--text3)">(${kwh.toLocaleString()} kWh × €${(r.res).toFixed(4)})</span><br>`:''}
    <span style="color:var(--text);font-weight:600">Total regulated (annual, excl. MDM):</span> <span style="color:var(--green);font-weight:600">€${total.toFixed(2)}</span>
  `;
}

/* ── Notices editor ── */
function fmtDoc(editorId, cmd){
  const el=document.getElementById(editorId);
  if(!el) return;
  el.focus();
  document.execCommand(cmd,false,null);
}
function fmtHeading(editorId, tag){
  const el=document.getElementById(editorId);
  if(!el) return;
  el.focus();
  document.execCommand('formatBlock',false,tag);
}
function getNotices(){
  const g=id=>DOMPurify.sanitize(document.getElementById(id)?.innerHTML||'');
  return {
    assumptions_en: g('assumptions-en'),
    assumptions_el: g('assumptions-el'),
    legal_en: g('legal-en'),
    legal_el: g('legal-el'),
    vulnerable_en: g('vulnerable-en'),
    vulnerable_el: g('vulnerable-el')
  };
}
function setNotices(n){
  if(!n) return;
  const s=(id,val)=>{ const el=document.getElementById(id); if(el&&val!==undefined) el.innerHTML=DOMPurify.sanitize(val); };
  s('assumptions-en', n.assumptions_en||n.assumptions||'');
  s('assumptions-el', n.assumptions_el||'');
  s('legal-en', n.legal_en||n.legal||'');
  s('legal-el', n.legal_el||'');
  s('vulnerable-en', n.vulnerable_en||'');
  s('vulnerable-el', n.vulnerable_el||'');
}
async function saveNotices(){
  const st=document.getElementById('notices-status');
  showStatus(st,'ok','Saving…');
  try{
    const resp=await fetch(_adminApiBase+'/api/admin/notices',{method:'PUT',headers:authHeaders(),body:JSON.stringify(getNotices())});
    if(resp.status===401){showLogin('Session expired.');return;}
    if(!resp.ok){const e=await resp.json().catch(()=>({}));showStatus(st,'err','Save failed: '+(e.detail||resp.status));return;}
    showStatus(st,'ok','Saved ✓ — now live on the customer calculator.');
    markClean('notices');
  } catch(e){showStatus(st,'err','Save failed: '+e.message);}
}

async function saveSampleInvoiceConfig(){
  const cb=document.getElementById('sample-invoice-enabled');
  const st=document.getElementById('sample-invoice-status');
  showStatus(st,'ok','Saving…');
  try{
    const resp=await fetch(_adminApiBase+'/api/admin/sample-invoice',{method:'PUT',headers:authHeaders(),body:JSON.stringify({enabled:cb.checked})});
    if(resp.status===401){showLogin('Session expired.');return;}
    if(!resp.ok){const e=await resp.json().catch(()=>({}));showStatus(st,'err','Save failed: '+(e.detail||resp.status));return;}
    if(cb.checked) showStatus(st,'ok','Saved ✓ — now live on the customer calculator.');
    else showStatus(st,'err','Saved ✓ — now disabled on the customer calculator.');
  } catch(e){showStatus(st,'err','Save failed: '+e.message);}
}

/* ── Audit calculator ── */
function auditPopulateTariffs(){
  const sel=document.getElementById('audit-tariff-sel');
  if(!sel) return;
  const cur=sel.value;
  sel.innerHTML='<option value="">— select tariff —</option>';
  tariffs.forEach(t=>{
    const o=document.createElement('option');
    o.value=t.id; o.textContent=`${t.name} (${t.supplier} · ${t.pricing} · ${t.voltage})`; // textContent — safe, no escaping needed
    sel.appendChild(o);
  });
  if(cur) sel.value=cur;
  auditPopulateMonths();
}

function auditTariffChanged(){
  const id=document.getElementById('audit-tariff-sel').value;
  const info=document.getElementById('audit-tariff-info');
  const monthField=document.getElementById('audit-month')?.closest('.field');
  if(!id){info.style.display='none';if(monthField)monthField.style.display='';return;}
  const t=tariffs.find(x=>x.id===id);
  if(!t){info.style.display='none';if(monthField)monthField.style.display='';return;}
  const prof=profiles.find(p=>p.id===t.profileId);
  const reg=getRegulated();
  const fpaRate=t.fpaSource==='custom'?t.fpaCustom:t.fpaSource==='none'?0:
    (t.voltage==='LV'?reg.fpaLV:t.voltage==='MV'?reg.fpaMV:reg.fpaHV);
  // Hide month selector for Variable — always runs full year
  if(monthField) monthField.style.display=t.pricing==='Variable'?'none':'';
  info.style.display='';
  let extra='';
  if(t.pricing==='Dynamic'){
    extra=`Mult: ×${t.rates.mult} Adder: €${t.rates.adder} Floor: ${t.rates.damFloor?'€'+t.rates.damFloor:'none'}`;
  } else if(t.pricing==='Variable'){
    const resetLabel={1:'Monthly',2:'Bimonthly',3:'Quarterly',6:'Semi-annual',12:'Annual'}[t.rates.resetMonths]||t.rates.resetMonths+'mo';
    const tierLines=(t.rates.tiers||[]).map((tier,i)=>{
      const prev=i>0?t.rates.tiers[i-1].upTo:0;
      const range=tier.upTo!=null?prev+'–'+tier.upTo:'above '+prev;
      const fixed=tier.fixedCharge?` + €${parseFloat(tier.fixedCharge).toFixed(2)}/period`:'';
      return range+' kWh @ €'+tier.rate.toFixed(4)+'/kWh'+fixed;
    }).join(' | ');
    extra=`Reset: ${resetLabel} | Tiers: ${tierLines}`;
  }
  info.innerHTML=
    `<strong>${esc(t.name)}</strong> · ${esc(t.supplier)} · ${esc(t.pricing)} · ${esc(t.voltage)}<br>`+
    `Profile: ${prof?esc(prof.name):'⚠ none (fallback)'} · `+
    `FPA: €${fpaRate.toFixed(4)}/kWh (${t.fpaSource}) · `+
    `Standing: €${(parseFloat(t.standing)||0).toFixed(2)}/mo`+
    (extra?`<br>${extra}`:'');
}

function getCyprusHolidaysAdmin(year){
  // Orthodox Easter (Meeus' Julian algorithm + 13 days, valid 1900-2099) —
  // same as tariff-api/pricing/daycounts.py easter_date().
  function ed(y){
    const a=y%4,b=y%7,c=y%19,d=(19*c+15)%30,e=(2*a+4*b-d+34)%7;
    const mo=Math.floor((d+e+114)/31)-1,dy=((d+e+114)%31)+1;
    return new Date(y,mo,dy+13);
  }
  const fixed=[[1,1],[1,6],[3,25],[4,1],[5,1],[8,15],[10,1],[10,28],[12,25],[12,26]]
    .map(([mo,d])=>`${year}${String(mo).padStart(2,'0')}${String(d).padStart(2,'0')}`);
  const e=ed(year);
  const add=(dt,n)=>{const r=new Date(dt);r.setDate(r.getDate()+n);return r;};
  const fmt=dt=>`${dt.getFullYear()}${String(dt.getMonth()+1).padStart(2,'0')}${String(dt.getDate()).padStart(2,'0')}`;
  // Green Monday, Good Friday, Easter Monday, Kataklysmos (Whit Monday)
  return new Set([...fixed,fmt(add(e,-48)),fmt(add(e,-2)),fmt(add(e,1)),fmt(add(e,50))]);
}

function isNonWorkingAdmin(year,mi,d){
  const dow=new Date(year,mi,d).getDay();
  const key=`${year}${String(mi+1).padStart(2,'0')}${String(d).padStart(2,'0')}`;
  return dow===0||dow===6||getCyprusHolidaysAdmin(year).has(key);
}

function getDayCountsAdmin(year){
  const h=getCyprusHolidaysAdmin(year);
  const isLeap=year%4===0&&(year%100!==0||year%400===0);
  const dims=[31,isLeap?29:28,31,30,31,30,31,31,30,31,30,31];
  return Array.from({length:12},(_,mi)=>{
    let w=0,nw=0;
    for(let d=1;d<=dims[mi];d++){
      const dow=new Date(year,mi,d).getDay();
      const key=`${year}${String(mi+1).padStart(2,'0')}${String(d).padStart(2,'0')}`;
      if(dow===0||dow===6||h.has(key)) nw++; else w++;
    }
    return {working:w,nonWorking:nw};
  });
}

// ── Audit calculator: same rules as the server engine (tariff-api/pricing/) ──
// The audit is a deliberately independent re-implementation, so it can check
// the server's numbers; auditCrossCheck() compares the two after every run.

// 12-month window: the 12 months starting the month after today (Cyprus
// time) — must match daycounts.py calc_window().
function auditWindow(){
  const [y,m]=new Intl.DateTimeFormat('en-CA',{timeZone:'Europe/Nicosia',year:'numeric',month:'2-digit',day:'2-digit'})
    .format(new Date()).split('-').map(Number);
  const start=y*12+m;   // m is 1-based -> next month
  return Array.from({length:12},(_,k)=>({year:Math.floor((start+k)/12),mi:(start+k)%12}));
}
function auditMonthLabel(w,short){
  const name=short?T('MONTH_'+w.mi).slice(0,3):T('MONTH_'+w.mi);
  return short?`${name} '${String(w.year).slice(-2)}`:`${name} ${w.year}`;
}
function auditWindowLabel(win){ return `${auditMonthLabel(win[0])} – ${auditMonthLabel(win[11])}`; }
function auditPopulateMonths(){
  const sel=document.getElementById('audit-month');
  if(!sel) return;
  const cur=sel.value;
  sel.innerHTML='';
  auditWindow().forEach((w,pos)=>{
    const o=document.createElement('option');
    o.value=pos; o.textContent=`${pos+1}. ${auditMonthLabel(w)}`;
    sel.appendChild(o);
  });
  if(cur&&sel.querySelector(`option[value="${cur}"]`)) sel.value=cur;
}
// Day counts per window month (each month uses its own year's calendar).
function auditWindowDayCounts(win){
  const byYear={};
  return win.map(w=>(byYear[w.year]=byYear[w.year]||getDayCountsAdmin(w.year))[w.mi]);
}
function auditMonthHHFF(pm,dcm){
  if(!pm) return 0;
  let t=0;
  for(let s=0;s<48;s++) t+=((pm.W||[])[s]||0)*dcm.working+((pm.NW||[])[s]||0)*dcm.nonWorking;
  return t;
}
function auditAnnualHHFF(prof,win,dc){
  return win.reduce((a,w,pos)=>a+auditMonthHHFF(prof.months[w.mi],dc[pos]),0);
}
// Month kWh (Annual mode) — engine.py m_kwh_for_month()
function auditMonthKwh(prof,win,dc,annualHHFF,annualKwh,pos){
  if(!prof||annualHHFF<=0) return annualKwh/12;
  return annualKwh*auditMonthHHFF(prof.months[win[pos].mi],dc[pos])/annualHHFF;
}
// Discounts as the customer page applies them by default (all offers on):
// monthNo 1 = first month after switching — discounts.py get_discount_factors()
function auditDiscountFactors(tar,monthNo){
  let e=0,st=0;
  (tar.discounts||[]).forEach(d=>{
    if(d.durationMonths&&monthNo>d.durationMonths) return;
    if(d.type==='energy') e+=parseFloat(d.percentage)||0;
    else if(d.type==='standing') st+=parseFloat(d.percentage)||0;
  });
  return {energyFactor:Math.max(0,1-e/100),standingFactor:Math.max(0,1-st/100)};
}
// DAM price for one date+slot: actual price, then same date 1 and 2 years
// earlier, then month slot average, then month average — engine.py
// DAM_LOOKBACK_YEARS. Returns {price, source} or null.
function auditDamPrice(year,mi,d,s){
  const days=(damDailyData&&damDailyData[mi])||[];
  for(let back=0;back<=2;back++){
    const ds=`${year-back}-${String(mi+1).padStart(2,'0')}-${String(d).padStart(2,'0')}`;
    const day=days.find(x=>x.dateStr===ds);
    if(day&&day.slots&&day.slots[s]!=null) return {price:day.slots[s],source:back?`${year-back}`:'actual'};
  }
  const sa=damBySlot&&damBySlot[mi]?damBySlot[mi][s]:null;
  if(sa!=null) return {price:sa,source:'slot avg'};
  if(damMonthly[mi]!=null) return {price:damMonthly[mi],source:'month avg'};
  return null;
}
// Compare the audit figure with what the customer page shows for the same
// tariff (POST /api/public/calculate, Annual mode, all offers on). pos = window
// month index, or null to compare the 12-month total.
async function auditCrossCheck(tar,annualKwh,pos,auditValue){
  const el=document.getElementById('audit-crosscheck');
  if(!el) return;
  el.textContent='Checking against the customer page…';
  el.style.color='var(--text3)';
  const body={inputMode:'annual',annualKwh,pricingFilter:tar.pricing,vulnerableEligible:true,offersEnabled:true,
    customerType:tar.contract==='Domestic'?'domestic':'ci',voltage:tar.voltage,
    loadEntitlement:tar.loadEntitlement==='gt70'?'gt70':'lt70'};
  try{
    const resp=await fetch(_adminApiBase+'/api/public/calculate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
    if(!resp.ok) throw new Error('HTTP '+resp.status);
    const data=await resp.json();
    const r=(data.results||[]).find(x=>x.id===tar.id);
    if(!r){
      const noDam=(data.noDamTariffs||[]).some(x=>x.id===tar.id);
      el.textContent=noDam?'Customer page: excluded (no DAM price for some months).'
        :`Not shown on the customer page (status: ${tar.status||'unknown'}), so there is nothing to compare.`;
      return;
    }
    const server=pos==null?r.base:(r.months[pos]?r.months[pos].total:null);
    if(server==null){el.textContent='Customer page has no figure for this month.';return;}
    const diff=auditValue-server;
    const ok=Math.abs(diff)<0.005;
    el.style.color=ok?'var(--green)':'#b45309';
    el.textContent=(ok?'✓ Matches the customer page':'⚠ Differs from the customer page')+
      ` — customer page €${server.toFixed(4)}, audit €${auditValue.toFixed(4)}`+(ok?'':` (difference €${diff.toFixed(4)}).`+
      ' If you changed regulated charges or DAM data without saving, the customer page still uses the saved values.');
  }catch(e){
    el.textContent='Could not reach the customer-page calculation ('+e.message+').';
  }
}
function auditCrossCheckBox(){
  return `<div id="audit-crosscheck" style="margin-top:10px;font-size:12px;font-family:var(--mono);padding:8px 10px;border:1px solid var(--border);border-radius:2px;background:var(--bg)"></div>`;
}

function applyTiersAdmin(tiers, kwh){
  if(!tiers||!tiers.length||isNaN(kwh)||kwh<=0) return 0;
  let cost=0,prev=0;
  for(let i=0;i<tiers.length;i++){
    const tier=tiers[i];
    const cap=tier.upTo!=null?tier.upTo:Infinity;
    const band=Math.min(kwh-prev,cap-prev);
    if(band<=0) break;
    cost+=band*(parseFloat(tier.rate)||0);
    prev=cap;
    if(tier.upTo==null||kwh<=cap) break;
  }
  return cost;
}

function runAuditVariable(tar, annualKwh, win){
  const dc=auditWindowDayCounts(win);
  const r=tar.rates;
  const tiers=r.tiers||[];
  const reset=r.resetMonths||1;
  const reg=getRegulated();
  const fpaRate=tar.fpaSource==='custom'?tar.fpaCustom:tar.fpaSource==='none'?0:
    (tar.voltage==='LV'?reg.fpaLV:tar.voltage==='MV'?reg.fpaMV:reg.fpaHV);
  const windowLabel=auditWindowLabel(win);

  // kWh per window month — profile distributed if available, else flat
  const prof=profiles.find(p=>p.id===tar.profileId);
  const annualHHFF=prof?auditAnnualHHFF(prof,win,dc):0;
  const mKwh=pos=>auditMonthKwh(prof,win,dc,annualHHFF,annualKwh,pos);

  const resetLabel={1:'Monthly',2:'Bimonthly',3:'Quarterly',6:'Semi-annual',12:'Annual'}[reset]||reset+'mo';

  // Build one row per billing period
  const periods=[];
  let totKwh=0,totEnergy=0,totFixed=0,totFpa=0,totStanding=0,totAfterDisc=0;

  // Billing periods start with the first month after switching.
  for(let ps=0;ps<12;ps+=reset){
    const pe=Math.min(ps+reset,12);
    const periodLen=pe-ps;
    // kWh for this period
    let periodKwh=0;
    for(let m=ps;m<pe;m++) periodKwh+=mKwh(m);
    // Energy cost via tiers
    const energyCost=applyTiersAdmin(tiers,periodKwh);
    // Fixed charges: cumulative for all tiers reached
    let fixedCost=0;
    let prev=0;
    for(let i=0;i<tiers.length;i++){
      const tier=tiers[i];
      const cap=tier.upTo!=null?tier.upTo:Infinity;
      if(periodKwh>prev) fixedCost+=parseFloat(tier.fixedCharge)||0;
      prev=cap;
      if(tier.upTo==null||periodKwh<=cap) break;
    }
    const fpaCost=periodKwh*fpaRate;
    const standingCost=tar.standing*periodLen;
    const periodTotal=energyCost+fixedCost+fpaCost+standingCost;
    // Discounts per month, as the customer page applies them: energy+FPA by
    // the energy factor, standing + tier fixed charges by the standing factor.
    let afterDisc=0;
    for(let pos=ps;pos<pe;pos++){
      const df=auditDiscountFactors(tar,pos+1);
      afterDisc+=(energyCost+fpaCost)/periodLen*df.energyFactor+((parseFloat(tar.standing)||0)+fixedCost/periodLen)*df.standingFactor;
    }

    // Tier breakdown detail
    const tierDetail=[];
    let tprev=0;
    for(let i=0;i<tiers.length;i++){
      const tier=tiers[i];
      const cap=tier.upTo!=null?tier.upTo:Infinity;
      const band=Math.min(periodKwh-tprev,cap-tprev);
      if(band<=0) break;
      tierDetail.push({
        label:tier.upTo!=null?tprev+'–'+tier.upTo:'above '+tprev,
        kwh:band,
        rate:parseFloat(tier.rate)||0,
        cost:band*(parseFloat(tier.rate)||0),
        fixedCharge:parseFloat(tier.fixedCharge)||0
      });
      tprev=cap;
      if(tier.upTo==null||periodKwh<=cap) break;
    }

    const monthNames=Array.from({length:periodLen},(_,i)=>auditMonthLabel(win[ps+i],true)).join(' + ');
    periods.push({ps,pe,periodLen,monthNames,periodKwh,energyCost,fixedCost,fpaCost,standingCost,periodTotal,afterDisc,tierDetail});
    totKwh+=periodKwh; totEnergy+=energyCost; totFixed+=fixedCost; totFpa+=fpaCost; totStanding+=standingCost; totAfterDisc+=afterDisc;
  }

  const annualTotal=totEnergy+totFixed+totFpa+totStanding;
  const summaryTitle=document.getElementById('audit-summary-card').querySelector('.card-title');
  if(summaryTitle) summaryTitle.textContent='12-month summary';

  document.getElementById('audit-summary').innerHTML=`
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:8px">
      ${[
        ['Period',windowLabel],
        ['Reset period',resetLabel],
        ['Billing periods',Math.ceil(12/reset)],
        ['Annual kWh',totKwh.toFixed(2)],
        ['Tiers',tiers.length],
        ['Energy cost','€'+totEnergy.toFixed(2)],
        ['Tier fixed charges','€'+totFixed.toFixed(2)],
        ['FPA cost','€'+totFpa.toFixed(2)],
        ['Standing (12mo)','€'+totStanding.toFixed(2)],
        ['Total before discounts','€'+annualTotal.toFixed(2)],
        ['12-month total (as customer page)','€'+totAfterDisc.toFixed(2)],
        ['FPA rate','€'+fpaRate.toFixed(4)+'/kWh'],
        ['Profile',prof?esc(prof.name):'flat (÷12)'],
      ].map(([k,v])=>`<div style="background:var(--bg);border:1px solid var(--border);border-radius:2px;padding:8px 10px">
        <div style="font-size:9px;font-family:var(--mono);color:var(--text3);text-transform:uppercase;margin-bottom:3px">${k}</div>
        <div style="font-size:13px;font-weight:500;font-family:var(--mono);color:var(--text)">${v}</div>
      </div>`).join('')}
    </div>${auditCrossCheckBox()}`;

  // Table columns: Period | kWh | Tier breakdown | Energy | Fixed | FPA | Standing | Total | After discounts
  const cols=['Period','Months','kWh','Tier breakdown','Energy','Tier fixed','FPA','Standing','Period total','After discounts'];
  document.getElementById('audit-hh-thead').innerHTML='<tr>'+cols.map(c=>`<th>${c}</th>`).join('')+'</tr>';
  document.getElementById('audit-table-title').textContent=`${windowLabel} · ${tar.name} · ${annualKwh.toLocaleString()} kWh annual · ${resetLabel} reset`;

  document.getElementById('audit-hh-body').innerHTML=periods.map(p=>{
    const tierStr=p.tierDetail.map(td=>
      td.label+' kWh: '+td.kwh.toFixed(2)+' × €'+td.rate.toFixed(4)+(td.fixedCharge?' +€'+td.fixedCharge.toFixed(2)+' fixed':'')
    ).join('<br>');
    return `<tr>
      <td style="white-space:nowrap;font-family:var(--mono)">${p.ps+1}–${p.pe}</td>
      <td style="white-space:nowrap">${p.monthNames}</td>
      <td style="color:var(--green)">${p.periodKwh.toFixed(2)}</td>
      <td style="font-size:10px;color:var(--text2);line-height:1.6">${tierStr}</td>
      <td>${'€'+p.energyCost.toFixed(4)}</td>
      <td style="color:#0d9488">${p.fixedCost>0?'€'+p.fixedCost.toFixed(4):'-'}</td>
      <td style="color:#b45309">${'€'+p.fpaCost.toFixed(4)}</td>
      <td style="color:var(--text3)">${'€'+p.standingCost.toFixed(4)}</td>
      <td style="color:var(--accent);font-weight:600">${'€'+p.periodTotal.toFixed(4)}</td>
      <td style="font-weight:600">${'€'+p.afterDisc.toFixed(4)}</td>
    </tr>`;
  }).join('')
  +`<tr style="background:var(--bg3);font-weight:600;border-top:2px solid var(--border2)">
    <td colspan="2">12-MONTH TOTAL</td>
    <td style="color:var(--green)">${totKwh.toFixed(2)}</td>
    <td></td>
    <td>€${totEnergy.toFixed(4)}</td>
    <td style="color:#0d9488">€${totFixed.toFixed(4)}</td>
    <td style="color:#b45309">€${totFpa.toFixed(4)}</td>
    <td style="color:var(--text3)">€${totStanding.toFixed(4)}</td>
    <td style="color:var(--accent)">€${annualTotal.toFixed(4)}</td>
    <td>€${totAfterDisc.toFixed(4)}</td>
  </tr>`;

  // CSV
  const csvHeader='Period,Months,kWh,Tier detail,Energy,Tier fixed,FPA,Standing,Period total,After discounts\n';
  const csvRows=periods.map(p=>
    `"${p.ps+1}–${p.pe}","${p.monthNames}",${p.periodKwh.toFixed(4)},"${p.tierDetail.map(td=>td.label+':'+td.kwh.toFixed(2)+'kWh@€'+td.rate).join('; ')}",${p.energyCost.toFixed(4)},${p.fixedCost.toFixed(4)},${p.fpaCost.toFixed(4)},${p.standingCost.toFixed(4)},${p.periodTotal.toFixed(4)},${p.afterDisc.toFixed(4)}`
  ).join('\n');
  window._auditCSV=csvHeader+csvRows+`\nTOTAL,,${totKwh.toFixed(4)},,${totEnergy.toFixed(4)},${totFixed.toFixed(4)},${totFpa.toFixed(4)},${totStanding.toFixed(4)},${annualTotal.toFixed(4)},${totAfterDisc.toFixed(4)}`;
  window._auditFilename=`audit_variable_${tar.name.replace(/\s+/g,'_')}_${win[0].year}-${String(win[0].mi+1).padStart(2,'0')}.csv`;

  document.getElementById('audit-download-btn').style.display='';
  document.getElementById('audit-download-btn').onclick=()=>{
    const blob=new Blob([window._auditCSV],{type:'text/csv'});
    const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=window._auditFilename;a.click();
  };
  document.getElementById('audit-results').style.display='';
  document.getElementById('audit-results').scrollIntoView({behavior:'smooth'});
  auditCrossCheck(tar,annualKwh,null,totAfterDisc);
}

function runAudit(){
  const id=document.getElementById('audit-tariff-sel').value;
  const annualKwh=parseFloat(document.getElementById('audit-kwh').value)||0;
  // Window position: 0 = first month after switching (see auditWindow)
  const pos=parseInt(document.getElementById('audit-month').value)||0;
  if(!id||annualKwh<=0){alert('Please select a tariff and enter consumption.');return;}

  const tar=tariffs.find(x=>x.id===id);
  if(!tar){alert('Tariff not found.');return;}

  const win=auditWindow();
  const {year,mi}=win[pos];

  // ── Variable tariff: full 12-month billing period audit ──
  if(tar.pricing==='Variable'){
    runAuditVariable(tar, annualKwh, win);
    return;
  }

  const dc=auditWindowDayCounts(win);
  const prof=profiles.find(p=>p.id===tar.profileId);
  const reg=getRegulated();
  const fpaRate=tar.fpaSource==='custom'?tar.fpaCustom:tar.fpaSource==='none'?0:
    (tar.voltage==='LV'?reg.fpaLV:tar.voltage==='MV'?reg.fpaMV:reg.fpaHV);
  const floor=tar.pricing==='Dynamic'?(tar.rates.damFloor||0):0;
  const MONTHS_FULL=['January','February','March','April','May','June','July','August','September','October','November','December'];
  const dim=new Date(year,mi+1,0).getDate();
  const windowDays=win.reduce((a,w)=>a+new Date(w.year,w.mi+1,0).getDate(),0);

  if(tar.pricing==='Dynamic'&&!prof){
    alert('This Dynamic tariff has no load profile, so the customer page leaves it out of the comparison.');
    return;
  }

  // Annual HHFF total over the 12-month window
  const annualHHFF=prof?auditAnnualHHFF(prof,win,dc):0;
  // Without a usable profile, Fixed/ToU use a flat month (annual ÷ 12) and,
  // for ToU, a peak-hours ÷ 24 split — no half-hourly table.
  const flat=tar.pricing!=='Dynamic'&&(!prof||annualHHFF<=0);

  // Get ToU rates for this month (season by calendar month)
  const r=tar.rates;
  // Season and peak window may wrap (Nov->Feb, 22:00->06:00) — engine.py _in_season/_in_peak
  const hs=r.hiStart||0,he=r.hiEnd||0,mo=mi+1;
  const isHigh=tar.pricing==='ToU'?(hs<=he?(mo>=hs&&mo<=he):(he!==0&&(mo>=hs||mo<=he))):false;
  const ps=isHigh?r.hiPeakStart:r.loPeakStart;
  const pe=isHigh?r.hiPeakEnd:r.loPeakEnd;
  const peakRate=isHigh?r.hiPeakRate:r.loPeakRate;
  const offRate=isHigh?r.hiOffRate:r.loOffRate;
  const isPeakSlot=s=>ps<=pe?(s/2>=ps&&s/2<pe):(s/2>=ps||s/2<pe);   // slot start in hours, e.g. 16.5

  const damAvg=damMonthly[mi];

  // Profile HHFF for this month
  const pm=prof?prof.months[mi]:null;

  // Build one row per day per slot
  let rows=[];
  let totKwhWD=0,totKwhNWD=0,totEnergy=0,totFpa=0,totSlot=0;
  let damMissing=false;

  if(flat){
    const mKwh=annualKwh/12;
    let energy=0;
    if(tar.pricing==='Fixed') energy=mKwh*tar.rates.rate;
    else{
      const pf=(ps<=pe?Math.min(24,pe-ps):24-ps+pe)/24;
      energy=mKwh*pf*peakRate+mKwh*(1-pf)*offRate;
    }
    totKwhWD=mKwh; totEnergy=energy; totFpa=mKwh*fpaRate; totSlot=totEnergy+totFpa;
  } else for(let d=1;d<=dim;d++){
    const dateStr=`${year}-${String(mi+1).padStart(2,'0')}-${String(d).padStart(2,'0')}`;
    const isNonWork=isNonWorkingAdmin(year,mi,d);
    const dayType=isNonWork?'NWD':'WD';

    for(let s=0;s<48;s++){
      const smm=s*30, sh=Math.floor(smm/60), smmm=smm%60;
      const timeLabel=`${String(sh).padStart(2,'0')}:${String(smmm).padStart(2,'0')}`;

      // HHFF for this slot and day type
      const hhff=pm?(isNonWork?((pm.NW||[])[s]||0):((pm.W||[])[s]||0)):0;

      // kWh for this slot on this day (all slots of the window add up to annualKwh)
      const kWhSlot=annualHHFF>0?annualKwh*hhff/annualHHFF:annualKwh/(windowDays*48);

      let damRaw=null,damSource='';
      if(tar.pricing==='Dynamic'){
        const dp=auditDamPrice(year,mi,d,s);
        if(dp){damRaw=dp.price;damSource=dp.source;} else damMissing=true;
      }
      const damEff=tar.pricing==='Dynamic'&&damRaw!==null?Math.max(damRaw,floor):damRaw;

      // Costs
      let energyCost=0,fpaCost=0;
      if(tar.pricing==='Fixed'){
        energyCost=kWhSlot*tar.rates.rate;
        fpaCost=kWhSlot*fpaRate;
      } else if(tar.pricing==='ToU'){
        energyCost=kWhSlot*(isPeakSlot(s)?peakRate:offRate);
        fpaCost=kWhSlot*fpaRate;
      } else if(tar.pricing==='Dynamic'&&damEff!==null){
        const mult=parseFloat(tar.rates.mult)||1;
        const adder=parseFloat(tar.rates.adder)||0;
        energyCost=kWhSlot*(damEff*mult+adder);
        fpaCost=kWhSlot*fpaRate;
      }
      const slotTotal=energyCost+fpaCost;

      if(isNonWork) totKwhNWD+=kWhSlot; else totKwhWD+=kWhSlot;
      totEnergy+=energyCost; totFpa+=fpaCost; totSlot+=slotTotal;

      rows.push({d,dateStr,dayType,s,timeLabel,hhff,kWhSlot,damRaw,damSource,damEff,energyCost,fpaCost,slotTotal});
    }
  }

  // Discounts for this window month, as the customer page applies them by default
  const df=auditDiscountFactors(tar,pos+1);
  const standing=parseFloat(tar.standing)||0;
  const monthTotalFull=totSlot+standing;
  const monthTotal=(totEnergy+totFpa)*df.energyFactor+standing*df.standingFactor;
  const discPct=f=>f<1?`−${((1-f)*100).toFixed(1)}%`:'none';

  // Render summary
  document.getElementById('audit-summary').innerHTML=`
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:8px">
      ${[
        ['Month',`${MONTHS_FULL[mi]} ${year} (month ${pos+1} of 12)`],
        ['Working days',dc[pos].working],
        ['Non-working days',dc[pos].nonWorking],
        ['Total days',dim],
        ['Annual HHFF total (12-month window)',annualHHFF.toFixed(4)],
        ['Month kWh (WD)',totKwhWD.toFixed(4)],
        ['Month kWh (NWD)',totKwhNWD.toFixed(4)],
        ['Month kWh total',(totKwhWD+totKwhNWD).toFixed(4)],
        ['Energy cost','€'+totEnergy.toFixed(4)],
        ['FPA cost','€'+totFpa.toFixed(4)],
        ['Standing charge','€'+standing.toFixed(2)],
        ['Total before discounts','€'+monthTotalFull.toFixed(4)],
        ['Energy discount (this month)',discPct(df.energyFactor)],
        ['Standing discount (this month)',discPct(df.standingFactor)],
        ['Month total (as customer page)',damMissing?'excluded — DAM missing':'€'+monthTotal.toFixed(4)],
        ['DAM avg (month)',damAvg!=null?'€'+damAvg.toFixed(6):'-'],
        ['FPA rate','€'+fpaRate.toFixed(4)+'/kWh'],
        ['Floor price',floor>0?'€'+floor.toFixed(4):'-'],
        ['Rows in table',flat?'none (no profile: flat ÷12)':rows.length.toLocaleString()],
      ].map(([k,v])=>`<div style="background:var(--bg);border:1px solid var(--border);border-radius:2px;padding:8px 10px">
        <div style="font-size:9px;font-family:var(--mono);color:var(--text3);text-transform:uppercase;margin-bottom:3px">${k}</div>
        <div style="font-size:13px;font-weight:500;font-family:var(--mono);color:var(--text)">${v}</div>
      </div>`).join('')}
    </div>${auditCrossCheckBox()}`;

  // ── Dynamic table structure based on pricing type ──
  const isDynamic=tar.pricing==='Dynamic';
  const isToU=tar.pricing==='ToU';

  // Column definitions per pricing type
  const cols=isDynamic
    ?['Date','Day','Time','HHFF','kWh','DAM raw (€/kWh)','DAM source','DAM eff. (€/kWh)','Energy cost','FPA cost','Slot total']
    :isToU
    ?['Date','Day','Time','HHFF','kWh','Rate type','Rate (€/kWh)','Energy cost','FPA cost','Slot total']
    :['Date','Day','Time','HHFF','kWh','Rate (€/kWh)','FPA (€/kWh)','Energy cost','FPA cost','Slot total'];

  const colCount=cols.length;

  document.getElementById('audit-hh-thead').innerHTML=
    '<tr>'+cols.map(c=>`<th>${c}</th>`).join('')+'</tr>';

  document.getElementById('audit-table-title').textContent=
    `${MONTHS_FULL[mi]} ${year} (month ${pos+1} of 12) · ${tar.name} · ${annualKwh.toLocaleString()} kWh annual · ${rows.length.toLocaleString()} rows`;


  // Build CSV
  let csvHeader=cols.join(',')+',DayType\n';
  const csvRows=rows.map(row=>{
    const base=`${row.dateStr},${new Date(year,mi,row.d).toLocaleDateString('en-GB',{weekday:'short'})},${row.timeLabel},${row.hhff.toFixed(6)},${row.kWhSlot.toFixed(6)},`;
    if(isDynamic){
      return base+`${row.damRaw!==null?row.damRaw.toFixed(6):''},${row.damSource},${row.damEff!==null?row.damEff.toFixed(6):''},${row.energyCost.toFixed(6)},${row.fpaCost.toFixed(6)},${row.slotTotal.toFixed(6)},${row.dayType}`;
    } else if(isToU){
      const isPeak=isPeakSlot(row.s);
      const rate=isPeak?peakRate:offRate;
      return base+`${isPeak?'Peak':'Off-peak'},${rate.toFixed(6)},${row.energyCost.toFixed(6)},${row.fpaCost.toFixed(6)},${row.slotTotal.toFixed(6)},${row.dayType}`;
    } else {
      return base+`${tar.rates.rate.toFixed(6)},${fpaRate.toFixed(6)},${row.energyCost.toFixed(6)},${row.fpaCost.toFixed(6)},${row.slotTotal.toFixed(6)},${row.dayType}`;
    }
  }).join('\n');
  const csvTotals=`TOTAL,,,,,,${isDynamic?',':''}${totEnergy.toFixed(6)},${totFpa.toFixed(6)},${totSlot.toFixed(6)},`+
    `\nSTANDING,${standing.toFixed(6)}\nTOTAL BEFORE DISCOUNTS,${monthTotalFull.toFixed(6)}\nMONTH TOTAL (AS CUSTOMER PAGE),${monthTotal.toFixed(6)}`;
  const csvFull=csvHeader+csvRows+'\n'+csvTotals;

  window._auditCSV=csvFull;
  window._auditFilename=`audit_${tar.name.replace(/\s+/g,'_')}_${year}-${String(mi+1).padStart(2,'0')}.csv`;

  document.getElementById('audit-download-btn').style.display='';
  document.getElementById('audit-download-btn').onclick=()=>{
    const blob=new Blob([csvFull],{type:'text/csv'});
    const a=document.createElement('a');
    a.href=URL.createObjectURL(blob);
    a.download=window._auditFilename;
    a.click();
  };

  // Render table (first 500 rows, full in CSV)
  const DISPLAY_LIMIT=500;
  const tbody=document.getElementById('audit-hh-body');

  tbody.innerHTML=rows.slice(0,DISPLAY_LIMIT).map((row,i)=>{
    const isNewDay=i===0||rows[i-1].d!==row.d;
    const bg=row.dayType==='NWD'?'background:rgba(139,92,246,.06)':'';
    const dateCell=isNewDay?row.dateStr:'';
    const dayCell=isNewDay?new Date(year,mi,row.d).toLocaleDateString('en-GB',{weekday:'short'})+(row.dayType==='NWD'?' 🟣':' 🔵'):'';
    const border=isNewDay?';border-top:1px solid var(--border2)':'';

    let specificCols='';
    if(isDynamic){
      specificCols=`
        <td>${row.damRaw!==null?row.damRaw.toFixed(5):'-'}</td>
        <td style="color:${row.damSource==='actual'?'var(--text3)':'#b45309'}">${row.damSource||'-'}</td>
        <td>${row.damEff!==null?row.damEff.toFixed(5):'-'}</td>`;
    } else if(isToU){
      const isPeak=isPeakSlot(row.s);
      specificCols=`
        <td style="color:${isPeak?'#b45309':'var(--text3)'}">${isPeak?'Peak':'Off-peak'}</td>
        <td style="color:${isPeak?'#b45309':'var(--text2)'}">${(isPeak?peakRate:offRate).toFixed(5)}</td>`;
    } else {
      specificCols=`
        <td>${tar.rates.rate.toFixed(5)}</td>
        <td>${fpaRate.toFixed(5)}</td>`;
    }

    return `<tr style="${bg}${border}">
      <td style="white-space:nowrap">${dateCell}</td>
      <td style="color:var(--text3);white-space:nowrap">${dayCell}</td>
      <td style="white-space:nowrap">${row.timeLabel}</td>
      <td>${row.hhff.toFixed(4)}</td>
      <td style="color:var(--green)">${row.kWhSlot.toFixed(5)}</td>
      ${specificCols}
      <td>${row.energyCost.toFixed(5)}</td>
      <td>${row.fpaCost.toFixed(5)}</td>
      <td style="color:var(--accent)">${row.slotTotal.toFixed(5)}</td>
    </tr>`;
  }).join('');

  if(rows.length>DISPLAY_LIMIT){
    tbody.innerHTML+=`<tr><td colspan="${colCount}" style="text-align:center;color:var(--text3);padding:12px;font-family:var(--mono)">
      … ${(rows.length-DISPLAY_LIMIT).toLocaleString()} more rows — download CSV for full data
    </td></tr>`;
  }

  tbody.innerHTML+=`<tr style="background:var(--bg3);font-weight:600;border-top:2px solid var(--border2)">
    <td colspan="4">TOTALS</td>
    <td style="color:var(--green)">${(totKwhWD+totKwhNWD).toFixed(5)}</td>
    <td colspan="2"></td>
    <td>${totEnergy.toFixed(5)}</td>
    <td>${totFpa.toFixed(5)}</td>
    <td style="color:var(--accent)">${totSlot.toFixed(5)}</td>
  </tr>
  <tr style="background:var(--bg3)">
    <td colspan="${colCount-1}" style="text-align:right;color:var(--text2)">+ Standing €${(parseFloat(tar.standing)||0).toFixed(2)}</td>
    <td style="color:var(--accent);font-weight:600">€${monthTotal.toFixed(5)}</td>
  </tr>`;

  document.getElementById('audit-results').style.display='';
  document.getElementById('audit-results').scrollIntoView({behavior:'smooth'});
}


/* ── Publish ── */
async function buildDashboard(){
  // Pending review — the main thing an admin should see immediately on opening the page
  const pending=tariffs.filter(t=>t.status==='pending');
  const cardEl=document.getElementById('dash-pending-card');
  const titleEl=document.getElementById('dash-pending-title');
  const pendEl=document.getElementById('dash-pending-list');
  cardEl.classList.toggle('has-pending',pending.length>0);
  titleEl.classList.toggle('has-pending',pending.length>0);
  if(!pending.length){
    titleEl.textContent=T('DASH_ALL_CAUGHT_UP');
    const emptyDiv=document.createElement('div');
    emptyDiv.className='empty-state';
    emptyDiv.textContent=T('DASH_NOTHING_PENDING');
    pendEl.replaceChildren(emptyDiv);
  }else{
    titleEl.textContent=`${pending.length} ${T('DASH_AWAITING_REVIEW')}`;
    const rows=pending.slice(0,10).map(t=>{
      const row=document.createElement('div');
      row.className='dash-row';
      const main=document.createElement('span');
      main.className='dash-row-main';
      main.textContent=`${t.name} — ${t.supplier}`;
      const btn=document.createElement('button');
      btn.className='btn btn-sm btn-review';
      btn.textContent='Review';
      btn.addEventListener('click',()=>openReview(t.id));
      row.append(main,btn);
      return row;
    });
    if(pending.length>10){
      const more=document.createElement('div');
      more.className='dash-row-sub';
      more.style.paddingTop='8px';
      more.textContent=`+${pending.length-10} more…`;
      rows.push(more);
    }
    pendEl.replaceChildren(...rows);
  }

  buildDamStatus();
  // Regulated/FPA freshness + unusual activity aren't part of the bulk config load — fetch separately
  try{
    const [regResp,usersResp,loginResp]=await Promise.all([
      fetch(_adminApiBase+'/api/admin/regulated',{headers:authHeaders()}),
      fetch(_adminApiBase+'/api/admin/users',{headers:authHeaders()}),
      fetch(_adminApiBase+'/api/admin/login-activity?limit=100',{headers:authHeaders()}),
    ]);
    const reg=regResp.ok?await regResp.json():null;
    const users=usersResp.ok?await usersResp.json():[];
    const logins=loginResp.ok?await loginResp.json():[];

    const fmtDate=iso=>{
      if(!iso) return T('DASH_NEVER_UPDATED');
      const dt=new Date(iso);
      return dt.toLocaleString(undefined,{year:'numeric',month:'short',day:'numeric',hour:'2-digit',minute:'2-digit'});
    };
    const regIso=reg&&reg.updated_at;
    const regYear=regIso?new Date(regIso).getFullYear():null;
    const regStale=!regIso||regYear<new Date().getFullYear();
    const regEl=document.getElementById('dash-reg-updated');
    if(regStale){
      regEl.innerHTML=`${fmtDate(regIso)} <span class="dash-expired">(${T('DASH_REG_YEARLY_NOTE')})</span>`;
    }else{
      regEl.textContent=fmtDate(regIso);
    }

    const fpaIso=reg&&reg.fpa_updated_at;
    const fpaExpiry=fpaIso?new Date(fpaIso):null;
    if(fpaExpiry) fpaExpiry.setMonth(fpaExpiry.getMonth()+1);
    const fpaExpired=!fpaIso||fpaExpiry<new Date();
    const fpaEl=document.getElementById('dash-fpa-updated');
    if(fpaExpired){
      fpaEl.innerHTML=`${fmtDate(fpaIso)} <span class="dash-expired">(${T('DASH_FPA_EXPIRED')} <a href="https://www.eac.com.cy/EL/RegulatedActivities/Supply/tariffs/Pages/anaprosarmogitimiskavsimou.aspx" target="_blank" rel="noopener">EAC</a>)</span>`;
    }else{
      fpaEl.textContent=fmtDate(fpaIso);
    }

    const lockedUsers=users.filter(u=>u.is_locked);
    const cutoff=Date.now()-24*60*60*1000;
    const recentFailed=logins.filter(l=>!l.success&&l.ts&&new Date(l.ts).getTime()>=cutoff);

    const unusualCard=document.getElementById('dash-unusual-card');
    if(!lockedUsers.length&&!recentFailed.length){
      unusualCard.style.display='none';
    }else{
      unusualCard.style.display='';
      let html=lockedUsers.map(u=>
        `<div class="dash-row"><span class="dash-row-main">🔒 ${esc(u.email)}</span><span class="dash-row-sub">locked out</span></div>`
      ).join('');
      if(recentFailed.length){
        html+=`<div class="dash-row"><span class="dash-row-main">${recentFailed.length} failed login attempt${recentFailed.length===1?'':'s'}</span><span class="dash-row-sub">last 24h</span></div>`;
      }
      document.getElementById('dash-unusual').innerHTML=html;
    }
  }catch(e){
    console.warn('Dashboard: could not load regulated/users/login-activity',e);
  }
}
/* ── Auth helpers ── */
const _adminApiBase=window.location.protocol==='file:'?'http://localhost:8000':'';

// Session lives in an httpOnly cookie (set by the server) — the browser
// attaches it to same-origin fetches automatically, so there is no token
// for JS to read or send explicitly. _sessionActive just tracks whether
// the last known API call succeeded, for UI state (idle timer, badge).
let _sessionActive=false;

function authHeaders(extra){
  return {'Content-Type':'application/json',...(extra||{})};
}

// FastAPI returns validation errors (422) as a list of {loc, msg}; turn that
// into readable text instead of "[object Object]".
function apiErrorText(detail,fallback){
  if(Array.isArray(detail)){
    return detail.map(d=>{
      const loc=(d.loc||[]).filter(x=>x!=='body').join(' › ');
      return (loc?loc+': ':'')+String(d.msg||'').replace(/^Value error, /,'');
    }).join('; ');
  }
  return detail||fallback;
}

function _isStrongPassword(pw){
  return pw.length>=8 && /[A-Za-z]/.test(pw) && /[0-9]/.test(pw) && /[^A-Za-z0-9]/.test(pw);
}

/* ── Forced password-expiry gate ── */
/* Every fetch is intercepted so a 403 {detail:'password_expired'} response
   (from auth.get_current_user) pops a blocking modal, regardless of which
   API call triggered it — no need to touch every individual call site. */
(function(){
  const _origFetch=window.fetch.bind(window);
  window.fetch=async function(...args){
    const resp=await _origFetch(...args);
    // The session cookie is shared across every tab in this browser, not
    // per-tab. If an admin logs into a second tab as a supplier (or vice
    // versa), that overwrites the cookie everywhere, including this
    // already-open admin tab — and its next API call silently starts acting
    // as the new identity. X-User-Role (set server-side on every response)
    // lets us catch that the moment it happens rather than showing stale or
    // wrong-scoped data.
    const actualRole=resp.headers.get('X-User-Role');
    if(actualRole && actualRole!=='admin' && sessionStorage.getItem('cera_admin_role')==='admin'){
      _localSignOut('Your session was terminated — please sign in again.');
    }
    if(resp.status===403){
      try{
        const data=await resp.clone().json();
        if(data&&data.detail==='password_expired') _showPasswordExpiredModal();
      }catch(e){}
    }
    // Outside the CERA office/VPN networks the server answers every admin
    // request with 404 "Website unavailable" (e.g. the VPN dropped mid-session).
    // Reloading the page lets the server show its own "Website unavailable" page.
    if(resp.status===404){
      try{
        const data=await resp.clone().json();
        if(data&&data.detail==='Website unavailable'){
          if(typeof _unsaved!=='undefined') _unsaved.clear(); // no "Leave site?" prompt
          window.location.replace('admin.html');
        }
      }catch(e){}
    }
    return resp;
  };
})();
function _showPasswordExpiredModal(){
  const el=document.getElementById('pw-expired-overlay');
  if(el) el.style.display='flex';
}
function _hidePasswordExpiredModal(){
  const el=document.getElementById('pw-expired-overlay');
  if(el) el.style.display='none';
}
async function doUpdatePasswordExpired(){
  const cur=document.getElementById('pwx-cur-pw').value;
  const np=document.getElementById('pwx-new-pw').value;
  const conf=document.getElementById('pwx-confirm-pw').value;
  const msg=document.getElementById('pwx-msg');
  msg.style.color='var(--red)';
  if(!cur||!np||!conf){msg.textContent='Please fill in all fields.';return;}
  if(np!==conf){msg.textContent='New passwords do not match.';return;}
  if(!_isStrongPassword(np)){msg.textContent='Password must be at least 8 characters and include a letter, a number, and a symbol.';return;}
  try{
    const resp=await fetch(_adminApiBase+'/api/auth/password',{
      method:'PUT',headers:{...authHeaders(),'Content-Type':'application/json'},
      body:JSON.stringify({current_password:cur,new_password:np})
    });
    const data=await resp.json().catch(()=>({}));
    if(resp.ok){
      document.getElementById('pwx-cur-pw').value='';
      document.getElementById('pwx-new-pw').value='';
      document.getElementById('pwx-confirm-pw').value='';
      _hidePasswordExpiredModal();
    }else{
      msg.textContent=apiErrorText(data.detail, 'Update failed.');
    }
  }catch(e){msg.textContent='Network error.';}
}

function showForgotForm(){
  document.getElementById('login-form-inner').style.display='none';
  document.getElementById('forgot-panel').style.display='block';
  document.getElementById('forgot-email').value='';
  document.getElementById('forgot-status').textContent='';
  document.getElementById('forgot-status').style.color='';
}
function hideForgotForm(){
  document.getElementById('forgot-panel').style.display='none';
  document.getElementById('login-form-inner').style.display='block';
}
async function doForgot(){
  const email=document.getElementById('forgot-email').value.trim();
  if(!email) return;
  const btn=document.getElementById('forgot-btn');
  const st=document.getElementById('forgot-status');
  btn.disabled=true; btn.textContent='…';
  st.textContent=''; st.style.color='';
  try{
    await fetch(_adminApiBase+'/api/auth/forgot-password',{
      method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({email})
    });
    st.textContent='If this email is registered, a reset link has been sent. Check your inbox.';
    st.style.color='var(--green)';
  }catch(e){
    st.textContent='Network error — please try again.';
    st.style.color='var(--red)';
  }
  btn.disabled=false; btn.textContent=T('BTN_SEND_RESET');
}
function showLogin(msg){
  document.getElementById('login-err').textContent=msg||'';
  document.getElementById('login-email').value='';
  document.getElementById('login-password').value='';
  hideForgotForm();
  document.getElementById('login-overlay').classList.remove('hidden');
  setTimeout(()=>document.getElementById('login-email').focus(),80);
  _clearIdleTimers();
}

function hideLogin(){
  document.getElementById('login-overlay').classList.add('hidden');
  _resetIdleTimer();
}

/* ── Idle auto sign-out (15 min, with a 60s warning) ── */
const IDLE_TIMEOUT_MS=15*60*1000, IDLE_WARNING_LEAD_MS=60*1000;
let _idleWarnTimer=null, _idleCountdownInterval=null, _idleWarningShown=false;

function _isLoggedIn(){
  return _sessionActive && document.getElementById('login-overlay').classList.contains('hidden');
}

function _clearIdleTimers(){
  clearTimeout(_idleWarnTimer); _idleWarnTimer=null;
  if(_idleCountdownInterval){clearInterval(_idleCountdownInterval);_idleCountdownInterval=null;}
  _idleWarningShown=false;
  document.getElementById('idle-warning-overlay').style.display='none';
}

function _resetIdleTimer(){
  if(_idleWarningShown||!_isLoggedIn()) return;
  clearTimeout(_idleWarnTimer);
  _idleWarnTimer=setTimeout(_showIdleWarning,IDLE_TIMEOUT_MS-IDLE_WARNING_LEAD_MS);
}

function _showIdleWarning(){
  _idleWarningShown=true;
  let secs=IDLE_WARNING_LEAD_MS/1000;
  const overlay=document.getElementById('idle-warning-overlay');
  const countEl=document.getElementById('idle-warning-count');
  countEl.textContent=secs;
  overlay.style.display='flex';
  _idleCountdownInterval=setInterval(()=>{
    secs--;
    countEl.textContent=secs;
    if(secs<=0){
      clearInterval(_idleCountdownInterval);_idleCountdownInterval=null;
      _idleWarningShown=false;
      overlay.style.display='none';
      doLogout('You were signed out due to inactivity.');
    }
  },1000);
}

function _dismissIdleWarning(){
  if(_idleCountdownInterval){clearInterval(_idleCountdownInterval);_idleCountdownInterval=null;}
  _idleWarningShown=false;
  document.getElementById('idle-warning-overlay').style.display='none';
  _resetIdleTimer();
}

['mousedown','keydown','scroll','touchstart'].forEach(evt=>document.addEventListener(evt,_resetIdleTimer,{passive:true}));

let _pendingOtpToken='';
let _pendingOtpEmail='';
let _otpResendInterval=null;

function _startOtpResendCountdown(){
  const link=document.getElementById('otp-resend-link');
  const timer=document.getElementById('otp-resend-timer');
  link.style.display='none'; timer.style.display='inline';
  if(_otpResendInterval) clearInterval(_otpResendInterval);
  let secs=120;
  timer.textContent=T('OTP_RESEND_WAIT').replace('{s}',secs);
  _otpResendInterval=setInterval(()=>{
    secs--;
    if(secs<=0){
      clearInterval(_otpResendInterval); _otpResendInterval=null;
      timer.style.display='none';
      link.textContent=T('OTP_RESEND'); link.style.display='inline';
    } else {
      timer.textContent=T('OTP_RESEND_WAIT').replace('{s}',secs);
    }
  },1000);
}

function showLoginForm(){
  document.getElementById('login-form-inner').style.display='block';
  document.getElementById('otp-panel').style.display='none';
  document.getElementById('forgot-panel').style.display='none';
  _pendingOtpToken='';_pendingOtpEmail='';
  if(_otpResendInterval){clearInterval(_otpResendInterval);_otpResendInterval=null;}
}

async function doLogin(){
  const email=document.getElementById('login-email').value.trim();
  const password=document.getElementById('login-password').value;
  const btn=document.getElementById('login-btn');
  const errEl=document.getElementById('login-err');
  errEl.textContent='';
  if(!email||!password){errEl.textContent='Enter your email and password.';return;}
  btn.disabled=true;btn.textContent='Signing in…';
  try{
    const resp=await fetch(_adminApiBase+'/api/auth/login',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({email,password})
    });
    const data=await resp.json().catch(()=>({}));
    if(!resp.ok){errEl.textContent=data.detail||'Login failed.';btn.disabled=false;btn.textContent=T('BTN_SIGNIN');return;}
    if(data.status==='otp_required'){
      _pendingOtpToken=data.pending_token;
      _pendingOtpEmail=email;
      document.getElementById('login-form-inner').style.display='none';
      document.getElementById('otp-panel').style.display='block';
      document.getElementById('otp-code').value='';
      document.getElementById('otp-err').textContent='';
      _startOtpResendCountdown();
      setTimeout(()=>document.getElementById('otp-code').focus(),80);
      btn.disabled=false;btn.textContent=T('BTN_SIGNIN');
      return;
    }
    // Direct login (no 2FA path — kept for forward compatibility)
    if(data.role!=='admin'){errEl.textContent='Invalid email or password.';btn.disabled=false;btn.textContent=T('BTN_SIGNIN');return;}
    sessionStorage.setItem('cera_admin_email',data.email);
    sessionStorage.setItem('cera_admin_role',data.role);
    showUserBadge(data.email);
    hideLogin();
    await loadConfig();
  }catch(e){
    errEl.textContent='Network error — is the server running?';
  }
  btn.disabled=false;btn.textContent=T('BTN_SIGNIN');
}

async function doVerifyOtp(){
  const code=document.getElementById('otp-code').value.trim();
  const btn=document.getElementById('otp-btn');
  const errEl=document.getElementById('otp-err');
  errEl.textContent='';
  if(code.length!==6){errEl.textContent='Enter the 6-digit code from your email.';return;}
  btn.disabled=true;btn.textContent='Verifying…';
  try{
    const resp=await fetch(_adminApiBase+'/api/auth/verify-otp',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({pending_token:_pendingOtpToken,code})
    });
    const data=await resp.json().catch(()=>({}));
    if(!resp.ok){errEl.textContent=data.detail||'Verification failed.';btn.disabled=false;btn.textContent=T('OTP_BTN');return;}
    if(data.role!=='admin'){errEl.textContent='Invalid email or password.';btn.disabled=false;btn.textContent=T('OTP_BTN');return;}
    sessionStorage.setItem('cera_admin_email',data.email);
    sessionStorage.setItem('cera_admin_role',data.role);
    showUserBadge(data.email);
    showLoginForm();
    hideLogin();
    await loadConfig();
  }catch(e){
    errEl.textContent='Network error — is the server running?';
  }
  btn.disabled=false;btn.textContent=T('OTP_BTN');
}

async function doResendOtp(){
  const errEl=document.getElementById('otp-err');
  const link=document.getElementById('otp-resend-link');
  errEl.textContent=''; link.style.display='none';
  try{
    const resp=await fetch(_adminApiBase+'/api/auth/resend-otp',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({pending_token:_pendingOtpToken})
    });
    const data=await resp.json().catch(()=>({}));
    if(!resp.ok){errEl.textContent=data.detail||'Failed to resend code.';link.style.display='inline';return;}
    errEl.style.color='var(--success,#2f6f4e)';
    errEl.textContent=T('OTP_RESEND_SENT');
    setTimeout(()=>{errEl.textContent='';errEl.style.color='';},4000);
    _startOtpResendCountdown();
  }catch(e){
    errEl.textContent='Network error — is the server running?';
    link.style.display='inline';
  }
}

function doLogout(msg){
  // msg is set for automatic sign-outs (idle timeout, expired session), which can't wait for an answer
  if(!msg&&_unsaved.size&&!confirm('You have unsaved changes in:\n'+_unsavedLabels([..._unsaved])+'\n\nSign out and discard them?')) return;
  fetch(_adminApiBase+'/api/auth/logout',{method:'POST'}).catch(()=>{});
  _localSignOut(msg);
}

function _localSignOut(msg){
  _unsaved.clear();_refreshUnsavedMarkers();
  _sessionActive=false;
  sessionStorage.removeItem('cera_admin_email');
  sessionStorage.removeItem('cera_admin_role');
  document.getElementById('user-badge').style.display='none';
  showLogin(msg);
}

function showUserBadge(email){
  document.getElementById('user-email-label').textContent=email;
  document.getElementById('user-badge').style.display='flex';
}

// Allow pressing Enter on the password field to submit
document.getElementById('login-password').addEventListener('keydown',e=>{if(e.key==='Enter') doLogin();});
document.getElementById('login-email').addEventListener('keydown',e=>{if(e.key==='Enter') document.getElementById('login-password').focus();});

/* ── Init — load config from API ── */
async function loadConfig(){
  try{
    const resp=await fetch(_adminApiBase+'/api/admin/config',{headers:authHeaders()});
    if(resp.status===401){_localSignOut('Session expired — please sign in again.');return;}
    if(!resp.ok) throw new Error('HTTP '+resp.status);

    let role=sessionStorage.getItem('cera_admin_role');
    let email=sessionStorage.getItem('cera_admin_email');
    // The httpOnly cookie may be valid even if this tab never ran doLogin() itself
    // (e.g. a fresh tab, or a reload) — sessionStorage would then be empty and the
    // user badge/Sign out button would never appear. Re-hydrate from /me in that case.
    if(!role){
      try{
        const meResp=await fetch(_adminApiBase+'/api/auth/me',{headers:authHeaders()});
        if(meResp.ok){
          const me=await meResp.json();
          role=me.role; email=me.email;
          if(role==='admin'){
            sessionStorage.setItem('cera_admin_email',email);
            sessionStorage.setItem('cera_admin_role',role);
          }
        }
      }catch(e){}
    }
    // /api/admin/config succeeds for ANY authenticated user — it scopes tariffs
    // down to one supplier for supplier accounts rather than rejecting them
    // (see admin.py's is_supplier checks). doLogin()/verify-otp already reject
    // non-admin roles at the login form itself, but a supplier's own cookie
    // carried into a fresh admin.html tab/reload never touches that form —
    // it goes straight through this function. Treat it exactly like "not
    // logged in" rather than silently accepting it or redirecting elsewhere.
    if(role!=='admin'){ _localSignOut('Your session was terminated — please sign in again.'); return; }

    _sessionActive=true;
    hideLogin();
    showUserBadge(email);
    const cfg=await resp.json();
    suppliers=(cfg.suppliers||[]).map(s=>typeof s==='string'?{name:s}:s);
    profiles=cfg.profiles||[];
    tariffs=cfg.tariffs||[];
    damMonthly=cfg.damMonthly||new Array(12).fill(null);
    damBySlot=cfg.damBySlot||[];
    damRowCount=cfg.damRowCount||0;
    if(cfg.damYear) document.getElementById('dam-year').value=cfg.damYear;
    if(cfg.regulated) setRegulated(cfg.regulated);
    if(cfg.notices) setNotices(cfg.notices);
    const sampleInvCb=document.getElementById('sample-invoice-enabled');
    if(sampleInvCb) sampleInvCb.checked=!!cfg.sampleInvoiceEnabled;
    if(cfg.damDailyData) damDailyData=cfg.damDailyData;
    damSavedDates=new Set(_damDates(damDailyData));
    if(cfg.changelog) changelog=cfg.changelog;
    if(cfg.reports) reports=cfg.reports;
    if(cfg.docTariffIds) docTariffIds=new Set(cfg.docTariffIds);
    document.getElementById('saved-label').textContent='Data loaded '+new Date().toLocaleTimeString();
  }catch(e){
    document.getElementById('saved-label').textContent='⚠ API offline — start server';
    console.warn('Could not load from API:',e);
  }
  renderSuppliers();
  renderProfiles();
  renderTariffs();
  if(damMonthly.some(v=>v!==null)) renderMonthGrid();
  if(damDailyData.some(m=>m.length>0)) renderDamCoverage();
  buildDashboard();
  updateReportsBubble();
  loadDamHistory();
}

// On page load: the session lives in an httpOnly cookie we can't read from
// JS, so we can't synchronously know whether we're logged in. Optimistically
// ask the API for the config; loadConfig() itself shows/hides the login
// overlay depending on whether the cookie is still valid (401 vs 200).
(function init(){
  renderPage(); // apply stored language preference before anything else
  const storedEmail=sessionStorage.getItem('cera_admin_email');
  if(storedEmail) showUserBadge(storedEmail);
  // render empty UI so the page isn't blank behind the login overlay while we check
  renderSuppliers();renderProfiles();renderTariffs();
  loadConfig();
})();

function openAccountModal(){
  const email=sessionStorage.getItem('cera_admin_email')||'';
  document.getElementById('acct-current-email').value=email;
  document.getElementById('acct-new-email').value='';
  document.getElementById('acct-email-pw').value='';
  document.getElementById('acct-cur-pw').value='';
  document.getElementById('acct-new-pw').value='';
  document.getElementById('acct-confirm-pw').value='';
  document.getElementById('acct-email-msg').textContent='';
  document.getElementById('acct-pw-msg').textContent='';
  document.getElementById('acct-overlay').style.display='flex';
}
function closeAccountModal(){
  document.getElementById('acct-overlay').style.display='none';
}
function _acctMsg(id,text,ok){
  const el=document.getElementById(id);
  el.textContent=text;
  el.style.color=ok?'var(--green)':'var(--red)';
}
async function doUpdateEmail(){
  const newEmail=document.getElementById('acct-new-email').value.trim();
  const curPw=document.getElementById('acct-email-pw').value;
  if(!newEmail){_acctMsg('acct-email-msg','Please enter a new email.',false);return;}
  if(!curPw){_acctMsg('acct-email-msg','Please enter your current password to change your email.',false);return;}
  try{
    const resp=await fetch(_adminApiBase+'/api/auth/email',{
      method:'PUT',headers:{...authHeaders(),'Content-Type':'application/json'},
      body:JSON.stringify({new_email:newEmail,current_password:curPw})
    });
    const data=await resp.json().catch(()=>({}));
    if(resp.ok){
      sessionStorage.setItem('cera_admin_email',newEmail);
      document.getElementById('acct-current-email').value=newEmail;
      document.getElementById('user-email-label').textContent=newEmail;
      document.getElementById('acct-new-email').value='';
      document.getElementById('acct-email-pw').value='';
      _acctMsg('acct-email-msg','Email updated successfully.',true);
    }else{
      _acctMsg('acct-email-msg',apiErrorText(data.detail,'Update failed.'),false);
    }
  }catch(e){_acctMsg('acct-email-msg','Network error.',false);}
}
async function doUpdatePassword(){
  const cur=document.getElementById('acct-cur-pw').value;
  const np=document.getElementById('acct-new-pw').value;
  const conf=document.getElementById('acct-confirm-pw').value;
  if(!cur||!np||!conf){_acctMsg('acct-pw-msg','Please fill in all fields.',false);return;}
  if(np!==conf){_acctMsg('acct-pw-msg','New passwords do not match.',false);return;}
  if(!_isStrongPassword(np)){_acctMsg('acct-pw-msg','Password must be at least 8 characters and include a letter, a number, and a symbol.',false);return;}
  try{
    const resp=await fetch(_adminApiBase+'/api/auth/password',{
      method:'PUT',headers:{...authHeaders(),'Content-Type':'application/json'},
      body:JSON.stringify({current_password:cur,new_password:np})
    });
    const data=await resp.json().catch(()=>({}));
    if(resp.ok){
      document.getElementById('acct-cur-pw').value='';
      document.getElementById('acct-new-pw').value='';
      document.getElementById('acct-confirm-pw').value='';
      _acctMsg('acct-pw-msg','Password updated successfully.',true);
      _hidePasswordExpiredModal();
    }else{
      _acctMsg('acct-pw-msg',apiErrorText(data.detail, 'Update failed.'),false);
    }
  }catch(e){_acctMsg('acct-pw-msg','Network error.',false);}
}

// ── Event wiring ────────────────────────────────────────────────────────────
// No inline event-handler attributes (onclick and the like): the page runs under
// a strict Content-Security-Policy that refuses any code written inside the page
// (main.py, _CSP_POLICY). Elements say what they do with data-action (click),
// data-change, data-input, data-enter (Enter key) or data-backdrop-close, plus
// data-arg/data-arg2; this table is the complete list of what they may call.
const _bool = v => v === 'true';
const _ACTIONS = {
  // sign-in, account, session
  setLang: el => setLang(el.dataset.arg),
  doLogin: () => doLogin(), doLogout: () => doLogout(),
  showForgotForm: () => showForgotForm(), hideForgotForm: () => hideForgotForm(), showLoginForm: () => showLoginForm(),
  doForgot: () => doForgot(), doVerifyOtp: () => doVerifyOtp(), doResendOtp: () => doResendOtp(),
  digitsOnly: el => { el.value = el.value.replace(/\D/g, ''); },
  dismissIdleWarning: () => _dismissIdleWarning(),
  openAccountModal: () => openAccountModal(), closeAccountModal: () => closeAccountModal(),
  doUpdateEmail: () => doUpdateEmail(), doUpdatePassword: () => doUpdatePassword(),
  doUpdatePasswordExpired: () => doUpdatePasswordExpired(),
  showPane: el => showPane(el.dataset.arg),
  // suppliers
  addSupplier: () => addSupplier(),
  openSupModal: el => openSupModal(el.dataset.sup), closeSupModal: () => closeSupModal(),
  removeSupplier: el => removeSupplier(el.dataset.sup), saveSupplierDetails: () => saveSupplierDetails(),
  regulatedCheckboxClick: (el, e) => { if(onRegulatedCheckboxClick(e) === false) e.preventDefault(); },
  cancelRegChange: () => _closeRegChange(false), confirmRegChange: () => _closeRegChange(true),
  closeRegulatedConfirm: () => closeRegulatedConfirm(), confirmRegulatedToggle: () => confirmRegulatedToggle(),
  // profiles
  parseAndAddProfile: () => parseAndAddProfile(),
  editProfileName: el => editProfileName(el.dataset.arg), deleteProfile: el => deleteProfile(el.dataset.arg),
  selectProfileMonth: el => selectProfileMonth(el.dataset.arg, +el.dataset.arg2),
  // tariffs: list, editor, review, documents
  renderTariffs: () => renderTariffs(),
  clearTariffFilters: () => { ['tf-sup','tf-pricing','tf-contract'].forEach(id => { document.getElementById(id).value = ''; }); renderTariffs(); },
  setTariffGroup: el => setTariffGroup(el.dataset.arg),
  openEditorNew: () => openEditor(null), openViewer: el => openViewer(el.dataset.arg),
  closeEditor: () => closeEditor(), saveTariff: () => saveTariff(),
  editorStartEdit: () => editorStartEdit(), editorDeleteFromViewer: () => editorDeleteFromViewer(),
  onEditSupplierChange: () => onEditSupplierChange(),
  updateLoadEntitlementField: () => updateLoadEntitlementField(), updatePricingFields: () => updatePricingFields(),
  updateDurationType: () => updateDurationType(), updateFpaSource: () => updateFpaSource(),
  addDiscount: el => addDiscount(el.dataset.arg),
  removeDiscountRow: el => { const row = document.getElementById(el.dataset.arg); if(row) row.remove(); },
  addTierRow: () => addTierRow(), removeTierRow: el => removeTierRow(el),
  openReview: el => openReview(el.dataset.arg), closeReview: () => closeReview(),
  suspendTariff: el => suspendTariff(el.dataset.arg),
  setTariffStatus: el => setTariffStatus(el.dataset.arg, el.dataset.arg2),
  confirmReject: () => confirmReject(), cancelReject: () => cancelReject(),
  showRejectCustom: () => { document.getElementById('reject-custom-text').style.display = 'block'; },
  openAdminDocs: el => openAdminDocs(el.dataset.arg), closeAdminDocs: () => closeAdminDocs(),
  downloadDoc: el => downloadDoc(+el.dataset.arg),
  // users
  usersToggleForm: () => usersToggleForm(), usersInvite: () => usersInvite(),
  usersToggleOtp: el => usersToggleOtp(+el.dataset.arg, _bool(el.dataset.arg2)),
  usersUnlock: el => usersUnlock(+el.dataset.arg),
  usersSetStatus: el => usersSetStatus(+el.dataset.arg, _bool(el.dataset.arg2)),
  usersReinvite: el => usersReinvite(+el.dataset.arg), usersDelete: el => usersDelete(+el.dataset.arg),
  loginActivityLoad: () => loginActivityLoad(), renderLoginActivity: () => renderLoginActivity(),
  // messages and schedules
  toggleAudienceMode: () => toggleAudienceMode(), sendMessage: () => sendMessage(),
  archiveMessage: el => archiveMessage(el.dataset.arg, _bool(el.dataset.arg2)),
  deleteMessageEntry: el => deleteMessageEntry(el.dataset.arg),
  openMsgStatusModal: el => openMsgStatusModal(el.dataset.arg), closeMsgStatusModal: () => closeMsgStatusModal(),
  schedToggleForm: () => schedToggleForm(), schedToggleAudienceMode: () => schedToggleAudienceMode(),
  saveSchedule: () => saveSchedule(), editSchedule: el => editSchedule(el.dataset.arg),
  deleteSchedule: el => deleteSchedule(el.dataset.arg),
  toggleScheduleEnabled: el => toggleScheduleEnabled(el.dataset.arg, _bool(el.dataset.arg2)),
  // DAM prices
  damPickFiles: () => document.getElementById('dam-file-input').click(),
  damLoadFromInput: el => damLoadFiles(el.files),
  saveDamData: () => saveDamData(), clearDAM: () => clearDAM(), exportDAM: el => exportDAM(el.dataset.arg),
  downloadDamCsv: () => downloadDamCsv(),
  damDownloadVersion: el => damDownloadVersion(el.dataset.arg), damRestoreVersion: el => damRestoreVersion(el.dataset.arg),
  damBackToMonths: () => damBackToMonths(), damNavWeek: el => damNavWeek(+el.dataset.arg),
  damOpenMonth: el => damOpenMonth(+el.dataset.arg, +el.dataset.arg2),
  selectDamMonth: el => selectDamMonth(+el.dataset.arg), damShowDay: el => damShowDay(el.dataset.arg),
  // regulated, audit, notices, sample invoice, changelog, reports
  updateRegPreview: () => updateRegPreview(), saveRegulated: () => saveRegulated(),
  openRegHistory: el => openRegHistory(el.dataset.arg), closeRegHistory: () => closeRegHistory(),
  renderRegHistory: () => renderRegHistory(),
  auditTariffChanged: () => auditTariffChanged(), runAudit: () => runAudit(),
  fmtDoc: el => fmtDoc(el.dataset.arg, el.dataset.arg2), fmtHeading: el => fmtHeading(el.dataset.arg, el.dataset.arg2),
  saveNotices: () => saveNotices(), saveSampleInvoiceConfig: () => saveSampleInvoiceConfig(),
  renderChangelog: () => renderChangelog(), exportChangelog: () => exportChangelog(),
  renderReports: () => renderReports(),
  setReportStatus: el => setReportStatus(el.dataset.arg, el.dataset.arg2),
};
function _wire(eventName, attr){
  document.addEventListener(eventName, e => {
    const el = e.target.closest && e.target.closest(`[data-${attr}]`);
    if(!el) return;
    const fn = _ACTIONS[el.dataset[attr]];
    if(fn) fn(el, e);
  });
}
_wire('change', 'change');
_wire('input', 'input');
document.addEventListener('click', e => {
  // A modal closes when its dimmed backdrop itself is clicked, not the dialog inside it.
  if(e.target.dataset && e.target.dataset.backdropClose){
    const fn = _ACTIONS[e.target.dataset.backdropClose];
    if(fn) fn(e.target, e);
    return;
  }
  const el = e.target.closest && e.target.closest('[data-action]');
  if(!el) return;
  if(el.tagName === 'A') e.preventDefault();        // href="#" links must not jump to the top
  const fn = _ACTIONS[el.dataset.action];
  if(fn) fn(el, e);
});
// Number boxes: browsers let you type "e" (as in 5e3), "+" and "-" into them. Those
// keys are ignored, except "-" in the boxes where a negative value is valid (their
// min is below 0: custom FPA, Dynamic adder, regulated FPA). Anything pasted is
// cleaned up the same way.
const _negAllowed = box => box.min === '' || +box.min < 0;
document.addEventListener('keydown', e => {
  const box = e.target;
  if(!(box instanceof HTMLInputElement) || box.type !== 'number') return;
  if(['e','E','+'].includes(e.key) || (e.key === '-' && !_negAllowed(box))) e.preventDefault();
});
document.addEventListener('input', e => {
  const box = e.target;
  if(!(box instanceof HTMLInputElement) || box.type !== 'number' || box.value === '') return;
  const v = box.valueAsNumber;
  if(!Number.isFinite(v) || (v < 0 && !_negAllowed(box))) box.value = '';
  else if(/[eE+]/.test(box.value)) box.value = String(v);
});
document.addEventListener('keydown', e => {
  if(e.key !== 'Enter') return;
  const el = e.target.closest && e.target.closest('[data-enter]');
  const fn = el && _ACTIONS[el.dataset.enter];
  if(fn) fn(el, e);
});
// DAM file drop zone: drag-and-drop of CSV files.
(function(){
  const dz = document.getElementById('dam-dropzone');
  if(!dz) return;
  dz.addEventListener('dragover', e => { e.preventDefault(); dz.classList.add('dam-dz-over'); });
  dz.addEventListener('dragleave', () => dz.classList.remove('dam-dz-over'));
  dz.addEventListener('drop', e => { e.preventDefault(); dz.classList.remove('dam-dz-over'); damLoadFiles(e.dataTransfer.files); });
})();

// ── Language ──────────────────────────────────────────────────────────────────
const LANG = {
  en: {
    LOGIN_TITLE:'CERA - Electricity Supplier Portal', LOGIN_SUB:'Sign in with to your account',
    LOGIN_EMAIL:'Email', LOGIN_PASSWORD:'Password', LOGIN_BTN:'Sign in', LOGIN_SIGNING_IN:'Signing in…',
    LOGIN_FORGOT:'Forgot password?',
    FORGOT_TITLE:'Reset password', FORGOT_SUB:'Enter your email to receive a reset link.',
    FORGOT_BTN:'Send reset link', FORGOT_SENDING:'Sending…', FORGOT_BACK:'← Back to sign in',
    FORGOT_OK:'If this email is registered, a reset link has been sent. Check your inbox.',
    IDLE_TITLE:'Still there?', IDLE_SUB:"You've been inactive for a while. For security, you'll be signed out soon.", IDLE_STAY:'Stay signed in',
    FORGOT_ERR:'Network error — please try again.',
    TOPBAR_TITLE:'CERA - Electricity Supplier Portal', BTN_MY_ACCOUNT:'My Account', BTN_SIGN_OUT:'Sign out', LBL_SUPPLIER_TAG:'Supplier',
    INFO_WORKFLOW_TITLE:'Submission workflow:',
    INFO_WORKFLOW_BODY:'New tariffs and edits are submitted as <em>Pending review</em> and go live only after a CERA administrator approves them. Editing an approved tariff will unpublish it until re-approved.',
    LBL_LIVE:'Live', LBL_PENDING_REVIEW:'Pending review', LBL_REJECTED:'Rejected', LBL_DRAFT:'Draft',
    CARD_MESSAGES:'Notifications', MSG_NO_MESSAGES:'No notifications.',
    BTN_ACK:'Acknowledge', MSG_ACKED_SECTION:'Acknowledged',
    CARD_MY_TARIFFS:'Available Tariffs', BTN_SUBMIT_NEW:'+ Submit new tariff',
    TH_NAME:'Name', TH_CONTRACT:'Contract', TH_VOLTAGE:'Voltage', TH_PRICING:'Pricing', TH_STATUS:'Status', TH_ACTIONS:'Actions',
    EMPTY_TARIFFS:'No tariffs yet. Submit your first tariff to get started.',
    STATUS_LIVE:'● Live', STATUS_PENDING:'⏳ Pending review', STATUS_REJECTED:'✕ Rejected', STATUS_DRAFT:'◌ Draft',
    STATUS_SUSPENDED:'● Suspended', STATUS_ARCHIVED:'▣ Archived',
    BTN_DOCS:'📎 Docs', BTN_EDIT:'Edit', BTN_DELETE:'Delete',
    EDIT_NOTE:'Editing will unpublish this tariff until re-approved',
    FORM_TITLE_NEW:'Submit new tariff', FORM_TITLE_EDIT:'Edit tariff',
    BTN_CLOSE:'✕ Close', BTN_SUBMIT:'Submit for review',
    BTN_SAVE_RESUBMIT_REVIEW:'Save & resubmit for review', BTN_SAVE_RESUBMIT:'Save & resubmit',
    BTN_SUBMITTING:'Submitting…', BTN_CANCEL:'Cancel',
    LBL_TARIFF_NAME:'Tariff name', LBL_CONTRACT_TYPE:'Contract type',
    OPT_DOMESTIC:'Domestic', OPT_COMMERCIAL:'Commercial', OPT_INDUSTRIAL:'Industrial',
    LBL_VOLTAGE:'Voltage level', OPT_LV:'LV — Low Voltage', OPT_MV:'MV — Medium Voltage', OPT_HV:'HV — High Voltage',
    LBL_PRICING_TYPE:'Pricing type', OPT_FIXED:'Fixed', OPT_TOU:'Time-of-use (ToU)', OPT_DYNAMIC:'Dynamic (DAM)', OPT_VARIABLE:'Variable (tiered)',
    LBL_LOAD_ENT:'Load entitlement',
    OPT_LE_ANY:'Any (applies to both <70kVA and >70kVA)', OPT_LE_LT70:'< 70 kVA', OPT_LE_GT70:'> 70 kVA',
    HINT_LE:'For Commercial/Industrial customers on LV or MV connections.',
    SEC_CONTRACT_DURATION:'Contract duration', LBL_DURATION_TYPE:'Duration type',
    OPT_INDEFINITE:'Indefinite (no minimum period)', OPT_FIXED_TERM:'Fixed term — specify months',
    LBL_DURATION_MONTHS:'Minimum length (months)',
    SEC_STANDING:'Standing charge', LBL_STANDING:'Monthly standing charge (€)',
    LBL_MDM:'MDM — Meter Data Management (€/month)',
    SEC_FPA:'Fuel Price Adjustment (FPA)', LBL_FPA_SOURCE:'FPA source',
    OPT_FPA_GLOBAL:'Use global FPA (from CERA regulated tab)', OPT_FPA_CUSTOM:'Enter custom FPA for this tariff', OPT_FPA_NONE:'No FPA for this tariff',
    LBL_FPA_CUSTOM_RATE:'Custom FPA rate (€/kWh)',
    SEC_SPECIAL:'Special categories',
    LBL_VULNERABLE:'Vulnerable consumer / social tariff — only shown to eligible customers',
    LBL_PROFILE:'Assigned load profile', OPT_PROFILE_NONE:'— None (hour-fraction fallback) —',
    HINT_PROFILE:'Required for accurate ToU and dynamic cost calculations.',
    SEC_DISCOUNTS:'Discounts & promotions', HINT_DISCOUNTS:'Add promotional discounts that customers can toggle on/off.',
    LBL_STANDING_DISCOUNTS:'Standing charge discounts', LBL_ENERGY_DISCOUNTS:'Energy discounts', BTN_ADD_DISCOUNT:'+ Add',
    SEC_FIXED:'Fixed rate', LBL_UNIT_RATE:'Unit rate (€/kWh)',
    SEC_SEASON:'Season boundaries', LBL_HI_START:'High season start (month 1–12)', LBL_HI_END:'High season end (inclusive)',
    SEC_PEAK:'Peak hour windows', LBL_HI_SEASON:'High season', LBL_LO_SEASON:'Low season',
    LBL_PEAK_START:'Peak start (h)', LBL_PEAK_END:'Peak end (h, exclusive)',
    SEC_RATES:'Rates (€/kWh)', LBL_PEAK_RATE:'Peak rate', LBL_OFF_PEAK_RATE:'Off-peak rate',
    SEC_DAM:'DAM pricing factors', LBL_MULT:'Multiplier (×)', HINT_MULT:'e.g. 1.15 = +15%',
    LBL_ADDER:'Adder (€/kWh)', HINT_ADDER:'Supplier margin',
    LBL_DAM_FLOOR:'Min DAM price (€/kWh)', LBL_OPTIONAL:'optional',
    HINT_DAM_FLOOR:'Floor price. Leave blank for none.',
    HINT_DAM_FORMULA:'Effective rate = (MAX(DAM, min) × multiplier) + adder',
    SEC_TIERED:'Tiered block pricing', LBL_BILLING_RESET:'Billing reset period',
    OPT_MONTHLY:'Monthly (resets every month)', OPT_BIMONTHLY:'Bimonthly (resets every 2 months)', OPT_QUARTERLY:'Quarterly (resets every 3 months)',
    LBL_RATE_TIERS:'Rate tiers', BTN_ADD_TIER:'+ Add tier',
    HINT_TIERS:'Enter tiers in order. The last tier has no upper limit (∞).',
    LBL_SUPPORT_DOC:'Supporting document', LBL_OPTIONAL_SUFFIX:'(optional)',
    HINT_DOC:'Relevant published tariff documentation must be provided for verification. PDF only, max 10 MB.',
    TIER_LBL:'Tier', TIER_UP_TO:'up to', TIER_KWH:'kWh', TIER_RATE:'rate', TIER_RATE_UNIT:'€/kWh', TIER_FIXED:'fixed', TIER_FIXED_UNIT:'€/period',
    ERR_TIER_NEEDED:'Variable tariff needs at least one tier.', ERR_NAME_REQUIRED:'Please provide the tariff name.',
    ERR_ONE_TIER:'Need at least one tier.',
    ERR_ENTER_EMAIL_PW:'Enter your email and password.',
    ERR_SESSION_EXPIRED:'Session expired — please sign in again.', ERR_SESSION_EXPIRED_SHORT:'Session expired.',
    ERR_LOGIN_FAILED:'Login failed.', ERR_SUPPLIER_ONLY:'Invalid email or password.',
    ERR_NETWORK:'Network error — is the server running?', ERR_DELETE_FAILED:'Delete failed.',
    MSG_TARIFF_UPDATED:'Tariff updated and resubmitted for review.', MSG_TARIFF_SUBMITTED:'Tariff submitted for CERA review.',
    MSG_DOC_UPLOAD_FAILED:'Document upload failed: ',
    CONFIRM_DELETE:'Delete "{name}"?\n\nThis cannot be undone.',
    CONFIRM_ARCHIVE:'Remove "{name}" from the public comparison?\n\nIt has been published before, so it will be kept in your list as Archived (read-only) and can only be restored by CERA.',
    PH_DISC_CONDITIONS:'Conditions, e.g. direct debit', PH_DISC_PCT:'% off', PH_DISC_MONTHS:'Months (blank = permanent)',
    ERR_VALIDATION:'Please correct the following:',
    ERR_FIELDS_SUMMARY:'Please correct the highlighted fields ({N}).',
    ERR_F_REQUIRED:'Please enter a value.', ERR_F_MIN:'This cannot be less than {N}.',
    ERR_F_ABOVE:'This must be more than {N}.', ERR_F_MAX:'This cannot be more than {N}.',
    ERR_F_WHOLE:'Please enter a whole number.', ERR_F_TOO_LONG:'Too long: at most {N} characters.',
    ERR_F_TIER_ORDER:'The limit of each tier must be higher than the one before it.',
    ERR_F_TIER_OPEN:'Only the last tier may be left without a limit (∞).',
    ERR_F_DISC_PCT:'Enter a percentage (more than 0, up to 100), or remove this discount.',
    ACCT_ERR_EMAIL_PW:'Please enter your current password to change your email.',
    CONFIRM_DISCARD:'You have unsaved changes to this tariff.\n\nDiscard them?',
    CONFIRM_DISCARD_SIGNOUT:'You have unsaved changes to a tariff.\n\nSign out and discard them?',
    ACCT_TITLE:'My Account', ACCT_EMAIL_SECTION:'Change email', ACCT_CURRENT_EMAIL:'Current email',
    ACCT_NEW_EMAIL:'New email', BTN_UPDATE_EMAIL:'Update email',
    ACCT_PW_SECTION:'Change password', ACCT_CUR_PW:'Current password', ACCT_NEW_PW:'New password',
    ACCT_CONFIRM_PW:'Confirm new password', BTN_UPDATE_PW:'Update password',
    ACCT_ERR_NEW_EMAIL:'Please enter a new email.', ACCT_EMAIL_OK:'Email updated successfully.',
    ACCT_PW_FILL:'Please fill in all fields.', ACCT_PW_MISMATCH:'New passwords do not match.',
    ACCT_PW_SHORT:'New password must be at least 8 characters.', ACCT_PW_OK:'Password updated successfully.',
    ACCT_PW_WEAK:'Password must be at least 8 characters and include a letter, a number, and a symbol.',
    PW_EXPIRED_TITLE:'Password change required',
    PW_EXPIRED_SUB:'Your password has expired and must be changed before you can continue.',
    ACCT_UPDATE_FAILED:'Update failed.', ACCT_NETWORK_ERR:'Network error.',
    DOCS_TITLE_PREFIX:'Documents — ', DOCS_LOADING:'Loading…', DOCS_EMPTY:'No documents uploaded yet.',
    DOCS_DOWNLOAD:'↓ Download', DOCS_UPLOAD_LABEL:'Upload additional document', BTN_UPLOAD:'Upload',
    DOCS_PICK_FILE:'Please select a PDF file.', DOCS_UPLOADING:'Uploading…',
    DOCS_RESUBMITTED:'Uploaded and resubmitted for CERA review.', DOCS_UPLOADED:'Uploaded successfully.',
    DOCS_LOAD_FAILED:'Failed to load documents.', DOCS_NETWORK_ERR:'Network error.',
    DOCS_DOWNLOAD_FAILED:'Download failed — please try again.', DOCS_DOWNLOAD_ERR:'Download error: ',
    OTP_TITLE:'Verify your identity', OTP_SUB:'A 6-digit code was sent to your email address. Enter it below to continue.',
    OTP_LBL:'Verification code', OTP_BTN:'Verify', OTP_INVALID:'Invalid or expired code — please try again.',
    OTP_RESEND:'Resend code', OTP_RESEND_WAIT:'Resend in {s}s', OTP_RESEND_SENT:'Code resent — check your email.',
  },
  el: {
    LOGIN_TITLE:'Εργαλείο Σύγκρισης Τιμών Προμηθευτών - Πύλη Σύνδεσης Προμηθευτή',
    LOGIN_SUB:'Σύνδεση με στον λογαριασμό Προμηθευτή Ηλ. Ενέργειας',
    LOGIN_EMAIL:'Ηλ. ταχυδρομίο', LOGIN_PASSWORD:'Κωδικός',
    LOGIN_BTN:'Σύνδεση', LOGIN_SIGNING_IN:'Σύνδεση…',
    LOGIN_FORGOT:'Ξεχάσατε τον κωδικό;',
    FORGOT_TITLE:'Επαναφορά κωδικού',
    FORGOT_SUB:'Εισάγετε το email σας για να λάβετε σύνδεσμο επαναφοράς.',
    FORGOT_BTN:'Αποστολή συνδέσμου',
    FORGOT_SENDING:'Αποστολή…',
    FORGOT_BACK:'← Επιστροφή στη σύνδεση',
    FORGOT_OK:'Αν το email είναι εγγεγραμμένο, έχει απσταλεί σύνδεσμος επαναφοράς. Ελέγξτε τα εισερχόμενα σας.',
    FORGOT_ERR:'Σφάλμα δικτύου — παρακαλώ δοκιμάστε ξανά.',
    IDLE_TITLE:'Είστε ακόμα εκεί;', IDLE_SUB:'Δεν έχετε δραστηριότητα για λίγη ώρα. Για λόγους ασφαλείας, θα αποσυνδεθείτε σύντομα.', IDLE_STAY:'Παραμονή συνδεδεμένος',
    TOPBAR_TITLE:'ΡΑΕΚ - Πύλη Προμηθευτών Ηλεκτρικής Ενέργειας',
    BTN_MY_ACCOUNT:'Ο λογαριασμός μου',
    BTN_SIGN_OUT:'Αποσύνδεση', LBL_SUPPLIER_TAG:'Προμηθευτής',
    INFO_WORKFLOW_TITLE:'Διαδικασία υποβολής:',
    INFO_WORKFLOW_BODY:'Νέες διατιμήσεις και τροποποιήσεις υποβάλλονται ως <em>Σε αναμονή έγκρισης</em> και δημοσιεύονται μόνο μετά από έγκριση από την ΡΑΕΚ. Η επεξεργασία εγκεκριμένης διατίμησης το αποδημοσιεύει μέχρι νέας έγκρισης.',
    LBL_LIVE:'Ενεργές', LBL_PENDING_REVIEW:'Σε αναμονή',
    LBL_REJECTED:'Απορρίφθηκαν', LBL_DRAFT:'Πρόχειρες',
    CARD_MESSAGES:'Ειδοποιήσεις', MSG_NO_MESSAGES:'Δεν υπάρχουν ειδοποιήσεις.',
    BTN_ACK:'Επιβεβαίωση ενημέρωσης', MSG_ACKED_SECTION:'Επιβεβαιωμένες',
    CARD_MY_TARIFFS:'Διαθέσιμες διατιμήσεις',
    BTN_SUBMIT_NEW:'+ Υποβολή νέας Διατίμησης',
    TH_NAME:'Όνομα', TH_CONTRACT:'Σύμβαση', TH_VOLTAGE:'Τάση',
    TH_PRICING:'Τύπος διατίμησης', TH_STATUS:'Κατάσταση', TH_ACTIONS:'Ενέργειες',
    EMPTY_TARIFFS:'Δεν υπάρχουν διατιμήσεις ακόμη. Υποβάλετε την πρώτη σας διατίμηση για να ξεκινήσετε.',
    STATUS_LIVE:'● Ενεργή', STATUS_PENDING:'⏳ Σε αναμονή έγκρισης',
    STATUS_REJECTED:'✕ Απορρίφθηκε', STATUS_DRAFT:'◌ Πρόχειρη',
    STATUS_SUSPENDED:'● Ανενεργή', STATUS_ARCHIVED:'▣ Αρχειοθετημένη',
    BTN_DOCS:'📎 Έγγραφα', BTN_EDIT:'Επεξεργασία', BTN_DELETE:'Διαγραφή',
    EDIT_NOTE:'Η επεξεργασία θα αποδημοσιεύσει την διατίμηση μέχρι νέας έγκρισης',
    FORM_TITLE_NEW:'Υποβολή νέας διατίμησης',
    FORM_TITLE_EDIT:'Επεξεργασία διατίμησης',
    BTN_CLOSE:'✕ Κλείσιμο',
    BTN_SUBMIT:'Υποβολή για έγκριση',
    BTN_SAVE_RESUBMIT_REVIEW:'Αποθήκευση & επανυποβολή για έγκριση',
    BTN_SAVE_RESUBMIT:'Αποθήκευση & επανυποβολή',
    BTN_SUBMITTING:'Υποβολή…', BTN_CANCEL:'Ακύρωση',
    LBL_TARIFF_NAME:'Όνομα διατίμησης', LBL_CONTRACT_TYPE:'Τύπος σύμβασης',
    OPT_DOMESTIC:'Οικιακή', OPT_COMMERCIAL:'Εμπορική', OPT_INDUSTRIAL:'Βιομηχανική',
    LBL_VOLTAGE:'Επίπεδο τάσης',
    OPT_LV:'ΧΤ — Χαμηλή Τάση', OPT_MV:'ΜΤ — Μέση Τάση', OPT_HV:'ΥΤ — Υψηλή Τάση',
    LBL_PRICING_TYPE:'Τύπος διατίμησης',
    OPT_FIXED:'Σταθερή', OPT_TOU:'Χρονοζωνική (Time of Use / ToU)', OPT_DYNAMIC:'Δυναμική (Βάσει ΠΗΑ)', OPT_VARIABLE:'Κλιμακωτή (τμηματική)',
    LBL_LOAD_ENT:'Εγκατεστημένη ισχύς',
    OPT_LE_ANY:'Οποιαδήποτε (<70kVA και >70kVA)', OPT_LE_LT70:'< 70 kVA', OPT_LE_GT70:'> 70 kVA',
    HINT_LE:'Για Εμπορικούς/Βιομηχανικούς πελάτες σε συνδέσεις ΧΤ ή ΜΤ.',
    SEC_CONTRACT_DURATION:'Διάρκεια σύμβασης', LBL_DURATION_TYPE:'Τύπος διάρκειας',
    OPT_INDEFINITE:'Αορίστου χρόνου (χωρίς ελάχιστη περίοδο)',
    OPT_FIXED_TERM:'Ορισμένου χρόνου — καθορίστε μήνες',
    LBL_DURATION_MONTHS:'Ελάχιστη διάρκεια (μήνες)',
    SEC_STANDING:'Πάγιο τέλος', LBL_STANDING:'Μηνιαίο πάγιο τέλος (€)',
    LBL_MDM:'Διαχείριση Δεδομένων Μέτρησης (€/μήνα)',
    SEC_FPA:'Ρήτρα Καυσίμου', LBL_FPA_SOURCE:'Πηγή ρήτρας καυσίμου',
    OPT_FPA_GLOBAL:'Χρήση ρήτρας Δεσπόζων Συμμετέχοντα (από καρτέλα ΡΑΕΚ)',
    OPT_FPA_CUSTOM:'Εισαγωγή προσαρμοσμένης ρήτρας για αυτή τη Διατίμηση',
    OPT_FPA_NONE:'Χωρίς ρήτρα καυσίμου για αυτό τη διατίμηση',
    LBL_FPA_CUSTOM_RATE:'Ρήτρα καυσίμου (€/kWh)',
    SEC_SPECIAL:'Ειδικές κατηγορίες',
    LBL_VULNERABLE:'Ευάλωτος καταναλωτής / κοινωνικό τιμολόγιο — εμφανίζεται μόνο σε δικαιούχους',
    LBL_PROFILE:'Εκχωρημένο προφίλ φορτίου',
    OPT_PROFILE_NONE:'— Κανένα (εφεδρική μέθοδος) —',
    HINT_PROFILE:'Απαιτείται για ακριβείς υπολογισμούς κόστους ToU και δυναμικών τιμολογίων.',
    SEC_DISCOUNTS:'Εκπτώσεις & προσφορές',
    HINT_DISCOUNTS:'Προσθέστε εκπτώσεις που οι πελάτες μπορούν να ενεργοποιήσουν/απενεργοποιήσουν.',
    LBL_STANDING_DISCOUNTS:'Εκπτώσεις στο πάγιο τέλος',
    LBL_ENERGY_DISCOUNTS:'Εκπτώσεις στην ενέργεια', BTN_ADD_DISCOUNT:'+ Προσθήκη',
    SEC_FIXED:'Σταθερή χρέωση', LBL_UNIT_RATE:'Χρέωση μονάδας (€/kWh)',
    SEC_SEASON:'Όρια εποχών',
    LBL_HI_START:'Έναρξη εποχής αιχμής (μήνας 1–12)',
    LBL_HI_END:'Λήξη εποχής αιχμής (συμπεριλαμβανομένου)',
    SEC_PEAK:'Ώρες αιχμής', LBL_HI_SEASON:'Εποχή αιχμής', LBL_LO_SEASON:'Εποχή εκτός αιχμής',
    LBL_PEAK_START:'Έναρξη ώρας αιχμής (ώρα)',
    LBL_PEAK_END:'Λήξη ώρας αιχμής (ώρα, αποκλειστικά)',
    SEC_RATES:'Χρεώσεις (€/kWh)', LBL_PEAK_RATE:'Χρέωση αιχμής', LBL_OFF_PEAK_RATE:'Χρέωση εκτός αιχμής',
    SEC_DAM:'Παράμετροι ΠΗΑ τιμολόγησης',
    LBL_MULT:'Πολλαπλασιαστής (×)', HINT_MULT:'π.χ. 1.15 = +15%',
    LBL_ADDER:'Προσαύξηση (€/kWh)', HINT_ADDER:'Σταθερο περιθώριο προμηθευτή',
    LBL_DAM_FLOOR:'Ελάχιστη τιμή ΠΗΑ (€/kWh)', LBL_OPTIONAL:'προαιρετικό',
    HINT_DAM_FLOOR:'Κατώτατη τιμή. Αφήστε κενό για καμία.',
    HINT_DAM_FORMULA:'Διατίμηση = (MAX(DAM, ελάχ.) × πολλαπλασιαστής) + προσαύξηση',
    SEC_TIERED:'Κλιμακωτή διατίμηση', LBL_BILLING_RESET:'Περίοδος επαναφοράς χρέωσης',
    OPT_MONTHLY:'Μηνιαία (επαναφορά κάθε μήνα)',
    OPT_BIMONTHLY:'Διμηνιαία (επαναφορά κάθε 2 μήνες)',
    OPT_QUARTERLY:'Τριμηνιαία (επαναφορά κάθε 3 μήνες)',
    LBL_RATE_TIERS:'Κλίμακες χρέωσης', BTN_ADD_TIER:'+ Προσθήκη κλίμακας',
    HINT_TIERS:'Εισάγετε κλίμακες κατά σειρά. Η τελευταία δεν έχει άνω όριο (∞).',
    LBL_SUPPORT_DOC:'Υποστηρικτικό έγγραφο', LBL_OPTIONAL_SUFFIX:'(προαιρετικό)',
    HINT_DOC:'Πρέπει να υποβληθεί σχετική δημοσιευμένη τεκμηρίωση για επαλήθευση. Μόνο PDF, έως 10 MB.',
    TIER_LBL:'Κλίμακα', TIER_UP_TO:'έως', TIER_KWH:'kWh', TIER_RATE:'χρέωση', TIER_RATE_UNIT:'€/kWh', TIER_FIXED:'πάγιο', TIER_FIXED_UNIT:'€/περίοδο',
    ERR_TIER_NEEDED:'Η κλιμακωτή διατίμηση χρειάζεται τουλάχιστον μία κλίμακα.',
    ERR_NAME_REQUIRED:'Παρακαλώ δώστε το όνομα της διατίμησης.',
    ERR_ONE_TIER:'Απαιτείται τουλάχιστον μία κλίμακα.',
    ERR_ENTER_EMAIL_PW:'Εισάγετε το email και τον κωδικό σας.',
    ERR_SESSION_EXPIRED:'Η συνεδρία έληξε — παρακαλώ συνδεθείτε ξανά.',
    ERR_SESSION_EXPIRED_SHORT:'Η συνεδρία έληξε.',
    ERR_LOGIN_FAILED:'Η σύνδεση απέτυχε.',
    ERR_SUPPLIER_ONLY:'Λανθασμένο email ή κωδικός πρόσβασης.',
    ERR_NETWORK:'Σφάλμα δικτύου — εκτελείται ο διακομιστής;',
    ERR_DELETE_FAILED:'Η διαγραφή απέτυχε.',
    MSG_TARIFF_UPDATED:'Η διατίμηση ενημερώθηκε και επανυποβλήθηκε για έγκριση.',
    MSG_TARIFF_SUBMITTED:'Η διατίμηση υποβλήθηκε για έγκριση από ΡΑΕΚ.',
    MSG_DOC_UPLOAD_FAILED:'Η φόρτωση εγγράφου απέτυχε: ',
    CONFIRM_DELETE:'Διαγραφή "{name}";\n\nΑυτή η ενέργεια δεν μπορεί να αναιρεθεί.',
    CONFIRM_ARCHIVE:'Αφαίρεση "{name}" από τη δημόσια σύγκριση;\n\nΈχει δημοσιευθεί στο παρελθόν, οπότε θα παραμείνει στη λίστα σας ως Αρχειοθετημένη (μόνο για ανάγνωση) και μπορεί να επαναφερθεί μόνο από τη ΡΑΕΚ.',
    PH_DISC_CONDITIONS:'Προϋποθέσεις, π.χ. πάγια εντολή', PH_DISC_PCT:'% έκπτωση', PH_DISC_MONTHS:'Μήνες (κενό = μόνιμη)',
    ERR_VALIDATION:'Παρακαλώ διορθώστε τα ακόλουθα:',
    ERR_FIELDS_SUMMARY:'Παρακαλώ διορθώστε τα επισημασμένα πεδία ({N}).',
    ERR_F_REQUIRED:'Παρακαλώ συμπληρώστε τιμή.', ERR_F_MIN:'Η τιμή δεν μπορεί να είναι μικρότερη από {N}.',
    ERR_F_ABOVE:'Η τιμή πρέπει να είναι μεγαλύτερη από {N}.', ERR_F_MAX:'Η τιμή δεν μπορεί να είναι μεγαλύτερη από {N}.',
    ERR_F_WHOLE:'Παρακαλώ εισάγετε ακέραιο αριθμό.', ERR_F_TOO_LONG:'Πολύ μεγάλο κείμενο: έως {N} χαρακτήρες.',
    ERR_F_TIER_ORDER:'Το όριο κάθε κλίμακας πρέπει να είναι μεγαλύτερο από το προηγούμενο.',
    ERR_F_TIER_OPEN:'Μόνο η τελευταία κλίμακα μπορεί να μείνει χωρίς όριο (∞).',
    ERR_F_DISC_PCT:'Εισάγετε ποσοστό (πάνω από 0, έως 100) ή αφαιρέστε αυτή την έκπτωση.',
    CONFIRM_DISCARD:'Έχετε μη αποθηκευμένες αλλαγές σε αυτή τη διατίμηση.\n\nΝα απορριφθούν;',
    CONFIRM_DISCARD_SIGNOUT:'Έχετε μη αποθηκευμένες αλλαγές σε διατίμηση.\n\nΑποσύνδεση και απόρριψη των αλλαγών;',
    ACCT_ERR_EMAIL_PW:'Παρακαλώ εισάγετε τον υφιστάμενο κωδικό σας για να αλλάξετε το email.',
    ACCT_TITLE:'Ο λογαριασμός μου',
    ACCT_EMAIL_SECTION:'Αλλαγή email', ACCT_CURRENT_EMAIL:'Τρέχον email', ACCT_NEW_EMAIL:'Νέο email',
    BTN_UPDATE_EMAIL:'Ενημέρωση email',
    ACCT_PW_SECTION:'Αλλαγή κωδικού', ACCT_CUR_PW:'Υφιστάμενος κωδικός',
    ACCT_NEW_PW:'Νέος κωδικός', ACCT_CONFIRM_PW:'Επιβεβαίωση νέου κωδικού',
    BTN_UPDATE_PW:'Ενημέρωση κωδικού',
    ACCT_ERR_NEW_EMAIL:'Παρακαλώ εισάγετε νέο email.',
    ACCT_EMAIL_OK:'Το email ενημερώθηκε με επιτυχία.',
    ACCT_PW_FILL:'Παρακαλώ συμπληρώστε όλα τα πεδία.',
    ACCT_PW_MISMATCH:'Οι νέοι κωδικοί δεν ταιριάζουν.',
    ACCT_PW_SHORT:'Ο νέος κωδικός πρέπει να έχει τουλάχιστον 8 χαρακτήρες.',
    ACCT_PW_OK:'Ο κωδικός ενημερώθηκε με επιτυχία.',
    ACCT_PW_WEAK:'Ο κωδικός πρέπει να έχει τουλάχιστον 8 χαρακτήρες και να περιλαμβάνει γράμμα, αριθμό και σύμβολο.',
    PW_EXPIRED_TITLE:'Απαιτείται αλλαγή κωδικού',
    PW_EXPIRED_SUB:'Ο κωδικός σας έχει λήξει και πρέπει να αλλαχθεί για να συνεχίσετε.',
    ACCT_UPDATE_FAILED:'Η ενημέρωση απέτυχε.', ACCT_NETWORK_ERR:'Σφάλμα δικτύου.',
    DOCS_TITLE_PREFIX:'Έγγραφα — ', DOCS_LOADING:'Φόρτωση…',
    DOCS_EMPTY:'Δεν έχουν φορτωθεί έγγραφα ακόμη.',
    DOCS_DOWNLOAD:'↓ Λήψη', DOCS_UPLOAD_LABEL:'Φόρτωση επιπλέον εγγράφου',
    BTN_UPLOAD:'Φόρτωση',
    DOCS_PICK_FILE:'Παρακαλώ επιλέξτε αρχείο PDF.',
    DOCS_UPLOADING:'Φόρτωση…',
    DOCS_RESUBMITTED:'Φορτώθηκε και επανυποβλήθηκε για έγκριση ΡΑΕΚ.',
    DOCS_UPLOADED:'Φορτώθηκε με επιτυχία.',
    DOCS_LOAD_FAILED:'Αποτυχία φόρτωσης εγγράφων.',
    DOCS_NETWORK_ERR:'Σφάλμα δικτύου.',
    DOCS_DOWNLOAD_FAILED:'Αποτυχία λήψης — παρακαλώ δοκιμάστε ξανά.',
    DOCS_DOWNLOAD_ERR:'Σφάλμα λήψης: ',
    OTP_TITLE:'Επαλήθευση ταυτότητας', OTP_SUB:'Ένας 6ψήφιος κωδικός στάλθηκε στη διεύθυνση email σας. Εισάγετέ τον παρακάτω για να συνεχίσετε.',
    OTP_LBL:'Κωδικός επαλήθευσης', OTP_BTN:'Επαλήθευση', OTP_INVALID:'Μη έγκυρος ή ληγμένος κωδικός — παρακαλώ δοκιμάστε ξανά.',
    OTP_RESEND:'Επαναποστολή κωδικού', OTP_RESEND_WAIT:'Επαναποστολή σε {s}δ', OTP_RESEND_SENT:'Ο κωδικός εστάλη ξανά — ελέγξτε το email σας.',
  }
};

let _lang = localStorage.getItem('cera_sup_lang') || 'en';
function T(k){ return (LANG[_lang]&&LANG[_lang][k]) || LANG.en[k] || k; }
function setLang(l){
  _lang = l;
  localStorage.setItem('cera_sup_lang', l);
  renderPage();
}
function renderPage(){
  document.getElementById('html-root').lang = _lang;
  document.title = T('TOPBAR_TITLE');
  document.querySelectorAll('[data-t]').forEach(el => { el.textContent = T(el.dataset.t); });
  document.querySelectorAll('[data-th]').forEach(el => { el.innerHTML = T(el.dataset.th); });
  document.querySelectorAll('.btn-lang,.btn-lang-login').forEach(b => {
    b.classList.toggle('active', b.dataset.lang === _lang);
  });
  // Update first profile option
  const profSel = document.getElementById('edit-profile');
  if(profSel && profSel.options[0] && profSel.options[0].value === '') profSel.options[0].textContent = T('OPT_PROFILE_NONE');
  // Re-render tariff rows so buttons/badges update
  if(typeof renderTariffs === 'function') renderTariffs();
}

// ── Auth ──────────────────────────────────────────────────────────────────────
const _base = window.location.protocol === 'file:' ? 'http://localhost:8000' : '';

// Session lives in an httpOnly cookie (set by the server) — the browser
// attaches it to same-origin fetches automatically, so there is no token
// for JS to read or send explicitly. _sessionActive just tracks whether
// the last known API call succeeded, for UI state (idle timer).
let _sessionActive = false;

function authHeaders(){
  return {'Content-Type':'application/json'};
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
    // per-tab. If a supplier logs into a second tab as an admin (or vice
    // versa), that overwrites the cookie everywhere, including this
    // already-open supplier tab — and its next API call silently starts
    // acting as the new identity. Because admin sessions are allowed
    // everywhere, that direction produces no error at all — just quietly
    // wider data — so this can't be caught by checking status codes; it needs
    // X-User-Role (set server-side on every response) compared against what
    // this tab expects.
    const actualRole=resp.headers.get('X-User-Role');
    if(actualRole && actualRole!=='supplier' && sessionStorage.getItem('cera_sup_role')==='supplier'){
      _localSignOut('Your session was terminated — please sign in again.');
    }
    if(resp.status===403){
      try{
        const data=await resp.clone().json();
        if(data&&data.detail==='password_expired') _showPasswordExpiredModal();
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
  if(!cur||!np||!conf){msg.textContent=T('ACCT_PW_FILL');return;}
  if(np!==conf){msg.textContent=T('ACCT_PW_MISMATCH');return;}
  if(!_isStrongPassword(np)){msg.textContent=T('ACCT_PW_WEAK');return;}
  try{
    const resp=await fetch(_base+'/api/auth/password',{
      method:'PUT',headers:authHeaders(),
      body:JSON.stringify({current_password:cur,new_password:np})
    });
    const data=await resp.json().catch(()=>({}));
    if(resp.ok){
      document.getElementById('pwx-cur-pw').value='';
      document.getElementById('pwx-new-pw').value='';
      document.getElementById('pwx-confirm-pw').value='';
      _hidePasswordExpiredModal();
    }else{
      msg.textContent=data.detail||'Update failed.';
    }
  }catch(e){msg.textContent='Network error.';}
}

function showForgotForm(){
  document.getElementById('login-form-inner').style.display = 'none';
  document.getElementById('forgot-panel').style.display = 'block';
  document.getElementById('forgot-email').value = '';
  document.getElementById('forgot-status').textContent = '';
  document.getElementById('forgot-status').style.color = '';
}
function hideForgotForm(){
  document.getElementById('forgot-panel').style.display = 'none';
  document.getElementById('login-form-inner').style.display = 'block';
}
async function doForgot(){
  const email = document.getElementById('forgot-email').value.trim();
  if(!email) return;
  const btn = document.getElementById('forgot-btn');
  const st  = document.getElementById('forgot-status');
  btn.disabled = true; btn.textContent = T('FORGOT_SENDING');
  st.textContent = ''; st.style.color = '';
  try{
    await fetch(_base + '/api/auth/forgot-password', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({email})
    });
    st.textContent = T('FORGOT_OK');
    st.style.color = 'var(--green)';
  }catch(e){
    st.textContent = T('FORGOT_ERR');
    st.style.color = 'var(--red)';
  }
  btn.disabled = false; btn.textContent = T('FORGOT_BTN');
}
let _pendingOtpToken = '';
let _pendingOtpEmail = '';
let _otpResendInterval = null;

function _startOtpResendCountdown(){
  const link  = document.getElementById('otp-resend-link');
  const timer = document.getElementById('otp-resend-timer');
  link.style.display = 'none'; timer.style.display = 'inline';
  if(_otpResendInterval) clearInterval(_otpResendInterval);
  let secs = 120;
  timer.textContent = T('OTP_RESEND_WAIT').replace('{s}', secs);
  _otpResendInterval = setInterval(() => {
    secs--;
    if(secs <= 0){
      clearInterval(_otpResendInterval); _otpResendInterval = null;
      timer.style.display = 'none';
      link.textContent = T('OTP_RESEND'); link.style.display = 'inline';
    } else {
      timer.textContent = T('OTP_RESEND_WAIT').replace('{s}', secs);
    }
  }, 1000);
}

function showLoginForm(){
  document.getElementById('login-form-inner').style.display = '';
  document.getElementById('otp-panel').style.display = 'none';
  hideForgotForm();
  document.getElementById('login-err').textContent = '';
  document.getElementById('otp-err').textContent = '';
  if(_otpResendInterval){ clearInterval(_otpResendInterval); _otpResendInterval = null; }
}

function showLogin(msg){
  document.getElementById('login-err').textContent = msg || '';
  document.getElementById('login-email').value = '';
  document.getElementById('login-password').value = '';
  showLoginForm();
  document.getElementById('app').style.display = 'none';
  document.getElementById('login-overlay').classList.remove('hidden');
  setTimeout(() => document.getElementById('login-email').focus(), 80);
  _clearIdleTimers();
}

function hideLogin(){
  document.getElementById('login-overlay').classList.add('hidden');
  _resetIdleTimer();
}

/* ── Idle auto sign-out (15 min, with a 60s warning) ── */
const IDLE_TIMEOUT_MS = 15*60*1000, IDLE_WARNING_LEAD_MS = 60*1000;
let _idleWarnTimer = null, _idleCountdownInterval = null, _idleWarningShown = false;

function _isLoggedIn(){
  return _sessionActive && document.getElementById('login-overlay').classList.contains('hidden');
}

function _clearIdleTimers(){
  clearTimeout(_idleWarnTimer); _idleWarnTimer = null;
  if(_idleCountdownInterval){ clearInterval(_idleCountdownInterval); _idleCountdownInterval = null; }
  _idleWarningShown = false;
  document.getElementById('idle-warning-overlay').style.display = 'none';
}

function _resetIdleTimer(){
  if(_idleWarningShown || !_isLoggedIn()) return;
  clearTimeout(_idleWarnTimer);
  _idleWarnTimer = setTimeout(_showIdleWarning, IDLE_TIMEOUT_MS - IDLE_WARNING_LEAD_MS);
}

function _showIdleWarning(){
  _idleWarningShown = true;
  let secs = IDLE_WARNING_LEAD_MS/1000;
  const overlay = document.getElementById('idle-warning-overlay');
  const countEl = document.getElementById('idle-warning-count');
  countEl.textContent = secs;
  overlay.style.display = 'flex';
  _idleCountdownInterval = setInterval(() => {
    secs--;
    countEl.textContent = secs;
    if(secs <= 0){
      clearInterval(_idleCountdownInterval); _idleCountdownInterval = null;
      _idleWarningShown = false;
      overlay.style.display = 'none';
      doLogout('You were signed out due to inactivity.');
    }
  }, 1000);
}

function _dismissIdleWarning(){
  if(_idleCountdownInterval){ clearInterval(_idleCountdownInterval); _idleCountdownInterval = null; }
  _idleWarningShown = false;
  document.getElementById('idle-warning-overlay').style.display = 'none';
  _resetIdleTimer();
}

['mousedown','keydown','scroll','touchstart'].forEach(evt => document.addEventListener(evt, _resetIdleTimer, {passive:true}));

async function doLogin(){
  const email    = document.getElementById('login-email').value.trim();
  const password = document.getElementById('login-password').value;
  const btn      = document.getElementById('login-btn');
  const errEl    = document.getElementById('login-err');
  errEl.textContent = '';
  if(!email || !password){ errEl.textContent = T('ERR_ENTER_EMAIL_PW'); return; }
  btn.disabled = true; btn.textContent = T('LOGIN_SIGNING_IN');
  try{
    const resp = await fetch(_base + '/api/auth/login', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({email, password})
    });
    const data = await resp.json().catch(() => ({}));
    if(!resp.ok){ errEl.textContent = data.detail || T('ERR_LOGIN_FAILED'); btn.disabled = false; btn.textContent = T('LOGIN_BTN'); return; }
    if(data.status === 'otp_required'){
      _pendingOtpToken = data.pending_token;
      _pendingOtpEmail = email;
      document.getElementById('login-form-inner').style.display = 'none';
      document.getElementById('otp-panel').style.display = '';
      document.getElementById('otp-code').value = '';
      document.getElementById('otp-err').textContent = '';
      _startOtpResendCountdown();
      setTimeout(() => document.getElementById('otp-code').focus(), 80);
      btn.disabled = false; btn.textContent = T('LOGIN_BTN');
      return;
    }
    if(data.role !== 'supplier'){
      errEl.textContent = T('ERR_SUPPLIER_ONLY'); btn.disabled = false; btn.textContent = T('LOGIN_BTN'); return;
    }
    sessionStorage.setItem('cera_sup_email',    data.email);
    sessionStorage.setItem('cera_sup_role',     data.role);
    sessionStorage.setItem('cera_sup_supplier', data.supplier || '');
    hideLogin();
    initApp(data);
  } catch(e){
    errEl.textContent = T('ERR_NETWORK');
  }
  btn.disabled = false; btn.textContent = T('LOGIN_BTN');
}

async function doVerifyOtp(){
  const code  = document.getElementById('otp-code').value.trim();
  const btn   = document.getElementById('otp-btn');
  const errEl = document.getElementById('otp-err');
  errEl.textContent = '';
  if(!code){ errEl.textContent = T('OTP_INVALID'); return; }
  btn.disabled = true; btn.textContent = '…';
  try{
    const resp = await fetch(_base + '/api/auth/verify-otp', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({pending_token: _pendingOtpToken, code})
    });
    const data = await resp.json().catch(() => ({}));
    if(!resp.ok){ errEl.textContent = data.detail || T('OTP_INVALID'); btn.disabled = false; btn.textContent = T('OTP_BTN'); return; }
    if(data.role !== 'supplier'){
      errEl.textContent = T('ERR_SUPPLIER_ONLY'); btn.disabled = false; btn.textContent = T('OTP_BTN'); return;
    }
    sessionStorage.setItem('cera_sup_email',    data.email);
    sessionStorage.setItem('cera_sup_role',     data.role);
    sessionStorage.setItem('cera_sup_supplier', data.supplier || '');
    hideLogin();
    initApp(data);
  } catch(e){
    errEl.textContent = T('ERR_NETWORK');
  }
  btn.disabled = false; btn.textContent = T('OTP_BTN');
}

async function doResendOtp(){
  const errEl = document.getElementById('otp-err');
  const link  = document.getElementById('otp-resend-link');
  errEl.textContent = ''; link.style.display = 'none';
  try{
    const resp = await fetch(_base + '/api/auth/resend-otp', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({pending_token: _pendingOtpToken})
    });
    const data = await resp.json().catch(() => ({}));
    if(!resp.ok){ errEl.textContent = data.detail || 'Failed to resend code.'; link.style.display = 'inline'; return; }
    errEl.style.color = 'var(--green, #2f6f4e)';
    errEl.textContent = T('OTP_RESEND_SENT');
    setTimeout(() => { errEl.textContent = ''; errEl.style.color = ''; }, 4000);
    _startOtpResendCountdown();
  } catch(e){
    errEl.textContent = T('ERR_NETWORK');
    link.style.display = 'inline';
  }
}

function doLogout(msg){
  // msg is set for automatic sign-outs (idle timeout, expired session), which can't wait for an answer
  if(!msg && _formUnsaved && !confirm(T('CONFIRM_DISCARD_SIGNOUT'))) return;
  _formUnsaved = false;
  fetch(_base + '/api/auth/logout', {method:'POST'}).catch(()=>{});
  _localSignOut(msg);
}

function _localSignOut(msg){
  _sessionActive = false;
  ['cera_sup_email','cera_sup_role','cera_sup_supplier'].forEach(k => sessionStorage.removeItem(k));
  showLogin(msg);
}

document.getElementById('login-password').addEventListener('keydown', e => { if(e.key==='Enter') doLogin(); });
document.getElementById('login-email').addEventListener('keydown',    e => { if(e.key==='Enter') document.getElementById('login-password').focus(); });

// ── State ──────────────────────────────────────────────────────────────────────
let tariffs  = [];
let profiles = [];
let supplierName = '';

// ── Render ─────────────────────────────────────────────────────────────────────
function statusBadge(status){
  const map = {
    approved: ['badge-live',     T('STATUS_LIVE')],
    pending:  ['badge-pending',  T('STATUS_PENDING')],
    rejected: ['badge-rejected', T('STATUS_REJECTED')],
    draft:    ['badge-draft',    T('STATUS_DRAFT')],
    suspended:['badge-suspended',T('STATUS_SUSPENDED')],
    archived: ['badge-archived', T('STATUS_ARCHIVED')],
  };
  const [cls, label] = map[status] || ['badge-draft', status];
  return `<span class="badge ${cls}">${label}</span>`;
}

function renderTariffs(){
  const tbody = document.getElementById('tariff-tbody');
  const empty = document.getElementById('tariff-empty');
  if(!tariffs.length){ tbody.innerHTML = ''; empty.textContent = T('EMPTY_TARIFFS'); empty.style.display = ''; return; }
  empty.style.display = 'none';

  let live=0, pending=0, rejected=0, draft=0;
  tariffs.forEach(t => {
    if(t.status==='approved') live++;
    else if(t.status==='pending') pending++;
    else if(t.status==='rejected') rejected++;
    else if(t.status!=='archived') draft++;
  });
  document.getElementById('cnt-live').textContent    = live;
  document.getElementById('cnt-pending').textContent = pending;
  document.getElementById('cnt-rejected').textContent = rejected;
  document.getElementById('cnt-draft').textContent   = draft;

  tbody.innerHTML = tariffs.map(t => {
    // Suppliers can edit anything except archived tariffs (edits go back to pending)
    const archived  = t.status === 'archived';
    const editNote  = t.status === 'approved' ? ` title="${T('EDIT_NOTE')}"` : '';
    return `<tr>
      <td><strong>${esc(t.name)}</strong></td>
      <td>${esc(t.contract||'')}</td>
      <td><span style="font-family:var(--mono);font-size:12px">${esc(t.voltage||'')}</span></td>
      <td>${esc(t.pricing||'')}</td>
      <td>${statusBadge(t.status||'draft')}${t.status==='rejected'&&t.rejectionReason?`<div style="font-size:11px;color:var(--red);margin-top:4px;max-width:220px">${esc(t.rejectionReason)}</div>`:''}</td>
      <td style="text-align:right;white-space:nowrap">
        <button class="btn btn-sm" data-id="${esc(t.id)}" data-action="openDocsModal">${T('BTN_DOCS')}</button>
        ${archived ? '' : `<button class="btn btn-sm" data-id="${esc(t.id)}"${editNote} data-action="editTariff" style="margin-left:6px">${T('BTN_EDIT')}</button>
        <button class="btn btn-sm btn-danger" data-id="${esc(t.id)}" data-name="${esc(t.name)}" data-action="deleteTariff" style="margin-left:6px">${T('BTN_DELETE')}</button>`}
      </td>
    </tr>`;
  }).join('');
}

function esc(s){ return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;'); }

// ── API calls ──────────────────────────────────────────────────────────────────
async function loadTariffs(){
  const resp = await fetch(_base + '/api/supplier/tariffs', {headers: authHeaders()});
  if(resp.status === 401){ _localSignOut(T('ERR_SESSION_EXPIRED')); return; }
  if(!resp.ok) throw new Error('HTTP ' + resp.status);
  _sessionActive = true;
  hideLogin();
  tariffs = await resp.json();
  renderTariffs();
}

async function loadProfiles(){
  const resp = await fetch(_base + '/api/supplier/profiles', {headers: authHeaders()});
  if(!resp.ok) return;
  profiles = await resp.json();
  const sel = document.getElementById('edit-profile');
  sel.innerHTML = `<option value="">${T('OPT_PROFILE_NONE')}</option>`;
  profiles.forEach(p => { const o = document.createElement('option'); o.value = p.id; o.textContent = p.name + (p.desc?' — '+p.desc:''); sel.appendChild(o); });
}

async function deleteTariff(id, name){
  // Published tariffs are archived server-side rather than removed.
  const t = tariffs.find(x => x.id === id);
  const willArchive = t && (t.everPublished || t.status === 'approved' || t.status === 'suspended');
  if(!confirm(T(willArchive ? 'CONFIRM_ARCHIVE' : 'CONFIRM_DELETE').replace('{name}',name))) return;
  const resp = await fetch(_base + '/api/supplier/tariffs/' + encodeURIComponent(id), {method:'DELETE', headers: authHeaders()});
  if(resp.status === 401){ _localSignOut(T('ERR_SESSION_EXPIRED_SHORT')); return; }
  if(!resp.ok){ alert(T('ERR_DELETE_FAILED')); return; }
  await loadTariffs();
}

// FastAPI returns validation errors (422) as a list of {loc, msg}; turn that
// into readable text instead of "[object Object]".
function apiErrorText(detail, fallback){
  if(Array.isArray(detail)){
    return T('ERR_VALIDATION') + ' ' + detail.map(d => {
      const loc = (d.loc || []).filter(x => x !== 'body').join(' › ');
      return (loc ? loc + ': ' : '') + String(d.msg || '').replace(/^Value error, /, '');
    }).join('; ');
  }
  return detail || fallback;
}

// ── Tariff form ────────────────────────────────────────────────────────────────
// Unsaved-changes guard for the tariff form: any real edit (typing, or
// adding/removing a discount or tier row) marks it; closing the form, signing
// out, or reloading/closing the tab then asks before discarding.
let _formUnsaved = false;
['input','change'].forEach(evt => document.addEventListener(evt, e => {
  // getClientRects: ignore a late "change" from a field whose form was already saved and hidden
  if(e.isTrusted && e.target instanceof Element && e.target.getClientRects().length
     && e.target.closest('#form-overlay')) _formUnsaved = true;
}, true));
document.addEventListener('click', e => {
  if(!e.isTrusted || !(e.target instanceof Element)) return;
  const b = e.target.closest('#form-overlay [data-action]');
  if(b && /^(addDiscount|addTierRow|removeTierRow|removeDiscountRow)$/.test(b.dataset.action)) _formUnsaved = true;
}, true);
window.addEventListener('beforeunload', e => { if(_formUnsaved){ e.preventDefault(); e.returnValue = ''; } });

function openForm(id){
  _formUnsaved = false;
  document.getElementById('form-overlay').classList.remove('hidden');
  document.getElementById('form-status').textContent = '';
  document.getElementById('form-status').className   = 'status-msg';
  _clearFieldErrors();

  if(id){
    const t = tariffs.find(x => x.id === id);
    if(!t) return;
    document.getElementById('form-title').textContent   = T('FORM_TITLE_EDIT');
    document.getElementById('submit-btn').textContent   = t.status==='approved' ? T('BTN_SAVE_RESUBMIT_REVIEW') : T('BTN_SAVE_RESUBMIT');
    populateForm(t);
  } else {
    document.getElementById('form-title').textContent   = T('FORM_TITLE_NEW');
    document.getElementById('submit-btn').textContent   = T('BTN_SUBMIT');
    resetForm();
  }
}

function closeForm(){
  if(_formUnsaved && !confirm(T('CONFIRM_DISCARD'))) return;
  _formUnsaved = false;
  document.getElementById('form-overlay').classList.add('hidden');
}

function resetForm(){
  document.getElementById('edit-id').value = '';
  document.getElementById('edit-name').value = '';
  document.getElementById('edit-contract').value = 'Domestic';
  document.getElementById('edit-voltage').value = 'LV';
  document.getElementById('edit-pricing').value = 'Fixed';
  document.getElementById('edit-duration-type').value = 'indefinite';
  document.getElementById('edit-duration-months').value = 12;
  document.getElementById('edit-standing').value = 5.50;
  document.getElementById('edit-mdm').value = 0;
  document.getElementById('edit-fpa-source').value = 'global';
  document.getElementById('edit-fpa-custom').value = 0;
  document.getElementById('edit-vulnerable').checked = false;
  document.getElementById('edit-profile').value = '';
  document.getElementById('fix-rate').value = 0.1650;
  document.getElementById('standing-discounts').innerHTML = '';
  document.getElementById('energy-discounts').innerHTML   = '';
  updatePricingFields();
  updateLoadEntitlementField();
  updateDurationType();
  updateFpaSource();
  document.getElementById('tier-rows').innerHTML = '';
  addTierRow();
  const fi = document.getElementById('edit-file');
  if(fi) fi.value = '';
}

function populateForm(t){
  const r = t.rates || {};
  document.getElementById('edit-id').value            = t.id;
  document.getElementById('edit-name').value          = t.name || '';
  document.getElementById('edit-contract').value      = t.contract || 'Domestic';
  document.getElementById('edit-voltage').value       = t.voltage || 'LV';
  document.getElementById('edit-pricing').value       = t.pricing || 'Fixed';
  document.getElementById('edit-standing').value      = t.standing ?? 0;
  document.getElementById('edit-mdm').value           = t.mdm || 0;
  document.getElementById('edit-fpa-source').value    = t.fpaSource || 'global';
  document.getElementById('edit-fpa-custom').value    = t.fpaCustom || 0;
  document.getElementById('edit-vulnerable').checked  = !!t.vulnerable;
  document.getElementById('edit-profile').value       = t.profileId || '';

  const hasDuration = t.durationMonths != null;
  document.getElementById('edit-duration-type').value = hasDuration ? 'fixed' : 'indefinite';
  if(hasDuration) document.getElementById('edit-duration-months').value = t.durationMonths;

  // Rates
  if(t.pricing === 'Fixed'){
    document.getElementById('fix-rate').value = r.rate || 0;
  } else if(t.pricing === 'ToU'){
    document.getElementById('tou-hi-start').value = r.hiStart || 6;
    document.getElementById('tou-hi-end').value   = r.hiEnd   || 9;
    document.getElementById('tou-hi-ps').value    = r.hiPeakStart || 8;
    document.getElementById('tou-hi-pe').value    = r.hiPeakEnd   || 23;
    document.getElementById('tou-lo-ps').value    = r.loPeakStart || 8;
    document.getElementById('tou-lo-pe').value    = r.loPeakEnd   || 23;
    document.getElementById('tou-hi-pr').value    = r.hiPeakRate  || 0;
    document.getElementById('tou-hi-or').value    = r.hiOffRate   || 0;
    document.getElementById('tou-lo-pr').value    = r.loPeakRate  || 0;
    document.getElementById('tou-lo-or').value    = r.loOffRate   || 0;
  } else if(t.pricing === 'Dynamic'){
    document.getElementById('var-mult').value      = r.mult     || 1.15;
    document.getElementById('var-adder').value     = r.adder    || 0.02;
    document.getElementById('var-dam-floor').value = r.damFloor || '';
  } else if(t.pricing === 'Variable'){
    document.getElementById('var-reset-months').value = r.resetMonths || 2;
    document.getElementById('tier-rows').innerHTML = '';
    (r.tiers || [{upTo:null, rate:0}]).forEach(tier => addTierRow(tier));
  }

  // Discounts
  document.getElementById('standing-discounts').innerHTML = '';
  document.getElementById('energy-discounts').innerHTML   = '';
  (t.discounts || []).forEach(d => addDiscountRow(d.type === 'standing' ? 'standing' : 'energy', d));

  updatePricingFields();
  updateLoadEntitlementField();
  updateDurationType();
  updateFpaSource();
}

function collectForm(){
  const pricing = sv('edit-pricing');
  let rates = {};
  if(pricing === 'Fixed'){
    rates = {rate: fv('fix-rate')};
  } else if(pricing === 'ToU'){
    rates = {
      hiStart: fv('tou-hi-start'), hiEnd: fv('tou-hi-end'),
      hiPeakStart: fv('tou-hi-ps'), hiPeakEnd: fv('tou-hi-pe'),
      loPeakStart: fv('tou-lo-ps'), loPeakEnd: fv('tou-lo-pe'),
      hiPeakRate: fv('tou-hi-pr'), hiOffRate: fv('tou-hi-or'),
      loPeakRate: fv('tou-lo-pr'), loOffRate: fv('tou-lo-or'),
    };
  } else if(pricing === 'Variable'){
    const tiers = getTiers();
    if(!tiers.length){ setFormStatus('err', T('ERR_TIER_NEEDED')); return null; }
    rates = {resetMonths: parseInt(document.getElementById('var-reset-months').value)||2, tiers};
  } else {
    const floorVal = parseFloat(document.getElementById('var-dam-floor').value);
    rates = {mult: fv('var-mult'), adder: fv('var-adder'), damFloor: isNaN(floorVal)||floorVal<=0 ? null : floorVal};
  }

  const name = sv('edit-name');
  if(!name){ setFormStatus('err', T('ERR_NAME_REQUIRED')); return null; }

  const contract = sv('edit-contract');
  const voltage  = sv('edit-voltage');
  const leApplies = (contract==='Commercial'||contract==='Industrial') && (voltage==='LV'||voltage==='MV');
  const durationType = sv('edit-duration-type');

  return {
    id:              sv('edit-id') || null,
    name,
    supplier:        supplierName,
    contract,
    voltage,
    pricing,
    standing:        fv('edit-standing'),
    mdm:             fv('edit-mdm'),
    rates,
    profileId:       sv('edit-profile') || null,
    fpaSource:       sv('edit-fpa-source'),
    fpaCustom:       sv('edit-fpa-source')==='custom' ? fv('edit-fpa-custom') : 0,
    durationMonths:  durationType==='fixed' ? fv('edit-duration-months') : null,
    loadEntitlement: leApplies ? (sv('edit-le') || 'any') : null,
    discounts:       getDiscounts(),
    vulnerable:      document.getElementById('edit-vulnerable').checked,
  };
}

// ── Field-level errors on the tariff form ─────────────────────────────────────
// Each problem is shown next to its own field (red outline + message), not only
// as one line by the submit button. The page checks first, using the server's
// limits (schemas.TariffIn); anything the server still refuses is mapped back
// to its field where possible (_showServerErrors).
const _MAX_RATE = 5;        // €/kWh — config.TARIFF_MAX_ENERGY_RATE default
const _MAX_MONTHLY = 1000;  // €/month — config.TARIFF_MAX_MONTHLY_CHARGE default
const _RATE_FIELDS = {rate:'fix-rate', hiStart:'tou-hi-start', hiEnd:'tou-hi-end', hiPeakStart:'tou-hi-ps',
  hiPeakEnd:'tou-hi-pe', loPeakStart:'tou-lo-ps', loPeakEnd:'tou-lo-pe', hiPeakRate:'tou-hi-pr',
  hiOffRate:'tou-hi-or', loPeakRate:'tou-lo-pr', loOffRate:'tou-lo-or', mult:'var-mult', adder:'var-adder',
  damFloor:'var-dam-floor', resetMonths:'var-reset-months'};
const _BODY_FIELDS = {name:'edit-name', standing:'edit-standing', mdm:'edit-mdm', fpaCustom:'edit-fpa-custom',
  durationMonths:'edit-duration-months', profileId:'edit-profile', loadEntitlement:'edit-le'};
const _TIER_FIELDS = {upTo:'.tier-upto', rate:'.tier-rate', fixedCharge:'.tier-fixed'};
const _DISC_FIELDS = {percentage:'.disc-pct', durationMonths:'.disc-months', conditions:'.disc-conditions'};

function _tn(key, n){ return T(key).replace('{N}', n); }

function _clearFieldErrors(){
  document.querySelectorAll('#form-overlay .field-invalid').forEach(el => { el.classList.remove('field-invalid'); el.removeAttribute('aria-invalid'); });
  document.querySelectorAll('#form-overlay .field-err-msg').forEach(el => el.remove());
}
// Mark one input (or the tier list) as wrong and put the message right under it.
function _fieldError(el, msg){
  if(!el || el.classList.contains('field-invalid')) return false;   // first problem per field wins
  el.classList.add('field-invalid');
  el.setAttribute('aria-invalid', 'true');
  const m = document.createElement('div');
  m.className = 'field-err-msg';
  m.textContent = msg;
  const host = el.closest('.field') || el.closest('.tier-row, .discount-row');
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

// Returns the number of problems found (0 = OK to send).
function _validateTariffForm(){
  _clearFieldErrors();
  const $ = id => document.getElementById(id);
  const RATE = {required:true, min:0, max:_MAX_RATE};
  const MONTHLY = {required:true, min:0, max:_MAX_MONTHLY};
  if(!sv('edit-name')) _fieldError($('edit-name'), T('ERR_NAME_REQUIRED'));
  else if(sv('edit-name').length > 200) _fieldError($('edit-name'), _tn('ERR_F_TOO_LONG', 200));
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
    if(!rows.length) _fieldError($('tier-rows'), T('ERR_TIER_NEEDED'));
    let prev = 0;
    rows.forEach((row, i) => {
      const upTo = row.querySelector('.tier-upto');
      const last = i === rows.length - 1;
      if(upTo.value.trim() === '' && !last) _fieldError(upTo, T('ERR_F_TIER_OPEN'));
      else if(!_checkNumber(upTo, {above:0, max:10000000}) && upTo.value.trim() !== ''){
        if(+upTo.value <= prev) _fieldError(upTo, T('ERR_F_TIER_ORDER'));
        prev = +upTo.value;
      }
      _checkNumber(row.querySelector('.tier-rate'), RATE);
      _checkNumber(row.querySelector('.tier-fixed'), {min:0, max:_MAX_MONTHLY});
    });
  }
  document.querySelectorAll('#form-overlay .discount-row').forEach(row => {
    const pct = row.querySelector('.disc-pct');
    const v = Number(pct.value);
    if(pct.value.trim() === '' || !(v > 0) || v > 100) _fieldError(pct, T('ERR_F_DISC_PCT'));
    _checkNumber(row.querySelector('.disc-months'), {whole:true, min:1, max:120});
  });
  return _showErrorSummary();
}

function _showErrorSummary(extra){
  const bad = document.querySelectorAll('#form-overlay .field-invalid');
  if(!bad.length && !extra) return 0;
  const parts = [];
  if(bad.length) parts.push(_tn('ERR_FIELDS_SUMMARY', bad.length));
  if(extra) parts.push(extra);
  setFormStatus('err', parts.join(' '));
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
// Map a 422 from the server onto the form's fields; anything unplaceable stays in the summary.
function _showServerErrors(detail){
  if(!Array.isArray(detail)) return false;
  _clearFieldErrors();
  const discRows = [...document.querySelectorAll('#form-overlay .discount-row')];
  const tierRows = [...document.querySelectorAll('#tier-rows .tier-row')];
  const unplaced = [];
  detail.forEach(d => {
    const loc = (d.loc || []).filter(x => x !== 'body');
    let el = null;
    if(loc.length === 1 && _BODY_FIELDS[loc[0]]) el = document.getElementById(_BODY_FIELDS[loc[0]]);
    else if(loc[0] === 'discounts' && discRows[loc[1]] && _DISC_FIELDS[loc[2]]) el = discRows[loc[1]].querySelector(_DISC_FIELDS[loc[2]]);
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
        else if(path[0] === 'tiers' || /tier/.test(msg)) rel = tierRows[tierRows.length - 1] ? tierRows[tierRows.length - 1].querySelector('.tier-upto') : null;
        if(rel) _fieldError(rel, _friendlyMsg(null, null, msg)); else unplaced.push(part);
      });
      return;
    }
    unplaced.push((loc.length ? loc.join(' › ') + ': ' : '') + _friendlyMsg(d.type, d.ctx, d.msg));
  });
  _showErrorSummary(unplaced.join('; '));
  return true;
}

async function submitForm(){
  if(_validateTariffForm()) return;
  const body = collectForm();
  if(!body) return;

  const btn = document.getElementById('submit-btn');
  btn.disabled = true; btn.textContent = T('BTN_SUBMITTING');
  setFormStatus('', '');

  try{
    const isEdit = !!body.id;
    const url    = _base + '/api/supplier/tariffs' + (isEdit ? '/'+encodeURIComponent(body.id) : '');
    const method = isEdit ? 'PUT' : 'POST';
    const resp   = await fetch(url, {method, headers: authHeaders(), body: JSON.stringify(body)});
    if(resp.status === 401){ _localSignOut(T('ERR_SESSION_EXPIRED_SHORT')); return; }
    const data   = await resp.json().catch(()=>({}));
    if(!resp.ok){
      if(!(resp.status === 422 && _showServerErrors(data.detail))) setFormStatus('err', apiErrorText(data.detail, 'Error: HTTP ' + resp.status));
      return;
    }

    if(isEdit){
      const idx = tariffs.findIndex(t => t.id === data.id);
      if(idx >= 0) tariffs[idx] = data; else tariffs.push(data);
    } else {
      tariffs.push(data);
    }

    // Upload supporting document if one was selected
    const fileInput = document.getElementById('edit-file');
    if(fileInput && fileInput.files.length > 0){
      const fd = new FormData();
      fd.append('file', fileInput.files[0]);
      const uploadResp = await fetch(_base + '/api/supplier/tariffs/' + encodeURIComponent(data.id) + '/documents', {
        method: 'POST',
        body: fd,
      });
      if(!uploadResp.ok){
        const ud = await uploadResp.json().catch(()=>({}));
        _formUnsaved = false; renderTariffs(); closeForm();
        setPageStatus('ok', (isEdit ? T('MSG_TARIFF_UPDATED') : T('MSG_TARIFF_SUBMITTED')) + ' ' + T('MSG_DOC_UPLOAD_FAILED') + (ud.detail || 'unknown error'));
        return;
      }
      fileInput.value = '';
    }

    _formUnsaved = false;
    renderTariffs();
    closeForm();
    setPageStatus('ok', isEdit ? T('MSG_TARIFF_UPDATED') : T('MSG_TARIFF_SUBMITTED'));
  } catch(e){
    setFormStatus('err', 'Network error: ' + e.message);
  } finally {
    btn.disabled = false;
    btn.textContent = document.getElementById('edit-id').value ? T('BTN_SAVE_RESUBMIT') : T('BTN_SUBMIT');
  }
}

// ── Form field helpers ────────────────────────────────────────────────────────
function sv(id){ return document.getElementById(id)?.value?.trim() || ''; }
function fv(id){ return parseFloat(document.getElementById(id)?.value) || 0; }

function setFormStatus(type, msg){
  const el = document.getElementById('form-status');
  el.textContent = msg;
  el.className = 'status-msg' + (type ? ' '+type : '');
}
function setPageStatus(type, msg){
  const el = document.getElementById('page-status');
  el.textContent = msg;
  el.className = 'status-msg' + (type ? ' '+type : '');
  if(msg) setTimeout(() => { el.textContent = ''; el.className = 'status-msg'; }, 4000);
}

function updatePricingFields(){
  const p = sv('edit-pricing');
  document.getElementById('fields-fixed').style.display    = p==='Fixed'    ? '' : 'none';
  document.getElementById('fields-tou').style.display      = p==='ToU'      ? '' : 'none';
  document.getElementById('fields-dynamic').style.display  = p==='Dynamic'  ? '' : 'none';
  document.getElementById('fields-variable').style.display = p==='Variable' ? '' : 'none';
}
function updateLoadEntitlementField(){
  const c = sv('edit-contract'), v = sv('edit-voltage');
  const show = (c==='Commercial'||c==='Industrial') && (v==='LV'||v==='MV');
  document.getElementById('le-field').style.display = show ? '' : 'none';
  const isDomestic = c === 'Domestic';
  document.getElementById('vulnerable-field').style.display = isDomestic ? '' : 'none';
  if(!isDomestic) document.getElementById('edit-vulnerable').checked = false;
}
function updateDurationType(){
  const fixed = sv('edit-duration-type') === 'fixed';
  document.getElementById('duration-months-field').style.display = fixed ? '' : 'none';
}
function updateFpaSource(){
  const s = sv('edit-fpa-source');
  document.getElementById('fpa-custom-field').style.display = s==='custom' ? '' : 'none';
}

// ── Tiers ─────────────────────────────────────────────────────────────────────
function addTierRow(existing){
  const container = document.getElementById('tier-rows');
  const idx = container.children.length;
  const row = document.createElement('div');
  row.className = 'tier-row';
  row.style.cssText = 'display:flex;gap:8px;align-items:center;flex-wrap:wrap;background:var(--bg3);border:1px solid var(--border);border-radius:2px;padding:8px 10px';
  const upToVal  = existing && existing.upTo  != null ? existing.upTo  : '';
  const rateVal  = existing ? existing.rate  : '';
  const fixedVal = existing && existing.fixedCharge != null ? existing.fixedCharge : '';
  const inp = `style="width:80px;padding:4px 6px;border:1px solid var(--border);border-radius:2px;background:var(--bg);color:var(--text);font-size:12px;font-family:var(--mono)"`;
  row.innerHTML =
    `<span style="font-size:11px;font-family:var(--mono);color:var(--text3);white-space:nowrap;min-width:50px">${T('TIER_LBL')} ${idx+1}</span>`+
    `<div style="display:flex;align-items:center;gap:4px"><span style="font-size:11px;color:var(--text3)">${T('TIER_UP_TO')}</span><input type="number" class="tier-upto" value="${esc(upToVal)}" placeholder="∞" min="1" step="1" ${inp}><span style="font-size:11px;color:var(--text3)">${T('TIER_KWH')}</span></div>`+
    `<div style="display:flex;align-items:center;gap:4px"><span style="font-size:11px;color:var(--text3)">${T('TIER_RATE')}</span><input type="number" class="tier-rate" value="${esc(rateVal)}" placeholder="€/kWh" min="0" step="0.0001" ${inp}><span style="font-size:11px;color:var(--text3)">${T('TIER_RATE_UNIT')}</span></div>`+
    `<div style="display:flex;align-items:center;gap:4px"><span style="font-size:11px;color:var(--text3)">${T('TIER_FIXED')}</span><input type="number" class="tier-fixed" value="${esc(fixedVal)}" placeholder="0.00" min="0" step="0.01" ${inp}><span style="font-size:11px;color:var(--text3)">${T('TIER_FIXED_UNIT')}</span></div>`+
    `<button data-action="removeTierRow" style="background:none;border:none;cursor:pointer;color:var(--red);font-size:14px;padding:2px 4px">✕</button>`;
  container.appendChild(row);
  updateTierLabels();
}
function removeTierRow(btn){
  const c = document.getElementById('tier-rows');
  if(c.children.length <= 1){ alert(T('ERR_ONE_TIER')); return; }
  btn.closest('.tier-row').remove();
  updateTierLabels();
}
function updateTierLabels(){
  document.querySelectorAll('#tier-rows .tier-row').forEach((row,i) => {
    const lbl = row.querySelector('span');
    if(lbl) lbl.textContent = T('TIER_LBL')+' '+(i+1);
  });
}
function getTiers(){
  const tiers = [];
  document.querySelectorAll('#tier-rows .tier-row').forEach(row => {
    const upTo = parseFloat(row.querySelector('.tier-upto').value);
    const rate  = parseFloat(row.querySelector('.tier-rate').value);
    const fixed = parseFloat(row.querySelector('.tier-fixed').value);
    tiers.push({upTo: isNaN(upTo)?null:upTo, rate: isNaN(rate)?0:rate, fixedCharge: isNaN(fixed)?null:fixed});
  });
  return tiers;
}

// ── Discounts ─────────────────────────────────────────────────────────────────
function addDiscount(type, existing){
  addDiscountRow(type, existing);
}
function addDiscountRow(type, existing){
  // Same shape as admin.html and the pricing engine:
  // {type, percentage, durationMonths (null = permanent), conditions}
  const container = document.getElementById(type+'-discounts');
  const row = document.createElement('div');
  row.className = 'discount-row';
  row.dataset.type = type;
  const condVal  = existing?.conditions || '';
  const pctVal   = existing?.percentage != null ? existing.percentage : '';
  const monthVal = existing?.durationMonths != null ? existing.durationMonths : '';
  const inputStyle = 'padding:5px 8px;border:1px solid var(--border);border-radius:2px;font-size:12px;background:var(--bg);color:var(--text);';
  row.innerHTML =
    `<input type="text"   class="disc-conditions" placeholder="${esc(T('PH_DISC_CONDITIONS'))}" value="${esc(condVal)}" maxlength="500" style="flex:1;min-width:100px;${inputStyle}">`+
    `<input type="number" class="disc-pct" placeholder="${esc(T('PH_DISC_PCT'))}" value="${esc(pctVal)}" step="0.01" min="0.01" max="100" style="width:80px;font-family:var(--mono);${inputStyle}">`+
    `<span style="font-size:11px;color:var(--text3)">%</span>`+
    `<input type="number" class="disc-months" placeholder="${esc(T('PH_DISC_MONTHS'))}" title="${esc(T('PH_DISC_MONTHS'))}" value="${esc(monthVal)}" step="1" min="1" max="120" style="width:110px;font-family:var(--mono);${inputStyle}">`+
    `<button data-action="removeDiscountRow" style="background:none;border:none;cursor:pointer;color:var(--red);font-size:14px;padding:2px 4px">✕</button>`;
  container.appendChild(row);
}
function getDiscounts(){
  const discounts = [];
  document.querySelectorAll('.discount-row').forEach(row => {
    const pct    = parseFloat(row.querySelector('.disc-pct').value);
    const months = parseInt(row.querySelector('.disc-months').value);
    if(!(pct > 0)) return;
    discounts.push({
      type: row.dataset.type,
      percentage: pct,
      durationMonths: months > 0 ? months : null,
      conditions: row.querySelector('.disc-conditions').value.trim(),
    });
  });
  return discounts;
}

// ── Init ──────────────────────────────────────────────────────────────────────
async function initApp(authData){
  supplierName = authData.supplier || '';
  document.getElementById('supplier-name-display').textContent = supplierName;
  document.getElementById('topbar-email').textContent = authData.email || '';
  document.getElementById('app').style.display = '';

  try{
    await Promise.all([loadTariffs(), loadProfiles(), loadMessages()]);
  } catch(e){
    setPageStatus('err', '⚠ Could not load data: ' + e.message);
  }
}

function _esc(s){
  const d = document.createElement('div');
  d.textContent = s ?? '';
  return d.innerHTML;
}

let _messages = [];

async function loadMessages(){
  try{
    const resp = await fetch(_base + '/api/supplier/messages', {headers: authHeaders()});
    if(!resp.ok) return;
    _messages = await resp.json();
    renderMessages();
  } catch(e){ /* non-critical — leave existing content */ }
}

function _updateUnreadBadge(){
  const badge = document.getElementById('messages-unread-badge');
  const unreadCount = _messages.filter(m => !m.read).length;
  badge.textContent = unreadCount;
  badge.style.display = unreadCount ? 'inline-block' : 'none';
}

function _renderMsgItem(m, acked){
  const date = new Date(m.createdAt).toLocaleString();
  const ackBtn = acked ? '' :
    `<div style="margin-top:10px;text-align:right"><button class="btn btn-primary btn-sm" data-action="ackMessage" data-arg="${esc(m.id)}">✓ ${T('BTN_ACK')}</button></div>`;
  return `<div class="msg-item ${m.read ? 'read' : 'unread'}">
    <div style="display:flex;align-items:center;gap:8px">
      <span class="msg-subject">${_esc(m.subject)}</span>
      <span style="font-size:10px;color:var(--text3);margin-left:auto;white-space:nowrap">${date}</span>
    </div>
    <div class="msg-body" style="font-size:13px;margin-top:8px;white-space:pre-wrap;color:var(--text)">${_esc(m.body)}</div>${ackBtn}
  </div>`;
}

function renderMessages(){
  const box = document.getElementById('messages-list');
  _updateUnreadBadge();
  if(!_messages.length){
    box.innerHTML = `<p class="hint" style="padding:20px" data-t="MSG_NO_MESSAGES">${T('MSG_NO_MESSAGES')}</p>`;
    return;
  }
  const active = _messages.filter(m => !m.acknowledged);
  const acked  = _messages.filter(m => m.acknowledged);
  let out = active.map(m => _renderMsgItem(m, false)).join('')
    || `<p class="hint" style="padding:20px">${T('MSG_NO_MESSAGES')}</p>`;
  if(acked.length){
    out += `<div style="padding:8px 20px;background:var(--bg3);border-top:1px solid var(--border);border-bottom:1px solid var(--border);font-size:11px;font-weight:600;color:var(--text3);letter-spacing:.04em;cursor:pointer" data-action="toggleAckedSection">
      ▸ ${T('MSG_ACKED_SECTION')} (${acked.length})</div>
      <div id="acked-messages" style="display:none;opacity:.7">${acked.map(m => _renderMsgItem(m, true)).join('')}</div>`;
  }
  box.innerHTML = out;
}

function _toggleAckedSection(hdr){
  const sec = document.getElementById('acked-messages');
  const open = sec.style.display !== 'none';
  sec.style.display = open ? 'none' : 'block';
  hdr.innerHTML = hdr.innerHTML.replace(open ? '▾' : '▸', open ? '▸' : '▾');
}

async function _ackMessage(id){
  try{
    const resp = await fetch(_base + '/api/supplier/messages/' + id + '/ack', {method:'POST', headers: authHeaders()});
    if(!resp.ok) return;
    const msg = _messages.find(m => m.id === id);
    if(msg){ msg.acknowledged = true; msg.read = true; }
    renderMessages();
  } catch(e){}
}

async function _markVisibleRead(){
  // All active messages are shown expanded, so opening the panel counts as reading them.
  // The bold "unread" styling stays for this viewing; next open renders them as read.
  const unread = _messages.filter(m => !m.read);
  for(const m of unread){
    try{
      await fetch(_base + '/api/supplier/messages/' + m.id + '/read', {method:'POST', headers: authHeaders()});
      m.read = true;
    } catch(e){}
  }
  _updateUnreadBadge();
}

function openMessagesModal(){
  renderMessages(); // fresh render — acknowledged section always starts collapsed
  document.getElementById('messages-overlay').style.display = 'flex';
  _markVisibleRead();
}

function closeMessagesModal(){
  document.getElementById('messages-overlay').style.display = 'none';
}

// The session lives in an httpOnly cookie we can't read from JS, so we can't
// synchronously know whether we're logged in. Optimistically call initApp();
// loadTariffs() shows/hides the login overlay depending on whether the
// cookie is still valid (401 vs 200).
async function boot(){
  renderPage();
  let email    = sessionStorage.getItem('cera_sup_email')    || '';
  let role     = sessionStorage.getItem('cera_sup_role')     || '';
  let supplier = sessionStorage.getItem('cera_sup_supplier') || '';
  // Admin accounts can authenticate via this portal's login form (same endpoint
  // as admin.html) but must never use it: the tariff endpoints only scope
  // results down to one supplier when the caller's role is 'supplier' (see
  // admin.py's is_supplier checks) — an admin has no supplier_name, so they'd
  // see every supplier's tariffs rendered inside what's meant to be a
  // single-supplier view. doLogin()/verify-otp() already reject non-supplier
  // roles at the form itself, but an admin's own cookie carried into a fresh
  // tab/reload never touches that form — it goes straight through here.
  // Treat it exactly like "not logged in" rather than silently accepting it.
  if(role && role !== 'supplier'){ _localSignOut('Your session was terminated — please sign in again.'); return; }
  // The httpOnly cookie may be valid even if this tab never ran doLogin() itself
  // (e.g. a fresh tab, or a reload) — sessionStorage would then be empty and the
  // topbar/Sign out UI would show a blank identity. Re-hydrate from /me in that case.
  if(!role){
    try{
      const meResp = await fetch(_base + '/api/auth/me', {headers: authHeaders()});
      if(meResp.ok){
        const me = await meResp.json();
        if(me.role !== 'supplier'){ _localSignOut('Your session was terminated — please sign in again.'); return; }
        email = me.email; role = me.role; supplier = me.supplier || '';
        sessionStorage.setItem('cera_sup_email',    email);
        sessionStorage.setItem('cera_sup_role',     role);
        sessionStorage.setItem('cera_sup_supplier', supplier);
      }
    }catch(e){}
  }
  initApp({email, role, supplier});
}
boot();

function openAccountModal(){
  const email = sessionStorage.getItem('cera_sup_email') || '';
  document.getElementById('acct-current-email').value = email;
  document.getElementById('acct-new-email').value = '';
  document.getElementById('acct-email-pw').value = '';
  document.getElementById('acct-cur-pw').value = '';
  document.getElementById('acct-new-pw').value = '';
  document.getElementById('acct-confirm-pw').value = '';
  document.getElementById('acct-email-msg').textContent = '';
  document.getElementById('acct-pw-msg').textContent = '';
  document.getElementById('acct-overlay').style.display = 'flex';
}
function closeAccountModal(){
  document.getElementById('acct-overlay').style.display = 'none';
}
function _acctMsg(id, text, ok){
  const el = document.getElementById(id);
  el.textContent = text;
  el.style.color = ok ? 'var(--green)' : 'var(--red)';
}
async function doUpdateEmail(){
  const newEmail = document.getElementById('acct-new-email').value.trim();
  const curPw = document.getElementById('acct-email-pw').value;
  if(!newEmail){ _acctMsg('acct-email-msg', T('ACCT_ERR_NEW_EMAIL'), false); return; }
  if(!curPw){ _acctMsg('acct-email-msg', T('ACCT_ERR_EMAIL_PW'), false); return; }
  try{
    const resp = await fetch(_base + '/api/auth/email', {
      method:'PUT', headers:{...authHeaders(),'Content-Type':'application/json'},
      body: JSON.stringify({new_email: newEmail, current_password: curPw})
    });
    const data = await resp.json().catch(()=>({}));
    if(resp.ok){
      sessionStorage.setItem('cera_sup_email', newEmail);
      document.getElementById('acct-current-email').value = newEmail;
      document.getElementById('topbar-email').textContent = newEmail;
      document.getElementById('acct-new-email').value = '';
      document.getElementById('acct-email-pw').value = '';
      _acctMsg('acct-email-msg', T('ACCT_EMAIL_OK'), true);
    } else {
      _acctMsg('acct-email-msg', apiErrorText(data.detail, T('ACCT_UPDATE_FAILED')), false);
    }
  }catch(e){ _acctMsg('acct-email-msg', T('ACCT_NETWORK_ERR'), false); }
}
async function doUpdatePassword(){
  const cur  = document.getElementById('acct-cur-pw').value;
  const np   = document.getElementById('acct-new-pw').value;
  const conf = document.getElementById('acct-confirm-pw').value;
  if(!cur || !np || !conf){ _acctMsg('acct-pw-msg', T('ACCT_PW_FILL'), false); return; }
  if(np !== conf){ _acctMsg('acct-pw-msg', T('ACCT_PW_MISMATCH'), false); return; }
  if(!_isStrongPassword(np)){ _acctMsg('acct-pw-msg', T('ACCT_PW_WEAK'), false); return; }
  try{
    const resp = await fetch(_base + '/api/auth/password', {
      method:'PUT', headers:{...authHeaders(),'Content-Type':'application/json'},
      body: JSON.stringify({current_password: cur, new_password: np})
    });
    const data = await resp.json().catch(()=>({}));
    if(resp.ok){
      document.getElementById('acct-cur-pw').value = '';
      document.getElementById('acct-new-pw').value = '';
      document.getElementById('acct-confirm-pw').value = '';
      _acctMsg('acct-pw-msg', T('ACCT_PW_OK'), true);
    } else {
      _acctMsg('acct-pw-msg', data.detail || T('ACCT_UPDATE_FAILED'), false);
    }
  }catch(e){ _acctMsg('acct-pw-msg', T('ACCT_NETWORK_ERR'), false); }
}

// ── Document download (authenticated) ────────────────────────────────────────
let _docsCache = {};
async function downloadDoc(docId){
  const filename = _docsCache[docId] || 'document.pdf';
  try{
    const resp = await fetch(_base+'/api/supplier/documents/'+docId+'/download', {headers: authHeaders()});
    if(!resp.ok){alert(T('DOCS_DOWNLOAD_FAILED'));return;}
    const blob = await resp.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = filename;
    document.body.appendChild(a); a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }catch(e){alert(T('DOCS_DOWNLOAD_ERR')+e.message);}
}

// ── Document history modal ────────────────────────────────────────────────────
let _docsTargetId = null;

function openDocsModal(tariffId){
  const tariffName = tariffs.find(t=>t.id===tariffId)?.name || '';
  _docsTargetId = tariffId;
  document.getElementById('docs-modal-title').textContent = T('DOCS_TITLE_PREFIX') + tariffName;
  document.getElementById('docs-modal-list').innerHTML = `<p style="color:var(--text3);font-size:13px">${T('DOCS_LOADING')}</p>`;
  document.getElementById('docs-modal-upload-msg').textContent = '';
  document.getElementById('docs-modal-file').value = '';
  document.getElementById('docs-modal-overlay').style.display = 'flex';
  loadDocsModal();
}

function closeDocsModal(){
  document.getElementById('docs-modal-overlay').style.display = 'none';
  _docsTargetId = null;
}

async function loadDocsModal(){
  const list = document.getElementById('docs-modal-list');
  try{
    const resp = await fetch(_base + '/api/supplier/tariffs/' + encodeURIComponent(_docsTargetId) + '/documents', {headers: authHeaders()});
    const docs = await resp.json();
    if(!docs.length){
      list.innerHTML = `<p style="color:var(--text3);font-size:13px">${T('DOCS_EMPTY')}</p>`;
      return;
    }
    docs.forEach(d=>{ _docsCache[d.id]=d.original_name; });
    list.innerHTML = docs.map(d => {
      const ts = new Date(d.uploaded_at).toLocaleString();
      return `<div style="display:flex;align-items:center;justify-content:space-between;padding:8px 0;border-bottom:1px solid var(--border)">
        <div>
          <div style="font-size:13px;font-weight:500">${esc(d.original_name)}</div>
          <div style="font-size:11px;color:var(--text3)">${ts}</div>
        </div>
        <a href="#" data-action="downloadDoc" data-arg="${d.id}" style="font-size:12px;color:var(--accent);text-decoration:none;font-weight:500">${T('DOCS_DOWNLOAD')}</a>
      </div>`;
    }).join('');
  }catch(e){
    list.innerHTML = `<p style="color:var(--red);font-size:13px">${T('DOCS_LOAD_FAILED')}</p>`;
  }
}

async function uploadDocModal(){
  const fi = document.getElementById('docs-modal-file');
  const msgEl = document.getElementById('docs-modal-upload-msg');
  msgEl.textContent = '';
  if(!fi.files.length){ msgEl.textContent = T('DOCS_PICK_FILE'); msgEl.style.color='var(--red)'; return; }
  const fd = new FormData();
  fd.append('file', fi.files[0]);
  msgEl.textContent = T('DOCS_UPLOADING'); msgEl.style.color='var(--text3)';
  try{
    const resp = await fetch(_base + '/api/supplier/tariffs/' + encodeURIComponent(_docsTargetId) + '/documents', {
      method: 'POST',
      body: fd,
    });
    const data = await resp.json().catch(()=>({}));
    if(resp.ok){
      fi.value = '';
      if(data.resubmitted){
        const t = tariffs.find(x => x.id === _docsTargetId);
        if(t){ t.status = 'pending'; t.rejectionReason = null; renderTariffs(); }
        msgEl.textContent = T('DOCS_RESUBMITTED'); msgEl.style.color='var(--green)';
      } else {
        msgEl.textContent = T('DOCS_UPLOADED'); msgEl.style.color='var(--green)';
      }
      loadDocsModal();
    } else {
      msgEl.textContent = data.detail || T('DOCS_LOAD_FAILED'); msgEl.style.color='var(--red)';
    }
  }catch(e){ msgEl.textContent = T('DOCS_NETWORK_ERR'); msgEl.style.color='var(--red)'; }
}

// ── Event wiring ────────────────────────────────────────────────────────────
// No inline event-handler attributes (onclick and the like): the page runs under
// a strict Content-Security-Policy that refuses any code written inside the page
// (main.py, _CSP_POLICY). Elements say what they do with data-action (click),
// data-change, data-input, data-enter (Enter key) or data-backdrop-close, plus
// data-arg; this table is the complete list of what they may call.
const _ACTIONS = {
  setLang: el => setLang(el.dataset.arg),
  doLogin: () => doLogin(),
  showForgotForm: () => showForgotForm(),
  hideForgotForm: () => hideForgotForm(),
  showLoginForm: () => showLoginForm(),
  doForgot: () => doForgot(),
  doVerifyOtp: () => doVerifyOtp(),
  doResendOtp: () => doResendOtp(),
  digitsOnly: el => { el.value = el.value.replace(/\D/g, ''); },
  dismissIdleWarning: () => _dismissIdleWarning(),
  doLogout: () => doLogout(),
  openForm: () => openForm(),
  editTariff: el => openForm(el.dataset.id),
  closeForm: () => closeForm(),
  submitForm: () => submitForm(),
  deleteTariff: el => deleteTariff(el.dataset.id, el.dataset.name),
  updateLoadEntitlementField: () => updateLoadEntitlementField(),
  updatePricingFields: () => updatePricingFields(),
  updateDurationType: () => updateDurationType(),
  updateFpaSource: () => updateFpaSource(),
  addDiscount: el => addDiscount(el.dataset.arg),
  removeDiscountRow: el => el.closest('.discount-row').remove(),
  addTierRow: () => addTierRow(),
  removeTierRow: el => removeTierRow(el),
  openMessagesModal: () => openMessagesModal(),
  closeMessagesModal: () => closeMessagesModal(),
  ackMessage: el => _ackMessage(el.dataset.arg),
  toggleAckedSection: el => _toggleAckedSection(el),
  openAccountModal: () => openAccountModal(),
  closeAccountModal: () => closeAccountModal(),
  doUpdateEmail: () => doUpdateEmail(),
  doUpdatePassword: () => doUpdatePassword(),
  doUpdatePasswordExpired: () => doUpdatePasswordExpired(),
  openDocsModal: el => openDocsModal(el.dataset.id),
  closeDocsModal: () => closeDocsModal(),
  uploadDocModal: () => uploadDocModal(),
  downloadDoc: el => downloadDoc(+el.dataset.arg),
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
// keys are ignored, except "-" in the few boxes where a negative value is valid (their
// min is below 0: custom FPA, Dynamic adder). Anything pasted is cleaned up the same way.
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

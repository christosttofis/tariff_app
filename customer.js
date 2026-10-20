const LANG = {
  en: {
    PAGE_EYEBROW: "Electricity cost calculator",
    PAGE_TITLE: "Compare electricity tariffs",
    PAGE_DESC: "Enter your consumption and see all available tariffs ranked cheapest first, with supplier contact details.",
    CARD_CONNECTION: "Your connection",
    TAB_DOMESTIC: "🏠 Domestic",
    TAB_CI: "🏢 Commercial / Industrial",
    LBL_VOLTAGE: "Voltage level",
    OPT_LV: "LV — Low Voltage",
    OPT_MV: "MV — Medium Voltage",
    OPT_HV: "HV — High Voltage",
    LBL_LOAD_ENT: "Load entitlement",
    LE_LT70: "< 70 kVA",
    LE_GT70: "> 70 kVA",
    LBL_PRICING: "Pricing type",
    OPT_ALL: "All types",
    OPT_FIXED: "Fixed only",
    OPT_TOU: "Time-of-use only",
    OPT_VARIABLE: "Dynamic only",
    OPT_VARIABLE_TIERED: "Variable (tiered) only",
    TAG_FIXED: "Fixed",
    TAG_TOU: "ToU",
    TAG_DYNAMIC: "Dynamic",
    TAG_VARIABLE: "Variable",
    TAG_LV: "LV",
    TAG_MV: "MV",
    TAG_HV: "HV",
    TAG_DOMESTIC: "Domestic",
    TAG_CI: "Commercial / Industrial",
    CARD_CONSUMPTION: "Your consumption",
    BTN_ANNUAL: "Annual",
    BTN_MONTHLY: "Monthly",
    BTN_BACK_TO_TOP: "Back to top",
    LBL_ANNUAL_KWH: "Annual consumption",
    UNIT_KWH_YEAR: "kWh / year",
    HINT_ANNUAL: "As per CERA's Power supply rules - Chapter 7.1.7 (a) all power suppliers are obliged to send to each consumer, at least once a year, their total consumption for the previous year, and the expected consumption for the current year.",
    RESULTS_SUB_ANNUAL: "cheapest supplier cost first · first 12 months after switching ({PERIOD}) · profile-distributed",
    RESULTS_SUB_MONTHLY: "cheapest bill first · {KWH} kWh per bill · first 12 months after switching ({PERIOD})",
    LAST_UPDATED: "Updated {DT}",
    LBL_STANDING: "/mo standing",
    LBL_NO_MIN: "No minimum period",
    LBL_MIN_MONTHS: "{N}-month-contract",
    LBL_INCL_DISC: "Price incl. promotional discounts. Expand to review conditions.",
    LBL_OFFER_ENDS: "Includes a {N}-month offer. After it ends: about €{X} / month (supplier charges).",
    LBL_SUP_YEAR: "/ year",
    LBL_SUP_MONTH: "/ month",
    LBL_SUP_2MO: "/ 2 months",
    BILLING_CYCLE: "Billing cycle",
    BILLING_M1: "Monthly",
    BILLING_M2: "Bi-monthly",
    MONTHLY_UNIT_1: "kWh / month",
    MONTHLY_UNIT_2: "kWh / 2 months",
    MONTHLY_CONS_LBL: "Consumption per bill",
    MONTHLY_CALC_NOTE: "This calculation is based on your consumption for the current month of {MONTH}. For more accurate results, please use the annual calculator.",
    BILL_BREAKDOWN_HDR: "Bill breakdown",
    BILL_YEAR_NOTE: "× {N} bills/year ≈ €{X} / year (excl. VAT)",
    NUDGE_ANNUAL: "💡 For a more accurate comparison based on your seasonal usage pattern, switch to Annual mode and enter your yearly consumption.",
    LBL_VULNERABLE_CHECK: "I am eligible for a social / vulnerable consumer tariff",
    LBL_VULNERABLE_INFO: "Who qualifies?",
    LBL_OFFERS_CHECK: "Show/Hide special offers",
    TITLE_VULNERABLE_MODAL: "Vulnerable consumer / social tariff — eligible cases",
    LBL_INCL_ADDITIONAL: "+ {X} additional charges",
    LBL_WITHOUT_VAT: "Without VAT",
    BTN_CONTACT: "📋 View contact details",
    BTN_REPORT_ISSUE: "Report an issue",
    REPORT_MODAL_TITLE: "Report an issue",
    REPORT_LBL_TARIFF: "Tariff",
    REPORT_LBL_SUPPLIER: "Supplier",
    REPORT_LBL_CATEGORY: "What's wrong?",
    REPORT_CAT_INCORRECT_PRICE: "Incorrect price",
    REPORT_CAT_TERMS_MISMATCH: "Terms don't match the supplier's site",
    REPORT_CAT_BROKEN_LINK: "Broken document/link",
    REPORT_CAT_OTHER: "Other",
    REPORT_LBL_NOTE: "Describe the issue",
    REPORT_NOTE_PLACEHOLDER: "e.g. the standing charge shown doesn't match the supplier's website",
    REPORT_LBL_EMAIL: "Your email (so CERA can contact you if needed)",
    REPORT_EMAIL_PLACEHOLDER: "you@example.com",
    REPORT_SUCCESS: "Thanks — your report has been sent to the regulator for review.",
    REPORT_ERROR: "Something went wrong sending your report. Please try again.",
    REPORT_EMAIL_REQUIRED: "Please enter your email address so CERA can contact you if needed.",
    REPORT_NOTE_REQUIRED: "Please describe the issue.",
    REPORT_MODAL_TITLE_GENERAL: "Report a general issue",
    REPORT_OFFLINE: "Reporting is unavailable in offline/demo mode.",
    BTN_CANCEL: "Cancel",
    BTN_SUBMIT_REPORT: "Submit",
    SKIP_LINK: "Skip to main content",
    NOTICES_TAB_ABOUT: "About & independence",
    BTN_A11Y_OFF: "Accessible mode",
    BTN_A11Y_ON: "Accessible mode: on",
    ABOUT_CONTENT: "<h3>Who operates this tool</h3><p>This tariff comparison tool is owned and operated by the <strong>Cyprus Energy Regulatory Authority (CERA)</strong>, the independent statutory regulator for the electricity and natural gas markets in Cyprus. CERA is a public authority and has no ownership, commercial, or financial relationship with any of the electricity suppliers listed on this tool.</p><p>The tool is funded as part of CERA's regulatory functions and is provided free of charge to consumers. Suppliers are not charged for their tariffs to appear here, and cannot pay for priority, featured, or preferential placement in the results.</p><h3>Independence and equal treatment</h3><p>Tariffs are ranked using the same calculation method and the same published criteria for every supplier — by default, lowest estimated cost first (see the \"Notices\" tab for the full calculation methodology). No supplier receives preferential visibility, sponsored placement, or any form of priority ranking. CERA does not endorse any individual supplier or tariff.</p><h3>Comparison criteria</h3><p>Tariffs are ranked by <strong>total estimated cost</strong> for the consumption you enter — lowest first. This includes energy charges, standing charges, and any applicable discounts. Regulated network, PSO and metering charges are shown separately and are not part of the ranking, and all figures exclude VAT. The same calculation is applied identically to every supplier (full methodology in the \"Notices\" tab).</p><p>Alongside price, every tariff also displays the following information so you can compare on more than cost alone:</p><ul><li>Pricing type — Fixed, Time-of-Use, Dynamic, or Variable</li><li>Minimum contract duration, or no minimum</li><li>Available discounts and the conditions that apply to them</li><li>Eligibility for social / vulnerable-consumer tariffs</li><li>Supplier contact details</li><li>Date the tariff information was last updated</li></ul><p>These service-related criteria are currently for your information and are not yet used to influence ranking order.</p><h3>Reporting an issue</h3><p>If you believe any information shown for a tariff is incorrect or out of date, use the \"Report an issue\" button on that tariff's card to notify CERA directly.</p>",
    TH_MONTH: "Month",
    TH_KWH: "kWh",
    TH_ENERGY: "Energy Cost",
    FPA_SHORT: "FPA",
    FPA_FULL: "Fuel price adjustment",
    FPA_DESC: "Fuel Price Adjustment (FPA): a per-kWh charge added to the supplier's energy rate to reflect fluctuations in fuel and purchased-power costs. Set by the supplier.",
    STANDING_DESC: "A fixed monthly charge set by the supplier — a competitive charge.",
    TH_STANDING: "Standing",
    TH_TOTAL: "Total",
    ROW_SUP_TOTAL: "Supplier total",
    ROW_TOTAL_REG: "Total (incl. additional charges, without VAT)",
    BTN_SAMPLE_INVOICE: "Sample invoice",
    SAMPLE_INV_BANNER: "⚠ Sample invoice — illustrative example, not a real bill",
    SAMPLE_INV_EX_NAME: "Example Customer",
    SAMPLE_INV_EX_ADDRESS: "Example Address, Nicosia, Cyprus",
    SAMPLE_INV_EX_ACCOUNT: "XXX XXX XXXX X",
    SAMPLE_INV_EX_METER: "XXXXXX",
    SAMPLE_INV_LBL_NAME: "Customer name",
    SAMPLE_INV_LBL_ACCOUNT: "Account number",
    SAMPLE_INV_LBL_ADDRESS: "Supply address",
    SAMPLE_INV_LBL_METER: "Meter number",
    SAMPLE_INV_LBL_TARIFF: "Tariff",
    SAMPLE_INV_LBL_SUPPLIER: "Supplier",
    SAMPLE_INV_LBL_PERIOD: "Billing period",
    SAMPLE_INV_CHARGES_TITLE: "Analysis for the period",
    SAMPLE_INV_SECTION_COMPETITIVE: "Competitive charges (set by your supplier)",
    SAMPLE_INV_SECTION_REGULATED: "Regulated charges (CERA)",
    SAMPLE_INV_COMPETITIVE_TOTAL: "Total competitive charges",
    SAMPLE_INV_REGULATED_TOTAL: "Total regulated charges",
    SAMPLE_INV_TOTAL_SUBJECT_VAT: "Total subject to VAT (19%)",
    SAMPLE_INV_RES_NOTE: "(not subject to VAT)",
    SAMPLE_INV_ENERGY_DESC: "The cost of the electricity you consumed, priced at your tariff's rate.",
    SAMPLE_INV_ENERGY_PEAK: "Energy Cost — Peak",
    SAMPLE_INV_ENERGY_OFFPEAK: "Energy Cost — Off-Peak",
    SAMPLE_INV_TOTAL_BEFORE_VAT: "Total before VAT",
    SAMPLE_INV_VAT: "VAT (19%)",
    SAMPLE_INV_AMOUNT_DUE: "Amount due",
    SAMPLE_INV_DISCLAIMER: "Illustrative example based on your inputs — not an actual bill. Customer name, address and meter/account numbers shown are placeholders. Actual bills may include other charges (e.g. arrears, credits) not shown here.",
    CHART_ANNUAL: "Annual cost comparison — all tariffs (competitive costs only)",
    CHART_MONTHLY_COST: "Monthly cost",
    VAR_NO_DAM_TITLE: "Dynamic tariffs — DAM data missing",
    VAR_ONLY_TITLE: "Dynamic tariffs require Annual mode",
    VAR_ONLY_BODY: "A single month's DAM price does not represent the annual cost of a dynamic tariff accurately. Please switch to Annual mode to compare variable tariffs.",
    NO_TARIFFS_TITLE: "No tariffs found",
    NO_TARIFFS_SUB: "No tariffs configured for {VOLTAGE} · {CONTRACT}.",
    NO_CONFIG_TITLE: "No configuration found",
    NO_CONFIG_BODY: "Open <strong>admin.html</strong> in the same browser, set up your suppliers and tariffs, then click <em>Save &amp; publish</em>.",
    PROMPT_ENTER: "Enter your consumption above to compare tariffs.",
    CALC_ERROR: "Unable to calculate tariffs right now — please try again in a moment.",
    CALC_LOADING: "Calculating…",
    DISC_HEADER: "🏷 Available discounts — uncheck if not applicable",
    DISC_ENERGY_LABEL: "⚡ Energy discount",
    DISC_STANDING_LABEL: "📋 Standing discount",
    DISC_DURATION_FIRST: "for first <strong>{N} months</strong>",
    DISC_DURATION_PERM: "permanent",
    CALC_FALLBACK: "⚠ Fallback: hour-fraction method (no DSO profile assigned)",
    CALC_DIST_FLAT: "flat monthly input — profile used for intra-day only",
    CALC_TOU: "📊 DSO profile · {NOTE} · WD/NWD shapes → half-hourly rates · {PROFILE}",
    CALC_DAM_SLOT: "📊 DSO profile × half-hourly DAM · {NOTE} · {PROFILE}",
    CALC_DAM_AVG: "📊 DSO profile × monthly DAM avg · {NOTE} · {PROFILE}",
    CALC_TIERED: "🔢 Tiered block · {N} month reset · {TIERS}",
    TARIFFS_AVAILABLE_ONE: "{N} tariff available",
    TARIFFS_AVAILABLE: "{N} tariffs available",
    LBL_VIEW_CONTACT: "View contact details",
    LBL_FIXED_ROW: "Fixed €{N}/month",
    LBL_FIXED_ROW_MDM: "€{N} / invoice",
    MDM_BILLED_MONTHLY: "Billed monthly",
    MDM_BILLED_BIMONTHLY: "Billed bimonthly",
    REGULATED_GRID: "Network Charge",
    REGULATED_PSO: "Public Service Obligation (PSO)",
    REGULATED_MDM: "Meter Data Management (MDM)",
    MDM_SUPPLIER: "Meter Data Management (MDM)",
    REGULATED_RES: "RES & Energy Conservation Fund",
    REG_GRID_DESC: "Distribution/Transmission system charge. Regulated charge.",
    REG_PSO_DESC: "Tariff for the recovery of Public Service Obligation (PSO) costs. Regulated charge. Applied per kWh consumed.",
    REG_RES_DESC: "Levy for the promotion of Renewable Energy Sources (RES) and energy conservation. Regulated charge. Applied per kWh consumed. Not subject to VAT.",
    REG_MDM_DESC: "Tariff for the recovery of metering costs incurred by the Distribution System Operator (DSO) (for users connected to the Distribution System). Regulated charge only for the dominant participant (EAC Supply).",
    MDM_SUPPLIER_DESC: "A metering data management charge set by the supplier — a competitive charge.",
    BTN_NOTICES: "ℹ️ Notices & Disclaimers",
    NOTICES_TITLE: "Notices & Disclaimers",
    NOTICES_TAB_ASSUMPTIONS: "Notices",
    NOTICES_TAB_LEGAL: "Disclaimers",
    FOOTER_ORG_NAME: "Cyprus Energy Regulatory Authority",
    FOOTER_ADDRESS: "20 Agias Paraskevis,<br>2002 Strovolos,<br>Nicosia, Cyprus",
    FOOTER_POBOX_CITY: "1305 Nicosia",
    FOOTER_POSTAL: "Postal Address",
    FOOTER_POBOX: "P.O. Box",
    FOOTER_PHONE: "Phone",
    FOOTER_FAX: "Fax",
    FOOTER_EMAIL: "Email",
    FOOTER_CONTACT: "Contact",
    BTN_ESTIMATE: "🧮 Estimate",
    EST_TITLE: "Estimate your consumption",
    EST_DESC: "Answer a few questions to get a rough estimate of your annual electricity use in Cyprus.",
    EST_DWELLING: "Dwelling type",
    EST_D_STUDIO: "Studio / bedsit (< 40 m²)",
    EST_D_APT1: "Small apartment — 1 bedroom (40–65 m²)",
    EST_D_APT2: "Apartment — 2 bedrooms (65–90 m²)",
    EST_D_APT3: "Apartment — 3 bedrooms (90–120 m²)",
    EST_D_SEMI: "Semi-detached house",
    EST_D_DET_S: "Detached house — small (140–200 m²)",
    EST_D_DET_L: "Detached house / Villa (> 200 m²)",
    EST_PERSONS: "Number of inhabitants",
    EST_AC: "Air conditioning",
    EST_AC_NONE: "None",
    EST_AC_LIGHT: "Light — 1 unit, occasional use",
    EST_AC_MOD: "Moderate — 2–3 units",
    EST_AC_HEAVY: "Heavy — 3+ units, all summer",
    EST_WATER: "Water heating",
    EST_WATER_SOLAR: "Solar heater (electric backup)",
    EST_WATER_ELEC: "Electric boiler",
    EST_WATER_OTHER: "Gas / other",
    EST_COOKING: "Electric cooker / oven",
    EST_YES: "Yes",
    EST_NO: "No",
    EST_CALC: "Calculate",
    EST_USE: "Use this estimate",
    EST_RESULT_LBL: "Estimated annual consumption",
    EST_RESULT_UNIT: "kWh / year",
    EST_NOTE: "Indicative estimate only. For an accurate comparison, use the actual annual kWh figure from your electricity bill.",
    EST_METH_TITLE: "Methodology & data sources",
    EST_METH_BODY: `<p><strong>Disclaimer:</strong> This tool provides indicative estimates based on typical consumption patterns for Cyprus households. It does not reflect your actual meter readings, contract terms, or specific appliance efficiency. Actual consumption may differ significantly depending on insulation quality, occupant behaviour, appliance age, and seasonal variation. This tool does not constitute a commercial offer or energy advice.</p>
<p><strong>Base consumption by dwelling size</strong> — derived from Eurostat household energy statistics (NRG_D_HHQ, Cyprus row) and EAC average billed kWh per domestic connection. The Cyprus household average of ~5,000–5,500 kWh/year is reproduced by a typical 2BR apartment + moderate AC + solar water heater in this model.</p>
<table>
<tr><th>Dwelling</th><th>Base kWh/yr</th><th>Basis</th></tr>
<tr><td>Studio</td><td>1,200</td><td>Minimal load, 1 person implied, small area</td></tr>
<tr><td>1BR apartment</td><td>1,800</td><td>Standard appliance base (lighting, fridge, TV, laundry)</td></tr>
<tr><td>2BR apartment</td><td>2,600</td><td>EAC LV domestic billing averages by connection size</td></tr>
<tr><td>3BR apartment</td><td>3,500</td><td>Larger circuit count, more occupant appliances</td></tr>
<tr><td>Semi-detached</td><td>4,500</td><td>Additional floors, garden/outdoor lighting</td></tr>
<tr><td>Small detached</td><td>6,000</td><td>EAC typical LV billing for 140–200 m²</td></tr>
<tr><td>Large detached / villa</td><td>9,000</td><td>Pool pump, gate motors, larger common areas</td></tr>
</table>
<p><strong>Per additional person (+600 kWh):</strong> Personal electronics ~150, laundry ~100, cooking ~100, hot water demand ~150, lighting ~100 kWh/yr. Consistent with ODYSSEE-MURE per-capita residential end-use data for Cyprus.</p>
<p><strong>Air conditioning</strong> — Cyprus has the highest cooling degree days in the EU. AC typically runs May–October (~150–180 days). Estimates assume 1.5 kW per unit: Light: 1 unit × 4 h/day × 120 days ≈ 700 kWh; Moderate: 2 units × 6 h/day × 140 days × 0.7 duty ≈ 1,800 kWh; Heavy: 3 units × 8 h/day × 150 days × 0.65 duty ≈ 3,500 kWh.</p>
<p><strong>Water heating:</strong> Solar + backup: ~300 kWh (backup runs Oct–Mar on low-solar days, ~80% solar coverage). Electric boiler: ~1,200 kWh (80L tank, 2 kW element, ~2 hrs/day × ~220 days). Gas/other: no electricity contribution.</p>
<p><strong>Electric cooking (+400 kWh):</strong> EU appliance studies (ADEME, Energy Saving Trust) cite 300–500 kWh/yr for typical household electric cooking. Midpoint used.</p>
<div class="est-meth-sources"><strong>Sources:</strong> Eurostat NRG_D_HHQ · ODYSSEE-MURE CY residential · EAC Annual Report · CERA Energy Report · JRC Heating &amp; Cooling study (CY cooling degree days)</div>`,
    MONTHS: ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
  },
  el: {
    PAGE_EYEBROW: "Υπολογισμός κόστους ηλεκτρικής ενέργειας",
    PAGE_TITLE: "Εργαλείο σύγκρισης διατιμήσεων προμηθευτών",
    PAGE_DESC: "Συμπληρώστε την εκτιμώμενη κατανάλωση σας και δείτε όλες τις διαθέσιμες διατιμήσεις, με σειρά αυξανόμενου κόστους και τα στοιχεία των προμηθευτών.",
    CARD_CONNECTION: "Τύπος σύνδεσης",
    TAB_DOMESTIC: "🏠 Οικιακή",
    TAB_CI: "🏢 Εμπορική/Βιομηχανική",
    LBL_VOLTAGE: "Τάση Ρεύματος",
    OPT_LV: "ΧΤ — Χαμηλή Τάση",
    OPT_MV: "ΜΤ — Μεσαία Τάση",
    OPT_HV: "ΥΤ — Υψηλή Τάση",
    LBL_LOAD_ENT: "Εγκατεστημένη ισχύς",
    LE_LT70: "< 70 kVA",
    LE_GT70: "> 70 kVA",
    LBL_PRICING: "Τύπος Διατίμησης",
    OPT_ALL: "Όλοι",
    OPT_FIXED: "Σταθερή μόνο",
    OPT_TOU: "Χρόνου Χρήσης (ToU)",
    OPT_VARIABLE: "Δυναμική μόνο",
    OPT_VARIABLE_TIERED: "Κλιμακωτή μόνο",
    TAG_FIXED: "Σταθερή",
    TAG_TOU: "ToU",
    TAG_DYNAMIC: "Δυναμική",
    TAG_VARIABLE: "Κλιμακωτή",
    TAG_LV: "ΧΤ",
    TAG_MV: "ΜΤ",
    TAG_HV: "ΥΤ",
    TAG_DOMESTIC: "Οικιακή",
    TAG_CI: "Εμπορική/Βιομηχανική",
    CARD_CONSUMPTION: "Η κατανάλωσή σας",
    BTN_ANNUAL: "Ετήσια",
    BTN_MONTHLY: "Μηνιαία",
    BTN_BACK_TO_TOP: "Επιστροφή στην κορυφή",
    LBL_ANNUAL_KWH: "Ετήσια κατανάλωση",
    UNIT_KWH_YEAR: "kWh / έτος",
    HINT_ANNUAL: "Βάσει των Κανόνων Προμηθειας Ηλεκτρισμού Άρθρο 7.1.7 (α) της ΡΑΕΚ, όλοι οι προμηθευτές υποχρεούνται να ενημερώνουν τους πελάτες τους κατ' ελάχιστο μια φορά τον χρόνο, για την συνολική τους κατανάλωση κατά το προηγούμενο έτος καθώς επίσης και την εκτίμιση κατανάλωσης για το τρέχον έτος.",
    RESULTS_SUB_ANNUAL: "Φθηνότερος προμηθευτής πρώτα · Πρώτοι 12 μήνες μετά την αλλαγή ({PERIOD}) · Κατανομή-προφίλ",
    RESULTS_SUB_MONTHLY: "Φθηνότερος λογαριασμός πρώτα · {KWH} kWh ανά λογαριασμό · Πρώτοι 12 μήνες μετά την αλλαγή ({PERIOD})",
    LAST_UPDATED: "Ενημερώθηκε {DT}",
    LBL_STANDING: "/μήνα πάγιο",
    LBL_NO_MIN: "Αορίστου χρόνου",
    LBL_MIN_MONTHS: "{N} μήνες συμβόλαιο",
    LBL_INCL_DISC: "Τιμή με εκπτώσεις. Αναπτύξτε για λεπτομέρειες.",
    LBL_OFFER_ENDS: "Περιλαμβάνει προσφορά {N} μηνών. Μετά τη λήξη της: περίπου €{X} / μήνα (χρεώσεις προμηθευτή).",
    LBL_SUP_YEAR: "/έτος",
    LBL_SUP_MONTH: "/μήνα",
    LBL_SUP_2MO: "/ 2 μήνες",
    BILLING_CYCLE: "Κύκλος τιμολόγησης",
    BILLING_M1: "Μηνιαία",
    BILLING_M2: "Διμηνιαία",
    MONTHLY_UNIT_1: "kWh / μήνα",
    MONTHLY_UNIT_2: "kWh / 2 μήνες",
    MONTHLY_CONS_LBL: "Κατανάλωση ανά λογαριασμό",
    MONTHLY_CALC_NOTE: "Ο υπολογισμός βασίζεται στην κατανάλωσή σας για τον τρέχοντα μήνα {MONTH}. Για πιο ακριβή αποτελέσματα, χρησιμοποιήστε τον ετήσιο υπολογιστή.",
    BILL_BREAKDOWN_HDR: "Ανάλυση λογαριασμού",
    BILL_YEAR_NOTE: "× {N} λογ./έτος ≈ €{X} / έτος (χωρίς ΦΠΑ)",
    NUDGE_ANNUAL: "💡 Για πιο ακριβή σύγκριση βάσει εποχικής κατανάλωσης, επιλέξτε Ετήσια σύγκριση και εισάγετε την ετήσια κατανάλωσή σας.",
    LBL_VULNERABLE_CHECK: "Δικαιούμαι κοινωνική / ευπαθή διατίμηση",
    LBL_VULNERABLE_INFO: "Ποιοι δικαιούνται;",
    LBL_OFFERS_CHECK: "Εμφάνιση/Απόκρυψη ειδικών προσφορών",
    TITLE_VULNERABLE_MODAL: "Κοινωνική διατίμηση / ευπαθείς καταναλωτές — επιλέξιμες περιπτώσεις",
    LBL_INCL_ADDITIONAL: "+ {X} πρόσθετες χρεώσεις",
    LBL_WITHOUT_VAT: "Χωρίς ΦΠΑ",
    BTN_CONTACT: "📋 Στοιχεία Επικοινωνίας",
    BTN_REPORT_ISSUE: "Αναφορά προβλήματος",
    REPORT_MODAL_TITLE: "Αναφορά προβλήματος",
    REPORT_LBL_TARIFF: "Διατίμηση",
    REPORT_LBL_SUPPLIER: "Προμηθευτής",
    REPORT_LBL_CATEGORY: "Τι δεν είναι σωστό;",
    REPORT_CAT_INCORRECT_PRICE: "Λανθασμένη τιμή",
    REPORT_CAT_TERMS_MISMATCH: "Οι όροι δεν ταιριάζουν με την ιστοσελίδα του προμηθευτή",
    REPORT_CAT_BROKEN_LINK: "Κατεστραμμένο έγγραφο/σύνδεσμος",
    REPORT_CAT_OTHER: "Άλλο",
    REPORT_LBL_NOTE: "Περιγράψτε το πρόβλημα",
    REPORT_NOTE_PLACEHOLDER: "π.χ. η πάγια χρέωση που εμφανίζεται δεν ταιριάζει με την ιστοσελίδα του προμηθευτή",
    REPORT_LBL_EMAIL: "Το email σας (για να επικοινωνήσει η ΡΑΕΚ μαζί σας αν χρειαστεί)",
    REPORT_EMAIL_PLACEHOLDER: "you@example.com",
    REPORT_SUCCESS: "Ευχαριστούμε — η αναφορά σας εστάλη στη ΡΑΕΚ για έλεγχο.",
    REPORT_ERROR: "Κάτι πήγε στραβά κατά την αποστολή. Παρακαλούμε δοκιμάστε ξανά.",
    REPORT_EMAIL_REQUIRED: "Παρακαλούμε εισάγετε το email σας ώστε να μπορεί η ΡΑΕΚ να επικοινωνήσει μαζί σας αν χρειαστεί.",
    REPORT_NOTE_REQUIRED: "Παρακαλούμε περιγράψτε το πρόβλημα.",
    REPORT_MODAL_TITLE_GENERAL: "Αναφορά γενικού προβλήματος",
    REPORT_OFFLINE: "Η αναφορά δεν είναι διαθέσιμη σε λειτουργία εκτός σύνδεσης/επίδειξης.",
    BTN_CANCEL: "Άκυρο",
    BTN_SUBMIT_REPORT: "Υποβολή",
    SKIP_LINK: "Μετάβαση στο κύριο περιεχόμενο",
    NOTICES_TAB_ABOUT: "Σχετικά & ανεξαρτησία",
    BTN_A11Y_OFF: "Προσβάσιμη λειτουργία",
    BTN_A11Y_ON: "Προσβάσιμη λειτουργία: ενεργή",
    ABOUT_CONTENT: "<h3>Ποιος διαχειρίζεται το εργαλείο</h3><p>Αυτό το εργαλείο σύγκρισης διατιμήσεων ανήκει και λειτουργεί από τη <strong>Ρυθμιστική Αρχή Ενέργειας Κύπρου (ΡΑΕΚ)</strong>, τον ανεξάρτητο ρυθμιστή της αγοράς ηλεκτρισμού και φυσικού αερίου στην Κύπρο. Η ΡΑΕΚ είναι δημόσια αρχή και δεν έχει ιδιοκτησιακή, εμπορική ή οικονομική σχέση με κανέναν από τους προμηθευτές ηλεκτρικής ενέργειας που παρουσιάζονται στο εργαλείο.</p><p>Το εργαλείο χρηματοδοτείται στο πλαίσιο των κανονιστικών λειτουργιών της ΡΑΕΚ και παρέχεται δωρεάν στους καταναλωτές. Οι προμηθευτές δεν χρεώνονται για την εμφάνιση των διατιμήσεών τους και δεν μπορούν να πληρώσουν για προτεραιότητα ή προνομιακή τοποθέτηση στα αποτελέσματα.</p><h3>Ανεξαρτησία και ίση μεταχείριση</h3><p>Οι διατιμήσεις κατατάσσονται με την ίδια μέθοδο υπολογισμού και τα ίδια δημοσιευμένα κριτήρια για κάθε προμηθευτή — από προεπιλογή, με βάση το χαμηλότερο εκτιμώμενο κόστος (δείτε την καρτέλα «Ανακοινώσεις» για την πλήρη μεθοδολογία υπολογισμού). Κανένας προμηθευτής δεν λαμβάνει προνομιακή προβολή, χορηγούμενη τοποθέτηση ή οποιαδήποτε μορφή προτεραιότητας στην κατάταξη. Η ΡΑΕΚ δεν υποστηρίζει ή προωθεί συγκεκριμένο προμηθευτή ή διατίμηση.</p><h3>Κριτήρια σύγκρισης</h3><p>Οι διατιμήσεις κατατάσσονται με βάση το <strong>συνολικό εκτιμώμενο κόστος</strong> για την κατανάλωση που εισάγετε — από το χαμηλότερο. Περιλαμβάνει χρεώσεις ενέργειας, πάγιες χρεώσεις και τυχόν εφαρμοζόμενες εκπτώσεις. Οι ρυθμιζόμενες χρεώσεις δικτύου, ΥΔΩ και μετρήσεων εμφανίζονται ξεχωριστά και δεν συμπεριλαμβάνονται στην κατάταξη, ενώ όλα τα ποσά δεν περιλαμβάνουν ΦΠΑ. Ο ίδιος υπολογισμός εφαρμόζεται με τον ίδιο τρόπο σε κάθε προμηθευτή (πλήρης μεθοδολογία στην καρτέλα «Ανακοινώσεις»).</p><p>Εκτός από την τιμή, κάθε διατίμηση εμφανίζει επίσης τις ακόλουθες πληροφορίες ώστε να συγκρίνετε πέραν του κόστους:</p><ul><li>Τύπος τιμολόγησης — Σταθερή, Ζωνική (Time-of-Use), Δυναμική ή Κυμαινόμενη</li><li>Ελάχιστη διάρκεια συμβολαίου, ή χωρίς ελάχιστο</li><li>Διαθέσιμες εκπτώσεις και οι όροι που τις διέπουν</li><li>Επιλεξιμότητα για κοινωνική / ευπαθή διατίμηση</li><li>Στοιχεία επικοινωνίας προμηθευτή</li><li>Ημερομηνία τελευταίας ενημέρωσης της διατίμησης</li></ul><p>Αυτά τα κριτήρια που σχετίζονται με τις υπηρεσίες είναι επί του παρόντος ενημερωτικά και δεν χρησιμοποιούνται ακόμη για να επηρεάσουν τη σειρά κατάταξης.</p><h3>Αναφορά προβλήματος</h3><p>Εάν πιστεύετε ότι κάποια πληροφορία που εμφανίζεται για μια διατίμηση είναι λανθασμένη ή μη επικαιροποιημένη, χρησιμοποιήστε το κουμπί «Αναφορά προβλήματος» στην κάρτα της διατίμησης για να ενημερώσετε απευθείας τη ΡΑΕΚ.</p>",
    TH_MONTH: "Μήνας",
    TH_KWH: "kWh",
    TH_ENERGY: "Κόστος Ενέργειας",
    FPA_SHORT: "ΑΤΚ",
    FPA_FULL: "Αναπροσαρμογή τιμής καυσίμου",
    FPA_DESC: "Αναπροσαρμογή Τιμής Καυσίμου (ΑΤΚ): χρέωση ανά kWh που προστίθεται στη χρέωση ενέργειας του προμηθευτή, για την κάλυψη διακυμάνσεων στο κόστος καυσίμου και αγοράς ενέργειας. Οριζόμενο από τον προμηθευτή.",
    STANDING_DESC: "Σταθερή μηνιαία χρέωση που ορίζεται από τον προμηθευτή — Ανταγωνιστίκή χρέωση.",
    TH_STANDING: "Πάγιο",
    TH_TOTAL: "Ολικό",
    ROW_SUP_TOTAL: "Ολικό Προμηθευτή",
    ROW_TOTAL_REG: "Ολικό (συμπ. πρόσθετων χρεώσεων, χωρίς ΦΠΑ)",
    BTN_SAMPLE_INVOICE: "Δείγμα λογαριασμού",
    SAMPLE_INV_BANNER: "⚠ Δείγμα λογαριασμού — ενδεικτικό παράδειγμα, όχι πραγματικός λογαριασμός",
    SAMPLE_INV_EX_NAME: "Παράδειγμα Πελάτη",
    SAMPLE_INV_EX_ADDRESS: "Παράδειγμα Διεύθυνσης, Λευκωσία, Κύπρος",
    SAMPLE_INV_EX_ACCOUNT: "XXX XXX XXXX X",
    SAMPLE_INV_EX_METER: "XXXXXX",
    SAMPLE_INV_LBL_NAME: "Όνομα πελάτη",
    SAMPLE_INV_LBL_ACCOUNT: "Αριθμός λογαριασμού",
    SAMPLE_INV_LBL_ADDRESS: "Διεύθυνση παροχής",
    SAMPLE_INV_LBL_METER: "Αριθμός μετρητή",
    SAMPLE_INV_LBL_TARIFF: "Διατίμηση",
    SAMPLE_INV_LBL_SUPPLIER: "Προμηθευτής",
    SAMPLE_INV_LBL_PERIOD: "Περίοδος χρέωσης",
    SAMPLE_INV_CHARGES_TITLE: "Ανάλυση για την περίοδο",
    SAMPLE_INV_SECTION_COMPETITIVE: "Ανταγωνιστικές χρεώσεις (καθορίζονται από τον προμηθευτή)",
    SAMPLE_INV_SECTION_REGULATED: "Ρυθμιζόμενες χρεώσεις (ΡΑΕΚ)",
    SAMPLE_INV_COMPETITIVE_TOTAL: "Σύνολο ανταγωνιστικών χρεώσεων",
    SAMPLE_INV_REGULATED_TOTAL: "Σύνολο ρυθμιζόμενων χρεώσεων",
    SAMPLE_INV_TOTAL_SUBJECT_VAT: "Σύνολο υποκείμενο σε ΦΠΑ (19%)",
    SAMPLE_INV_RES_NOTE: "(δεν υπόκειται σε ΦΠΑ)",
    SAMPLE_INV_ENERGY_DESC: "Το κόστος της ηλεκτρικής ενέργειας που καταναλώσατε, τιμολογημένο με βάση τη χρέωση της διατίμησής σας.",
    SAMPLE_INV_ENERGY_PEAK: "Κόστος Ενέργειας — Αιχμή",
    SAMPLE_INV_ENERGY_OFFPEAK: "Κόστος Ενέργειας — Εκτός Αιχμής",
    SAMPLE_INV_TOTAL_BEFORE_VAT: "Σύνολο πριν τον ΦΠΑ",
    SAMPLE_INV_VAT: "ΦΠΑ (19%)",
    SAMPLE_INV_AMOUNT_DUE: "Οφειλόμενο ποσό",
    SAMPLE_INV_DISCLAIMER: "Ενδεικτικό παράδειγμα βάσει των στοιχείων που εισαγάγατε — όχι πραγματικός λογαριασμός. Το όνομα πελάτη, η διεύθυνση και οι αριθμοί μετρητή/λογαριασμού είναι ενδεικτικοί. Πραγματικοί λογαριασμοί ενδέχεται να περιλαμβάνουν και άλλες χρεώσεις (π.χ. οφειλές, πιστώσεις) που δεν εμφανίζονται εδώ.",
    CHART_ANNUAL: "Σύγκριση ετήσιου κόστους — ανταγωνιστικές χρεώσεις μόνο",
    CHART_MONTHLY_COST: "Μηνιαίο κόστος",
    VAR_NO_DAM_TITLE: "Δυναμική διατίμηση — Δεν υπάρχουν δεδομένα ΠΗΑ",
    VAR_ONLY_TITLE: "Οι δυναμικές διατιμήσεις είναι μόνο στην ετήσια σύγκριση",
    VAR_ONLY_BODY: "Οι τιμές ΠΗΑ ενός μεμονωμένου μήνα δεν αντιπροσωπεύουν ορθά όλο το έτος για τη δυναμική τιμολόγηση. Παρακαλώ επιλέξτε ετήσια σύγκριση για να συγκρίνετε και δυναμικές τιμολογήσεις.",
    NO_TARIFFS_TITLE: "Δεν υπάρχουν διατιμήσεις.",
    NO_TARIFFS_SUB: "Δεν υπάρχουν διατιμήσεις για {VOLTAGE} · {CONTRACT}.",
    NO_CONFIG_TITLE: "Δεν βρέθηκε σχετική ρύθμιση",
    NO_CONFIG_BODY: "Ανοίξτε το αρχείο <strong>admin.html</strong> στο ίδιο πρόγραμμα περιήγησης, ρυθμίστε τους προμηθευτές και τις τιμές, και κάντε κλικ στην επιλογή <em>Αποθήκευση &amp; δημοσίευση</em>.",
    PROMPT_ENTER: "Εισάγετε την κατανάλωση σας πιο πάνω για σύγκριση διατιμήσεων.",
    CALC_ERROR: "Δεν ήταν δυνατός ο υπολογισμός αυτή τη στιγμή — δοκιμάστε ξανά σε λίγο.",
    CALC_LOADING: "Υπολογισμός…",
    DISC_HEADER: "🏷 Διαθέσιμες εκπτώσεις — επιλέξτε ότι ισχύει",
    DISC_ENERGY_LABEL: "⚡ Έκπτωση στην ενέργεια",
    DISC_STANDING_LABEL: "📋 Έκπτωση στο Πάγιο",
    DISC_DURATION_FIRST: "για τους πρώτους <strong>{N} μήνες</strong>",
    DISC_DURATION_PERM: "μόνιμα",
    CALC_FALLBACK: "⚠ Εφεδρική μέθοδος (δεν έχει αντιστοιχιστεί σε προφίλ ΔΣΔ)",
    CALC_DIST_FLAT: "σταθερή μηνιαία είσοδος — προφίλ που χρησιμοποιείται μόνο για ενδοημερήσια χρήση",
    CALC_TOU: "📊 Προφίλ ΔΣΔ · {NOTE} · Χωρισμένο σε εργάσιμες/μη εργάσιμες → ημιωριαίες τιμές · {PROFILE}",
    CALC_DAM_SLOT: "📊 Προφίλ ΔΣΔ × ημιωριαία τιμή ΠΗΑ · {NOTE} · {PROFILE}",
    CALC_DAM_AVG: "📊 Προφίλ ΔΣΔ × μηνιαίος μέσος όρος τιμής ΠΗΑ · {NOTE} · {PROFILE}",
    CALC_TIERED: "🔢 Κλιμακωτό μπλοκ · {N} επαναφορά μήνα · {TIERS}",
    TARIFFS_AVAILABLE_ONE: "{N} διατίμηση διαθέσιμη",
    TARIFFS_AVAILABLE: "{N} διατιμήσεις διαθέσιμες",
    LBL_VIEW_CONTACT: "Στοιχεία προμηθευτή",
    LBL_FIXED_ROW: "Σταθερό €{N}/μήνα",
    LBL_FIXED_ROW_MDM: "€{N} / λογαριασμό",
    MDM_BILLED_MONTHLY: "Εκδίδεται μηνιαία",
    MDM_BILLED_BIMONTHLY: "Εκδίδεται διμηνιαία",
    REGULATED_GRID: "Κόστος Δικτύου",
    REGULATED_PSO: "Υποχρεώσεις Δημόσιας Ωφέλειας (ΥΔΩ)",
    REGULATED_MDM: "Κόστος Διαχείρισης Μετρητικών Δεδομένων",
    MDM_SUPPLIER: "Κόστος Διαχείρισης Μετρητικών Δεδομένων",
    REGULATED_RES: "Ταμείο ΑΠΕ & ΕΞΕ",
    REG_GRID_DESC: "Διατίμηση χρήσης του Συστήματος Διανομής/Μεταφοράς. Ρυθμιζόμενη χρέωση.",
    REG_PSO_DESC: "Διατίμηση για την ανάκτηση των δαπανών των Υπηρεσιών Δημοσίας Ωφέλειας (ΥΔΩ). Ρυθμιζόμενη χρέωση.",
    REG_RES_DESC: "Εισφορά για το Ταμείο Ανανεώσιμων Πηγών Ενέργειας (ΑΠΕ) και Εξοικονόμησης Ενέργειας (ΕΞΕ) του Υπουργείου Ενέργειας, Εμπορίου και Βιομηχανίας. Το ειδικό τέλος χρεώνεται σε όλους τους πελάτες με βάση τις μονάδες (kWh) που καταναλώνουν. Δεν υπόκειται σε ΦΠΑ.",
    REG_MDM_DESC: "Διατίμηση για την ανάκτηση των δαπανών μετρήσεων που ανακύπτουν από το Διαχειριστή του Συστήματος Διανομής (ΔΣΔ) (για χρήστες που συνδέονται στο Σύστημα Διανομής). Ρυθμιζόμενη χρέωση μόνο για τον δεσπόζων συμμετέχοντα (ΑΗΚ Προμήθεια).",
    MDM_SUPPLIER_DESC: "Χρέωση διαχείρισης μετρητικών δεδομένων που ορίζεται από τον προμηθευτή — Ανταγωνιστίκή χρέωση.",
    BTN_NOTICES: "ℹ️ Σημειώσεις & Αποποιήσεις Ευθυνών",
    NOTICES_TITLE: "Σημειώσεις & Αποποιήσεις Ευθυνών",
    NOTICES_TAB_ASSUMPTIONS: "Σημειώσεις/Παραδοχές",
    NOTICES_TAB_LEGAL: "Αποποιήσεις Ευθυνών",
    FOOTER_ORG_NAME: "Ρυθμιστική Αρχή Ενέργειας Κύπρου",
    FOOTER_ADDRESS: "Αγίας Παρασκευής 20,<br>2002 Στρόβολος,<br>Λευκωσία, Κύπρος",
    FOOTER_POBOX_CITY: "1305 ΛΕΥΚΩΣΙΑ",
    FOOTER_POSTAL: "Ταχυδρομική Διεύθυνση",
    FOOTER_POBOX: "Ταχ. Θυρ.",
    FOOTER_PHONE: "Τηλέφωνο",
    FOOTER_FAX: "Φαξ",
    FOOTER_EMAIL: "Ηλ. Ταχυδρομείο",
    FOOTER_CONTACT: "Επικοινωνία",
    BTN_ESTIMATE: "🧮 Εκτίμηση",
    EST_TITLE: "Εκτίμηση κατανάλωσης",
    EST_DESC: "Απαντήστε μερικές ερωτήσεις για να λάβετε μια κατά προσέγγιση εκτίμηση της ετήσιας ηλεκτρικής σας κατανάλωσης.",
    EST_DWELLING: "Τύπος κατοικίας",
    EST_D_STUDIO: "Studio / γκαρσονιέρα (< 40 τ.μ.)",
    EST_D_APT1: "Μικρό διαμέρισμα — 1 υπνοδωμάτιο (40–65 τ.μ.)",
    EST_D_APT2: "Διαμέρισμα — 2 υπνοδωμάτια (65–90 τ.μ.)",
    EST_D_APT3: "Διαμέρισμα — 3 υπνοδωμάτια (90–120 τ.μ.)",
    EST_D_SEMI: "Ημιανεξάρτητη κατοικία",
    EST_D_DET_S: "Μονοκατοικία — μικρή (140–200 τ.μ.)",
    EST_D_DET_L: "Μονοκατοικία / Βίλα (> 200 τ.μ.)",
    EST_PERSONS: "Αριθμός ενοίκων",
    EST_AC: "Κλιματισμός",
    EST_AC_NONE: "Κανένας",
    EST_AC_LIGHT: "Ελαφρύς — 1 κλιματιστικό, περιστασιακή χρήση",
    EST_AC_MOD: "Μέτριος — 2–3 κλιματιστικά",
    EST_AC_HEAVY: "Έντονος — 3+ κλιματιστικά, όλο το καλοκαίρι",
    EST_WATER: "Θέρμανση νερού",
    EST_WATER_SOLAR: "Ηλιακός θερμοσίφωνας (ηλεκτρικό backup)",
    EST_WATER_ELEC: "Ηλεκτρικός θερμοσίφωνας",
    EST_WATER_OTHER: "Αέριο / άλλο",
    EST_COOKING: "Ηλεκτρική κουζίνα / φούρνος",
    EST_YES: "Ναι",
    EST_NO: "Όχι",
    EST_CALC: "Υπολογισμός",
    EST_USE: "Χρήση εκτίμησης",
    EST_RESULT_LBL: "Εκτιμώμενη ετήσια κατανάλωση",
    EST_RESULT_UNIT: "kWh / έτος",
    EST_NOTE: "Ενδεικτική εκτίμηση μόνο. Για ακριβέστερη σύγκριση, χρησιμοποιήστε την πραγματική ετήσια κατανάλωσή σας από τον λογαριασμό ρεύματος.",
    EST_METH_TITLE: "Μεθοδολογία & πηγές δεδομένων",
    EST_METH_BODY: `<p><strong>Αποποίηση ευθύνης:</strong> Το εργαλείο παρέχει ενδεικτικές εκτιμήσεις βάσει τυπικών προτύπων κατανάλωσης κυπριακών νοικοκυριών. Δεν αντικατοπτρίζει τις πραγματικές ενδείξεις του μετρητή, τους όρους συμβολαίου ή την ενεργειακή απόδοση των συγκεκριμένων συσκευών σας. Η πραγματική κατανάλωση μπορεί να διαφέρει σημαντικά ανάλογα με τη θερμομόνωση, τη συμπεριφορά των ενοίκων, την ηλικία των συσκευών και τις εποχιακές διακυμάνσεις. Το εργαλείο δεν αποτελεί εμπορική προσφορά ή ενεργειακή συμβουλή.</p>
<p><strong>Βασική κατανάλωση ανά τύπο κατοικίας</strong> — προκύπτει από στατιστικά στοιχεία νοικοκυριών της Eurostat (NRG_D_HHQ, Κύπρος) και μέσες χρεώσεις ΑΗΚ ανά οικιακή σύνδεση. Ο κυπριακός μέσος όρος ~5.000–5.500 kWh/έτος αναπαράγεται από τυπικό διαμέρισμα 2 υπνοδωματίων + μέτριος κλιματισμός + ηλιακός θερμοσίφωνας.</p>
<table>
<tr><th>Κατοικία</th><th>Βάση kWh/έτος</th><th>Βάση εκτίμησης</th></tr>
<tr><td>Studio</td><td>1.200</td><td>Ελάχιστο φορτίο, 1 άτομο, μικρή επιφάνεια</td></tr>
<tr><td>Διαμ. 1 ΥΔ</td><td>1.800</td><td>Βασικές συσκευές (φωτισμός, ψυγείο, TV, πλυντήριο)</td></tr>
<tr><td>Διαμ. 2 ΥΔ</td><td>2.600</td><td>Μέσες χρεώσεις ΑΗΚ ανά μέγεθος σύνδεσης</td></tr>
<tr><td>Διαμ. 3 ΥΔ</td><td>3.500</td><td>Περισσότερα κυκλώματα, περισσότερες συσκευές</td></tr>
<tr><td>Ημιανεξάρτητη</td><td>4.500</td><td>Επιπλέον όροφοι, εξωτερικός φωτισμός</td></tr>
<tr><td>Μονοκατοικία μικρή</td><td>6.000</td><td>Τυπικές χρεώσεις ΑΗΚ για 140–200 τ.μ.</td></tr>
<tr><td>Μονοκατοικία / Βίλα</td><td>9.000</td><td>Αντλία πισίνας, ηλεκτρικές πύλες, κοινόχρηστοι χώροι</td></tr>
</table>
<p><strong>Ανά επιπλέον άτομο (+600 kWh):</strong> Ηλεκτρονικές συσκευές ~150, πλυντήριο ~100, μαγειρική ~100, ζεστό νερό ~150, φωτισμός ~100 kWh/έτος. Συνάδει με τα δεδομένα ODYSSEE-MURE για κατά κεφαλήν κατανάλωση κυπριακού νοικοκυριού.</p>
<p><strong>Κλιματισμός</strong> — η Κύπρος έχει τις υψηλότερες βαθμοημέρες ψύξης στην ΕΕ. Ο κλιματισμός λειτουργεί συνήθως Μάιο–Οκτώβριο (~150–180 ημέρες). Υποθέτουμε 1,5 kW ανά μονάδα: Ελαφρύς: 1 μον. × 4 ώρ./ημ. × 120 ημ. ≈ 700 kWh· Μέτριος: 2 μον. × 6 ώρ./ημ. × 140 ημ. × 0,7 ≈ 1.800 kWh· Έντονος: 3 μον. × 8 ώρ./ημ. × 150 ημ. × 0,65 ≈ 3.500 kWh.</p>
<p><strong>Θέρμανση νερού:</strong> Ηλιακός + backup: ~300 kWh (ηλεκτρικό backup Οκτ–Μαρ, κάλυψη ηλιακού ~80%). Ηλεκτρικός θερμοσίφωνας: ~1.200 kWh (δεξαμενή 80L, αντίσταση 2 kW, ~2 ώρ./ημ. × ~220 ημ.). Αέριο/άλλο: χωρίς συμβολή στην ηλεκτρική κατανάλωση.</p>
<p><strong>Ηλεκτρική κουζίνα (+400 kWh):</strong> Ευρωπαϊκές μελέτες (ADEME, Energy Saving Trust) αναφέρουν 300–500 kWh/έτος για τυπική οικιακή ηλεκτρική μαγειρική. Χρησιμοποιείται ο μέσος όρος.</p>
<div class="est-meth-sources"><strong>Πηγές:</strong> Eurostat NRG_D_HHQ · ODYSSEE-MURE CY οικιακός τομέας · Ετήσια Έκθεση ΑΗΚ · Ετήσια Έκθεση ΡΑΕΚ · JRC μελέτη Θέρμανσης &amp; Ψύξης (βαθμοημέρες ψύξης Κύπρος)</div>`,
    MONTHS: ["Ιαν","Φεβ","Μαρ","Απρ","Μαι","Ιουν","Ιουλ","Αυγ","Σεπ","Οκτ","Νοε","Δεκ"]
  }
};
let lang = 'el'; // default Greek
function T(key, vars){
  const s=(LANG[lang]||LANG.en)[key]||(LANG.en)[key]||key;
  if(!vars) return s;
  return Object.entries(vars).reduce((a,[k,v])=>a.replaceAll('{'+k+'}',v),s);
}
function pricingTag(p){
  const map={Fixed:'TAG_FIXED',ToU:'TAG_TOU',Dynamic:'TAG_DYNAMIC',Variable:'TAG_VARIABLE'};
  return map[p]?T(map[p]):p;
}
function fmtLocalTs(isoStr){
  try{
    const d=new Date(isoStr);
    return d.toLocaleDateString('en-GB',{day:'2-digit',month:'short',year:'numeric'})+
      ' '+d.toLocaleTimeString('en-GB',{hour:'2-digit',minute:'2-digit'});
  } catch(e){return isoStr||'—';}
}
function fmtLocalDate(isoStr){
  try{ return new Date(isoStr).toLocaleDateString('en-GB',{day:'2-digit',month:'short',year:'numeric'}); }
  catch(e){return isoStr||'—';}
}

// MONTHS is language-aware — defined after LANG
function getMonths(){ return (LANG[lang]||LANG.en).MONTHS; }

function setLang(l){
  lang=l;
  document.getElementById('lang-btn-en').classList.toggle('active',l==='en');
  document.getElementById('lang-btn-el').classList.toggle('active',l==='el');
  renderPage();
  if(connCollapsed) updateConnSummary();
  if(document.getElementById('notices-overlay').style.display!=='none')
    switchNoticesTab(_noticesTab);
}

/* Accessible mode toggle — guaranteed-AA-contrast colors + strong focus outlines */
function updateA11yToggleUI(on){
  const btn=document.getElementById('a11y-toggle');
  if(!btn) return;
  btn.setAttribute('aria-pressed',on?'true':'false');
  document.getElementById('a11y-toggle-label').textContent=T(on?'BTN_A11Y_ON':'BTN_A11Y_OFF');
}
function toggleA11yMode(){
  const on=!document.documentElement.classList.contains('a11y-mode');
  document.documentElement.classList.toggle('a11y-mode',on);
  try{ localStorage.setItem('elec-a11y-mode',on?'1':'0'); }catch(e){}
  updateA11yToggleUI(on);
}
(function initA11yMode(){
  let on=false;
  try{ on=localStorage.getItem('elec-a11y-mode')==='1'; }catch(e){}
  if(on) document.documentElement.classList.add('a11y-mode');
})();

const PALETTE=[
  '#1a3a5e','#b06c2c','#2f6f8f','#5b7a52','#8a5a83',
  '#a85438','#3f6f6a','#7a6a4f','#4a5a8a','#6a8f3f',
  '#9f6a2e','#2e7a6a','#705a8f','#3f7a52','#9f4a52'
];
// Shared Chart.js styling — premium, governmental, legible
const CHART_FONT_MONO="'Roboto'";
const CHART_FONT_SANS="'Roboto'";
const CHART_GRID='rgba(21,32,46,0.055)';
const CHART_TICK='#8893a3';
function chartTooltip(){
  return {
    backgroundColor:'#11283f',titleColor:'#ffffff',bodyColor:'#d6e2f0',
    padding:11,cornerRadius:8,boxPadding:5,
    borderColor:'rgba(255,255,255,.10)',borderWidth:1,
    titleFont:{family:CHART_FONT_SANS,weight:'600',size:12},
    bodyFont:{family:CHART_FONT_MONO,size:11.5},
    usePointStyle:true,
    callbacks:{label:ctx=>' '+(ctx.dataset.label||'')+': €'+(ctx.parsed.y??0).toFixed(2)}
  };
}
if(window.Chart){
  Chart.defaults.font.family=CHART_FONT_MONO;
  Chart.defaults.color=CHART_TICK;
}
// Line dash patterns — cycles independently so same-colour lines are still distinguishable
const DASH_PATTERNS=[[],[5,3],[10,3],[3,3],[8,3,2,3]];
function esc(s){ return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;'); }
// Greek typographic convention: capital letters drop the tonos (accent) —
// CSS text-transform:uppercase does NOT reliably strip it across browsers, so
// dynamic/translated text destined for all-caps display must be uppercased
// here in JS instead of via CSS. Use this (not CSS text-transform:uppercase)
// for ANY text that may contain Greek — no-op on non-Greek text.
const GREEK_TONOS_MAP={'ά':'α','έ':'ε','ή':'η','ί':'ι','ό':'ο','ύ':'υ','ώ':'ω','ΐ':'ι','ΰ':'υ','Ά':'Α','Έ':'Ε','Ή':'Η','Ί':'Ι','Ό':'Ο','Ύ':'Υ','Ώ':'Ω'};
function upperText(s){ return String(s==null?'':s).replace(/[ΆΈΉΊΌΎΏάέήίόύώΐΰ]/g,c=>GREEK_TONOS_MAP[c]||c).toUpperCase(); }
// Only allow http(s) URLs in href — blocks javascript:/data: scheme injection via supplier-entered website fields.
function safeUrl(u){ u=String(u==null?'':u).trim(); return /^https?:\/\//i.test(u) ? esc(u) : '#'; }
let cfg=null, openCards=new Set(), _resultsVisible=false;
window._lastCalcResults={};
const chartRegistry={};
function destroyAllCharts(){
  Object.keys(chartRegistry).forEach(k=>{
    try{ chartRegistry[k].destroy(); }catch(e){}
    delete chartRegistry[k];
  });
}
let inputMode='annual'; // 'annual' | 'monthly'
let _billingPeriod=1; // billing period in months: 1=monthly, 2=bimonthly, 3=quarterly
let customerType='domestic'; // 'domestic' | 'ci'
let loadEntitlement='lt70';  // 'lt70' | 'gt70'

function setCustomerType(type){
  customerType=type;
  document.getElementById('tab-domestic').classList.toggle('active',type==='domestic');
  document.getElementById('tab-ci').classList.toggle('active',type==='ci');
  document.getElementById('ci-options').style.display=type==='ci'?'':'none';
  document.getElementById('tab-domestic').innerHTML=T('TAB_DOMESTIC');
  document.getElementById('tab-ci').innerHTML=T('TAB_CI');
  // Update load entitlement labels
  const leHdr=document.getElementById('lbl-load-ent');
  if(leHdr) leHdr.textContent=T('LBL_LOAD_ENT');
  const llLt=document.querySelector('#le-lt');
  const llGt=document.querySelector('#le-gt');
  if(llLt) llLt.innerHTML=`<input type="radio" name="le" value="lt70" ${loadEntitlement==='lt70'?'checked':''}> ${T('LE_LT70')}`;
  if(llGt) llGt.innerHTML=`<input type="radio" name="le" value="gt70" ${loadEntitlement==='gt70'?'checked':''}> ${T('LE_GT70')}`;
  // Update voltage/pricing labels
  const vLabel=document.querySelector('#ci-options .ff label');
  if(vLabel) vLabel.textContent=T('LBL_VOLTAGE');
  const pLabel=document.querySelector('[for="sel-pricing"]');
  if(pLabel) pLabel.textContent=T('LBL_PRICING');
  applyFilters();
}

function onVoltageChange(){
  const v=document.getElementById('sel-voltage').value;
  // Hide load entitlement for HV
  document.getElementById('le-field').style.display=(v==='HV')?'none':'';
  applyFilters();
}

function setLoadEntitlement(val){
  loadEntitlement=val;
  document.getElementById('le-lt').classList.toggle('active',val==='lt70');
  document.getElementById('le-gt').classList.toggle('active',val==='gt70');
  applyFilters();
}

function getFilterParams(){
  if(customerType==='domestic'){
    return {voltage:'LV', contracts:['Domestic'], le:null};
  } else {
    const v=document.getElementById('sel-voltage')?.value||'LV';
    const le=v==='HV'?null:loadEntitlement;
    return {voltage:v, contracts:['Commercial','Industrial'], le};
  }
}

/* ── Mode toggle ── */
function setMode(mode){
  inputMode=mode;
  document.getElementById('btn-annual').classList.toggle('active',mode==='annual');
  document.getElementById('btn-monthly').classList.toggle('active',mode==='monthly');
  document.getElementById('mode-annual').style.display=mode==='annual'?'':'none';
  document.getElementById('mode-monthly').style.display=mode==='monthly'?'':'none';
  document.getElementById('est-trigger-btn').style.display=mode==='annual'?'':'none';
  document.getElementById('btn-annual').textContent=T('BTN_ANNUAL');
  document.getElementById('btn-monthly').textContent=T('BTN_MONTHLY');
  const hint=document.getElementById('consumption-hint');
  if(hint){
    hint.style.display=mode==='annual'?'':'none';
    if(mode==='annual') hint.textContent=T('HINT_ANNUAL');
  }
  // Update input labels
  const annLabel=document.querySelector('#mode-annual label');
  if(annLabel) annLabel.textContent=T('LBL_ANNUAL_KWH');
  const moLabel=document.getElementById('monthly-kwh-label');
  if(moLabel) moLabel.textContent=T('MONTHLY_CONS_LBL');
  const units=document.querySelectorAll('.kwh-unit');
  if(units[0]) units[0].textContent=T('UNIT_KWH_YEAR');
  const moUnit=document.getElementById('monthly-kwh-unit');
  if(moUnit) moUnit.textContent=T('MONTHLY_UNIT_'+_billingPeriod);
  const bcLbl=document.getElementById('billing-cycle-lbl');
  if(bcLbl) bcLbl.textContent=T('BILLING_CYCLE');
  const bpKeys=['BILLING_M1','BILLING_M2'];
  [1,2].forEach((p,i)=>{ const b=document.getElementById('bp-btn-'+p); if(b) b.textContent=T(bpKeys[i]); });
  updateMonthlyCalcNote();
  applyFilters();
}

function updateMonthlyCalcNote(){
  const note=document.getElementById('monthly-calc-note');
  if(!note) return;
  const raw=parseFloat(document.getElementById('monthly-kwh').value)||0;
  if(raw>0){
    const month=new Date().toLocaleDateString(lang==='el'?'el-GR':'en-GB',{month:'long'});
    note.textContent=T('MONTHLY_CALC_NOTE',{MONTH:month});
    note.style.display='';
  } else {
    note.style.display='none';
  }
}

// Pricing is now computed server-side per keystroke — debounce the two
// consumption fields so fast typing doesn't fire a request per digit.
let _kwhDebounceTimer=null;
function _debouncedApplyFilters(){
  clearTimeout(_kwhDebounceTimer);
  _kwhDebounceTimer=setTimeout(applyFilters,300);
}
function onAnnualInput(){_debouncedApplyFilters();}
function onMonthlyInput(){
  updateMonthlyCalcNote();
  _debouncedApplyFilters();
}
function setBillingPeriod(n){
  _billingPeriod=n;
  [1,2].forEach(p=>{ const b=document.getElementById('bp-btn-'+p); if(b) b.classList.toggle('active',p===n); });
  const moUnit=document.getElementById('monthly-kwh-unit');
  if(moUnit) moUnit.textContent=T('MONTHLY_UNIT_'+n);
  onMonthlyInput();
}
function periodCost(annualCost){ return annualCost*_billingPeriod/12; }
function periodCostLabel(){
  if(_billingPeriod===1) return T('LBL_SUP_MONTH');
  return T('LBL_SUP_2MO');
}

/* ── Progressive collapse: connection only ── */
let connCollapsed=false;
function setConnCollapsed(v){
  connCollapsed=v;
  const c=document.getElementById('conn-card');
  if(c) c.classList.toggle('collapsed',v);
  const h=document.getElementById('cc-head');
  if(h) h.setAttribute('aria-expanded',v?'false':'true');
  if(v) updateConnSummary();
}
function toggleConn(){ setConnCollapsed(!connCollapsed); }
// Collapse the connection box once the user moves on to entering consumption
// — not on every field change within the box itself, which used to collapse
// it out from under the very field the user was still using (and for
// keyboard users, orphaned focus on a now-invisible control).
function onConsumptionFocus(){ setConnCollapsed(true); }
function updateConnSummary(){
  const chips=[];
  const ct=document.querySelector('.ctype-tab.active');
  if(ct) chips.push(ct.textContent.trim());
  if(customerType==='ci'){
    const v=document.querySelector('#sel-voltage option:checked');
    if(v) chips.push(v.textContent.trim());
    const le=document.querySelector('.le-option.active');
    if(le) chips.push(le.textContent.replace(/\s+/g,' ').trim());
  }
  const pr=document.querySelector('#sel-pricing option:checked');
  if(pr) chips.push(pr.textContent.trim());
}

function regRateStr(k,v){
  if(v.perKwh) return '€'+v.rate.toFixed(4)+'/kWh';
  if(k==='mdm'){
    const freqTitle=T(v.invoiceMonths===1?'MDM_BILLED_MONTHLY':'MDM_BILLED_BIMONTHLY');
    return `<span title="${esc(freqTitle)}">${T('LBL_FIXED_ROW_MDM',{N:v.rate.toFixed(2)})}</span>`;
  }
  return T('LBL_FIXED_ROW',{N:v.rate.toFixed(2)});
}

/* Notices modal */
let _noticesTab='assumptions';
function openNotices(){
  if(!cfg.notices) return;
  switchNoticesTab('about');
  document.getElementById('notices-overlay').style.display='flex';
}
function closeNotices(){
  document.getElementById('notices-overlay').style.display='none';
}
function openRegInfo(titleKey,descKey){
  document.getElementById('reg-info-title').textContent=T(titleKey);
  document.getElementById('reg-info-body').textContent=T(descKey);
  document.getElementById('reg-info-overlay').style.display='flex';
}
function closeRegInfo(){
  document.getElementById('reg-info-overlay').style.display='none';
}
// Shared attributes for the small "ⓘ" info triggers (regulated-charge rows, FPA
// labels) — keyboard-operable custom controls, not native buttons/links. Class
// (not inline style) so call sites remain free to add their own inline color.
function regInfoAttrs(titleKey,descKey){
  return `class="reg-info-trigger" role="button" tabindex="0" data-action="openRegInfo" data-arg="${esc(titleKey)}" data-arg2="${esc(descKey)}"`;
}
function switchNoticesTab(tab){
  _noticesTab=tab;
  document.getElementById('ntab-about').classList.toggle('active',tab==='about');
  document.getElementById('ntab-assumptions').classList.toggle('active',tab==='assumptions');
  document.getElementById('ntab-legal').classList.toggle('active',tab==='legal');
  const body=document.getElementById('notices-body');
  const n=cfg.notices||{};
  let html='';
  if(tab==='about'){
    html=T('ABOUT_CONTENT');
  } else if(tab==='assumptions'){
    html=(lang==='el'?n.assumptions_el:n.assumptions_en)||n.assumptions_en||n.assumptions_el||n.assumptions||'';
  } else {
    html=(lang==='el'?n.legal_el:n.legal_en)||n.legal_en||n.legal_el||n.legal||'';
  }
  body.innerHTML=html?DOMPurify.sanitize(html):(tab==='assumptions'
    ?'<p style="color:var(--text3)">'+(lang==='el'?'Δεν έχουν εισαχθεί παραδοχές ακόμα.':'No assumptions have been added yet.')+'</p>'
    :'<p style="color:var(--text3)">'+(lang==='el'?'Δεν υπάρχουν νομικές ανακοινώσεις ακόμα.':'No legal notices have been added yet.')+'</p>');
}

/* Supplier contact modal */
function openSupContact(name){
  const s=cfg.supplierDetails?.find(x=>x.name===name)||(cfg.suppliers||[]).map(x=>typeof x==='string'?{name:x}:x).find(x=>x.name===name);
  if(!s){return;}
  document.getElementById('sup-contact-name').textContent=s.name;
  const rows=[];
  // Licence is internal — not shown to customers
  if(s.address) rows.push(`<div class="sup-contact-row"><span class="sup-contact-icon">📍</span><span>${esc(s.address)}</span></div>`);
  if(s.tel) rows.push(`<div class="sup-contact-row"><span class="sup-contact-icon">📞</span><a href="tel:${esc(s.tel)}">${esc(s.tel)}</a></div>`);
  if(s.email) rows.push(`<div class="sup-contact-row"><span class="sup-contact-icon">✉️</span><a href="mailto:${esc(s.email)}">${esc(s.email)}</a></div>`);
  if(s.website) rows.push(`<div class="sup-contact-row"><span class="sup-contact-icon">🌐</span><a href="${safeUrl(s.website)}" target="_blank" rel="noopener">${esc(s.website)}</a></div>`);
  if(!rows.length) rows.push('<div style="font-size:13px;color:var(--text3)">No contact details available yet.</div>');
  document.getElementById('sup-contact-body').innerHTML=rows.join('');
  document.getElementById('sup-contact-overlay').style.display='flex';
}
function closeSupContact(){
  document.getElementById('sup-contact-overlay').style.display='none';
}

/* Report an issue modal — Article 121(ζ). openReportIssue() with no args opens
   the general/footer variant (no tariff context, tariff_id sent as null). */
const REPORT_CATEGORIES=['incorrect_price','terms_mismatch','broken_link','other'];
let _reportTariffId=null;
function openReportIssue(id,name,supplier){
  _reportTariffId=id||null;
  const isGeneral=!id;
  document.getElementById('report-modal-title').textContent=T(isGeneral?'REPORT_MODAL_TITLE_GENERAL':'REPORT_MODAL_TITLE');
  document.getElementById('report-tariff-block').style.display=isGeneral?'none':'';
  document.getElementById('report-tariff-name').textContent=name||'';
  document.getElementById('report-supplier-name').textContent=supplier||'';
  document.getElementById('report-category').value='other';
  document.getElementById('report-note').value='';
  document.getElementById('report-email').value='';
  document.getElementById('report-error').style.display='none';
  document.getElementById('report-success').style.display='none';
  const offline=window._reportingUnavailable===true;
  document.getElementById('report-offline-notice').style.display=offline?'':'none';
  document.getElementById('report-category').style.display=offline?'none':'';
  document.getElementById('report-note').style.display=offline?'none':'';
  document.getElementById('report-email').style.display=offline?'none':'';
  document.getElementById('report-submit-btn').style.display=offline?'none':'';
  document.getElementById('report-overlay').style.display='flex';
}
function closeReportIssue(){
  document.getElementById('report-overlay').style.display='none';
}
async function submitReportIssue(){
  const btn=document.getElementById('report-submit-btn');
  const errEl=document.getElementById('report-error');
  errEl.style.display='none';
  const email=document.getElementById('report-email').value.trim();
  const note=document.getElementById('report-note').value.trim();
  if(!note){
    errEl.textContent=T('REPORT_NOTE_REQUIRED');
    errEl.style.display='';
    return;
  }
  if(!email){
    errEl.textContent=T('REPORT_EMAIL_REQUIRED');
    errEl.style.display='';
    return;
  }
  btn.disabled=true;
  try{
    const resp=await fetch('/api/public/report-tariff',{
      method:'POST', headers:{'Content-Type':'application/json'},
      body:JSON.stringify({
        tariff_id:_reportTariffId,
        category:document.getElementById('report-category').value||'other',
        note:note,
        reporter_email:email,
      })
    });
    if(!resp.ok) throw new Error('status '+resp.status);
    document.getElementById('report-category').style.display='none';
    document.getElementById('report-note').style.display='none';
    document.getElementById('report-email').style.display='none';
    btn.style.display='none';
    document.getElementById('report-success').style.display='';
  }catch(e){
    errEl.textContent=T('REPORT_ERROR');
    errEl.style.display='';
  }finally{
    btn.disabled=false;
  }
}

/* Sample invoice modal — bill-styled breakdown fetched on demand from
   POST /api/public/sample-invoice, gated entirely by cfg.sampleInvoiceEnabled
   (admin toggle). Laid out to resemble
   a real EAC bill (letterhead info block, itemised charges, highlighted
   total) — customer name, address, account and meter numbers are all fixed
   placeholders, never real. */
async function openSampleInvoice(tariffId,btn){
  const t=cfg.tariffs.find(x=>x.id===tariffId);
  if(!t) return;
  const showOffers=document.getElementById('offers-check')?.checked!==false;
  const origBtnHtml=btn?btn.innerHTML:null;
  if(btn){ btn.disabled=true; btn.innerHTML='<span class="spinner" style="width:12px;height:12px"></span> '+T('CALC_LOADING'); }
  let data;
  try{
    const resp=await fetch('/api/public/sample-invoice',{
      method:'POST', headers:{'Content-Type':'application/json'},
      body:JSON.stringify({
        tariffId, inputMode,
        annualKwh:parseFloat(document.getElementById('annual-kwh').value)||0,
        monthlyKwh:parseFloat(document.getElementById('monthly-kwh').value)||0,
        billingPeriod:_billingPeriod, offersEnabled:showOffers,
        discountOverrides:window._discountState||{}
      })
    });
    if(!resp.ok) throw new Error('status '+resp.status);
    data=await resp.json();
  }catch(e){ return; }
  finally{ if(btn){ btn.disabled=false; btn.innerHTML=origBtnHtml; } }
  if(!data) return;
  data.t=t;
  data.startDate=new Date(data.startDate+'T00:00:00');
  data.endDate=new Date(data.endDate+'T00:00:00');
  document.getElementById('sample-invoice-title').innerHTML=
    `<div class="invoice-title-supplier">${esc(upperText(t.supplier))}</div>`+
    `<div class="invoice-title-tariff">${esc(t.name)}</div>`;
  document.getElementById('sample-invoice-body').innerHTML=renderSampleInvoiceBody(data);
  document.getElementById('sample-invoice-overlay').style.display='flex';
}
function closeSampleInvoice(){
  document.getElementById('sample-invoice-overlay').style.display='none';
}
function fmtInvoiceDate(d){ return d.toLocaleDateString('en-GB',{day:'2-digit',month:'2-digit',year:'numeric'}); }
function renderSampleInvoiceBody(data){
  const {t,startDate,endDate,monthsCount,periodKwh,energy,fpa,standing,
    energyFull,fpaFull,standingFull,supplierTotal,fpaRate,
    grid,pso,res,mdm,mdmRegulated,vat,vatBase,totalBeforeVat,amountDue,
    energyRate,gridRate,psoRate,resRate,mdmRate,mdmInvoices,
    isToU,peakKwh,offPeakKwh,peakEnergy,offPeakEnergy,peakEnergyFull,offPeakEnergyFull,peakRate,offPeakRate}=data;
  const showFpa=fpaRate>0;
  const kwhFmt=periodKwh.toFixed(0);
  // formula is computed from the pre-discount base rate/qty, so it reconciles
  // to fullValue, not valueEur — when a discount is active those differ, so
  // show both (strikethrough full, actual due), same convention the ranked
  // comparison list uses elsewhere on this page.
  const row=(labelHtml,valueEur,formula,fullValue)=>{
    const hasDisc=fullValue!=null&&fullValue>valueEur+0.005;
    const valueHtml=hasDisc
      ?`<span style="text-decoration:line-through;color:var(--text3);font-size:11px;margin-right:4px">€${fullValue.toFixed(2)}</span>€${valueEur.toFixed(2)}`
      :`€${valueEur.toFixed(2)}`;
    return `<tr><td>${labelHtml}</td><td class="calc-col">${formula?`<span class="invoice-calc">${formula}</span>`:''}</td><td class="cost-col">${valueHtml}</td></tr>`;
  };
  const energyLabel=`<span ${regInfoAttrs('TH_ENERGY','SAMPLE_INV_ENERGY_DESC')}>${esc(T('TH_ENERGY'))} <span style="font-size:11px;opacity:.6">ℹ</span></span>`;
  // Only Fixed tariffs have one true €/kWh rate — Dynamic/Variable still charge
  // a different rate per slot/tier with no single real rate to show, so their
  // formula line stays omitted. ToU has exactly two real rates (peak/off-peak),
  // so it gets its own two-row breakdown below instead of one blended line.
  const energyFormula=t.pricing==='Fixed'?`${kwhFmt} kWh × €${energyRate.toFixed(4)}/kWh`:null;
  const peakEnergyLabel=`<span ${regInfoAttrs('SAMPLE_INV_ENERGY_PEAK','SAMPLE_INV_ENERGY_DESC')}>${esc(T('SAMPLE_INV_ENERGY_PEAK'))} <span style="font-size:11px;opacity:.6">ℹ</span></span>`;
  const offPeakEnergyLabel=`<span ${regInfoAttrs('SAMPLE_INV_ENERGY_OFFPEAK','SAMPLE_INV_ENERGY_DESC')}>${esc(T('SAMPLE_INV_ENERGY_OFFPEAK'))} <span style="font-size:11px;opacity:.6">ℹ</span></span>`;
  const peakEnergyFormula=`${peakKwh.toFixed(0)} kWh × €${peakRate.toFixed(4)}/kWh`;
  const offPeakEnergyFormula=`${offPeakKwh.toFixed(0)} kWh × €${offPeakRate.toFixed(4)}/kWh`;
  const fpaLabel=`<span ${regInfoAttrs('FPA_FULL','FPA_DESC')}>${esc(T('FPA_FULL'))} <span style="font-size:11px;opacity:.6">ℹ</span></span>`;
  const fpaFormula=`${kwhFmt} kWh × €${fpaRate.toFixed(4)}/kWh`;
  const standingLabel=`<span ${regInfoAttrs('TH_STANDING','STANDING_DESC')}>${esc(T('TH_STANDING'))} <span style="font-size:11px;opacity:.6">ℹ</span></span>`;
  const standingFormula=`€${(t.standing||0).toFixed(2)}/mo × ${monthsCount}`;
  // MDM sits with whichever bucket actually reflects who set the rate — the
  // regulated supplier (e.g. EAC) case uses the CERA-set rate, so it belongs
  // with the regulated charges, not the competitive ones (mdmForTariff() server-side).
  const mdmInfo=mdmRegulated?['REGULATED_MDM','REG_MDM_DESC']:['MDM_SUPPLIER','MDM_SUPPLIER_DESC'];
  const mdmFormula=`€${mdmRate.toFixed(2)} × ${mdmInvoices%1===0?mdmInvoices.toFixed(0):mdmInvoices.toFixed(2)}`;
  const mdmRowHtml=`<tr style="${mdmRegulated?'background:rgba(59,130,246,.04)':''}">
      <td style="color:${mdmRegulated?'#1d4ed8':'var(--text2)'}" ${regInfoAttrs(mdmInfo[0],mdmInfo[1])}>${esc(T(mdmInfo[0]))} <span style="font-size:11px;opacity:.6">ℹ</span></td>
      <td class="calc-col"><span class="invoice-calc">${mdmFormula}</span></td>
      <td class="cost-col" style="color:${mdmRegulated?'#1d4ed8':'var(--text2)'}">€${mdm.toFixed(2)}</td>
    </tr>`;
  const regRow=(key,val,rate)=>{
    const info={grid:['REGULATED_GRID','REG_GRID_DESC'],pso:['REGULATED_PSO','REG_PSO_DESC']}[key];
    const formula=`${kwhFmt} kWh × €${rate.toFixed(4)}/kWh`;
    return `<tr style="background:rgba(59,130,246,.04)">
      <td style="color:#1d4ed8" ${regInfoAttrs(info[0],info[1])}>${esc(T(info[0]))} <span style="font-size:11px;opacity:.6">ℹ</span></td>
      <td class="calc-col"><span class="invoice-calc">${formula}</span></td>
      <td class="cost-col" style="color:#1d4ed8">€${val.toFixed(2)}</td>
    </tr>`;
  };
  const competitiveTotal=supplierTotal+(mdmRegulated?0:mdm);
  const regulatedTotal=grid+pso+(mdmRegulated?mdm:0);
  const resFormula=`${kwhFmt} kWh × €${resRate.toFixed(4)}/kWh`;
  const infoRow=(label,value)=>`<div class="invoice-info-row"><span class="invoice-info-lbl">${esc(label)}</span><span class="invoice-info-val">${esc(value)}</span></div>`;
  return `
    <div class="invoice-banner">${T('SAMPLE_INV_BANNER')}</div>
    <div class="invoice-letterhead">
      <div>
        ${infoRow(T('SAMPLE_INV_LBL_NAME'),T('SAMPLE_INV_EX_NAME'))}
        ${infoRow(T('SAMPLE_INV_LBL_ACCOUNT'),T('SAMPLE_INV_EX_ACCOUNT'))}
        ${infoRow(T('SAMPLE_INV_LBL_ADDRESS'),T('SAMPLE_INV_EX_ADDRESS'))}
      </div>
      <div>
        ${infoRow(T('SAMPLE_INV_LBL_SUPPLIER'),t.supplier)}
        ${infoRow(T('SAMPLE_INV_LBL_TARIFF'),t.name)}
        ${infoRow(T('SAMPLE_INV_LBL_METER'),T('SAMPLE_INV_EX_METER'))}
        ${infoRow(T('SAMPLE_INV_LBL_PERIOD'),`${fmtInvoiceDate(startDate)} – ${fmtInvoiceDate(endDate)}`)}
      </div>
    </div>
    <div class="invoice-section-title">${upperText(T('SAMPLE_INV_CHARGES_TITLE'))}</div>
    <div style="overflow-x:auto">
    <table class="mo-table invoice-table">
      <tbody>
        <tr><td colspan="3" class="invoice-section-row">${upperText(T('SAMPLE_INV_SECTION_COMPETITIVE'))}</td></tr>
        ${isToU
          ?row(peakEnergyLabel,peakEnergy,peakEnergyFormula,peakEnergyFull)+row(offPeakEnergyLabel,offPeakEnergy,offPeakEnergyFormula,offPeakEnergyFull)
          :row(energyLabel,energy,energyFormula,energyFull)}
        ${showFpa?row(fpaLabel,fpa,fpaFormula,fpaFull):''}
        ${row(standingLabel,standing,standingFormula,standingFull)}
        ${!mdmRegulated?mdmRowHtml:''}
        <tr class="invoice-subtotal-row"><td colspan="2">${T('SAMPLE_INV_COMPETITIVE_TOTAL')}</td><td class="cost-col">€${competitiveTotal.toFixed(2)}</td></tr>
        <tr><td colspan="3" class="invoice-section-row">${upperText(T('SAMPLE_INV_SECTION_REGULATED'))}</td></tr>
        ${regRow('grid',grid,gridRate)}
        ${regRow('pso',pso,psoRate)}
        ${mdmRegulated?mdmRowHtml:''}
        <tr class="invoice-subtotal-row"><td colspan="2">${T('SAMPLE_INV_REGULATED_TOTAL')}</td><td class="cost-col">€${regulatedTotal.toFixed(2)}</td></tr>
        <tr style="border-top:1.5px solid var(--border2);background:var(--bg3)"><td colspan="2"><strong>${T('SAMPLE_INV_TOTAL_SUBJECT_VAT')}</strong></td><td class="cost-col"><strong>€${vatBase.toFixed(2)}</strong></td></tr>
        <tr>
          <td style="color:#1d4ed8" ${regInfoAttrs('REGULATED_RES','REG_RES_DESC')}>${esc(T('REGULATED_RES'))} <span style="font-size:11px;opacity:.6">ℹ</span> <span style="font-size:10.5px;color:var(--text3)">${T('SAMPLE_INV_RES_NOTE')}</span></td>
          <td class="calc-col"><span class="invoice-calc">${resFormula}</span></td>
          <td class="cost-col" style="color:#1d4ed8">€${res.toFixed(2)}</td>
        </tr>
        <tr style="background:var(--bg3)"><td colspan="2">${T('SAMPLE_INV_TOTAL_BEFORE_VAT')}</td><td class="cost-col">€${totalBeforeVat.toFixed(2)}</td></tr>
        <tr><td colspan="2">${T('SAMPLE_INV_VAT')}</td><td class="cost-col">€${vat.toFixed(2)}</td></tr>
        <tr class="invoice-total-row"><td colspan="2"><strong>${T('SAMPLE_INV_AMOUNT_DUE')}</strong></td><td class="cost-col"><strong>€${amountDue.toFixed(2)}</strong></td></tr>
      </tbody>
    </table>
    </div>
    <div style="font-size:11px;color:var(--text3);margin-top:12px;line-height:1.6">${T('SAMPLE_INV_DISCLAIMER')}</div>
  `;
}

function updateVulnerableRow(){
  const hasVulnerable=(cfg.tariffs||[]).some(t=>t.vulnerable);
  const row=document.getElementById('vulnerable-row');
  if(row) row.style.display=hasVulnerable?'':'none';
  // Also show/hide info button based on whether cases text exists
  const infoBtn=document.getElementById('vulnerable-info-btn');
  if(infoBtn){
    const hasText=cfg.notices&&(cfg.notices.vulnerable_en||cfg.notices.vulnerable_el);
    infoBtn.style.display=hasText?'':'none';
  }
}
function openVulnerableModal(){
  const notices=cfg.notices||{};
  const body=lang==='el'
    ?(notices.vulnerable_el||notices.vulnerable_en||'')
    :(notices.vulnerable_en||notices.vulnerable_el||'');
  if(!body) return;
  document.getElementById('vulnerable-modal-title').textContent=T('TITLE_VULNERABLE_MODAL');
  const bodyEl=document.getElementById('vulnerable-modal-body');
  bodyEl.innerHTML=DOMPurify.sanitize(body);
  // Pasted text often contains spacer paragraphs (<p>&nbsp;</p>) that leave large gaps
  bodyEl.querySelectorAll('p').forEach(p=>{if(!p.textContent.trim()&&!p.querySelector('img'))p.remove();});
  bodyEl.scrollTop=0;
  document.getElementById('vulnerable-overlay').style.display='flex';
}
function closeVulnerableModal(){
  document.getElementById('vulnerable-overlay').style.display='none';
}

function calcNote(t,res){
  if(t.pricing==='Fixed') return null;
  if(t.pricing==='Variable'){
    const resetLabel={1:'monthly',2:'bimonthly',3:'quarterly',6:'semi-annual',12:'annual'}[res.resetMonths]||res.resetMonths+'mo';
    const tierSummary=(res.tierSummary||[]).map(tier=>{
      const range=tier.upTo!=null?tier.from+'–'+tier.upTo:'above '+tier.from;
      const fixed=tier.fixedCharge?(' +€'+parseFloat(tier.fixedCharge).toFixed(2)+'/period'):'';
      return range+' kWh: €'+tier.rate.toFixed(4)+'/kWh'+fixed;
    }).join(' · ');
    return T('CALC_TIERED',{N:resetLabel,TIERS:tierSummary});
  }
  const profileName=res.profileName;
  const hasSlot=!!window._hasSlotDam;
  if(!profileName) return T('CALC_FALLBACK');
  const distNote=inputMode==='monthly'?T('CALC_DIST_FLAT'):'';
  if(t.pricing==='ToU') return T('CALC_TOU',{NOTE:distNote,PROFILE:esc(profileName)});
  return hasSlot?T('CALC_DAM_SLOT',{NOTE:distNote,PROFILE:esc(profileName)})
    :T('CALC_DAM_AVG',{NOTE:distNote,PROFILE:esc(profileName)});
}

function renderPage(){
  // Update all static text elements
  const setText=(id,key)=>{ const el=document.getElementById(id); if(el) el.textContent=T(key); };
  const setHtml=(id,key)=>{ const el=document.getElementById(id); if(el) el.innerHTML=T(key); };
  setText('pg-eyebrow','PAGE_EYEBROW');
  setText('pg-title','PAGE_TITLE');
  setText('pg-desc','PAGE_DESC');
  setText('ct-connection','CARD_CONNECTION');
  setText('ct-consumption','CARD_CONSUMPTION');
  setText('prompt-enter','PROMPT_ENTER');
  setText('notices-open-btn','BTN_NOTICES');
  setText('notices-title','NOTICES_TITLE');
  setText('ntab-about','NOTICES_TAB_ABOUT');
  setText('ntab-assumptions','NOTICES_TAB_ASSUMPTIONS');
  setText('ntab-legal','NOTICES_TAB_LEGAL');
  setText('no-config-title','NO_CONFIG_TITLE');
  setHtml('no-config-body','NO_CONFIG_BODY');
  setText('footer-org-name','FOOTER_ORG_NAME');
  setHtml('footer-address','FOOTER_ADDRESS');
  setText('footer-pobox-city','FOOTER_POBOX_CITY');
  setText('footer-postal','FOOTER_POSTAL');
  setText('footer-pobox-lbl','FOOTER_POBOX');
  setText('footer-phone-lbl','FOOTER_PHONE');
  setText('footer-fax-lbl','FOOTER_FAX');
  setText('footer-email-lbl','FOOTER_EMAIL');
  setText('footer-contact-lbl','FOOTER_CONTACT');
  setText('footer-report-issue-lbl','BTN_REPORT_ISSUE');
  setText('vulnerable-check-label','LBL_VULNERABLE_CHECK');
  setText('vulnerable-info-label','LBL_VULNERABLE_INFO');
  setText('offers-check-label','LBL_OFFERS_CHECK');
  setText('skip-link','SKIP_LINK');
  updateA11yToggleUI(document.documentElement.classList.contains('a11y-mode'));
  setText('report-modal-title','REPORT_MODAL_TITLE');
  setText('report-lbl-tariff','REPORT_LBL_TARIFF');
  setText('report-lbl-supplier','REPORT_LBL_SUPPLIER');
  setText('report-lbl-category','REPORT_LBL_CATEGORY');
  setText('report-lbl-note','REPORT_LBL_NOTE');
  setText('report-lbl-email','REPORT_LBL_EMAIL');
  setText('report-success','REPORT_SUCCESS');
  setText('report-offline-notice','REPORT_OFFLINE');
  setText('report-btn-cancel','BTN_CANCEL');
  setText('report-submit-btn','BTN_SUBMIT_REPORT');
  const reportNoteEl=document.getElementById('report-note');
  if(reportNoteEl) reportNoteEl.placeholder=T('REPORT_NOTE_PLACEHOLDER');
  const reportEmailEl=document.getElementById('report-email');
  if(reportEmailEl) reportEmailEl.placeholder=T('REPORT_EMAIL_PLACEHOLDER');
  const reportCategoryEl=document.getElementById('report-category');
  if(reportCategoryEl){
    const cur=reportCategoryEl.value;
    reportCategoryEl.innerHTML=REPORT_CATEGORIES.map(c=>`<option value="${c}">${esc(T('REPORT_CAT_'+c.toUpperCase()))}</option>`).join('');
    reportCategoryEl.value=cur||'other';
  }
  const backToTop=document.getElementById('back-to-top');
  if(backToTop){ backToTop.title=T('BTN_BACK_TO_TOP'); backToTop.setAttribute('aria-label',T('BTN_BACK_TO_TOP')); }
  // Tabs
  document.getElementById('tab-domestic').innerHTML='🏠 '+T('TAB_DOMESTIC').replace('🏠 ','');
  document.getElementById('tab-ci').innerHTML='🏢 '+T('TAB_CI').replace('🏢 ','');
  // Voltage options
  const vo=document.getElementById('sel-voltage');
  if(vo){ vo.options[0].text=T('OPT_LV'); vo.options[1].text=T('OPT_MV'); vo.options[2].text=T('OPT_HV'); }
  // Pricing options
  const po=document.getElementById('sel-pricing');
  if(po){ po.options[0].text=T('OPT_ALL'); po.options[1].text=T('OPT_FIXED'); po.options[2].text=T('OPT_TOU'); po.options[3].text=T('OPT_VARIABLE'); po.options[4].text=T('OPT_VARIABLE_TIERED'); }
  // Field labels
  const vLbl=document.querySelector('[for="sel-voltage"]');
  if(vLbl) vLbl.textContent=T('LBL_VOLTAGE');
  const pLbl=document.querySelector('[for="sel-pricing"]');
  if(pLbl) pLbl.textContent=T('LBL_PRICING');
  setText('lbl-load-ent','LBL_LOAD_ENT');
  // Load entitlement labels
  document.getElementById('le-lt').childNodes[1].textContent=' '+T('LE_LT70');
  document.getElementById('le-gt').childNodes[1].textContent=' '+T('LE_GT70');
  // Mode buttons
  document.getElementById('btn-annual').textContent=T('BTN_ANNUAL');
  document.getElementById('btn-monthly').textContent=T('BTN_MONTHLY');
  // Estimator trigger button
  setText('est-trigger-btn','BTN_ESTIMATE');
  // If estimator is open, re-render its contents
  if(document.getElementById('est-overlay')?.style.display!=='none') renderEstimator();
  // Annual/monthly labels and hints
  const annualLabel=document.querySelector('label[for-annual]');
  const annualUnit=document.querySelector('.kwh-unit');
  // Update consumption labels via setMode re-call
  setMode(inputMode);
  // Re-run filters to rebuild results with new language
  applyFilters();
}

let _calcReqId=0;
// The 12 months the server priced ([{year, month 1-12}], first month after
// switching first) — every per-month array in a /calculate result is in
// this order, not January-December.
let _calcWindow=null;
function windowMonthLabels(){
  if(!_calcWindow||_calcWindow.length!==12) return getMonths();
  return _calcWindow.map(w=>getMonths()[w.month-1]+" '"+String(w.year).slice(-2));
}
function windowPeriodLabel(){
  if(!_calcWindow||!_calcWindow.length) return '';
  const f=_calcWindow[0],l=_calcWindow[_calcWindow.length-1];
  return `${getMonths()[f.month-1]} ${f.year} – ${getMonths()[l.month-1]} ${l.year}`;
}
async function fetchCalculate(payload){
  const resp=await fetch('/api/public/calculate',{
    method:'POST', headers:{'Content-Type':'application/json'},
    body:JSON.stringify(payload)
  });
  if(!resp.ok) throw new Error('status '+resp.status);
  return resp.json();
}

// Loading indicator for the results area — only shown if a /calculate
// request is still pending after a short grace period, so a fast (e.g.
// local/dev) response never flickers a spinner on screen.
let _loadingShowTimer=null;
function showLoadingSoon(){
  clearTimeout(_loadingShowTimer);
  _loadingShowTimer=setTimeout(()=>{
    const lbl=document.getElementById('results-loading-label');
    if(lbl) lbl.textContent=T('CALC_LOADING');
    document.getElementById('results-loading')?.classList.add('visible');
  },250);
}
function hideLoading(){
  clearTimeout(_loadingShowTimer);
  document.getElementById('results-loading')?.classList.remove('visible');
}

async function applyFilters(){
  const {voltage,contracts,le}=getFilterParams();
  const pricing=document.getElementById('sel-pricing').value;
  const area=document.getElementById('results-area');
  destroyAllCharts();
  window._lastCalcResults={};

  const annualKwh=inputMode==='annual'
    ?(parseFloat(document.getElementById('annual-kwh').value)||0)
    :((parseFloat(document.getElementById('monthly-kwh').value)||0)/_billingPeriod)*12;
  const rawMonthlyKwhInput=parseFloat(document.getElementById('monthly-kwh').value)||0;
  const monthlyKwhInput=rawMonthlyKwhInput/_billingPeriod;

  if(annualKwh<=0){
    _resultsVisible=false;
    hideLoading();
    area.innerHTML=`<div class="card prompt-card" id="prompt-enter" style="text-align:center;padding:32px;color:var(--text3);font-size:13px">${T('PROMPT_ENTER')}</div>`;
    return;
  }

  const isVulnerableEligible=document.getElementById('vulnerable-check')?.checked||false;
  const showOffers=document.getElementById('offers-check')?.checked!==false;

  // Pricing/discount/regulated-rate calculation now runs server-side (see
  // tariff-api/pricing/) — the client only sends the customer's inputs and
  // renders whatever comes back. reqId guards against an older, slower
  // request's response landing after a newer one (e.g. fast typing in the
  // consumption field).
  const reqId=++_calcReqId;
  showLoadingSoon();
  let data;
  try{
    data=await fetchCalculate({
      customerType, voltage, loadEntitlement:le,
      pricingFilter:pricing, vulnerableEligible:isVulnerableEligible, offersEnabled:showOffers,
      inputMode,
      annualKwh:parseFloat(document.getElementById('annual-kwh').value)||0,
      monthlyKwh:rawMonthlyKwhInput, billingPeriod:_billingPeriod,
      discountOverrides:window._discountState||{}
    });
  }catch(e){
    if(reqId!==_calcReqId) return;
    hideLoading();
    area.innerHTML=`<div class="card" style="text-align:center;padding:32px;color:var(--text3);font-size:13px">${T('CALC_ERROR')}</div>`;
    return;
  }
  if(reqId!==_calcReqId) return;
  hideLoading();

  const scored=(data.results||[]).map(r=>{
    const t=cfg.tariffs.find(x=>x.id===r.id);
    return t?{t,r}:null;
  }).filter(Boolean);
  scored.forEach(({t,r})=>{ window._lastCalcResults[t.id]=r; });
  window._hasSlotDam=!!data.hasSlotDam;
  _calcWindow=data.window||null;
  const noDam=(data.noDamTariffs||[]).map(x=>cfg.tariffs.find(y=>y.id===x.id)||x);

  if(!scored.length&&!noDam.length){
    _resultsVisible=false;
    if(inputMode==='monthly'&&pricing==='Dynamic'){
      area.innerHTML=`<div class="card" style="border-color:rgba(99,102,241,.3);background:rgba(99,102,241,.04);text-align:center;padding:32px">
        <div style="font-size:32px;margin-bottom:12px">📊</div>
        <h2 style="font-size:15px;font-weight:500;color:#4338ca;margin-bottom:8px">${T('VAR_ONLY_TITLE')}</h2>
        <p style="font-size:13px;color:#4338ca;line-height:1.6;max-width:420px;margin:0 auto">${T('VAR_ONLY_BODY')}</p>
      </div>`;
    } else {
      const ctLabel=T(customerType==='domestic'?'TAG_DOMESTIC':'TAG_CI');
      const leLabel=le?(le==='lt70'?' · '+T('LE_LT70'):' · '+T('LE_GT70')):'';
      area.innerHTML=`<div class="no-results"><h2 style="font-size:16px;font-weight:500;color:var(--text);margin-bottom:6px">${T('NO_TARIFFS_TITLE')}</h2>
        <p>${T('NO_TARIFFS_SUB',{VOLTAGE:T('TAG_'+voltage),CONTRACT:ctLabel})}${leLabel}${pricing!=='All'?' · '+pricingTag(pricing):''}.</p></div>`;
    }
    return;
  }

  const firstShow=!_resultsVisible; _resultsVisible=true;
  const introCls=firstShow?' intro':'';
  let html='';

  html+=`<div class="card" id="tariffs-card"><div class="results-header">
    <div>
      <div class="results-title">${T(scored.length===1?'TARIFFS_AVAILABLE_ONE':'TARIFFS_AVAILABLE',{N:scored.length})}</div>
      <div class="results-sub">${inputMode==='monthly'?T('RESULTS_SUB_MONTHLY',{KWH:rawMonthlyKwhInput,PERIOD:windowPeriodLabel()}):T('RESULTS_SUB_ANNUAL',{PERIOD:windowPeriodLabel()})}</div>
    </div>
    <div style="display:flex;gap:6px;flex-wrap:wrap">
      <span class="fbadge">${T('TAG_'+voltage)}</span>
      <span class="fbadge">${T(customerType==='domestic'?'TAG_DOMESTIC':'TAG_CI')}</span>
      ${le?`<span class="fbadge">${T(le==='lt70'?'LE_LT70':'LE_GT70')}</span>`:''}
      ${pricing!=='All'?`<span class="fbadge">${pricingTag(pricing)}</span>`:''}
    </div>
  </div>`;

  if(inputMode==='monthly') html+=`<div style="font-size:12px;color:var(--text2);font-family:var(--mono);background:rgba(99,102,241,.06);border:1px solid rgba(99,102,241,.2);border-radius:2px;padding:10px 14px;margin-bottom:4px;line-height:1.6">${T('NUDGE_ANNUAL')}</div>`;
  html+=`<div class="ranked-list${introCls}">`;  scored.forEach(({t,r},rank)=>{
    const {base,reg,fullBase,months:moBd,moKwh,regBd,fpaRate}=r;
    // Discounted only if it actually saves at least half a cent (guards against
    // floating-point noise between the two totals).
    const hasDisc=fullBase!=null&&fullBase-base>=0.005;
    const isOpen=openCards.has(t.id);
    const showFpa=fpaRate>0;
    const fpaRateStr=`€${fpaRate.toFixed(4)}/kWh`;
    const fpaInfoAttrs=regInfoAttrs('FPA_FULL','FPA_DESC');
    const fpaLabelShort=`<span ${fpaInfoAttrs}>${esc(T('FPA_SHORT'))} <span style="font-size:11px;opacity:.6">ℹ</span><br><span style="font-size:11px;letter-spacing:normal">${fpaRateStr}</span></span>`;
    const fpaLabelFull=`<span ${fpaInfoAttrs}>${esc(T('FPA_FULL'))} <span style="font-size:11px">(${fpaRateStr})</span> <span style="font-size:11px;opacity:.6">ℹ</span></span>`;
    const standingInfoAttrs=regInfoAttrs('TH_STANDING','STANDING_DESC');
    const standingLabel=`<span ${standingInfoAttrs}>${esc(T('TH_STANDING'))} <span style="font-size:11px;opacity:.6">ℹ</span></span>`;

    const hasEnergyDisc=r.discounts&&r.discounts.some(d=>d.type==='energy');
    const hasStandingDisc=r.discounts&&r.discounts.some(d=>d.type==='standing');
    const moRows=windowMonthLabels().map((m,i)=>{
      const bd=moBd[i];
      return `<tr>
        <td>${m}</td>
        <td>${moKwh[i].toFixed(0)}</td>
        <td style="color:var(--text2)">
          ${bd&&hasEnergyDisc&&bd.energyDisc>0?`<span style="color:var(--text3);text-decoration:line-through;font-size:11px">€${bd.energyFull.toFixed(2)}</span><br>`:''}
          €${bd?bd.energy.toFixed(2):'—'}
        </td>
        ${showFpa?`<td style="color:var(--text)">€${bd?bd.fpa.toFixed(2):'—'}</td>`:''}
        <td style="color:var(--text3)">
          ${bd&&hasStandingDisc&&bd.standingDisc>0?`<span style="color:var(--text3);text-decoration:line-through;font-size:11px">€${bd.standingFull.toFixed(2)}</span><br>`:''}
          €${bd?bd.standing.toFixed(2):'—'}
        </td>
        <td class="cost-col">€${bd?bd.total.toFixed(2):'—'}</td>
      </tr>`;
    }).join('');

    const totKwh=moKwh.reduce((a,x)=>a+x,0);
    const annEnergy=moBd.reduce((a,v)=>a+(v?v.energy:0),0);
    const annFpa=moBd.reduce((a,v)=>a+(v?v.fpa:0),0);
    const annStanding=moBd.reduce((a,v)=>a+(v?v.standing:0),0);

    const regInfoMap={grid:['REGULATED_GRID','REG_GRID_DESC'],pso:['REGULATED_PSO','REG_PSO_DESC'],res:['REGULATED_RES','REG_RES_DESC'],mdm:['REGULATED_MDM','REG_MDM_DESC'],mdmSupplier:['MDM_SUPPLIER','MDM_SUPPLIER_DESC']};
    const regRows=Object.entries(regBd).filter(([k])=>k!=='total').map(([k,v])=>{
      const info=regInfoMap[v.regulated?k:'mdmSupplier']||[];
      const c=v.regulated?'#1d4ed8':'var(--text2)';
      return `<tr style="${v.regulated?'background:rgba(59,130,246,.04)':''}">
        <td style="color:${c}" ${regInfoAttrs(info[0],info[1])}>${T(v.label)} <span style="font-size:11px;opacity:.6">ℹ</span></td>
        <td style="color:var(--text3)">${regRateStr(k,v)}</td>
        <td colspan="${showFpa?4:3}" style="color:${c}">€${v.annual.toFixed(2)}</td>
      </tr>`;
    }).join('');

    const totRow=`
      <tr style="border-top:1.5px solid var(--border2);background:var(--bg3)">
        <td><strong>${T('ROW_SUP_TOTAL')}</strong></td>
        <td>${totKwh.toFixed(0)}</td>
        <td style="color:var(--text2)">€${annEnergy.toFixed(2)}</td>
        ${showFpa?`<td style="color:var(--text)">€${annFpa.toFixed(2)}</td>`:''}
        <td style="color:var(--text3)">€${annStanding.toFixed(2)}</td>
        <td class="cost-col"><strong>€${base.toFixed(2)}</strong></td>
      </tr>
      ${regRows}
      <tr style="background:var(--bg3)">
        <td><strong>${T('ROW_TOTAL_REG')}</strong></td>
        <td colspan="${showFpa?4:3}"></td>
        <td class="cost-col"><strong>€${(base+reg).toFixed(2)}</strong></td>
      </tr>`;

    const moTableHead=`<thead><tr>
      <th>${T('TH_MONTH')}</th><th>${T('TH_KWH')}</th>
      <th>${T('TH_ENERGY')}</th>
      ${showFpa?`<th style="color:var(--text)">${fpaLabelShort}</th>`:''}
      <th>${standingLabel}</th><th>${T('TH_TOTAL')}</th>
    </tr></thead>`;

    html+=`<div class="rank-card rank-${rank+1}" id="rc-${t.id}">
      <div class="rank-header" role="button" tabindex="0" aria-expanded="${isOpen?'true':'false'}" aria-controls="rd-${t.id}" data-action="toggleCard" data-arg="${esc(t.id)}">
        <div class="rank-num">${rank+1}</div>
        <div class="rank-info">
          <div class="rank-name-row">
            <div class="rank-name">${esc(t.name)}</div>
            <span class="rank-sup-dash">–</span>
            <span class="rank-sup-pill" data-supplier="${esc(t.supplier)}" role="button" tabindex="0" data-action="openSupContact" title="${T('LBL_VIEW_CONTACT')}">${esc(t.supplier)}</span>
            ${t.updatedAt?`<span class="rank-sup-dash">–</span><span style="font-size:11px;color:var(--text3);font-family:var(--mono)" title="${esc(fmtLocalTs(t.updatedAt))}">${esc(T('LAST_UPDATED',{DT:fmtLocalDate(t.updatedAt)}))}</span>`:''}
          </div>
          <div class="rank-meta">
            <span class="badge badge-${t.pricing}">${pricingTag(t.pricing)}</span>
            ${t.pricing==='Dynamic'&&r.damFloor?`<span style="font-size:11px;padding:2px 6px;border-radius:2px;background:rgba(139,92,246,.1);color:#7c3aed;font-family:var(--mono)">floor €${r.damFloor.toFixed(4)}/kWh</span>`:''}
            <span style="font-size:11px;color:var(--text3);font-family:var(--mono)">€${t.standing.toFixed(2)}${T('LBL_STANDING')}</span>
            ${t.vulnerable?`<span style="font-size:11px;padding:2px 7px;border-radius:2px;background:rgba(236,72,153,.12);color:#9d174d;font-family:var(--mono);font-weight:500">🛡 ${T('LBL_VULNERABLE_CHECK').split('/')[0].trim()}</span>`:''}
            ${t.durationMonths
              ?`<span style="font-size:11px;padding:2px 7px;border-radius:2px;background:rgba(239,68,68,.1);color:#9f1239;font-family:var(--mono);font-weight:500">⏱ ${T('LBL_MIN_MONTHS',{N:t.durationMonths})}</span>`
              :`<span style="font-size:11px;padding:2px 7px;border-radius:2px;background:var(--bg3);color:var(--text3);font-family:var(--mono)">${T('LBL_NO_MIN')}</span>`}
          </div>
          ${hasDisc?`<div style="font-size:11px;color:var(--green);font-family:var(--mono);margin-top:auto;padding-top:6px;line-height:1.5">*${T('LBL_INCL_DISC')}</div>`:''}
          ${r.offer?`<div style="font-size:11px;color:#92400e;font-family:var(--mono);padding-top:3px;line-height:1.5">⚠ ${T('LBL_OFFER_ENDS',{N:r.offer.months,X:r.offer.afterMonthlyAvg.toFixed(2)})}</div>`:''}
        </div>
        <div class="rank-cost-col">
          ${inputMode==='monthly'
            ? `<div class="rank-annual-val" style="${hasDisc?'color:var(--green)':''}">${hasDisc?`<span style="font-size:13px;font-weight:400;color:var(--text3);text-decoration:line-through;margin-right:5px">€${periodCost(fullBase).toFixed(2)}</span>`:''}€${periodCost(base).toFixed(2)}${hasDisc?'<sup style="font-size:11px">*</sup>':''}<span class="rank-annual-lbl" style="font-size:12px;margin-left:3px">${periodCostLabel()}</span><span class="rank-toggle ${isOpen?'open':''}">▼</span></div>
          <div style="font-size:13px;font-weight:500;font-family:var(--mono);color:var(--text3);text-align:right;margin-top:4px">≈ €${base.toFixed(0)}<span class="rank-annual-lbl" style="font-size:11px;margin-left:3px">${T('LBL_SUP_YEAR')}</span></div>`
            : `<div class="rank-annual-val" style="${hasDisc?'color:var(--green)':''}">${hasDisc?`<span style="font-size:13px;font-weight:400;color:var(--text3);text-decoration:line-through;margin-right:5px">€${fullBase.toFixed(0)}</span>`:''}€${base.toFixed(0)}${hasDisc?'<sup style="font-size:11px">*</sup>':''}<span class="rank-annual-lbl" style="font-size:12px;margin-left:3px">${T('LBL_SUP_YEAR')}</span><span class="rank-toggle ${isOpen?'open':''}">▼</span></div>
          <div style="font-size:13px;font-weight:500;font-family:var(--mono);color:var(--text3);text-align:right;margin-top:4px">€${(base/12).toFixed(2)}<span class="rank-annual-lbl" style="font-size:11px;margin-left:3px">${T('LBL_SUP_MONTH')}</span></div>`}
          ${reg>0?`<div style="font-size:11px;color:#1d4ed8;font-family:var(--mono);margin-top:3px;text-align:right">${T('LBL_INCL_ADDITIONAL',{X:'€'+(inputMode==='monthly'?periodCost(reg):reg).toFixed(0)})} / ${T('LBL_WITHOUT_VAT')}</div>`:''}
        </div>
      </div>
      <div class="rank-detail ${isOpen?'open':''}" id="rd-${t.id}">
        <div class="rank-detail-inner">
        <div class="rank-detail-pad">
        ${showOffers?renderDiscountToggles(t,r):''}
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;flex-wrap:wrap;gap:8px">
          <span style="font-size:13px;font-weight:500;color:var(--text)">${esc(t.supplier)}</span>
          <div style="display:flex;gap:8px;flex-wrap:wrap">
          <button data-tid="${esc(t.id)}" data-tname="${esc(t.name)}" data-tsup="${esc(t.supplier)}" data-action="reportTariff" class="rd-act-btn"
            style="display:inline-flex;align-items:center;gap:6px;padding:6px 14px;border-radius:2px;border:1px solid var(--border2);background:var(--bg3);color:var(--text2);font-size:12px;font-family:var(--font);cursor:pointer;transition:all .12s">
            🚩 ${T('BTN_REPORT_ISSUE')}
          </button>
          <button data-supplier="${esc(t.supplier)}" data-action="openSupContact" class="rd-act-btn"
            style="display:inline-flex;align-items:center;gap:6px;padding:6px 14px;border-radius:2px;border:1px solid var(--border2);background:var(--bg3);color:var(--text2);font-size:12px;font-family:var(--font);cursor:pointer;transition:all .12s">
            ${T('BTN_CONTACT')}
          </button>
          ${cfg.sampleInvoiceEnabled?`<button data-tid="${esc(t.id)}" data-action="openSampleInvoice" class="rd-act-btn"
            style="display:inline-flex;align-items:center;gap:6px;padding:6px 14px;border-radius:2px;border:1px solid var(--border2);background:var(--bg3);color:var(--text2);font-size:12px;font-family:var(--font);cursor:pointer;transition:all .12s">
            📄 ${T('BTN_SAMPLE_INVOICE')}
          </button>`:''}
          </div>
        </div>
          ${calcNote(t,r)?`<div class="calc-note">${calcNote(t,r)}</div>`:''}
          ${inputMode==='annual'?`<div style="overflow-x:auto">
            <table class="mo-table">
              ${moTableHead}
              <tbody>${moRows}${totRow}</tbody>
            </table>
          </div>
          <div class="chart-wrap"><canvas id="chart-${t.id}"></canvas></div>`
          : moBd[0]?`<div style="overflow-x:auto;margin-top:4px">
            <table class="mo-table">
              <thead><tr>
                <th colspan="2" style="text-align:left;font-size:11px;letter-spacing:.05em">${T('BILL_BREAKDOWN_HDR')} — ${periodCostLabel()} · ${(monthlyKwhInput*_billingPeriod).toFixed(0)} kWh</th>
              </tr></thead>
              <tbody>
                <tr>
                  <td>${T('TH_ENERGY')}</td>
                  <td class="cost-col">€${(moBd[0].energy*_billingPeriod).toFixed(2)}</td>
                </tr>
                ${showFpa?`<tr>
                  <td style="color:var(--text)">${fpaLabelFull}</td>
                  <td class="cost-col" style="color:var(--text)">€${(moBd[0].fpa*_billingPeriod).toFixed(2)}</td>
                </tr>`:''}
                <tr>
                  <td>${standingLabel} <span style="font-size:11px;color:var(--text3);font-family:var(--mono)">€${t.standing.toFixed(2)}/mo × ${_billingPeriod}</span></td>
                  <td class="cost-col">€${(moBd[0].standing*_billingPeriod).toFixed(2)}</td>
                </tr>
                <tr style="border-top:1.5px solid var(--border2);background:var(--bg3)">
                  <td><strong>${T('ROW_SUP_TOTAL')}</strong></td>
                  <td class="cost-col"><strong>€${periodCost(base).toFixed(2)}</strong></td>
                </tr>
                ${Object.entries(regBd).filter(([k])=>k!=='total').map(([k,v])=>{
                  const info=regInfoMap[v.regulated?k:'mdmSupplier']||[];
                  const rateStr=regRateStr(k,v);
                  const c=v.regulated?'#1d4ed8':'var(--text2)';
                  return `<tr style="${v.regulated?'background:rgba(59,130,246,.04)':''}">
                  <td style="color:${c}" ${regInfoAttrs(info[0],info[1])}>${T(v.label)} <span style="font-size:11px">(${rateStr})</span> <span style="font-size:11px;opacity:.6">ℹ</span></td>
                  <td class="cost-col" style="color:${c}">€${(v.annual/12*_billingPeriod).toFixed(2)}</td>
                </tr>`;}).join('')}
                <tr style="background:var(--bg3)">
                  <td><strong>${T('ROW_TOTAL_REG')}</strong></td>
                  <td class="cost-col"><strong>€${(periodCost(base)+periodCost(reg)).toFixed(2)}</strong></td>
                </tr>
                <tr style="font-size:11px;color:var(--text3);font-family:var(--mono)">
                  <td colspan="2" style="padding-top:6px">${T('BILL_YEAR_NOTE',{N:12/_billingPeriod,X:(base+reg).toFixed(0)})}</td>
                </tr>
              </tbody>
            </table>
          </div>`:''}

        </div>
        </div>
      </div>
    </div>`;
  });
  html+='</div>';
  html+='</div>';

  if(scored.length>1&&inputMode==='annual') html+=`<div class="card">
    <div class="card-title">${T('CHART_ANNUAL')}</div>
    <div class="chart-wrap-lg"><canvas id="cmp-chart"></canvas></div>
  </div>`;

  // ── ANNUAL MODE block removed — merged above ──
  if(noDam.length) html+=`<div class="card" style="border-color:#fde68a;background:#fffbeb">
    <div class="card-title" style="color:#92400e">${T('VAR_NO_DAM_TITLE')}</div>
    <ul style="padding-left:18px;font-size:13px;color:#92400e;line-height:1.9">${noDam.map(t=>`<li>${esc(t.name)} (${esc(t.supplier)})</li>`).join('')}</ul>
  </div>`;

  area.innerHTML=html;

  if(scored.length>1){
    const _cmpC=document.getElementById('cmp-chart');
    if(_cmpC){ chartRegistry['cmp']=new Chart(_cmpC,{
      type:'line',
      data:{labels:windowMonthLabels(),datasets:scored.map(({t,r},idx)=>({
        label:t.name,
        data:r.months.map(v=>v!=null?+v.total.toFixed(2):null),
        borderColor:PALETTE[idx%PALETTE.length],
        backgroundColor:PALETTE[idx%PALETTE.length]+'1f',
        borderDash:DASH_PATTERNS[idx%DASH_PATTERNS.length],
        borderWidth:idx===0?3:1.75,
        fill:false,tension:.35,
        pointStyle:'circle',pointRadius:idx===0?3.5:0,pointHoverRadius:5,
        pointBackgroundColor:PALETTE[idx%PALETTE.length],pointBorderColor:'#fff',pointBorderWidth:1.5
      }))},
      options:{responsive:true,maintainAspectRatio:false,
        interaction:{mode:'index',intersect:false},
        plugins:{
          legend:{labels:{font:{family:CHART_FONT_MONO,size:11},color:'#54606f',boxWidth:10,boxHeight:10,usePointStyle:true,pointStyle:'circle',padding:15}},
          tooltip:chartTooltip()
        },
        scales:{
          x:{ticks:{font:{family:CHART_FONT_MONO,size:11},color:CHART_TICK},grid:{display:false},border:{color:'#e2e7ef'}},
          y:{ticks:{callback:v=>'€'+v.toFixed(0),font:{family:CHART_FONT_MONO,size:11},color:CHART_TICK,padding:6},grid:{color:CHART_GRID},border:{display:false}}
        }}
    }); }
  }

  scored.forEach(({t})=>{ if(openCards.has(t.id)&&inputMode==='annual') drawCardChart(t); });
}

function drawCardChart(t){
  const r=window._lastCalcResults[t.id];
  const canvas=document.getElementById('chart-'+t.id);
  if(!canvas||!r) return;
  if(chartRegistry[t.id]){try{chartRegistry[t.id].destroy();}catch(e){} delete chartRegistry[t.id];}
  const color={Fixed:'#1a3a5e',ToU:'#2f6f8f',Dynamic:'#b06c2c',Variable:'#5b7a52'}[t.pricing]||'#1a3a5e';
  chartRegistry[t.id]=new Chart(canvas,{
    type:'bar',
    data:{labels:windowMonthLabels(),datasets:[{
      label:T('CHART_MONTHLY_COST'),
      data:r.months.map(v=>v!=null?+v.total.toFixed(2):null),
      backgroundColor:color+'2e',borderColor:color,borderWidth:1.5,borderRadius:5,
      borderSkipped:false,hoverBackgroundColor:color+'55',maxBarThickness:38
    }]},
    options:{responsive:true,maintainAspectRatio:false,
      plugins:{legend:{display:false},tooltip:chartTooltip()},
      scales:{
        x:{ticks:{font:{family:CHART_FONT_MONO,size:10},color:CHART_TICK},grid:{display:false},border:{display:false}},
        y:{ticks:{callback:v=>'€'+v.toFixed(0),font:{family:CHART_FONT_MONO,size:10},color:CHART_TICK,padding:6},grid:{color:CHART_GRID},border:{display:false}}
      }}
  });
}

function renderDiscountToggles(t,r){
  const discounts=r.discounts||[];
  if(!discounts.length) return '';
  const rows=discounts.map((d,di)=>{
    const key=t.id+'_disc_'+di;
    const checked=!window._discountState||!(window._discountState[t.id])||window._discountState[t.id][key]!==false;
    const typeLabel=d.type==='energy'?T('DISC_ENERGY_LABEL'):T('DISC_STANDING_LABEL');
    const durLabel=d.durationMonths?T('DISC_DURATION_FIRST',{N:d.durationMonths}):'<strong>'+T('DISC_DURATION_PERM')+'</strong>';
    const condLabel=d.conditions?' — '+esc(d.conditions):'';   // supplier-typed free text
    return '<label style="display:flex;align-items:flex-start;gap:8px;font-size:12px;cursor:pointer">'
      +'<input type="checkbox" '+(checked?'checked':'')
      +' data-tariff="'+esc(t.id)+'" data-idx="'+di+'"'
      +' style="margin-top:2px;accent-color:var(--accent)"'
      +' data-change="toggleDiscount">'
      +'<span style="color:var(--text2)">'+typeLabel+': <strong>'+d.percentage+'%</strong> '+durLabel+condLabel+'</span>'
      +'</label>';
  }).join('');
  return '<div style="background:rgba(16,185,129,.05);border:1px solid rgba(16,185,129,.2);border-radius:2px;padding:10px 12px;margin-bottom:12px">'
    +'<div style="font-size:11px;font-family:var(--mono);color:var(--green);letter-spacing:.07em;margin-bottom:8px">'+T('DISC_HEADER')+'</div>'
    +'<div style="display:flex;flex-direction:column;gap:6px">'+rows+'</div>'
    +'</div>';
}

async function toggleDiscount(tariffId, discIdx, active){
  if(!window._discountState) window._discountState={};
  if(!window._discountState[tariffId]) window._discountState[tariffId]={};
  window._discountState[tariffId][tariffId+'_disc_'+discIdx]=active;
  const wasOpen=new Set(openCards);
  await applyFilters();
  wasOpen.forEach(id=>{
    openCards.add(id);
    const det=document.getElementById('rd-'+id);
    if(det) det.classList.add('open');
    const tog=document.querySelector('#rc-'+id+' .rank-toggle');
    if(tog) tog.classList.add('open');
    const t=cfg.tariffs.find(x=>x.id===id);
    if(t) requestAnimationFrame(()=>drawCardChart(t));
  });
}

/* Clicking a tariff expands its detail inline (others stay as they are). */
function toggleCard(id){
  if(openCards.has(id)) openCards.delete(id); else openCards.add(id);
  document.getElementById('rd-'+id)?.classList.toggle('open',openCards.has(id));
  document.querySelector(`#rc-${id} .rank-toggle`)?.classList.toggle('open',openCards.has(id));
  document.querySelector(`#rc-${id} .rank-header`)?.setAttribute('aria-expanded',openCards.has(id)?'true':'false');
  if(openCards.has(id)){
    const t=cfg.tariffs.find(x=>x.id===id);
    if(t) drawCardChart(t);
  }
}

/* ─────────────────────────────────────────────────────────────────────────
   SAMPLE CONFIG — used only when the live backend (/api/public/config) is
   unreachable, so the page renders standalone for design/preview. The real
   deployment fetches the authoritative config and never hits this.
   ───────────────────────────────────────────────────────────────────────── */
function buildSampleConfig(){
  // Build a 48-slot half-hourly shape from 24 hourly weights
  const expand=h=>{const s=[];for(let i=0;i<48;i++)s.push(h[Math.floor(i/2)]);return s;};
  // Residential: low overnight, soft morning bump, strong evening peak
  const resWD=[0.5,0.4,0.35,0.35,0.4,0.6,1.0,1.5,1.6,1.3,1.1,1.1,1.2,1.1,1.0,1.0,1.2,1.6,2.2,2.6,2.5,2.1,1.4,0.8];
  const resNW=[0.6,0.5,0.4,0.4,0.45,0.6,0.9,1.2,1.6,1.8,1.9,1.9,1.8,1.6,1.5,1.5,1.7,2.0,2.4,2.6,2.4,2.0,1.4,0.9];
  // Commercial: daytime-heavy on working days, low otherwise
  const comWD=[0.3,0.3,0.3,0.3,0.3,0.4,0.7,1.4,2.4,2.9,3.0,3.0,2.8,2.9,3.0,2.9,2.5,1.8,1.1,0.7,0.5,0.4,0.35,0.3];
  const comNW=[0.3,0.3,0.3,0.3,0.3,0.35,0.5,0.8,1.1,1.3,1.4,1.4,1.3,1.2,1.1,1.0,0.9,0.7,0.5,0.45,0.4,0.35,0.3,0.3];
  const profile=(id,name,monthlyFractions,wd,nw)=>({
    id,name,monthlyFractions,
    months:Array.from({length:12},()=>({W:expand(wd),NW:expand(nw)}))
  });
  // Cyprus seasonality: summer cooling peak (Jul/Aug), mild winter heating
  const resFr=[.085,.075,.075,.07,.075,.085,.10,.105,.085,.075,.075,.095];
  const comFr=[.083,.078,.082,.08,.084,.087,.092,.085,.084,.083,.08,.082];
  const norm=a=>{const s=a.reduce((x,y)=>x+y,0);return a.map(v=>v/s);};
  const suppliers=[
    {name:"EAC Supply",tradingName:"EAC Supply (ΑΗΚ Προμήθεια)",phone:"+357 22 845000",email:"customerservice@eac.com.cy",website:"https://www.eac.com.cy",address:"11 Amfipoleos St, 2025 Strovolos, Nicosia",licenseType:"Supplier",regulated:true},
    {name:"Bright Energy",tradingName:"Bright Energy Ltd",phone:"+357 24 100200",email:"hello@brightenergy.com.cy",website:"https://www.brightenergy.com.cy",address:"42 Spyrou Kyprianou, 6051 Larnaca",licenseType:"Supplier"},
    {name:"Hellenic Power",tradingName:"Hellenic Power Cyprus",phone:"+357 25 778899",email:"support@hellenicpower.com.cy",website:"https://www.hellenicpower.com.cy",address:"18 Griva Digeni, 3035 Limassol",licenseType:"Supplier"},
    {name:"Helios Power",tradingName:"Helios Power",phone:"+357 22 556677",email:"info@heliospower.com.cy",website:"https://www.heliospower.com.cy",address:"7 Stasinou Ave, 1060 Nicosia",licenseType:"Supplier"},
    {name:"Cyfield Energy",tradingName:"Cyfield Energy",phone:"+357 22 449900",email:"energy@cyfield.com.cy",website:"https://www.cyfieldenergy.com.cy",address:"170 Athalassas Ave, 2025 Nicosia",licenseType:"Supplier"}
  ];
  const profiles=[
    profile("res","Residential LV",norm(resFr),resWD,resNW),
    profile("com","Commercial LV/MV",norm(comFr),comWD,comNW)
  ];
  const today=new Date();
  const iso=d=>new Date(today.getTime()-d*86400000).toISOString();
  const tariffs=[
    {id:"eac-dom-fix",name:"EAC Home Standard",supplier:"EAC Supply",updatedAt:iso(8),voltage:"LV",contract:"Domestic",loadEntitlement:"any",pricing:"Fixed",rates:{rate:0.1620},standing:4.50,profileId:"res",mdm:0.55,mdmInvoiceMonths:2,fpaSource:"global",discounts:[],durationMonths:null},
    {id:"bright-dom-fix",name:"Bright FixSaver 12",supplier:"Bright Energy",updatedAt:iso(3),voltage:"LV",contract:"Domestic",loadEntitlement:"any",pricing:"Fixed",rates:{rate:0.1490},standing:3.90,profileId:"res",mdm:0,fpaSource:"global",discounts:[{type:"energy",percentage:8,durationMonths:12,conditions:"e-bill + direct debit"}],durationMonths:12},
    {id:"hellenic-dom-tou",name:"Hellenic Day & Night",supplier:"Hellenic Power",updatedAt:iso(5),voltage:"LV",contract:"Domestic",loadEntitlement:"any",pricing:"ToU",rates:{hiStart:6,hiEnd:9,hiPeakStart:7,hiPeakEnd:23,hiPeakRate:0.1950,hiOffRate:0.1050,loPeakStart:7,loPeakEnd:23,loPeakRate:0.1720,loOffRate:0.0980},standing:4.20,profileId:"res",mdm:0,fpaSource:"global",discounts:[],durationMonths:null},
    {id:"helios-dom-dyn",name:"Helios Market Flex",supplier:"Helios Power",updatedAt:iso(2),voltage:"LV",contract:"Domestic",loadEntitlement:"any",pricing:"Dynamic",rates:{mult:1.08,adder:0.0380,damFloor:0.0500},standing:3.50,profileId:"res",mdm:0,fpaSource:"global",discounts:[],durationMonths:null},
    {id:"cyfield-dom-var",name:"Cyfield Tiered Home",supplier:"Cyfield Energy",updatedAt:iso(11),voltage:"LV",contract:"Domestic",loadEntitlement:"any",pricing:"Variable",rates:{resetMonths:1,tiers:[{upTo:150,rate:0.1380,fixedCharge:0},{upTo:400,rate:0.1680,fixedCharge:0},{upTo:null,rate:0.2050,fixedCharge:0}]},standing:4.00,profileId:"res",mdm:0,fpaSource:"global",discounts:[],durationMonths:6},
    {id:"eac-dom-social",name:"EAC Social Tariff",supplier:"EAC Supply",updatedAt:iso(20),voltage:"LV",contract:"Domestic",loadEntitlement:"any",pricing:"Fixed",rates:{rate:0.1280},standing:2.50,profileId:"res",mdm:0.55,mdmInvoiceMonths:2,fpaSource:"global",discounts:[],durationMonths:null,vulnerable:true},
    // Commercial LV
    {id:"eac-com-fix",name:"EAC Business Standard",supplier:"EAC Supply",updatedAt:iso(8),voltage:"LV",contract:"Commercial",loadEntitlement:"lt70",pricing:"Fixed",rates:{rate:0.1710},standing:9.00,profileId:"com",mdm:0.55,mdmInvoiceMonths:1,fpaSource:"global",discounts:[],durationMonths:null},
    {id:"bright-com-tou",name:"Bright Business ToU",supplier:"Bright Energy",updatedAt:iso(4),voltage:"LV",contract:"Commercial",loadEntitlement:"lt70",pricing:"ToU",rates:{hiStart:6,hiEnd:9,hiPeakStart:8,hiPeakEnd:20,hiPeakRate:0.2050,hiOffRate:0.1150,loPeakStart:8,loPeakEnd:20,loPeakRate:0.1820,loOffRate:0.1080},standing:8.00,profileId:"com",mdm:0,fpaSource:"global",discounts:[{type:"standing",percentage:15,durationMonths:null,conditions:"annual prepayment"}],durationMonths:24},
    {id:"hellenic-com-dyn",name:"Hellenic Business Flex",supplier:"Hellenic Power",updatedAt:iso(6),voltage:"LV",contract:"Commercial",loadEntitlement:"gt70",pricing:"Dynamic",rates:{mult:1.05,adder:0.0320,damFloor:0.0450},standing:14.00,profileId:"com",mdm:0,fpaSource:"global",discounts:[],durationMonths:12}
  ];
  // Day-ahead market monthly averages (€/kWh) — plausible Cyprus 2026 shape
  const damMonthly=[0.118,0.112,0.104,0.096,0.101,0.124,0.149,0.156,0.132,0.108,0.110,0.121];
  const regulated={lv:0.0620,mv:0.0510,hv:0.0410,pso:0.0095,fpaLV:0.0060,fpaMV:0.0050,fpaHV:0.0040,mdm:0.55,updated_at:iso(1),fpa_updated_at:iso(1)};
  const notices={
    assumptions_en:"<h3>How costs are calculated</h3><p>Estimates use each tariff's assigned load profile to distribute your consumption across the year, weighting working and non-working days using the current calendar.</p><ul><li>Dynamic tariffs use day-ahead market (DAM) price assumptions.</li><li>Regulated network, PSO and metering charges are shown separately and excluded from the supplier ranking.</li><li>Figures exclude VAT.</li></ul>",
    assumptions_el:"<h3>Πώς υπολογίζεται το κόστος</h3><p>Οι εκτιμήσεις χρησιμοποιούν το προφίλ κατανάλωσης κάθε διατίμησης για να κατανείμουν την κατανάλωσή σας στο έτος, σταθμίζοντας εργάσιμες και μη εργάσιμες ημέρες με βάση το τρέχον ημερολόγιο.</p><ul><li>Οι δυναμικές διατιμήσεις χρησιμοποιούν τιμές της Προημερήσιας Αγοράς (ΠΗΑ).</li><li>Οι ρυθμιζόμενες χρεώσεις δικτύου, ΥΔΩ και μετρήσεων εμφανίζονται ξεχωριστά.</li><li>Τα ποσά δεν περιλαμβάνουν ΦΠΑ.</li></ul>",
    legal_en:"<h3>Disclaimer</h3><p>This tool provides indicative estimates only and does not constitute a commercial offer. Actual costs depend on your real consumption, contract terms and prevailing prices. Always confirm details directly with the supplier.</p>",
    legal_el:"<h3>Αποποίηση ευθύνης</h3><p>Το εργαλείο παρέχει ενδεικτικές εκτιμήσεις και δεν αποτελεί εμπορική προσφορά. Το πραγματικό κόστος εξαρτάται από την πραγματική σας κατανάλωση, τους όρους του συμβολαίου και τις ισχύουσες τιμές. Επιβεβαιώνετε πάντα τα στοιχεία απευθείας με τον προμηθευτή.</p>",
    vulnerable_en:"<p>You may qualify for a social / vulnerable consumer tariff if you:</p><ul><li>Receive a guaranteed minimum income or public assistance;</li><li>Are a recipient of a severe disability or care allowance;</li><li>Belong to a low-income multi-child household;</li><li>Depend on electrically-powered medical equipment.</li></ul><p>Eligibility is confirmed by the relevant authority. Contact your supplier for the application process.</p>",
    vulnerable_el:"<p>Ενδέχεται να δικαιούστε κοινωνική / ευπαθή διατίμηση εάν:</p><ul><li>Λαμβάνετε Ελάχιστο Εγγυημένο Εισόδημα ή δημόσιο βοήθημα·</li><li>Είστε λήπτης επιδόματος βαριάς αναπηρίας ή φροντίδας·</li><li>Ανήκετε σε πολύτεκνη οικογένεια χαμηλού εισοδήματος·</li><li>Εξαρτάστε από ιατρικό εξοπλισμό που λειτουργεί με ηλεκτρισμό.</li></ul><p>Η επιλεξιμότητα επιβεβαιώνεται από την αρμόδια αρχή. Επικοινωνήστε με τον προμηθευτή σας.</p>"
  };
  return {suppliers,tariffs,profiles,damMonthly,regulated,notices};
}

async function init(){
  try{
    const resp=await fetch('/api/public/config');
    if(!resp.ok) throw new Error('API returned '+resp.status);
    cfg=await resp.json();
    document.getElementById('app').style.display='';
    setMode('annual');
    setCustomerType('domestic');
    renderPage();
    updateVulnerableRow();
    // "About & independence" content is always present (static, not admin-driven),
    // so this button is always shown regardless of whether assumptions/legal text
    // has been filled in yet — it's the only entry point to that Article 121
    // disclosure content.
    const _nb=document.getElementById('notices-open-btn');
    if(_nb) _nb.style.display='';
  }catch(e){
    // Backend unavailable — fall back to embedded sample config so the page
    // still renders (design preview / standalone use).
    console.warn('Live config unavailable, using sample config.',e);
    window._reportingUnavailable=true;
    try{
      cfg=buildSampleConfig();
      document.getElementById('app').style.display='';
      setMode('annual');
      setCustomerType('domestic');
      renderPage();
      updateVulnerableRow();
      const _nb=document.getElementById('notices-open-btn');
      if(_nb) _nb.style.display='';
      // Seed a sample consumption so results are visible immediately on first load
      const ak=document.getElementById('annual-kwh');
      if(ak&&!ak.value){ ak.value=6000; applyFilters(); }
    }catch(e2){
      document.getElementById('no-config').style.display='';console.error(e2);
    }
  }
  setConnCollapsed(false);
}
init();

/* ── Consumption Estimator ── */
function openEstimator(){
  document.getElementById('est-overlay').style.display='flex';
  document.getElementById('est-result-wrap').style.display='none';
  document.getElementById('est-use-btn').style.display='none';
  window._estValue=null;
  renderEstimator();
}
function closeEstimator(){
  document.getElementById('est-overlay').style.display='none';
}
function renderEstimator(){
  document.getElementById('est-title').textContent=T('EST_TITLE');
  document.getElementById('est-desc').textContent=T('EST_DESC');
  document.getElementById('est-lbl-dwelling').textContent=T('EST_DWELLING');
  document.getElementById('est-lbl-persons').textContent=T('EST_PERSONS');
  document.getElementById('est-lbl-ac').textContent=T('EST_AC');
  document.getElementById('est-lbl-water').textContent=T('EST_WATER');
  document.getElementById('est-lbl-cooking').textContent=T('EST_COOKING');
  document.getElementById('est-calc-btn').textContent=T('EST_CALC');
  document.getElementById('est-use-btn').textContent=T('EST_USE');
  document.getElementById('est-result-lbl').textContent=T('EST_RESULT_LBL');
  document.getElementById('est-result-unit').textContent=T('EST_RESULT_UNIT');
  document.getElementById('est-note').textContent=T('EST_NOTE');
  document.getElementById('est-meth-title').textContent=T('EST_METH_TITLE');
  document.getElementById('meth-modal-title').textContent=T('EST_METH_TITLE');
  document.getElementById('est-meth-body').innerHTML=T('EST_METH_BODY');
  // dwelling options
  const dSel=document.getElementById('est-dwelling');
  const dKeys=['EST_D_STUDIO','EST_D_APT1','EST_D_APT2','EST_D_APT3','EST_D_SEMI','EST_D_DET_S','EST_D_DET_L'];
  const dVals=['studio','apt1','apt2','apt3','semi','det_s','det_l'];
  const prev=dSel.value;
  dSel.innerHTML=dKeys.map((k,i)=>`<option value="${dVals[i]}">${T(k)}</option>`).join('');
  if(prev) dSel.value=prev;
  // radio groups
  const acOpts=[['none','EST_AC_NONE'],['light','EST_AC_LIGHT'],['mod','EST_AC_MOD'],['heavy','EST_AC_HEAVY']];
  renderEstRadios('est-ac-group','est-ac',acOpts,'mod');
  const wOpts=[['solar','EST_WATER_SOLAR'],['elec','EST_WATER_ELEC'],['other','EST_WATER_OTHER']];
  renderEstRadios('est-water-group','est-water',wOpts,'solar');
  const cOpts=[['yes','EST_YES'],['no','EST_NO']];
  renderEstRadios('est-cooking-group','est-cooking',cOpts,'no');
  document.getElementById('est-trigger-btn').textContent=T('BTN_ESTIMATE');
}
function renderEstRadios(groupId,name,opts,defaultVal){
  const g=document.getElementById(groupId);
  if(!g) return;
  const cur=g.querySelector('.active')?.dataset.val||defaultVal;
  g.innerHTML=opts.map(([v,k])=>
    `<label class="est-radio${cur===v?' active':''}" data-val="${v}" data-action="selectEstRadio" data-arg="${groupId}" data-arg2="${v}">
      <input type="radio" name="${name}" value="${v}"${cur===v?' checked':''}>${T(k)}
    </label>`
  ).join('');
}
function selectEstRadio(groupId,val){
  document.querySelectorAll(`#${groupId} .est-radio`).forEach(el=>{
    el.classList.toggle('active',el.dataset.val===val);
    el.querySelector('input').checked=el.dataset.val===val;
  });
}
function getEstRadio(groupId){
  const el=document.querySelector(`#${groupId} .est-radio.active`);
  return el?el.dataset.val:null;
}
function calcEstimate(){
  const dwelling=document.getElementById('est-dwelling').value||'apt2';
  const persons=Math.max(1,Math.min(10,parseInt(document.getElementById('est-persons').value)||2));
  const ac=getEstRadio('est-ac-group')||'mod';
  const water=getEstRadio('est-water-group')||'solar';
  const cooking=getEstRadio('est-cooking-group')||'no';
  const bases={studio:1200,apt1:1800,apt2:2600,apt3:3500,semi:4500,det_s:6000,det_l:9000};
  const acAdd={none:0,light:700,mod:1800,heavy:3500};
  const waterAdd={solar:300,elec:1200,other:0};
  let total=(bases[dwelling]||2600)+Math.max(0,persons-1)*600+(acAdd[ac]||0)+(waterAdd[water]||0)+(cooking==='yes'?400:0);
  total=Math.round(total/100)*100;
  window._estValue=total;
  document.getElementById('est-result-num').textContent=total.toLocaleString();
  document.getElementById('est-result-wrap').style.display='';
  document.getElementById('est-use-btn').style.display='';
}
function openEstMeth(){
  document.getElementById('meth-modal-overlay').style.display='flex';
}
function closeEstMeth(){
  document.getElementById('meth-modal-overlay').style.display='none';
}
function applyEstimate(){
  if(!window._estValue) return;
  setMode('annual');
  const ak=document.getElementById('annual-kwh');
  ak.value=window._estValue;
  onAnnualInput();
  closeEstimator();
}

// ── Event wiring ────────────────────────────────────────────────────────────
// No inline event-handler attributes (onclick and the like): the page runs under a strict Content-Security-
// Policy that refuses any code written inside the page (main.py, _CSP_POLICY).
// Elements say what they do with data-action (click), data-change, data-input,
// data-focus or data-backdrop-close, plus data-arg/data-arg2; this table is the
// complete list of what they may call. The innermost element with an action
// wins, so a supplier pill inside a card header doesn't also toggle the card.
const _ACTIONS = {
  setLang: el => setLang(el.dataset.arg),
  openNotices: () => openNotices(),
  closeNotices: () => closeNotices(),
  switchNoticesTab: el => switchNoticesTab(el.dataset.arg),
  toggleConn: () => toggleConn(),
  setCustomerType: el => setCustomerType(el.dataset.arg),
  onVoltageChange: () => onVoltageChange(),
  setLoadEntitlement: el => setLoadEntitlement(el.dataset.arg),
  applyFilters: () => applyFilters(),
  setMode: el => setMode(el.dataset.arg),
  onAnnualInput: () => onAnnualInput(),
  onMonthlyInput: () => onMonthlyInput(),
  onConsumptionFocus: () => onConsumptionFocus(),
  setBillingPeriod: el => setBillingPeriod(+el.dataset.arg),
  openEstimator: () => openEstimator(),
  closeEstimator: () => closeEstimator(),
  calcEstimate: () => calcEstimate(),
  applyEstimate: () => applyEstimate(),
  openEstMeth: () => openEstMeth(),
  closeEstMeth: () => closeEstMeth(),
  selectEstRadio: el => selectEstRadio(el.dataset.arg, el.dataset.arg2),
  openVulnerableModal: () => openVulnerableModal(),
  closeVulnerableModal: () => closeVulnerableModal(),
  openRegInfo: el => openRegInfo(el.dataset.arg, el.dataset.arg2),
  closeRegInfo: () => closeRegInfo(),
  toggleCard: el => toggleCard(el.dataset.arg),
  openSupContact: el => openSupContact(el.dataset.supplier),
  closeSupContact: () => closeSupContact(),
  reportTariff: el => openReportIssue(el.dataset.tid, el.dataset.tname, el.dataset.tsup),
  reportGeneral: () => openReportIssue(),
  closeReportIssue: () => closeReportIssue(),
  submitReportIssue: () => submitReportIssue(),
  openSampleInvoice: el => openSampleInvoice(el.dataset.tid, el),
  closeSampleInvoice: () => closeSampleInvoice(),
  toggleDiscount: el => toggleDiscount(el.dataset.tariff, +el.dataset.idx, el.checked),
  scrollToTop: () => window.scrollTo({top:0,behavior:'smooth'}),
  toggleA11yMode: () => toggleA11yMode(),
};
function _wire(eventName, attr){
  document.addEventListener(eventName, e => {
    const el = e.target.closest && e.target.closest(`[data-${attr}]`);
    if(!el) return;
    const fn = _ACTIONS[el.dataset[attr.replace(/-(\w)/g, (_, c) => c.toUpperCase())]];
    if(fn) fn(el, e);
  });
}
_wire('change', 'change');
_wire('input', 'input');
_wire('focusin', 'focus');
document.addEventListener('click', e => {
  // A modal closes when its dimmed backdrop itself is clicked, not the dialog inside it.
  if(e.target.dataset && e.target.dataset.backdropClose){
    const fn = _ACTIONS[e.target.dataset.backdropClose];
    if(fn) fn(e.target, e);
    return;
  }
  const el = e.target.closest && e.target.closest('[data-action]');
  if(!el) return;
  const fn = _ACTIONS[el.dataset.action];
  if(fn) fn(el, e);
});
// Keyboard: Enter/Space on the custom role="button" controls (card headers, pills, ⓘ).
document.addEventListener('keydown', e => {
  if(e.key !== 'Enter' && e.key !== ' ') return;
  const el = e.target.closest && e.target.closest('[role="button"][data-action]');
  if(!el || el !== e.target) return;
  e.preventDefault();
  const fn = _ACTIONS[el.dataset.action];
  if(fn) fn(el, e);
});
// Consumption boxes: plain non-negative kWh only. Number boxes otherwise accept
// "-", "+" and "e" (as in 5e3), and a negative or huge entry just showed no results.
// Those keys are ignored; anything pasted is cleaned up before the calculation runs.
const _KWH_MAX = 5000000;   // the server's limit (schemas._KWH_FIELD)
document.querySelectorAll('.kwh-input').forEach(box => {
  box.max = _KWH_MAX;
  box.addEventListener('keydown', e => { if(['-','+','e','E'].includes(e.key)) e.preventDefault(); });
  box.addEventListener('input', () => {
    if(box.value === '') return;
    const v = box.valueAsNumber;
    if(!(v >= 0)) box.value = '';
    else if(v > _KWH_MAX) box.value = _KWH_MAX;
    else if(/[eE+]/.test(box.value)) box.value = String(v);
  });
});
// The CERA logo falls back to a text badge if the image can't load (it may already
// have failed before this script ran).
(function(){
  const img = document.querySelector('.header-logo');
  if(!img) return;
  const fallback = () => { img.style.display='none'; document.getElementById('cera-fallback').style.display='flex'; };
  if(img.complete && !img.naturalWidth) fallback(); else img.addEventListener('error', fallback);
})();

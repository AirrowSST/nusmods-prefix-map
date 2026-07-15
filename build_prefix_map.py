"""Build the NUSMods module-prefix map (fully online, self-contained).

Emits a small shell page (prefix_map.html) that fetches moduleInfo.json from the
NUSMods API on load and computes the whole faculty -> department -> prefix tree in
the browser. Only the curated glosses, display config and CSS are baked in below.

This is the single source of truth: edit CURATED / ABBR / DEPT_FIX / PALETTE here,
then re-run `python build_prefix_map.py`.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))

ACAD_YEAR = "2026-2027"  # floor + default label; the page auto-advances to the current AY at runtime (falls back to this)

ABBR = {
    "Arts and Social Science": "FASS",
    "College of Design and Engineering": "CDE",
    "NUS Business School": "BIZ",
    "Computing": "SoC",
    "Science": "FoS",
    "Law": "LAW",
    "Yong Loo Lin Sch of Medicine": "YLLSoM",
    "Duke-NUS Medical School": "Duke-NUS",
    "Dentistry": "DEN",
    "SSH School of Public Health": "SSHSPH",
    "LKY School of Public Policy": "LKYSPP",
    "YST Conservatory of Music": "YSTCM",
    "Yale-NUS College": "Yale-NUS",
    "NUS College": "NUSC",
    "Residential College": "RC",
    "Cont and Lifelong Education": "SCALE",
    "NUS-ISS": "ISS",
    "Center for Engl Lang Comms": "CELC",
    "NUS Graduate School": "NUSGS",
    "Temasek Defence Sys. Institute": "TDSI",
    "Risk Management Institute": "RMI",
    "Multi Disciplinary Programme": "MDP",
    "Mechanobiology Institute (MBI)": "MBI",
    "Logistics Inst-Asia Pac": "TLI-AP",
    "Non-Faculty-based Departments": "NFB",
    "NUS": "NUS",
}

DEPT_FIX = {
    "English,Ling.andTheatre Studies": "English, Linguistics & Theatre Studies",
    "PharmacyandPharmaceuticalScience": "Pharmacy & Pharmaceutical Sciences",
}

CURATED = {
    # ---- FASS: Arts & Social Sciences ----
    "PS": "Political Science", "HY": "History", "EC": "Economics", "ECA": "Economics (applied)",
    "PL": "Psychology", "PLC": "Clinical Psychology", "PLS": "Psychology (personal development)",
    "PLB": "Psychology (elective)", "CH": "Chinese Studies", "CL": "Chinese Language",
    "CHC": "Chinese Studies (grad)", "TRA": "Translation & Interpreting", "INT": "Interpretation & Translation",
    "EN": "English Literature", "ENC": "English Literature (grad)", "EL": "English Language & Linguistics",
    "ELC": "Linguistics (grad)", "SC": "Sociology & Anthropology", "AN": "Anthropology", "GSA": "Sociology & Anthropology (grad)",
    "GE": "Geography", "GI": "Geospatial Intelligence", "CCS": "Climate Change & Sustainability",
    "PH": "Philosophy", "PE": "Philosophy, Politics & Economics", "NM": "Communications & New Media",
    "NMC": "Communications & New Media (grad)", "VCU": "Communications & New Media (capstone)",
    "ACE": "Arts & Cultural Entrepreneurship", "CSA": "Cultural Studies", "SW": "Social Work",
    "SWD": "Social Work (grad)", "SWM": "Social Work (Mgmt)", "SWK": "Criminology & Rehabilitation",
    "SE": "Southeast Asian Studies", "SEA": "Southeast Asian Studies (grad)", "CAS": "Comparative Asian Studies",
    "JS": "Japanese Studies", "JSC": "Japanese Studies (grad)", "GL": "Global Studies", "TS": "Theatre & Performance",
    "TPS": "Theatre & Performance (grad)", "SN": "South Asian Studies", "SNG": "South Asian Studies (grad)",
    "MS": "Malay Studies", "EU": "European Studies", "AS": "American Studies", "AH": "Art History",
    "SSA": "Singapore Studies", "NHS": "Interdisciplinary Humanities", "UIS": "Independent Study modules",
    "FAS": "Internships & academic writing", "ASP": "Research programme (H3)",
    "DMA": "Design-Your-Own module", "AX": "Exchange placeholder", "RX": "Exchange placeholder",
    "GN": "Exchange placeholder", "CK": "China Studies internship", "XD": "Interdisciplinary courses",
    "SSX": "Exchange placeholder", "XFA": "Integrated Honours project", "FMA": "Field Studies modules",
    "HSA": "Interdisciplinary Asian Studies", "HSH": "Interdisciplinary Humanities",
    "HSS": "Interdisciplinary Social Science", "HS": "Career readiness (Career Compass)",
    "IAN": "Internship (Anthropology)", "IEU": "Internship (European Studies)", "IGL": "Internship (Global Studies)",
    "IJS": "Internship (Japanese Studies)", "INM": "Internship (Communications & New Media)", "IPS": "Internship (Political Science)",
    "ISC": "Internship (Sociology)", "ISE": "Internship (Southeast Asian Studies)", "ISN": "Internship (South Asian Studies)",
    "UTOA": "Teaching assistantship (UTOP)",
    # Centre for Language Studies
    "LAB": "Indonesian", "LAC": "Chinese", "LAF": "French", "LAG": "German",
    "LAH": "Hindi", "LAJ": "Japanese", "LAK": "Korean", "LAL": "Tamil", "LAM": "Malay",
    "LAR": "Arabic", "LAS": "Spanish", "LAT": "Thai", "LAV": "Vietnamese", "LAX": "Exchange placeholder",
    # General Education pillars
    "GEA": "Gen-Ed: Data Literacy", "GEC": "Gen-Ed: Cultures & Connections", "GEH": "Gen-Ed: Human Cultures",
    "GEI": "Gen-Ed: Digital Literacy", "GEK": "Gen-Ed: Broadening", "GEM": "Gen-Ed: Broadening",
    "GEN": "Gen-Ed: Communities & Engagement", "GEQ": "Gen-Ed: Asking Questions", "GER": "Gen-Ed: Quantitative Reasoning",
    "GES": "Gen-Ed: Singapore Studies", "GESS": "Gen-Ed: Singapore Studies", "GET": "Gen-Ed: Thinking & Expression",
    "GEX": "Gen-Ed: Critique & Expression", "GXK": "Exchange placeholder (Gen-Ed)", "GDM": "Placeholder module",
    # ---- CELC: Centre for English Language Communication ----
    "UTW": "Critical thinking & writing", "ES": "Academic & Professional English",
    "RVX": "Communication seminars", "EM": "Academic English (Music)",
    # ---- CDE: College of Design & Engineering ----
    "IE": "Industrial & Systems Eng.", "EE": "Electrical & Computer Eng.", "CE": "Civil & Environmental Eng.",
    "CEE": "Civil & Environmental Eng.", "ME": "Mechanical Eng.", "AR": "Architecture",
    "ARD": "Architecture design studio", "ARX": "Exchange placeholder", "AC": "Architectural Conservation",
    "CN": "Chemical & Biomolecular Eng.", "MLE": "Materials Science & Eng.", "MST": "Materials Science",
    "ID": "Industrial Design", "IDX": "Exchange placeholder", "BN": "Biomedical Eng.",
    "ESE": "Environmental & Sustainability Eng.", "SH": "Safety & Health Eng.",
    "MT": "Technology & Innovation Mgmt", "OT": "Offshore & Petroleum Eng.", "ESP": "Engineering Science",
    "CDE": "Interdisciplinary design & innovation", "EG": "Eng. (common core)", "PF": "Project & Facilities Mgmt",
    "LA": "Landscape Architecture", "LAD": "Landscape Architecture", "BPS": "Building Performance (grad)",
    "DEP": "Urban & Regional Planning", "IPM": "Infrastructure & Project Mgmt", "PM": "Project Mgmt",
    "CEG": "Computer Eng.", "RB": "Robotics", "EEK": "Semiconductor & IC Eng.", "SYE": "Systems Eng.",
    "TD": "Technology & Design (systems)", "UD": "Urban Design", "DE": "Environmental Mgmt",
    "CIT": "Cities & Urban Systems", "ISD": "Sustainable Design studio", "MTM": "Maritime Technology & Mgmt",
    "SDM": "Systems Design & Mgmt", "BS": "Built Environment (research)", "DTK": "Design Thinking",
    "TP": "Transportation Eng.", "NE": "Nanoengineering", "TDEE": "Electronic Devices & Materials",
    "TDEG": "Eng. (Tech & Design)", "DMD": "Design-Your-Own module", "SSD": "Singapore Built Environment",
    "BX": "Interdisciplinary elective", "LX": "Environmental Law elective", "EX": "Exchange placeholder",
    "PFX": "Exchange placeholder", "UTOD": "Teaching assistantship (UTOP)",
    "UTOE": "Teaching assistantship (UTOP)", "XFE": "Integrated Honours project",
    # ---- Computing ----
    "CS": "Computer Science", "IS": "Information Systems & Analytics", "CP": "Computing (innovation & self-study)",
    "BT": "Business Analytics", "IT": "Computing (general IT)", "IFS": "Information Security",
    "AI": "Artificial Intelligence (exec)", "FT": "FinTech", "CSX": "Exchange placeholder",
    "DMC": "Design-Your-Own module", "UTOC": "Teaching assistantship (UTOP)", "XFC": "Integrated Honours project",
    # ---- SCALE: Continuing & Lifelong Education (BTech / part-time) ----
    "TCE": "BTech Civil Eng.", "TEE": "BTech Electrical Eng.", "TME": "BTech Mechanical Eng.",
    "TCN": "BTech Chemical Eng.", "TIC": "BTech Computing", "TCX": "BTech Computing",
    "TIE": "BTech Industrial Eng.", "TBA": "Business Analytics", "MSI": "AI & Innovation",
    "TSC": "BTech Supply Chain", "TE": "BTech Eng.", "TM": "BTech Eng.",
    "TTG": "BTech Eng. (general)", "AII": "AI & Innovation", "TX": "BTech (general electives)",
    "MEM": "Environmental Mgmt", "TC": "BTech Chemical Eng.", "TG": "BTech Eng. (general)",
    "TMA": "BTech Mathematics", "SSE": "BTech (electives)",
    # ---- Dentistry ----
    "RD": "Restorative Dentistry", "PRV": "Preventive Dentistry", "DY": "Dentistry (grad)",
    "OMS": "Oral & Maxillofacial Surgery", "BV": "Behavioural Science", "GPM": "Dental Practice Mgmt",
    "RY": "Dental Radiology", "DI": "Dental Implantology", "CD": "Clinical Dentistry",
    "IY": "Independent Study", "OL": "Oral Biology", "OY": "Oral Pathology", "RS": "Research (UROP)",
    # ---- Duke-NUS / LKYSPP ----
    "GMS": "Medicine", "PP": "Public Policy", "PPX": "Exchange placeholder",
    # ---- Law ----
    "LL": "Law", "LLJ": "Law (grad)", "LC": "Law (LLB core)", "LLD": "Law (doctoral)",
    "LE": "Exchange placeholder", "LCJ": "Law (JD core)", "LCC": "Law (common law)", "LCD": "Law (grad)",
    # ---- Institutes / interdisciplinary ----
    "LI": "Logistics & Supply Chain", "MB": "Mechanobiology (external)", "CG": "Computer Eng.",
    "FE": "Financial Eng.", "DTS": "Defence Technology & Systems", "QT": "Quantum Technologies",
    # ---- NUS central units ----
    "ETP": "Entrepreneurship", "TR": "Entrepreneurship & start-ups", "CFG": "Career readiness",
    "DMX": "Design-Your-Own module", "ADS": "Applied Data Science", "CLC": "Community Leadership",
    "SFI": "Southeast Asia immersion", "THE": "Wellbeing & learning skills", "RW": "Wellbeing modules",
    "ALS": "Learning skills", "IDS": "Data Science (grad)", "POY": "Polytechnic bridging modules",
    "BBB": "Advanced Placement credit", "BBC": "Credit transfer", "BBD": "Advanced Placement credit",
    "DMY": "Design-Your-Own module",
    # ---- NUS Business School ----
    "BMA": "Business Administration (grad)", "BMS": "Business (grad core)", "FIN": "Finance",
    "MKT": "Marketing", "MNO": "Mgmt & Organisation", "RE": "Real Estate", "REX": "Exchange placeholder",
    "BME": "Business (exec)", "ACC": "Accounting", "BAA": "Accounting (PhD)", "BMC": "Business Mgmt (grad)",
    "BXT": "Exchange placeholder", "DOS": "Operations & Supply Chain", "DBA": "Business Analytics & Operations",
    "DAO": "Decision Analytics & Operations", "DSC": "Decision Analytics", "DSN": "Analytics",
    "BMF": "Finance (grad)", "BMD": "Finance (FinTech)", "BMK": "Marketing Analytics", "BZD": "Business research methods (PhD)",
    "BSP": "Strategy & Policy", "BSN": "Entrepreneurship", "BBP": "Business (PhD)", "BSE": "Business Economics",
    "BSS": "Business seminars", "SSB": "Business Law", "BI": "Business Internship", "BWS": "Work-study internship",
    "DMB": "Design-Your-Own module", "BDC": "Operations Research (PhD)", "BMT": "Accounting & Analytics",
    "BMO": "Mgmt & Organisation (PhD)", "BMH": "HR Analytics", "BMG": "Sustainable Finance", "BMP": "Business Strategy (exec)",
    "BMU": "Business (MBA core)", "BMX": "Business (exec)", "IND": "Industry 4.0 & consulting",
    "BLD": "Leadership Development", "BRP": "Business (PhD seminars)", "BHD": "Honours dissertation",
    "BPM": "Business foundations", "BST": "Business (special topics)", "STR": "Career readiness",
    "XFB": "Integrated Honours project", "BCP": "Consulting Practicum", "FSP": "Field Service Project",
    "UTOB": "Teaching assistantship (UTOP)",
    # ---- NUS College ----
    "NST": "NUS College: Science & Technology", "NTW": "NUS College: Thinking with Writing", "NEX": "NUS College: Global Experience",
    "NFB": "Exchange placeholder", "NFC": "Exchange placeholder", "NFS": "Exchange placeholder",
    "NGN": "NUS College: Global Narratives", "NHT": "NUS College: Creative", "NSW": "NUS College: Understanding the Social World",
    "NEP": "NUS College: Impact Experience", "NSS": "NUS College: Science & Society", "NGT": "NUS College: Global Social Thought",
    "NPS": "NUS College: Problem Solving", "NRM": "NUS College: Research (UROP)",
    # ---- NUS Graduate School ----
    "GS": "Graduate research skills", "NG": "Graduate research skills", "GSN": "Neuroscience (grad)",
    "GSE": "Exchange placeholder (grad)", "LSE": "Environmental Life Sciences Eng.", "GSC": "Computational Biology",
    "GSG": "Materials Science (grad)", "GSS": "Graduate seminars",
    # ---- NUS-ISS: Institute of Systems Science ----
    "EBA": "Business Analytics", "DL": "Digital Leadership", "ED": "Digital Technology Mgmt",
    "SA": "Software Eng.", "SWE": "Software Eng. (grad)", "ISY": "Intelligent Systems",
    "EDT": "Digital Technology Mgmt",
    # ---- Residential Colleges ----
    "UTC": "UTown College Programme", "UTS": "UTown College: Singapore Studies", "RVN": "Ridge View College",
    "RVC": "Ridge View College", "RVSS": "Ridge View College", "RVR": "Ridge View College: Research", "DMR": "Design-Your-Own module",
    "WR": "Workplace Readiness", "UTOR": "Teaching assistantship (UTOP)",
    # ---- Public Health ----
    "SPH": "Public Health", "HE": "Health Economics (HEOR)",
    # ---- Science ----
    "MA": "Mathematics", "LSM": "Life Sciences", "PC": "Physics", "CM": "Chemistry", "SCE": "Chemistry (sustainability)",
    "PR": "Pharmacy", "PHS": "Pharmaceutical Science", "ST": "Statistics & Data Science", "DSS": "Data Science (applied)",
    "FST": "Food Science & Technology", "DSA": "Data Science & Analytics", "BL": "Biological Sciences",
    "ZB": "Bioinformatics", "QF": "Quantitative Finance", "DSE": "Data Science & Economics", "ENV": "Environmental Studies",
    "FSC": "Forensic Science", "SP": "Science research & communication", "MW": "Science Communication",
    "HSI": "Gen-Ed: Scientific Inquiry", "AIS": "AI in Science", "COS": "Computational Thinking",
    "CZ": "Computational Science & Eng.", "ML": "Materials Science (grad)", "LSX": "Veterinary Science (exchange)",
    "SX": "Exchange placeholder", "SCI": "External modules", "DMS": "Design-Your-Own module",
    "FDP": "Foundation Maths & Physics", "XFS": "Integrated Honours project", "SSS": "Natural Heritage of Singapore",
    "UTOS": "Teaching assistantship (UTOP)",
    # ---- YST Conservatory of Music ----
    "MUA": "Music (performance)", "MUT": "Music Theory & Composition", "MUH": "Music History",
    "MUL": "Languages for Musicians", "MUX": "Exchange placeholder", "CFA": "Performing Arts practice",
    "UTOM": "Teaching assistantship (UTOP)",
    # ---- Yale-NUS College (winding down) ----
    "YHU": "Yale-NUS: Humanities", "YSS": "Yale-NUS: Social Sciences", "YSC": "Yale-NUS: Sciences",
    "YCC": "Yale-NUS: Common Curriculum", "YID": "Yale-NUS: Environmental Studies", "YIR": "Yale-NUS: Independent Research",
    "YCI": "Yale-NUS: Exchange", "YLE": "Yale-NUS: Exchange", "YIL": "Yale-NUS: Languages", "YLC": "Yale-NUS: Chinese",
    "YLS": "Yale-NUS: Spanish", "YLG": "Yale-NUS: Ancient Greek", "YLL": "Yale-NUS: Latin", "YLN": "Yale-NUS: Singapore Sign Language",
    "YCT": "Yale-NUS: College Seminars", "YSP": "Yale-NUS: Strategy & Leadership",
    # ---- Yong Loo Lin School of Medicine ----
    "NUR": "Nursing", "NX": "Exchange placeholder", "MD": "Medicine (MBBS)", "MDG": "Biomedical Science (grad)",
    "SLP": "Speech & Language Pathology", "PHC": "Pharmacology", "PA": "Pharmacology", "BMI": "Biomedical Informatics",
    "AUD": "Audiology", "PHM": "Precision Medicine", "CMH": "Clinical Mental Health", "HM": "Psychiatry (grad)",
    "BIS": "Behavioural & Implementation Science", "BIH": "Behavioural & Implementation Science",
    "HPP": "Human Potential & Performance", "ABM": "Biomedicine (grad)", "IDE": "Infectious Disease & Outbreak",
    "SM": "Sustainable Healthcare", "NLM": "Nutrition & Lifestyle Medicine", "MCI": "Clinical Research",
    "CAH": "Child & Adolescent Health", "OPT": "Optometry", "VM": "Palliative Medicine", "MIH": "Integrative Health",
    "CDM": "Cancer Biology", "EHB": "Bioethics", "HI": "Health Informatics", "HLM": "Healthy Longevity Medicine",
    "HLE": "Healthcare Law & Ethics", "AY": "Anatomy", "MIC": "Microbiology & Immunology", "PX": "Pathology",
    "PY": "Physiology", "VHC": "Sports & Health", "UTON": "Teaching assistantship (UTOP)",
}

PALETTE = ["#4f46e5", "#0891b2", "#059669", "#d97706", "#dc2626", "#7c3aed",
           "#db2777", "#2563eb", "#65a30d", "#ea580c", "#0d9488", "#9333ea",
           "#c026d3", "#e11d48", "#0284c7", "#16a34a", "#ca8a04", "#be123c",
           "#7c2d12", "#1e40af", "#4d7c0f", "#a21caf", "#0f766e", "#b91c1c",
           "#334155", "#475569"]


CSS = r""":root{--bg:#f7f7f9;--card:#fff;--ink:#1a1a1f;--mut:#6b7280;--line:#e6e6eb;}
*{box-sizing:border-box}
body{margin:0;font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
background:var(--bg);color:var(--ink)}
header{position:sticky;top:0;z-index:10;background:rgba(247,247,249,.92);
backdrop-filter:blur(8px);border-bottom:1px solid var(--line);padding:16px 24px}
h1{margin:0 0 2px;font-size:19px;letter-spacing:-.01em}
.sub{color:var(--mut);font-size:13px}
.stats{display:flex;gap:18px;margin-top:10px;flex-wrap:wrap}
.stat b{font-size:18px} .stat span{color:var(--mut);font-size:12px;display:block}
.controls{display:flex;gap:12px;margin-top:12px;align-items:center;flex-wrap:wrap}
#q{flex:1;min-width:220px;padding:9px 13px;border:1px solid var(--line);border-radius:9px;
font-size:14px;background:var(--card)}
.toggle{font-size:13px;color:var(--mut);display:flex;gap:6px;align-items:center;cursor:pointer;user-select:none}
#minorN{width:44px;padding:2px 5px;border:1px solid var(--line);border-radius:6px;font:inherit;font-size:12.5px}
main{max-width:1180px;margin:20px auto;padding:0 24px 80px}
.fac{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--c);
border-radius:12px;margin-bottom:14px;overflow:hidden}
.fac-h{width:100%;display:flex;align-items:center;gap:12px;padding:14px 18px;border:0;
background:none;cursor:pointer;text-align:left;font:inherit}
.badge{background:var(--c);color:#fff;font-weight:700;font-size:12px;padding:3px 9px;
border-radius:6px;letter-spacing:.02em;white-space:nowrap}
.fac-name{font-weight:650;font-size:16px}
.fac-stats{margin-left:auto;color:var(--mut);font-size:12.5px;white-space:nowrap}
.caret{color:var(--mut);margin-left:6px}
.fac.closed .caret{transform:rotate(-90deg)}
.fac-body{padding:4px 18px 16px}
.btn{font:inherit;font-size:13px;padding:8px 13px;border:1px solid var(--line);
border-radius:9px;background:var(--card);color:var(--ink);cursor:pointer}
.btn:hover{border-color:#c7c7d1}
.dept{padding:12px 0;border-top:1px dashed var(--line)}
.dept-h{width:100%;display:flex;align-items:center;gap:6px;padding:0;margin-bottom:9px;
border:0;background:none;cursor:pointer;text-align:left;font:inherit;
font-size:13px;font-weight:650;color:#374151}
.dcaret{color:var(--mut);font-size:10px;flex:none}
.dept.dclosed .dcaret{transform:rotate(-90deg)}
/* collapsed department: prefixes compact to an inline row on the header line */
.dept.dclosed{display:flex;flex-wrap:wrap;align-items:center;gap:6px 10px}
.dept.dclosed .dept-h{width:auto;margin-bottom:0;flex:none}
.dept.dclosed .chips{display:flex;flex-wrap:wrap;gap:6px;margin:0}
.dept.dclosed .chip{padding:2px 9px;border-radius:7px;display:inline-flex;align-items:center;gap:5px;background:#fff}
.dept.dclosed .chip>.gloss,.dept.dclosed .chip>.cnt,.dept.dclosed .chip>.ratio,.dept.dclosed .chip>.ratio-l,.dept.dclosed .chip>.eg{display:none}
.dept.dclosed .pfx{font-size:13px;font-weight:700}
.dept.dclosed .span{font-size:10px}
.dept-c{font-weight:400;color:var(--mut);font-size:12px;margin-left:6px}
.dept-hidden{font-weight:600;font-size:11px;color:#b45309;background:#fef3c7;
border-radius:20px;padding:1px 8px;margin-left:8px}
.dept-hidden:empty{display:none}
.chips{display:grid;grid-template-columns:repeat(auto-fill,minmax(158px,1fr));gap:8px}
.chip{border:1px solid var(--line);border-radius:9px;padding:9px 11px;background:#fcfcfd;
transition:border-color .15s,box-shadow .15s}
.chip:hover{border-color:var(--c);box-shadow:0 1px 6px rgba(0,0,0,.05)}
/* grad-only prefixes: subtle red outline + tint */
.chip[data-gradonly="1"]{border-color:#e9b0b0;background:#fdf4f4}
.chip[data-gradonly="1"]:hover{border-color:#d76b6b;box-shadow:0 1px 6px rgba(180,40,40,.09)}
.dept.dclosed .chip[data-gradonly="1"]{background:#fbeded}
.pfx{font-weight:750;font-size:16px;letter-spacing:.01em;color:var(--c)}
.span{font-size:11px;color:var(--mut)}
.gloss{font-size:12px;font-weight:600;color:#111827;margin-top:2px;line-height:1.3}
.cnt{font-size:12px;color:#374151;margin-top:3px}
.cnt .off{color:var(--mut);margin-left:7px}
.ratio{display:flex;height:3px;border-radius:2px;overflow:hidden;margin-top:8px;background:#edf0f3}
.ratio .ug{background:#7c9cc4}
.ratio .gr{background:#c78287}
.ratio.nolevel{background:repeating-linear-gradient(45deg,#e9ebee,#e9ebee 3px,#f3f4f6 3px,#f3f4f6 6px)}
.ratio-l{display:flex;justify-content:space-between;font-size:9.5px;margin-top:2px;color:var(--mut)}
.ru,.rg,.rn{color:var(--mut);font-weight:400}
.eg{font-size:11px;color:var(--mut);margin-top:4px;white-space:nowrap;overflow:hidden;
text-overflow:ellipsis}
.chip{cursor:pointer}
.chip:focus-visible{outline:2px solid var(--c);outline-offset:1px}
.hide{display:none!important}
/* chips filtered out by the toggles: greyed card while the dept is expanded,
   removed (and counted as "N hidden") once the dept is collapsed to pills */
.dept:not(.dclosed) .chip.filtered{opacity:.4;filter:grayscale(.9)}
.dept:not(.dclosed) .chip.filtered:hover{opacity:.75;filter:grayscale(.35)}
.dept.dclosed .chip.filtered{display:none}
.dept:not(.dclosed) .dept-hidden{display:none}
/* instant (0-delay) hover tooltip for prefix descriptions */
#tip{position:fixed;z-index:60;pointer-events:none;display:none;max-width:280px;
background:#1a1a1f;color:#fff;font-size:12px;line-height:1.35;padding:5px 9px;
border-radius:6px;box-shadow:0 4px 14px rgba(0,0,0,.22)}
#tip.on{display:block}
footer{text-align:center;color:var(--mut);font-size:12px;padding:24px}
/* detail drawer */
#ov{position:fixed;inset:0;background:rgba(15,15,20,.5);backdrop-filter:blur(2px);
z-index:50;display:none}
#ov.on{display:block}
#drw{position:fixed;top:0;right:0;height:100%;width:min(640px,100%);background:var(--card);
box-shadow:-8px 0 40px rgba(0,0,0,.2);transform:translateX(100%);transition:transform .22s ease;
display:flex;flex-direction:column;z-index:51}
#ov.on #drw{transform:none}
.d-head{padding:18px 20px;border-bottom:1px solid var(--line)}
.d-top{display:flex;align-items:center;gap:11px}
.d-badge{color:#fff;font-weight:750;font-size:15px;padding:5px 12px;border-radius:8px}
.d-gloss{font-size:13.5px;font-weight:600;color:#111827;margin-top:7px}
.d-gloss:empty{display:none}
.d-sub{color:var(--mut);font-size:12.5px;margin-top:6px}
#dx{margin-left:auto;border:0;background:none;font-size:22px;color:var(--mut);cursor:pointer;
line-height:1;padding:2px 6px}
#dq{margin-top:12px;width:100%;padding:8px 12px;border:1px solid var(--line);border-radius:8px;
font-size:13.5px}
.d-body{overflow-y:auto;padding:8px 20px 40px}
.mod{padding:13px 0;border-bottom:1px solid var(--line)}
.mod-h{display:flex;align-items:baseline;gap:9px;flex-wrap:wrap}
.mod-c{font-weight:750;font-size:14px}
.mod-t{font-size:13.5px}
.mod-tag{font-size:10.5px;padding:1px 7px;border-radius:20px;background:#eef;color:#3730a3}
.mod-tag.live{background:#dcfce7;color:#166534}
.mod-tag.dorm{background:#f1f5f9;color:#64748b}
.mod-d{font-size:12.5px;color:#4b5563;margin-top:6px;line-height:1.55}
.mod-d.load,.mod-d.err{color:#9aa1ab;font-style:italic}
.d-count{font-size:12px;color:var(--mut);margin:6px 0 2px}"""

CFG = {"ACAD_YEAR": ACAD_YEAR, "ABBR": ABBR, "DEPT_FIX": DEPT_FIX,
       "CURATED": CURATED, "PALETTE": PALETTE}

CFG_JSON = json.dumps(CFG, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

# Extra CSS for the online-only loading / error states.
EXTRA_CSS = """
#loading,#errbox{text-align:center;color:var(--mut);padding:64px 20px;font-size:14px}
#errbox{display:none}
#errbox.on{display:block}
#loading .spin{display:inline-block;width:18px;height:18px;margin-right:9px;vertical-align:-3px;
border:2px solid var(--line);border-top-color:#4f46e5;border-radius:50%;animation:spin .8s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.retry{font:inherit;font-size:13px;margin-top:14px;padding:8px 16px;border:1px solid var(--line);
border-radius:9px;background:var(--card);color:var(--ink);cursor:pointer}
.retry:hover{border-color:#c7c7d1}
"""

# ---- the page's own runtime: fetch -> compute -> render -> interact ----
JS = r"""
const CFG=JSON.parse(document.getElementById('CFG').textContent);
const CURATED=CFG.CURATED,ABBR=CFG.ABBR,DEPT_FIX=CFG.DEPT_FIX,PALETTE=CFG.PALETTE,ACAD_YEAR=CFG.ACAD_YEAR;
let DATA={};

const grid=document.getElementById('grid'),loading=document.getElementById('loading'),errbox=document.getElementById('errbox');
const ov=document.getElementById('ov'),dbody=document.getElementById('dbody'),dq=document.getElementById('dq'),dcount=document.getElementById('dcount');
const q=document.getElementById('q'),live=document.getElementById('liveOnly'),nores=document.getElementById('nores');
const hideMinor=document.getElementById('hideMinor'),minorN=document.getElementById('minorN'),hideGrad=document.getElementById('hideGrad');
const s_mod=document.getElementById('s-mod'),s_off=document.getElementById('s-off'),s_pfx=document.getElementById('s-pfx'),s_fac=document.getElementById('s-fac'),s_dep=document.getElementById('s-dep');
let curColor='#4f46e5';

/* ---------- helpers (mirrors of the Python build) ---------- */
function esc(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
function cleanDep(n){n=DEPT_FIX[n]||n;n=n.replace(/’/g,"'");n=n.replace(/([,.;:])(?=\S)/g,'$1 ');return n.trim();}
function prefixOf(code){const m=/^([A-Z]+)/.exec(code||'');return m?m[1]:null;}
function inc(map,k){map.set(k,(map.get(k)||0)+1);}
function topKey(map){let bk=null,bv=-1;for(const [k,v] of map){if(v>bv){bv=v;bk=k;}}return bk;}
function sumTotal(recs){let s=0;for(const r of recs)s+=r.total;return s;}

/* ---------- build the tree from raw moduleInfo ---------- */
function build(mods){
  const pf=new Map(),modrecs=new Map();
  for(const m of mods){
    const p=prefixOf(m.moduleCode); if(!p)continue;
    if(!pf.has(p)){pf.set(p,{fac:new Map(),dep:new Map(),total:0,offered:0,ug:0,grad:0,examples:new Map()});modrecs.set(p,[]);}
    const e=pf.get(p);
    inc(e.fac,m.faculty||'(none)');
    inc(e.dep,cleanDep(m.department||'(none)'));
    e.total++;
    const off=Array.isArray(m.semesterData)&&m.semesterData.length>0;
    if(off)e.offered++;
    if(m.title)inc(e.examples,m.title);
    let dig=null; for(const c of (m.moduleCode||'')){if(c>='0'&&c<='9'){dig=c;break;}}
    if(dig){if('1234'.includes(dig))e.ug++;else e.grad++;}
    modrecs.get(p).push({c:m.moduleCode||'',t:m.title||'',u:m.moduleCredit||'',o:off?1:0,d:(m.description||'').trim()});
  }
  for(const recs of modrecs.values())recs.sort((a,b)=>a.c<b.c?-1:a.c>b.c?1:0);
  const tree=new Map(),facTot=new Map(),facOff=new Map();
  DATA={};
  for(const [p,e] of pf){
    const fac=topKey(e.fac),dep=topKey(e.dep);
    const rec={prefix:p,total:e.total,offered:e.offered,ug:e.ug,grad:e.grad,spanFac:e.fac.size,example:topKey(e.examples)||''};
    if(!tree.has(fac))tree.set(fac,new Map());
    const dm=tree.get(fac); if(!dm.has(dep))dm.set(dep,[]);
    dm.get(dep).push(rec);
    facTot.set(fac,(facTot.get(fac)||0)+e.total);
    facOff.set(fac,(facOff.get(fac)||0)+e.offered);
    DATA[p]={fac,abbr:ABBR[fac]||fac.slice(0,4).toUpperCase(),dep,gloss:CURATED[p]||'',total:e.total,offered:e.offered,m:modrecs.get(p)};
  }
  const facOrder=[...facTot.keys()].sort((a,b)=>facTot.get(b)-facTot.get(a)); // stable -> ties keep first-seen
  return {tree,facTot,facOff,facOrder};
}

/* ---------- render the same DOM the Python page produced ---------- */
function render(b){
  const secs=[];
  b.facOrder.forEach((fac,i)=>{
    const color=PALETTE[i%PALETTE.length];
    const abbr=ABBR[fac]||fac.slice(0,4).toUpperCase();
    const depts=[...b.tree.get(fac).entries()].sort((x,y)=>sumTotal(y[1])-sumTotal(x[1]));
    let nPfx=0; depts.forEach(([,r])=>nPfx+=r.length);
    const deptHtml=depts.map(([dep,recs])=>{
      const chips=recs.map(r=>{
        const span=r.spanFac>1?' <span class="span" title="also appears in other faculties/departments">⧉</span>':'';
        const ug=r.ug,gr=r.grad,known=ug+gr; let bar;
        if(known){const ugp=Math.round(ug*100/known);
          bar='<div class="ratio" title="'+ug+' undergraduate · '+gr+' graduate ('+ugp+'% UG)">'
            +'<span class="ug" style="width:'+ugp+'%"></span><span class="gr" style="width:'+(100-ugp)+'%"></span></div>'
            +'<div class="ratio-l"><span class="ru">'+ug+' UG</span><span class="rg">'+gr+' grad</span></div>';
        }else{bar='<div class="ratio nolevel" title="no level data"></div><div class="ratio-l"><span class="rn">no level</span></div>';}
        const gradOnly=(r.grad>0&&r.ug===0)?1:0;
        const gloss=CURATED[r.prefix]||'';
        const tip=esc(r.prefix)+(gloss?' — '+esc(gloss):'');
        return '<div class="chip" onclick="openPrefix(\''+esc(r.prefix)+'\')" role="button" tabindex="0" '
          +'data-search="'+esc(r.prefix.toLowerCase())+' '+esc(dep.toLowerCase())+' '+esc(fac.toLowerCase())+' '+esc(abbr.toLowerCase())+'" '
          +'data-offered="'+r.offered+'" data-total="'+r.total+'" data-gradonly="'+gradOnly+'" data-tip="'+tip+'">'
          +'<div class="pfx">'+esc(r.prefix)+span+'</div>'
          +'<div class="gloss">'+esc(gloss)+'</div>'
          +'<div class="cnt"><b>'+r.total+'</b> modules<span class="off">'+r.offered+' live</span></div>'
          +bar
          +'<div class="eg" title="e.g. '+esc(r.example)+'">e.g. '+esc(r.example)+'</div></div>';
      }).join('');
      return '<div class="dept"><button class="dept-h" onclick="this.parentElement.classList.toggle(\'dclosed\')">'
        +'<span class="dcaret">▾</span><span class="dept-n">'+esc(dep)+'</span>'
        +'<span class="dept-c">'+recs.length+' prefixes · '+sumTotal(recs)+' modules</span>'
        +'<span class="dept-hidden"></span></button><div class="chips">'+chips+'</div></div>';
    }).join('');
    secs.push('<section class="fac" style="--c:'+color+'" data-fac="'+esc(fac.toLowerCase())+' '+esc(abbr.toLowerCase())+'">'
      +'<button class="fac-h" onclick="toggleFac(this)"><span class="badge">'+esc(abbr)+'</span>'
      +'<span class="fac-name">'+esc(fac)+'</span>'
      +'<span class="fac-stats">'+nPfx+' prefixes · '+b.facTot.get(fac).toLocaleString()+' modules · '+b.facOff.get(fac).toLocaleString()+' live</span>'
      +'<span class="caret">▾</span></button><div class="fac-body">'+deptHtml+'</div></section>');
  });
  grid.innerHTML=secs.join('');
}

/* ---------- drawer (descriptions come from the fetched payload) ---------- */
function facColor(el){const s=el.closest('.fac');return s?getComputedStyle(s).getPropertyValue('--c').trim():'#4f46e5';}
function openPrefix(p){
  const info=DATA[p]; if(!info)return;
  const src=(typeof event!=='undefined'&&event&&event.currentTarget)?event.currentTarget:null;
  curColor=src?facColor(src):'#4f46e5';
  const b=document.getElementById('dbadge'); b.textContent=p; b.style.background=curColor;
  document.getElementById('dtitle').textContent=info.dep;
  document.getElementById('dgloss').textContent=info.gloss||'';
  document.getElementById('dsub').textContent=info.abbr+' · '+info.fac+' — '+info.total+' modules, '+info.offered+' currently offered';
  dq.value=''; renderMods(p,''); ov.classList.add('on'); document.body.style.overflow='hidden'; dq.focus();
}
function renderMods(p,filter){
  const list=DATA[p].m,f=filter.trim().toLowerCase(),lo=live.checked;
  const rows=list.filter(m=>(!f||(m.c+' '+m.t+' '+m.d).toLowerCase().includes(f))&&(!lo||m.o));
  dcount.textContent=rows.length+' module'+(rows.length==1?'':'s')+(f?' matching':'')+(lo?' · live only':'');
  const frag=document.createDocumentFragment();
  rows.forEach(m=>{
    const d=document.createElement('div'); d.className='mod';
    const h=document.createElement('div'); h.className='mod-h';
    const c=document.createElement('span'); c.className='mod-c'; c.textContent=m.c; c.style.color=curColor;
    const t=document.createElement('span'); t.className='mod-t'; t.textContent=m.t;
    const u=document.createElement('span'); u.className='mod-tag'; u.textContent=m.u+' MC';
    const lv=document.createElement('span'); lv.className='mod-tag '+(m.o?'live':'dorm'); lv.textContent=m.o?'live':'not offered';
    h.append(c,t,u,lv); d.append(h);
    if(m.d){const p2=document.createElement('div'); p2.className='mod-d'; p2.textContent=m.d; d.append(p2);}
    frag.append(d);
  });
  dbody.replaceChildren(frag); dbody.scrollTop=0;
}
let curP=null;
const _op=openPrefix; openPrefix=function(p){curP=p;_op(p);};
dq.addEventListener('input',()=>renderMods(curP,dq.value));
function closeDrw(){ov.classList.remove('on');document.body.style.overflow='';}
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeDrw();});
document.addEventListener('keydown',e=>{if(e.key==='Enter'&&document.activeElement.classList.contains('chip'))document.activeElement.click();});

/* ---------- filters + stats (unchanged from the offline page) ---------- */
function apply(){
  const t=q.value.trim().toLowerCase(),lo=live.checked;
  const hm=hideMinor.checked,mn=+minorN.value||0,hg=hideGrad.checked;
  let anyFac=false;
  document.querySelectorAll('.fac').forEach(fac=>{
    let facVis=false; const facMatch=!t||fac.dataset.fac.includes(t);
    fac.querySelectorAll('.dept').forEach(dep=>{
      let depVis=false,filteredN=0;
      dep.querySelectorAll('.chip').forEach(ch=>{
        const okS=facMatch||ch.dataset.search.includes(t);       // search: a true filter
        const okL=!lo||(+ch.dataset.offered>0);
        const okM=!hm||(+ch.dataset.total>mn);
        const okG=!hg||ch.dataset.gradonly!=='1';
        const passToggles=okL&&okM&&okG;
        ch.classList.toggle('hide',!okS);                        // search removes in every view
        ch.classList.toggle('filtered',okS&&!passToggles);       // toggles: grey (expanded) / hide (collapsed)
        if(okS){depVis=true; if(!passToggles)filteredN++;}
      });
      dep.querySelector('.dept-hidden').textContent=filteredN?filteredN+' hidden':'';
      dep.classList.toggle('hide',!depVis); if(depVis)facVis=true;
      if(t&&depVis)dep.classList.remove('dclosed');
    });
    fac.classList.toggle('hide',!facVis); if(facVis)anyFac=true;
  });
  nores.classList.toggle('hide',anyFac);
  updateStats();
}
function updateStats(){
  const lo=live.checked;
  let mods=0,offr=0,pfx=0; const facs=new Set(),deps=new Set();
  document.querySelectorAll('.chip:not(.hide):not(.filtered)').forEach(ch=>{
    const tot=+ch.dataset.total,off=+ch.dataset.offered;
    mods+=lo?off:tot; offr+=off; pfx++;
    facs.add(ch.closest('.fac')); deps.add(ch.closest('.dept'));
  });
  s_mod.textContent=mods.toLocaleString();
  s_off.textContent=offr.toLocaleString();
  s_pfx.textContent=pfx.toLocaleString();
  s_fac.textContent=facs.size.toLocaleString();
  s_dep.textContent=deps.size.toLocaleString();
  document.getElementById('lbl-mod').textContent=lo?'live modules':'modules';
  document.getElementById('stat-off').classList.toggle('hide',lo);
}
function toggleFac(h){
  const fac=h.parentElement,collapse=!fac.classList.contains('closed');
  fac.classList.toggle('closed',collapse);
  fac.querySelectorAll('.dept').forEach(d=>d.classList.toggle('dclosed',collapse));
}
function toggleAll(btn){
  const facs=document.querySelectorAll('.fac');
  const collapse=[...facs].some(f=>!f.classList.contains('closed'));
  facs.forEach(f=>{f.classList.toggle('closed',collapse);f.querySelectorAll('.dept').forEach(d=>d.classList.toggle('dclosed',collapse));});
  btn.textContent=collapse?'expand all':'collapse all';
}

/* ---------- instant hover tooltip ---------- */
const tip=document.getElementById('tip');let tipFor=null;
document.addEventListener('mouseover',e=>{
  const c=e.target.closest('.chip'); if(c===tipFor)return; tipFor=c;
  if(!c||!c.dataset.tip){tip.classList.remove('on');return;}
  tip.textContent=c.dataset.tip; tip.classList.add('on');
  const r=c.getBoundingClientRect(),t=tip.getBoundingClientRect();
  let x=Math.max(6,Math.min(r.left+r.width/2-t.width/2,innerWidth-t.width-6));
  let y=r.top-t.height-7; if(y<6)y=r.bottom+7;
  tip.style.left=x+'px'; tip.style.top=y+'px';
});
document.addEventListener('mouseout',e=>{if(e.target.closest('.chip')&&!(e.relatedTarget&&e.relatedTarget.closest('.chip'))){tip.classList.remove('on');tipFor=null;}});
document.addEventListener('scroll',()=>{if(tipFor){tip.classList.remove('on');tipFor=null;}},true);

q.addEventListener('input',apply);
hideMinor.addEventListener('change',apply);
hideGrad.addEventListener('change',apply);
minorN.addEventListener('input',()=>{if(hideMinor.checked)apply();});
live.addEventListener('change',()=>{apply(); if(ov.classList.contains('on')&&curP)renderMods(curP,dq.value);});

/* ---------- academic year: auto-advance by date, with fallback ---------- */
// NUS academic years start in August. Before August we're still in the AY that
// began the previous calendar year. We try the current AY, then fall back to the
// previous one if the new year's data isn't published yet. ACAD_YEAR (the year
// the glosses were curated against) is the floor, so we never probe older data.
function candidateAYs(){
  const now=new Date();
  let start=now.getFullYear();
  if(now.getMonth()<7) start-=1;                 // Jan–Jul -> AY began last year
  const floor=parseInt(ACAD_YEAR.split('-')[0],10);
  const out=[];
  for(const y of [start,start-1]){ if(y>=floor) out.push(y+'-'+(y+1)); }
  if(!out.length) out.push(ACAD_YEAR);           // opened before the floor year
  return out;
}
// Show when NUSMods last rebuilt the data, from the response's Last-Modified
// header (a CORS-safelisted header, so readable even from a file:// page).
function showDataDate(lastModified){
  const wrap=document.getElementById('asofwrap'), out=document.getElementById('asof');
  if(!wrap||!out) return;
  const d=lastModified?new Date(lastModified):null;
  if(!d||isNaN(d)){ wrap.style.display='none'; return; }
  out.textContent=d.toLocaleDateString('en-GB',{day:'numeric',month:'short',year:'numeric'});
  wrap.style.display='';
}

/* ---------- boot: fetch live data, then build+render ---------- */
async function boot(){
  errbox.classList.remove('on'); loading.style.display='block'; grid.innerHTML='';
  for(const ay of candidateAYs()){
    try{
      const r=await fetch('https://api.nusmods.com/v2/'+ay+'/moduleInfo.json');
      if(!r.ok)throw new Error('HTTP '+r.status);
      const mods=await r.json();
      showDataDate(r.headers.get('last-modified'));
      render(build(mods));
      loading.style.display='none';
      apply();
      applyHash();
      return;
    }catch(e){ /* try the next candidate year */ }
  }
  loading.style.display='none'; errbox.classList.add('on');
}
/* deep-link: prefix_map.html#CS types CS into the search box and filters
   (used by Anki cards) — does NOT open the drawer, so the user lands on the
   live search view for that prefix. */
function applyHash(){
  const h=decodeURIComponent((location.hash||'').replace(/^#/,'')).trim().toUpperCase();
  if(h){ q.value=h; apply(); q.scrollIntoView({block:'start'}); }
}
window.addEventListener('hashchange',applyHash);
boot();
"""

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>NUSMods Prefix Map</title>
<style>
__CSS__
__EXTRA_CSS__
</style></head><body>
<header>
<h1>NUSMods Module Prefix Map</h1>
<div class="sub">Fetched live from the NUSMods API · every course-code prefix grouped by faculty &amp; department</div>
<div class="stats">
<div class="stat"><b id="s-mod">…</b><span id="lbl-mod">modules</span></div>
<div class="stat" id="stat-off"><b id="s-off">…</b><span>currently offered</span></div>
<div class="stat"><b id="s-pfx">…</b><span>prefixes</span></div>
<div class="stat"><b id="s-fac">…</b><span>faculties</span></div>
<div class="stat"><b id="s-dep">…</b><span>departments</span></div>
</div>
<div class="controls">
<input id="q" placeholder="Search prefix, department or faculty… (e.g. MA, chemistry, CDE)" autocomplete="off">
<label class="toggle"><input type="checkbox" id="liveOnly"> live modules only</label>
<label class="toggle"><input type="checkbox" id="hideMinor"> hide minor prefixes (≤<input type="number" id="minorN" value="3" min="1" max="99" title="max modules to treat as minor"> modules)</label>
<label class="toggle"><input type="checkbox" id="hideGrad"> hide grad-only prefixes</label>
<button class="btn" id="collapseAll" onclick="toggleAll(this)">collapse all</button>
</div>
</header>
<main>
<div id="loading"><span class="spin"></span>Loading modules from the NUSMods API…</div>
<div id="grid"></div>
<div id="nores" class="hide" style="text-align:center;color:var(--mut);padding:40px">No matching prefixes.</div>
<div id="errbox">Couldn’t reach the NUSMods API. This page needs an internet connection.<br><button class="retry" onclick="boot()">Retry</button></div>
</main>
<div id="tip" role="tooltip"></div>
<footer>Source: NUSMods API v2 (api.nusmods.com) · fetched live on load<span id="asofwrap" style="display:none"> · data as of <span id="asof"></span></span> · ⧉ = prefix also used by other faculties/departments · “live” = offered in ≥ 1 semester · click any prefix for its modules</footer>
<div id="ov" onclick="if(event.target===this)closeDrw()">
 <aside id="drw" role="dialog" aria-modal="true">
  <div class="d-head">
   <div class="d-top"><span class="d-badge" id="dbadge"></span><div id="dtitle" style="font-weight:650"></div><button id="dx" onclick="closeDrw()" aria-label="Close">×</button></div>
   <div class="d-gloss" id="dgloss"></div>
   <div class="d-sub" id="dsub"></div>
   <input id="dq" placeholder="Filter these modules by code, title or description…" autocomplete="off">
  </div>
  <div class="d-count" id="dcount" style="padding:0 20px"></div>
  <div class="d-body" id="dbody"></div>
 </aside>
</div>
<script id="CFG" type="application/json">__CFG__</script>
<script>
__JS__
</script>
</body></html>"""

page = (PAGE
        .replace("__CSS__", CSS)
        .replace("__EXTRA_CSS__", EXTRA_CSS)
        .replace("__CFG__", CFG_JSON)
        .replace("__JS__", JS))

out = os.path.join(HERE, "prefix_map.html")
open(out, "w", encoding="utf-8").write(page)
kb = round(len(page.encode("utf-8")) / 1024, 1)
print(f"Wrote prefix_map.html  ({kb} KB, {len(CFG['CURATED'])} curated glosses)")

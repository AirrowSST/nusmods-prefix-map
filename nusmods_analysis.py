"""Scrape all NUSMods modules and analyze prefixes, faculties, and frequency."""
import json, re, urllib.request, collections, csv, os

ACAD_YEAR = "2026-2027"
URL = f"https://api.nusmods.com/v2/{ACAD_YEAR}/moduleInfo.json"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

print(f"Downloading {URL} ...")
with urllib.request.urlopen(URL) as r:
    modules = json.load(r)
print(f"Loaded {len(modules)} modules for AY{ACAD_YEAR}\n")

# Save raw for reuse
with open(os.path.join(OUT_DIR, "nusmods_raw.json"), "w", encoding="utf-8") as f:
    json.dump(modules, f)

PREFIX_RE = re.compile(r"^([A-Z]+)")

rows = []
prefix_counter = collections.Counter()
faculty_counter = collections.Counter()
dept_counter = collections.Counter()
prefix_faculty = collections.defaultdict(collections.Counter)  # prefix -> faculty counts
prefix_offered = collections.Counter()  # prefix -> # modules actually offered a semester this year

for m in modules:
    code = m.get("moduleCode", "")
    mp = PREFIX_RE.match(code)
    prefix = mp.group(1) if mp else "?"
    fac = m.get("faculty") or "(none)"
    dept = m.get("department") or "(none)"
    sems = [s.get("semester") for s in m.get("semesterData", [])]
    offered = len(sems) > 0

    prefix_counter[prefix] += 1
    faculty_counter[fac] += 1
    dept_counter[dept] += 1
    prefix_faculty[prefix][fac] += 1
    if offered:
        prefix_offered[prefix] += 1

    rows.append({
        "moduleCode": code,
        "prefix": prefix,
        "title": m.get("title", ""),
        "faculty": fac,
        "department": dept,
        "moduleCredit": m.get("moduleCredit", ""),
        "semestersOffered": "|".join(str(s) for s in sems),
        "offeredThisAY": offered,
    })

# Per-module CSV
csv_path = os.path.join(OUT_DIR, "nusmods_modules.csv")
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

# Prefix summary CSV: prefix, count, offered, dominant faculty, all faculties
prefix_path = os.path.join(OUT_DIR, "nusmods_prefixes.csv")
with open(prefix_path, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["prefix", "moduleCount", "offeredThisAY", "dominantFaculty", "facultiesSpanned"])
    for pfx, cnt in prefix_counter.most_common():
        facs = prefix_faculty[pfx]
        dom = facs.most_common(1)[0][0]
        w.writerow([pfx, cnt, prefix_offered[pfx], dom, len(facs)])

# Faculty summary CSV
fac_path = os.path.join(OUT_DIR, "nusmods_faculties.csv")
with open(fac_path, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["faculty", "moduleCount"])
    for fac, cnt in faculty_counter.most_common():
        w.writerow([fac, cnt])

# ---- Console report ----
print("=" * 70)
print(f"NUSMods AY{ACAD_YEAR}  —  {len(modules)} total modules")
print(f"Distinct prefixes: {len(prefix_counter)}   Distinct faculties: {len(faculty_counter)}")
offered_total = sum(1 for r in rows if r["offeredThisAY"])
print(f"Modules offered at least one semester this AY: {offered_total} "
      f"({offered_total*100//len(modules)}%)")
print("=" * 70)

print("\n### Faculties by module count ###")
for fac, cnt in faculty_counter.most_common():
    print(f"  {cnt:5d}  {fac}")

print(f"\n### Top 40 prefixes by module count (of {len(prefix_counter)}) ###")
print(f"  {'PFX':<6}{'total':>6}{'offered':>8}  dominant faculty")
for pfx, cnt in prefix_counter.most_common(40):
    dom = prefix_faculty[pfx].most_common(1)[0][0]
    print(f"  {pfx:<6}{cnt:>6}{prefix_offered[pfx]:>8}  {dom}")

print("\nWrote:")
for p in (csv_path, prefix_path, fac_path, os.path.join(OUT_DIR, "nusmods_raw.json")):
    print("  ", p)

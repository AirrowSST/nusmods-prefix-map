# NUSMods Prefix Map

An interactive, single-file web page that groups every NUS module-code prefix
(e.g. `CS`, `HY`, `GEC`) under its faculty and department, with a short
human-readable gloss for each prefix. NUSMods itself has no concept of prefixes —
the glosses and grouping are curated here.

## Just download and open it

You don't need to run or build anything to use this. **Download
[`prefix_map.html`](prefix_map.html), double-click it, and it opens in your
browser** — no server, no install, no dependencies. It's a single self-contained
~37 KB file you can also email or share as-is.

The only requirement is an internet connection: the module data is fetched live
from the NUSMods API on load rather than bundled into the file.

## `prefix_map.html`

A self-contained ~37 KB page. Open it in any browser and it fetches the live
NUSMods catalogue (`api.nusmods.com`) and builds the tree in-browser:

- Faculty → department → prefix drawers, each prefix showing its modules.
- Hover a prefix for its gloss; ⧉ marks prefixes shared across faculties.
- Filter by "offered this year", search, and expand/collapse.

The page stays current on its own: on load it works out the current NUS academic
year (which starts in August) and fetches that, falling back to the previous year
if the new year's data isn't published yet — so you don't need to rebuild each
year. The footer shows a **"data as of \<date\>"** stamp taken from the API's
`Last-Modified` header, so you can always see how fresh the data is. `ACAD_YEAR`
in the generator is just the earliest year it will fetch (the floor).

## Building

```bash
python build_prefix_map.py    # regenerates prefix_map.html
```

`build_prefix_map.py` is self-contained: the curated prefix glosses (`CURATED`),
abbreviation/department fixups, colour palette, and CSS all live in this one
file. `CURATED` is the single source of truth for the glosses — edit it and
re-run to rebuild the page.

## `nusmods_analysis.py` (optional)

A standalone scraper for offline analysis. Downloads the full module list from
the NUSMods API and writes a raw snapshot (`nusmods_raw.json`) plus CSV
breakdowns of prefixes, faculties, and modules. Not required to build or use the
prefix map — those data files are git-ignored and regenerable.

```bash
python nusmods_analysis.py
```

## Data source

All module data comes from the [NUSMods API v2](https://api.nusmods.com/v2/).

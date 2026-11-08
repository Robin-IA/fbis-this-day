# FBIS This Day

**One Foreign Broadcast Information Service Daily Report for every day of
the year, 1978–1996**, from the Internet Archive's
[`us-fbis`](https://archive.org/details/us-fbis) collection in
[Democracy's Library](https://archive.org/details/democracys-library), with
what happened, why it mattered, and what the monitors heard. The home page
moves to the next day at midnight. Live at
**https://internetarchivecanada.github.io/fbis-this-day/**.

## What it does

Each day shows one event that happened on that date in some year between
1978 and 1996, preferring spycraft (espionage, defections, covert action,
the intelligence services) and then the crises of the late Cold War. Every
event is anchored to the Daily Report that carried it: the entry links the
archive.org item and the page, and quotes the OCR text where it was found.
Below it are other events for the same date and every Daily Report dated
that day in any year. A calendar page lists all 366 days.

- **Source of materials:** the
  [United States Foreign Broadcast Information Service (FBIS)](https://archive.org/details/us-fbis)
  collection at the Internet Archive, scanned from microfiche. It is part
  of Democracy's Library **by scope** (through `USGovernmentDocuments`,
  which Democracy's Library's `search_collection` includes); it does not
  carry the `democracys-library` tag.
- **Years covered:** January 3, 1978, to August 30, 1996. Nothing before 1978
  is in the collection, so the Bay of Pigs and the Cuban Missile Crisis
  cannot appear.
- **Regions:** Soviet Union, East Europe, Near East / Middle East, Latin
  America (all years); East Asia from 1990; Africa, China and West Europe
  barely at all.
- **Size:** 22,903 items, 21,850 dated (`collection:us-fbis`, scrape API,
  November 6, 2026).
- **Not included:** JPRS, the CIA Reading Room's FBIS memos, World News
  Connection, and undated items. For those see the
  [FBIS explorer](https://wayback-labs.sf.archive.org/fbis/) in Wayback
  Machine Labs.

**The written entries are AI-assisted.** Each was written with Claude, and
a script confirmed that its Daily Report carries the event; no specialist
has reviewed the history around it. The site says so on every entry and
asks readers to report mistakes.

## How it was built

### The data

1. `tools/build_index.py` reads every item in `collection:us-fbis` from
   archive.org's scrape API (`/services/search/v1/scrape`, fields
   `identifier,date,title,collection`) into `data/issues.json`, assigning a
   region from the item's `fbis-reports-*` subcollection or its title.
2. `candidates/MM.json` hold several candidate events per day, drafted to
   the brief in [docs/drafting.md](docs/drafting.md).
3. `tools/verify.py` checks each candidate against the OCR: it fetches each
   issue's `_hocr_searchtext.txt.gz` and `_hocr_pageindex.json.gz`, and
   accepts the candidate only if one page of an issue dated the event day
   or up to three days later, in the candidate's regions, matches every
   keyword group. It prefers a body page to the contents list and records
   the item, page and a snippet in `verified/MM.json`.
4. `tools/build_site.py` writes `data/days/MM-DD.json` (the pick,
   alternates and that day's issues), `data/calendar.json` and
   `data/stats.json`. Only candidates with evidence are published.

### The code

Plain HTML, CSS and JavaScript, no build step, published with GitHub Pages
from `main`. The palette is red, dark blue, gold and white (tokens at the
top of `style.css`; gold is never used as text on white, and every text
pair meets WCAG AA in light and dark modes). Images in `img/` are public
domain, from Wikimedia Commons, credited on the About page: the FBIS logo,
the FCC Laurel, Maryland listening post (Library of Congress), the FBIS
teletype message reporting Tito's death (CIA, 1980) and FBIS monitoring
equipment (1945). `index.html` + `app.js` is the day view; `calendar.html` and
`about.html` are self-contained. Python 3 standard library only.

### Rebuilding it

```bash
python3 tools/build_index.py
python3 tools/verify.py
python3 tools/build_site.py
```

OCR is cached in `.cache/ocr/` (not committed).

### Who built it

Built by Robin Fay, Project Manager, Digital Collections, Democracy's
Library, with [Claude Code](https://claude.com/claude-code) (Claude Opus
5.5), November 2026. Robin set the scope and the publishing arrangement;
Claude wrote the code, drafted the candidate events and their context, and
ran the OCR checks. Each commit names Claude as co-author. Draws on Mark
Graham's FBIS explorer in Wayback Machine Labs.

## How to use it

### Run it on your Mac

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000/. Add `?d=11-22` to see a particular day.

## Accessibility and security

Not yet checked with the
[accessibility and security checker](https://github.com/internetarchivecanada/accessibility-security-checker).
That is required before the explorer is published.

## Source and mirror

Developed at `Robin-IA/fbis-this-day`; published from the public mirror
`internetarchivecanada/fbis-this-day`, whose GitHub Pages serves the site.

## Feedback

robin.fay@archive.org, subject *Explorer Feedback USFBIS-Democracy's Library*.

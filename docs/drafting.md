# How day entries are drafted and checked

Every calendar day (366, including 02-29) gets one featured entry and, where
found, alternates. An entry is an event that happened on that month-day in
some year 1978–1996, **anchored to a real FBIS Daily Report in archive.org's
`us-fbis` collection** that reported it. The emphasis is spycraft and
intelligence (defections, espionage arrests and expulsions, spy swaps, covert
operations and their exposure, assassinations, coups, hijackings and
hostage-taking, intelligence failures and services in the news), then the
major crises of the late Cold War and its end.

Nothing goes on the site unless `tools/verify.py` has found it in the OCR.

## What the collection can anchor

`data/issues.json` is the index (`collection:us-fbis`, 22,903 items; 21,850
dated). Issues run **1978-01-03 to 1996-08-30**. Region codes and coverage:

| code | series | usable years |
|---|---|---|
| SOV | Soviet Union / Central Eurasia | 1978–1996 |
| EEU | East Europe | 1978–1996 |
| NES | Middle East & North Africa / Near East & South Asia | 1978–1996 |
| LAT | Latin America | 1978–1996 |
| EAS | East Asia / Asia & Pacific | 1990–1996 only |
| AFR | Sub-Saharan Africa | 1978 only, effectively |
| CHI, WEU | China, West Europe | almost nothing — do not rely on them |

So an event in China, Western Europe, Africa or (before 1990) East Asia must
be anchored through how another region's media reported it — Moscow on
Tiananmen, East Berlin or Warsaw on a NATO spy case, Havana or Tripoli on a
US operation. List every region whose broadcasters plausibly carried it.

No Daily Report is dated 07-04, 11-11 or 12-25; the event can still fall on
those days, because the verifier looks at issues dated the event day and up
to three days after.

## Candidate file format

`candidates/MM.json` — a JSON list, several candidates per day:

```json
{
  "md": "11-04",
  "date": "1979-11-04",
  "regions": ["NES", "SOV"],
  "keywords": [["embassy"], ["student"], ["tehran"]],
  "headline": "Students seize the US Embassy in Tehran",
  "category": "hostage",
  "spycraft": true,
  "summary": "One or two sentences: what happened, plainly dated.",
  "significance": "Two to four sentences: why it mattered to the US and to world events at the time.",
  "fbis": "",
  "pick": false
}
```

- `keywords`: a list of groups; **every group must match on one page**, and a
  group matches if any alternative appears (case-insensitive substring). Use
  stems and spelling variants, because the OCR is noisy and FBIS used its
  own transliteration (`qadhdhafi`, `khomeyni`, `andropov`). Put the most
  distinctive term first: the evidence snippet is centered on it. Two or three
  groups is usually right; one group alone proves little.
- `category`: one of `espionage`, `defection`, `covert-action`, `coup`,
  `assassination`, `terrorism`, `hostage`, `war`, `crisis`, `diplomacy`,
  `uprising`, `disaster`, `politics`.
- `spycraft`: true for intelligence, espionage, covert action, defection and
  the security services; these are preferred when choosing the day's pick.
- `fbis`: written **after** verification, from the evidence snippet and the
  page itself: what the monitored broadcaster said (outlet, language, slant).
  One or two sentences. Never claim something the page does not show.
- `pick`: exactly one `true` per day, a verified candidate, spycraft
  preferred where a verified one exists.

## Accuracy

These are drafts for human review, and the site says so. Write only what you
are confident of; prefer fewer, firmer facts to colourful ones. If you are
unsure an event fell on that exact date, either drop it or let the verifier
decide — but a match three days later does not prove the date, so the
`summary` date must be one you know. Quote nothing from the OCR in
`summary` or `significance`; quote at most a short phrase in `fbis`.

## Loop

```bash
python3 tools/verify.py candidates/11.json
```

writes `verified/11.json` (adds `evidence` with identifier, issue date, page
and snippet — or `fail` with the issues tried) and prints the days still
missing. Replace or re-keyword failures and re-run; candidates whose keywords
have not changed keep their evidence without re-fetching. Cached OCR is in
`.cache/ocr/<identifier>_hocr_searchtext.txt.gz`; read a page in full with

```python
import sys; sys.path.insert(0, "tools"); import verify
dict(verify.pages("micro_IA1176910_0590"))[7]
```

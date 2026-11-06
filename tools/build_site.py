"""Write the site's data from data/issues.json and verified/*.json.

    data/days/MM-DD.json  one per calendar day (366): the featured entry,
                          alternates, and every us-fbis issue dated that
                          month-day in any year.
    data/calendar.json    one line per day, for the calendar view.

Only candidates with OCR evidence are published. A day with no verified
pick still gets a file (its issues), and the page says it has no entry yet.

    python3 tools/build_site.py
"""
import datetime
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
REGIONS = {
    "SOV": "Soviet Union / Central Eurasia", "EEU": "East Europe", "WEU": "West Europe",
    "CHI": "China", "EAS": "East Asia", "NES": "Near East & South Asia",
    "AFR": "Sub-Saharan Africa", "LAT": "Latin America", "": "Unassigned",
}
KEEP = ("md", "date", "headline", "category", "spycraft", "summary", "significance", "fbis", "evidence")


def all_days():
    d = datetime.date(2024, 1, 1)  # a leap year, so 02-29 is included
    return [(d + datetime.timedelta(i)).strftime("%m-%d") for i in range(366)]


def main():
    issues = json.loads((ROOT / "data" / "issues.json").read_text())
    by_md = {}
    for ident, date, reg, title in issues:
        if date:
            by_md.setdefault(date[5:], []).append([ident, date, reg, title])

    cands = []
    for f in sorted((ROOT / "verified").glob("*.json")):
        cands += [c for c in json.loads(f.read_text()) if "evidence" in c]
    by_day = {}
    for c in cands:
        by_day.setdefault(c["md"], []).append({k: c[k] for k in KEEP if k in c} | {"pick": bool(c.get("pick"))})

    out = ROOT / "data" / "days"
    out.mkdir(parents=True, exist_ok=True)
    calendar, missing, multi = [], [], []
    for md in all_days():
        entries = by_day.get(md, [])
        picks = [e for e in entries if e["pick"]]
        if len(picks) > 1:
            multi.append(md)
        if not picks and entries:  # fall back: spycraft first, then earliest
            entries.sort(key=lambda e: (not e.get("spycraft"), e["date"]))
            picks = [entries[0]]
        pick = picks[0] if picks else None
        alts = sorted((e for e in entries if e is not pick), key=lambda e: e["date"])
        for e in [pick, *alts]:
            if e:
                e.pop("pick", None)
        day_issues = sorted(by_md.get(md, []), key=lambda r: (r[1], r[2]))
        (out / f"{md}.json").write_text(json.dumps(
            {"md": md, "pick": pick, "alternates": alts, "issues": day_issues},
            ensure_ascii=False, separators=(",", ":")))
        if pick:
            calendar.append({"md": md, "year": pick["date"][:4], "headline": pick["headline"],
                             "category": pick.get("category", ""), "spycraft": bool(pick.get("spycraft")),
                             "n": len(day_issues)})
        else:
            missing.append(md)
            calendar.append({"md": md, "n": len(day_issues)})
    (ROOT / "data" / "calendar.json").write_text(json.dumps(calendar, ensure_ascii=False, separators=(",", ":")))
    (ROOT / "data" / "regions.json").write_text(json.dumps(REGIONS))

    stats = {
        "built": datetime.date.today().isoformat(),
        "items": len(issues),
        "dated": sum(1 for r in issues if r[1]),
        "first": min(r[1] for r in issues if r[1]),
        "last": max(r[1] for r in issues if r[1]),
        "days_with_entry": 366 - len(missing),
        "spycraft_picks": sum(1 for c in calendar if c.get("spycraft")),
        "verified_events": len(cands),
    }
    (ROOT / "data" / "stats.json").write_text(json.dumps(stats, indent=1))
    print(json.dumps(stats))
    if missing:
        print(f"{len(missing)} days without an entry: {' '.join(missing)}")
    if multi:
        print(f"days with more than one pick (first used): {' '.join(multi)}")


if __name__ == "__main__":
    main()

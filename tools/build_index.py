"""Build data/issues.json: every item in archive.org's us-fbis collection.

Each row is [identifier, date (YYYY-MM-DD or ""), region code, title].
Read from the live scrape API, not from another explorer's export, so the
count is the collection's own (collection:us-fbis).

    python3 tools/build_index.py
"""
import json
import pathlib
import re
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "issues.json"
IDENT = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,99}")
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
UA = "fbis-this-day/0.1 (Internet Archive, Democracy's Library)"

# Region subcollection -> code. Titles are the fallback (some items carry
# only the parent collection).
SUBCOLL = {
    "fbis-reports-soviet-union-central-eurasia": "SOV",
    "fbis-reports-east-europe": "EEU",
    "fbis-reports-west-europe": "WEU",
    "fbis-reports-peoples-republic-china": "CHI",
    "fbis-reports-east-asia": "EAS",
    "fbis-reports-asia-pacific": "EAS",
    "fbis-reports-middle-east-africa": "NES",
    "fbis-reports-near-east-south-asia": "NES",
    "fbis-reports-south-asia": "NES",
    "fbis-reports-sub-saharan-africa": "AFR",
    "fbis-reports-latin-america": "LAT",
}
TITLE_RULES = [
    (r"soviet|central eurasia|ussr", "SOV"),
    (r"east europe", "EEU"),
    (r"west europe|western europe", "WEU"),
    (r"china", "CHI"),
    (r"east asia|asia & pacific|asia and pacific|asia pacific", "EAS"),
    (r"middle east|near east|south asia", "NES"),
    (r"africa", "AFR"),
    (r"latin america", "LAT"),
]


def region(colls, title):
    for c in colls:
        if c in SUBCOLL:
            return SUBCOLL[c]
    t = (title or "").lower()
    for pat, code in TITLE_RULES:
        if re.search(pat, t):
            return code
    return ""


def main():
    rows, rejected, cursor = [], [], None
    while True:
        params = {"q": "collection:us-fbis", "fields": "identifier,date,title,collection", "count": "10000"}
        if cursor:
            params["cursor"] = cursor
        url = "https://archive.org/services/search/v1/scrape?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=120) as r:
            d = json.load(r)
        for it in d["items"]:
            colls = it.get("collection") or []
            colls = [colls] if isinstance(colls, str) else colls
            title = it.get("title") or ""
            title = title if isinstance(title, str) else title[0]
            ident, date = it.get("identifier") or "", (it.get("date") or "")[:10]
            # Validate what goes into the site's data: archive.org identifiers
            # and ISO dates only. Anything else is reported and left out.
            if not IDENT.fullmatch(ident):
                rejected.append(ident)
                continue
            if date and not DATE.fullmatch(date):
                date = ""
            rows.append([ident, date, region(colls, title), title])
        cursor = d.get("cursor")
        if not cursor:
            break
    rows.sort(key=lambda r: (r[1], r[2], r[0]))
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(rows, separators=(",", ":")))
    if rejected:
        print(f"left out {len(rejected)} item(s) with an unexpected identifier: {rejected[:5]}")
    dated = sum(1 for r in rows if r[1])
    noreg = sum(1 for r in rows if not r[2])
    print(f"{len(rows)} items (collection:us-fbis), {dated} dated, {noreg} without a region")


if __name__ == "__main__":
    main()

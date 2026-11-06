"""Check candidate events against the OCR text of the Daily Reports.

A candidate is only evidence-checked when a us-fbis issue dated on the event
day or up to LAG days after it, in one of the candidate's regions, has a page
on which every keyword group matches (a group matches when any of its
alternatives appears, case-insensitive; OCR is noisy, so give stems).

Input:  candidates/*.json  -- list of
    {"md": "11-06", "date": "1979-11-06", "regions": ["NES"],
     "keywords": [["bazargan"], ["resign"]], "headline": ..., ...}
Output: verified/<same name>.json -- the same objects plus "evidence" (or "fail").

OCR is cached under .cache/ocr/ (gitignored).

    python3 tools/verify.py [candidates/11.json ...] [--lag 3] [--recheck]
"""
import argparse
import datetime
import gzip
import json
import pathlib
import re
import time
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
CACHE = ROOT / ".cache" / "ocr"
UA = "fbis-this-day/0.1 (Internet Archive, Democracy's Library)"


def fetch(ident, suffix):
    CACHE.mkdir(parents=True, exist_ok=True)
    p = CACHE / f"{ident}{suffix}"
    if p.exists():
        return p.read_bytes() or None
    url = f"https://archive.org/download/{ident}/{ident}{suffix}"
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r:
                data = r.read()
            p.write_bytes(data)
            return data
        except urllib.error.HTTPError as e:
            if e.code == 404:
                p.write_bytes(b"")
                return None
            time.sleep(2 + attempt * 3)
        except Exception:
            time.sleep(2 + attempt * 3)
    return None


def pages(ident):
    """Return list of (leaf_index, text) for an item, or None."""
    st = fetch(ident, "_hocr_searchtext.txt.gz")
    pi = fetch(ident, "_hocr_pageindex.json.gz")
    if not st or not pi:
        return None
    # pageindex rows are [start, end, hocr_start, hocr_end]; the first two are
    # character offsets into the decoded search text, one row per leaf.
    text = gzip.decompress(st).decode("utf-8", "replace")
    idx = json.loads(gzip.decompress(pi))
    return [(n, text[a:b]) for n, (a, b, _, _) in enumerate(idx)]


def is_contents(text):
    """Contents pages: a CONTENTS heading, rows of dot leaders, or dense
    'Headline /Source/' rows (the contents list cites a source on every line)."""
    if "CONTENTS" in text[:600].upper() or len(re.findall(r"\.{5,}", text)) >= 6:
        return True
    tags = len(re.findall(r"/[A-Z][A-Za-z0-9 ]{1,20}\]?/?", text))
    return tags >= 8 and tags * 120 > len(text)


def group_re(group):
    return re.compile("|".join(re.escape(k) for k in group), re.I)


def snippet(text, m, width=220):
    a, b = max(0, m.start() - width), min(len(text), m.end() + width)
    s = re.sub(r"\s+", " ", text[a:b]).strip()
    return ("…" if a else "") + s + ("…" if b < len(text) else "")


def check(cand, by_date, lag):
    groups = [group_re(g) for g in cand["keywords"]]
    d0 = datetime.date.fromisoformat(cand["date"])
    regions = set(cand.get("regions") or [])
    tried, contents_hit = [], None
    for off in range(lag + 1):
        d = (d0 + datetime.timedelta(days=off)).isoformat()
        for ident, date, reg, title in by_date.get(d, []):
            if regions and reg not in regions:
                continue
            tried.append(ident)
            pg = pages(ident)
            if not pg:
                continue
            for n, text in pg:
                ms = [g.search(text) for g in groups]
                if not all(ms):
                    continue
                hit = {"identifier": ident, "issue_date": date, "region": reg, "title": title,
                       "page": n, "snippet": snippet(text, ms[0])}
                if not is_contents(text):  # the report itself, not the contents list
                    return hit
                contents_hit = contents_hit or dict(hit, contents_only=True)
    if contents_hit:
        return contents_hit
    return {"fail": f"no page matched all keyword groups in {len(tried)} issue(s)", "tried": tried}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*", help="candidate files (default: candidates/*.json)")
    ap.add_argument("--lag", type=int, default=3)
    ap.add_argument("--recheck", action="store_true", help="re-run candidates already verified")
    args = ap.parse_args()

    issues = json.loads((ROOT / "data" / "issues.json").read_text())
    by_date = {}
    for row in issues:
        by_date.setdefault(row[1], []).append(row)

    files = [pathlib.Path(f) for f in args.files] or sorted((ROOT / "candidates").glob("*.json"))
    (ROOT / "verified").mkdir(exist_ok=True)
    key = lambda c: (c["md"], c["date"], c["headline"])
    for f in files:
        out_p = ROOT / "verified" / f.name
        prev = {key(c): c for c in json.loads(out_p.read_text())} if out_p.exists() else {}
        result = []
        for c in json.loads(f.read_text()):
            old = prev.get(key(c))
            if old and "evidence" in old and old.get("keywords") == c.get("keywords") and not args.recheck:
                c = dict(c, evidence=old["evidence"])
            else:
                res = check(c, by_date, args.lag)
                c = dict(c, **({"fail": res} if "fail" in res else {"evidence": res}))
            result.append(c)
            print(c["md"], c["date"], "OK " if "evidence" in c else "-- ", c["headline"][:70], flush=True)
        out_p.write_text(json.dumps(result, indent=1, ensure_ascii=False))
        days = {c["md"] for c in result}
        ok_days = {c["md"] for c in result if "evidence" in c}
        print(f"{f.name}: {sum('evidence' in c for c in result)}/{len(result)} candidates verified; "
              f"{len(ok_days)}/{len(days)} days have one; missing: {sorted(days - ok_days)}")


if __name__ == "__main__":
    main()

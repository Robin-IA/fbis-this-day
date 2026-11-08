# Security and accessibility checks

**Status: passing.** All three checks passed on 2026-11-08 at commit `99fb0ec2f0`. Nothing is open. Advisory items below are optional.

| | |
|---|---|
| Explorer | https://github.com/Robin-IA/fbis-this-day |
| Commit | `99fb0ec2f0` on `explorer-checks` |
| Date | 2026-11-08 |
| Pages checked | `./`, `./?d=11-07`, `calendar.html`, `about.html` |
| Served from | repository root, served locally |
| Live site (headers) | https://internetarchivecanada.github.io/fbis-this-day/ |
| Standard | WCAG 2.2 Level AA |
| Security references | OWASP Top 10:2025 and ASVS 5.0.0 |
| Tools | axe-core 4.14.0, html5lib, ruff, bandit, pip-audit, headless Chromium |
| Reviewed by | Claude (claude-opus-5-5) via the explorer-checks skill |
| Skill version | 2026.11.05.9 |

## Summary

| Check | Result | Must fix | Needs review | Advisory |
|---|---|---:|---:|---:|
| Code validity | Pass | 0 | 0 | 0 |
| Code security | Pass | 0 | 0 | 2 |
| Accessibility (WCAG 2.2 AA) | Pass | 0 | 0 | 0 |

## Standards met

Checked 8 November 2026 at commit `99fb0ec2f0`, on the pages listed above:

- **WCAG 2.2 Level AA**: every Level A and AA success criterion, by automated tests and a manual review of each criterion (checklists under each check below).
- **WCAG 2.1 Level AA** and **WCAG 2.0 Level AA**, which WCAG 2.2 includes. 4.1.1 Parsing, dropped from 2.2 but still in 2.0 and 2.1, is covered by the code validity check (no HTML parse errors, no duplicate ids).
- These are the web content requirements of **Section 508** (US federal; WCAG 2.0 AA) and **EN 301 549** clause 9 (WCAG 2.1 AA).
- Security was checked against the OWASP Top 10:2025 risks and ASVS 5.0.0 chapters that apply to an explorer; each finding and checklist item names its category. That is not an ASVS verification at any level.

## What a pass means

Each check combines automated tools with a review of the code and pages against a written checklist. A pass means neither found anything open on the date and commit above. The standards are met as far as those checks can establish: it is a self-assessment, not third-party certification. Automated testing finds a minority of accessibility barriers. Testing with people who use assistive technology is still worth doing, and a change to the explorer needs a re-run.

## Code validity

No open items.

## Code security

No open items.

<details><summary>Manual checklist (7 pass, 0 fail, 3 n/a)</summary>

| Item | Result | Note |
|---|---|---|
| No secrets | pass | The credential scan found nothing; the site is static with no keys, tokens or config files. |
| Untrusted data is escaped | pass | All 10 markup sinks traced above; every data field goes through esc(); numbers are coerced. |
| URLs from data are safe | pass | Item and page links are built from a fixed https://archive.org/details/ prefix with encodeURIComponent(identifier); calendar links are relative ./?d= with an escaped MM-DD; ?d= is read back only after validMd(). |
| Harvested data is validated | pass | build_index.py now accepts only archive.org-style identifiers and ISO dates and reports anything it leaves out (all 22,903 current items conform); build_site.py publishes only events with OCR evidence. |
| Third-party code is pinned | n/a | No third-party scripts or CDN code. |
| No mixed content | pass | Everything loads from the site itself; all links are https. |
| Dependencies are pinned and maintained | n/a | Python standard library only; no requirements file, no workflows. |
| Dependencies have no known vulnerabilities | n/a | No dependencies. |
| Third parties a visitor's browser contacts | pass | None: fonts (Courier Prime) and images are served from the repository; data files are local. |
| What Pages publishes | pass | Public repository by design; the served folder holds the site, its data, the candidate and verified event files and the build tools, all intended to be public; the OCR cache is gitignored. |

</details>

<details><summary>Cleared on review (12)</summary>

| Id | Item | Where | Why cleared |
|---|---|---|---|
| `S-c11200` | String rendered as markup or code (innerHTML) | `app.js:46` | el() helper (app.js:46): callers pass only literals, numbers, MONTHS names, esc()'d data, or itemUrl() (fixed https://archive.org/details/ prefix + encodeURIComponent(identifier)). esc() (app.js:38) replaces & < > " '  |
| `S-4dd6bf` | String rendered as markup or code (innerHTML) | `app.js:71` | Empty-day sheet (app.js:71): only esc(label(md)); md has passed validMd() (^\d\d-\d\d$ and a real day) and label() maps it through the fixed MONTHS array. |
| `S-beb641` | String rendered as markup or code (innerHTML) | `app.js:77` | Day sheet (app.js:77): every data field (headline, summary, significance, fbis, category, date, title, snippet) goes through esc(); page numbers are coerced with Number(); the href is pageUrl(), a fixed archive.org prefix with encodeURIComponent(identifier) and a numeric page. |
| `S-50cdb3` | String rendered as markup or code (innerHTML) | `app.js:95` | Clears the list with an empty string literal. |
| `S-fc0173` | String rendered as markup or code (innerHTML) | `app.js:99` | Alternates (app.js:99): year, headline, summary, significance and fbis all through esc(); evidenceHtml() escapes title and snippet and uses pageUrl(). |
| `S-c4bc29` | String rendered as markup or code (innerHTML) | `app.js:116` | Clears the list with an empty string literal. |
| `S-381a62` | String rendered as markup or code (innerHTML) | `app.js:157` | Fixed literal error message, no data. |
| `S-35d42f` | String rendered as markup or code (innerHTML) | `app.js:196` | Clears the day <select> with an empty string literal; options are added with el() and String(number). |
| `S-b2f073` | String rendered as markup or code (innerHTML) | `calendar.html:53` | Clears the calendar with an empty string literal. |
| `S-b4b3fe` | String rendered as markup or code (insertAdjacentHTML) | `calendar.html:65` | Calendar rows (calendar.html:65): mm is a zero-padded loop counter, name from the fixed MONTHS array; r.md, r.headline and r.year go through esc() (calendar.html:49, escapes & < > " '); the day number is numeric. |
| `S-19e802` | Audit url open for permitted schemes. Allowing use of file:/ or custom schemes is often unexpected. | `tools/build_index.py:67` | tools/build_index.py:65 opens a fixed https://archive.org/services/search/v1/scrape URL whose query is built with urllib.parse.urlencode; no file: or custom scheme can reach it. Build-time tool, not served. |
| `S-782ce8` | Audit url open for permitted schemes. Allowing use of file:/ or custom schemes is often unexpected. | `tools/verify.py:41` | tools/verify.py:41 opens https://archive.org/download/<ident>/<ident><suffix>, where ident comes from data/issues.json (validated against an archive.org identifier pattern in build_index.py) and suffix is one of two literals. Build-time tool, not served. |

</details>

## Accessibility (WCAG 2.2 AA)

No open items.

<details><summary>Manual checklist (21 pass, 0 fail, 1 n/a)</summary>

| Item | Result | Note |
|---|---|---|
| 1.1.1 Non-text content | pass | Logos have alt naming their link target; the FBIS emblem is alt="" inside a link named by its text; photographs have descriptive alt; the stamp, fold and shadows are CSS. |
| 1.3.1 Info and relationships | pass | h1, then h2 per section, h3 inside the entry; About's table has th scope=col; lists are ul/ol; selects have labels. |
| 1.3.2 Meaningful sequence | pass | DOM order reads file line, stamp, date, headline, sections, evidence, link; the stamp is positioned but follows the file line in source. |
| 1.4.1 Use of color | pass | Spycraft is marked by a dot with aria-label 'Spycraft' and in the entry by a 'Spycraft' stamp, not by colour alone; tab colours carry no meaning beyond their labels. |
| 1.4.11 Non-text contrast | pass | Focus rings are 3px, red #8a1420 on the folder (7.7:1) and gold on navy. The pastel tabs carry no outline by the owner's choice; each is identified by its typed label (text 10:1 or better), so no boundary is required to identify it. |
| 1.4.4 Resize text / 1.4.12 Text spacing | pass | At 320px wide (equivalent to 400% zoom at 1280px) nothing overflows (scrollWidth 320 = viewport); tabs wrap; heights are not fixed, so added text spacing does not clip. |
| 2.4.4 Link purpose | pass | Links say where they go: 'Read the November 9, 1987 Daily Report', 'How entries are made', 'Report a mistake', 'Email us', collection names. |
| 2.4.6 Headings and labels | pass | Headings name their sections; month/day selects have labels 'Month' and 'Day'; the calendar checkbox reads 'Spycraft only'. |
| 3.1.1 Language of page | pass | <html lang="en"> on all three pages; quoted OCR is English translation. |
| 2.1.1 Keyboard | pass | Everything is native buttons, links, selects, a checkbox and details/summary; tabbed through every control. |
| 2.1.2 No keyboard trap | pass | No custom widgets; focus moves on past every control. |
| 2.4.1 Bypass blocks | pass | 'Skip to content' link to #main on every page; header, nav, main and footer landmarks (the masthead is now a <header>). |
| 2.4.3 Focus order | pass | Skip link, brand, logos, nav, Pause, caption link, previous/next/today tabs, month, day, entry links, alternates, issues, footer: matches reading order. |
| 2.4.7 Focus visible | pass | Pressing Tab showed :focus-visible outlines: 3px gold on the Pause button, 3px red on the tabs. |
| 2.4.11 Focus not obscured | pass | No sticky header or footer. The folder edge overlaps the bottom 9px of each tab, but the focus ring stays visible on three sides. |
| 2.5.8 Target size | pass | Tabs are at least 44px tall; the two links under each entry now have 24px targets; Pause is 26px; calendar rows are full-width block links. |
| 2.2.2 Pause, stop, hide | pass | The live countdown and its blinking light update continuously; a Pause/Resume button (aria-pressed) now stops both. The light does not blink at all under prefers-reduced-motion. |
| 3.2.2 On input | pass | Changing month or day loads that day's entry in place; focus stays on the select; no new window or page. |
| 3.3.2 Labels or instructions | pass | Both selects and the checkbox are labelled. |
| 4.1.2 Name, role, value | pass | Previous/next tabs are named 'Previous day, Nov 6' / 'Next day, Nov 8' (visible date included); Pause/Resume exposes aria-pressed; all other controls are native. |
| 4.1.3 Status messages | pass | The entry is an aria-live=polite region with aria-busy while loading; the calendar's day count is aria-live=polite. |
| 1.2.2 Captions | n/a | No audio or video. |

</details>

<details><summary>Cleared on review (6)</summary>

| Id | Item | Where | Why cleared |
|---|---|---|---|
| `A-6c64c1` | Elements must meet minimum color contrast ratio thresholds | `/ color-contrast` | Contrast measured by hand where axe could not determine the background (gradient band, textured folder, pseudo-element layers): every visible text element on /, /?d=11-07, calendar.html and about.html was paired with its painted background (band checked against both ends of its gradient, #14274e and |
| `A-cae34d` | Elements must meet minimum color contrast ratio thresholds (dark mode) | `/ color-contrast (dark mode)` | Contrast measured by hand where axe could not determine the background (gradient band, textured folder, pseudo-element layers): every visible text element on /, /?d=11-07, calendar.html and about.html was paired with its painted background (band checked against both ends of its gradient, #14274e and |
| `A-0e81c4` | Elements must meet minimum color contrast ratio thresholds | `/calendar.html color-contrast` | Contrast measured by hand where axe could not determine the background (gradient band, textured folder, pseudo-element layers): every visible text element on /, /?d=11-07, calendar.html and about.html was paired with its painted background (band checked against both ends of its gradient, #14274e and |
| `A-3683f7` | Elements must meet minimum color contrast ratio thresholds (dark mode) | `/calendar.html color-contrast (dark mode)` | Contrast measured by hand where axe could not determine the background (gradient band, textured folder, pseudo-element layers): every visible text element on /, /?d=11-07, calendar.html and about.html was paired with its painted background (band checked against both ends of its gradient, #14274e and |
| `A-2c8611` | Elements must meet minimum color contrast ratio thresholds | `/about.html color-contrast` | Contrast measured by hand where axe could not determine the background (gradient band, textured folder, pseudo-element layers): every visible text element on /, /?d=11-07, calendar.html and about.html was paired with its painted background (band checked against both ends of its gradient, #14274e and |
| `A-7692ad` | Elements must meet minimum color contrast ratio thresholds (dark mode) | `/about.html color-contrast (dark mode)` | Contrast measured by hand where axe could not determine the background (gradient band, textured folder, pseudo-element layers): every visible text element on /, /?d=11-07, calendar.html and about.html was paired with its painted background (band checked against both ends of its gradient, #14274e and |

</details>

## Advisory (2)

Optional. These items never block a pass.

| Id | Check | Item | Where | Reference | Suggestion |
|---|---|---|---|---|---|
| `S-a955d4` | security | No content-security-policy header | `https://internetarchivecanada.github.io/fbis-this-day/` | A02:2025 · ASVS V3 | Set it; it limits the damage of any XSS that gets through; a <meta http-equiv> CSP works on static hosts. |
| `S-6f66da` | security | No x-content-type-options header | `https://internetarchivecanada.github.io/fbis-this-day/` | A02:2025 · ASVS V3 | Set it; it stops browsers guessing content types. It has no <meta> form, so on a host that cannot set headers (GitHub Pages) it stays open; the explorer's owners decide whether that matters enough to change host. |

<!-- explorer-checks:state {"passing": true, "date": "2026-11-08", "commit": "99fb0ec2f0e20db2f95898ead49825f996344e9f", "open": [], "titles": {}} -->

# Explorer design checks

**Checked November 9, 2026** for Robin-IA/fbis-this-day against the explorer best practices ([internetarchivecanada/Documentation-Explorer-Best-Practices](https://github.com/internetarchivecanada/Documentation-Explorer-Best-Practices)).

**Status: open items.** 1 missing. 10 to look at by eye. 0 optional to decide.

Accessibility, security and code validity are in [security-accessibility-checks.md](security-accessibility-checks.md).

## Basis

| | Item | Detail |
|---|---|---|
| pass | Best-practices guide | checks match internetarchivecanada/Documentation-Explorer-Best-Practices as of 70b946d |

## Repository

| | Item | Detail |
|---|---|---|
| pass | Repository description | FBIS This Day: one Foreign Broadcast Information Service Daily Report for every day of the year, 1978-1996, from archive.org's us-fbis collection in Democracy's Library. Developed by Robin Fay, Democracy's Library. Reach out to collaborate! |
| pass | Topic labels | democracys-library, explorers, government-resources |
| pass | Public | public |
| pass | GitHub Pages | https://robin-ia.github.io/fbis-this-day/ |
| pass | Website link on the repository | https://internetarchivecanada.github.io/fbis-this-day/ |
| pass | README: what it does | heading “what it does” |
| pass | README: how it was built | heading “how it was built” |
| pass | README: how to use it | heading “how to use it” |

## Requirements on the page

| | Item | Detail |
|---|---|---|
| pass | Title: <title> | FBIS This Day |
| pass | Title: visible <h1> | FBIS This Day |
| pass | Brief description | One day, one Daily Report: what the Foreign Broadcast Information Service heard from the w… |
| pass | About page | about.html |
| look | About: source of materials | names wayback machine, archive.org, internet archive, democracy's library: check it says where the items come from |
| look | About: dates covered | mentions 1941, 1961, 1962, 1978, 1996, 2005, 2026: check these are the dates the material covers |
| look | About: topics covered | if applicable: read the About page |
| look | About: when the numbers were taken | …in America reported them. When the numbers were taken The collection held 22,903 items o…: check the date is current |
| look | About: what is left out | …for collection:us-fbis ). What is left out FBIS material outside the us-fbis…: check it covers what a reader would expect |
| pass | Link to the Internet Archive | https://archive.org/ |
| look | Links to the collections | 3 link(s), e.g. https://archive.org/details/democracys-library: check every source collection is linked |
| pass | Internet Archive logo | alt “Internet Archive” |
| pass | Feedback? mailto | info@archive.org, subject “Democracy's Library Explorer” |
| pass | Nothing about the code on the page | no GitHub mention or link |
| look | About: what it is written in | …quipment 1945 . How it was built A Python script indexes the collection from…: check it names the language and tools |
| pass | No security or validity claims | none on the page |
| pass | Accessibility statement | …lication. Feedback? Email us Meets WCAG 2.2 Level AA accessibility (and WC… |
| pass | Democracy's Library logo | alt “Democracy's Library” |
| pass | Accessibility and security report | Status: passing. All three checks passed on 2026-11-08 at commit `4e1ef82915`. Nothing is open. Advisory items below are optional. |

## Optional elements

| | Item | Detail |
|---|---|---|
| look | Disclaimer | …s Library at the Internet Archive; not an official FBIS or U.S. government publicatio…: check it reads right |
| look | Source credit in the footer | footer links https://archive.org/details/us-fbis: check it reads right |
| look | See also | https://wayback-labs.sf.archive.org/fbis/: check it reads right |
| FAIL | Why the archive matters | wanted, not on the page yet: a sentence on why the archived copy matters, e.g. the original is gone (sentence for the About page's project section) |
| pass | Wayback Labs listing | owner will tell Mark Graham: already done |

Decisions about optional elements are in `explorer-design.json`.

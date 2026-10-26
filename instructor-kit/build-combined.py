#!/usr/bin/env python3
"""
Assemble the three combined instructor-kit books from the per-session source docs.

Kit:    PHP and WordPress Development (the whole course, Modules 1 to 9), 18 sessions x 3 hours = 54 h, in two
        parts: Part 1 "Themes" (Sessions 1 to 8, Modules 1 to 4) runs on its own as a short course and ends with
        the Part 1 project and assessment (Session 8); Part 2 "Plugins to Launch" (Sessions 9 to 18, Modules 5 to
        9) ends with the final project (Sessions 17 and 18).
Reads:  source/module-NN/{facilitator-guide,participant-workbook,answer-key}.html   (NN = 01 ... 18)
        ../course-config.json   (lesson titles, so the contents page always matches the course)
Writes: ./participant-workbook.html, ./facilitator-guide.html, ./answer-key.html
        (the hand-out documents: a cover, a contents page, a divider before each part, then one chapter per session)

A "module" folder is one 3-hour SESSION of the kit (not a course module): module-07 = Session 7.
Session 8 teaches no new lesson (Part 1 project studio + assessment); Sessions 4 and 13 hold the two
30-minute checkpoints (CHECKPOINTS below).

A session whose source doc is missing (or has no sheet/foot) is skipped with a warning, so a
partly written kit still builds. The exit code is 0 when every session was found, 1 otherwise;
add --strict to stop at the first missing doc instead.

Links: a source doc sits two folders below the kit root, a book sits in the root, so every
href="../../..." or src="../../..." in a source doc is rewritten (the leading "../../" is dropped).

After editing a session's source doc, run this again, then render the PDFs
(python3 ~/projects/_kit_tools/php_wordpress/render_pdfs_wp.py, or each book's Print button).

Usage:  python3 build-combined.py [--strict]      (works from any folder)
"""
import json
import re
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent
COURSE = "PHP and WordPress Development"   # the course on the site (rays-php-wordpress.netlify.app)
KIT_TITLE = "PHP and WordPress Development"  # this kit's name: masthead foot lines and book covers
KIT_KEY = ""                   # one kit: the instructor-kit/ folder itself
AUTHOR = "Ray de la Paz"
SESSIONS = 18
HOURS = 54
FORMAT_CHIP = "18 sessions × 3 h · 54 h"
LESSON_CHIP = "31 lessons"
SCOPE = "Modules 1 to 9, in two parts"

# (session number, session title, the lesson ids taught in it). Lesson TITLES are read from
# ../course-config.json when the script runs; do not type them here. Session 8 teaches no new lesson.
MODULES = [
    (1, "WordPress for Developers and Your Local Environment", ["1.1", "1.2"]),
    (2, "PHP the WordPress Way and the Content Model", ["1.3", "2.1"]),
    (3, "Core Architecture, the Database and Hooks", ["2.2", "2.3"]),
    (4, "Theme Anatomy and Building a Block Theme", ["3.1", "3.2"]),
    (5, "Patterns, Style Variations and Child Themes", ["3.3", "3.4"]),
    (6, "The Loop and Custom Queries", ["4.1", "4.2"]),
    (7, "functions.php: Supports, Assets, Menus & Widgets", ["4.3"]),
    (8, "Part 1 Project and Assessment", []),
    (9, "Your First Plugin and Custom Post Types", ["5.1", "5.2"]),
    (10, "Security and the Settings API", ["5.3", "5.4"]),
    (11, "Custom Tables, Shortcodes and Block Setup", ["5.5", "6.1"]),
    (12, "Static and Dynamic Blocks", ["6.2", "6.3"]),
    (13, "The Interactivity API and Using the REST API", ["6.4", "7.1"]),
    (14, "Custom Endpoints, External APIs and Cron", ["7.2", "7.3"]),
    (15, "Debugging, Testing and Performance", ["8.1", "8.2"]),
    (16, "Distribution and Deployment", ["8.3", "8.4"]),
    (17, "Final Project Kickoff and Studio I", ["9.1"]),
    (18, "Final Project Studio II, Showcase and Next Steps", ["9.1", "9.2"]),
]

# (part number, title, first session, last session, one-line description). The books put a divider page
# before each part; check_kit_wp.py and gen_syllabus_wp.py read this list too.
PARTS = [
    (1, "Part 1: Themes", 1, 8,
     "Modules 1 to 4: set up a WordPress 7.1 development site with Docker, WP-CLI, debugging and Mailpit, write PHP "
     "the WordPress way, learn the content model, the database and hooks, then build the Pages & Co. block theme "
     "with theme.json, templates, patterns and style variations, a child theme, and a classic/hybrid theme with the "
     "Loop, custom queries and functions.php. Runs on its own as a short course and ends with the Part 1 project "
     "and assessment."),
    (2, "Part 2: Plugins to Launch", 9, 18,
     "Modules 5 to 9: the pagesco-books plugin (custom post types, security, settings, custom tables), custom "
     "blocks with the Interactivity API, the REST API and custom endpoints, external APIs and cron, debugging, "
     "testing, performance, internationalization and deployment, ending with the final project: the Pages & Co. "
     "website, launched."),
]
CHECKPOINTS = {4: "Checkpoint 1", 13: "Checkpoint 2"}   # session -> the 30-minute checkpoint row it holds
FINAL_SESSIONS = (8, 17, 18)                            # sessions that use final-assessment.html


def part_of(num):
    return next(p for p in PARTS if p[2] <= num <= p[3])

DOCS = {
    "participant-workbook": dict(
        base="participant-workbook.html", role="Participant Workbook",
        eyebrow=f"Instructor Kit · {KIT_TITLE} · Complete Workbook",
        sub=f"Your working notebook for all {SESSIONS} sessions of {KIT_TITLE}. Read the key ideas, study the worked examples, do the guided labs, predict before you run, and check yourself with the self-check quizzes.",
        chips=[f'<span class="chip"><b>{SESSIONS}</b> sessions · {LESSON_CHIP}</span>', '<span class="chip">Write-in exercises &amp; self-checks</span>', '<span class="chip">Name: ____________________</span>'],
        toolbar=("Student workbook —", "write in it · bring it to every session")),
    "facilitator-guide": dict(
        base="facilitator-guide.html", role="Facilitator Guide",
        eyebrow=f"Instructor Kit · {KIT_TITLE} · Complete Facilitator Guide",
        sub=f"The full teaching manual for the {SESSIONS}-session {KIT_TITLE} kit ({SCOPE}; one 3-hour session, two lessons each). Timing, live-demo scripts, the mistakes to pre-empt, lab facilitation, and checks for understanding, for every session.",
        chips=[f'<span class="chip"><b>{SESSIONS}</b> sessions · {LESSON_CHIP}</span>', f'<span class="chip">{FORMAT_CHIP}</span>', '<span class="chip">Instructor copy · not for students</span>'],
        toolbar=("Instructor copy —", "contains answers &amp; timing · not for students")),
    "answer-key": dict(
        base="answer-key.html", role="Answer Key",
        eyebrow=f"Instructor Kit · {KIT_TITLE} · Complete Answer Key",
        sub=f"Every self-check item answered and explained, plus reference notes for each lab, for all {SESSIONS} sessions. Use for grading and reteaching. Confidential instructor material.",
        chips=[f'<span class="chip"><b>{SESSIONS}</b> sessions</span>', f'<span class="chip">{SESSIONS * 12} self-check items + lab solutions</span>', '<span class="chip">Confidential · do not distribute</span>'],
        toolbar=("Instructor copy —", "answers &amp; solutions · not for students")),
}

SHEET_OPEN = '<div class="sheet">'
FOOT_OPEN = '<div class="foot">'


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def folder(num):
    """Session 7 -> 'module-07'."""
    return f"module-{num:02d}"


def lesson_titles():
    """{'1.1': 'WordPress for Developers', ...} from the course's course-config.json."""
    for cfg in (KIT.parent / "course-config.json", KIT.parent.parent / "course-config.json", KIT / "course-config.json"):
        if cfg.is_file():
            break
    try:
        data = json.loads(cfg.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise SystemExit(f"Cannot read lesson titles from {cfg}: {e}")
    return {les["id"]: les["title"] for mod in data["modules"] for les in mod["lessons"]}


def lessons_for(num, titles=None):
    """[('1.1', 'WordPress for Developers'), ('1.2', 'Your Local Development Environment')] for a session (used by the checker too); [] for Session 8."""
    titles = titles or lesson_titles()
    ids = next(ids for n, _, ids in MODULES if n == num)
    missing = [i for i in ids if i not in titles]
    if missing:
        raise SystemExit(f"Lesson id(s) {missing} are not in course-config.json")
    return [(i, titles[i]) for i in ids]


def extract_body(path):
    """Inner content of .sheet minus the trailing .foot block; None (with a reason) if it cannot be cut."""
    try:
        html = path.read_text(encoding="utf-8")
    except OSError:
        return None, "file not found"
    if html.count(SHEET_OPEN) != 1 or html.count(FOOT_OPEN) != 1:
        return None, f'needs exactly one {SHEET_OPEN} and one {FOOT_OPEN}'
    i = html.index(SHEET_OPEN) + len(SHEET_OPEN)
    j = html.index(FOOT_OPEN)
    if j < i:
        return None, "the foot comes before the sheet"
    body = html[i:j].strip()
    body = re.sub(r'\b(href|src)="\.\./\.\./', r'\1="', body)
    return body, ""


def build(key, titles, strict=False):
    d = DOCS[key]
    toc_rows, chapters, skipped = [], [], []
    for num, title, _ in MODULES:
        part = part_of(num)
        if num == part[2]:
            toc_rows.append(f'<li class="part">{esc(part[1])} · Sessions {part[2]} to {part[3]}</li>')
            chapters.append(f'<section class="part-divider">\n  <div class="kit-eyebrow">{esc(KIT_TITLE)} · {d["role"]}</div>\n'
                            f'  <h2>{esc(part[1])}</h2>\n  <p class="sub">Sessions {part[2]} to {part[3]}. {esc(part[4])}</p>\n</section>')
        path = KIT / "source" / folder(num) / d["base"]
        body, why = extract_body(path)
        if body is None:
            if strict:
                raise SystemExit(f"Session {num:02d}: {path.relative_to(KIT)}: {why}")
            if why != "file not found":       # a doc that exists but cannot be cut deserves its own line
                print(f"WARNING: Session {num:02d} skipped in {d['base']}: {path.relative_to(KIT)}: {why}")
            skipped.append(num)
            toc_rows.append(f'<li class="mod missing"><span class="mnum">S{num:02d}</span>{esc(title)} (not written yet)</li>')
            continue
        cp = f' · {CHECKPOINTS[num]}' if num in CHECKPOINTS else ''
        toc_rows.append(f'<li class="mod"><span class="mnum">S{num:02d}</span>{esc(title)}{cp}</li>')
        for lc, lt in lessons_for(num, titles):
            toc_rows.append(f'<li class="les"><span class="lc">{lc}</span><span>{esc(lt)}</span></li>')
        chapters.append(f'<section class="modwrap">\n{body}\n</section>')
    toc = "\n        ".join(toc_rows)
    mods = "\n\n".join(chapters)
    n_done = sum(1 for ch in chapters if ch.startswith('<section class="modwrap">'))
    scope = f"all {SESSIONS} sessions" if not skipped else f"{n_done} of {SESSIONS} sessions (draft)"

    out = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{d['role']} | {KIT_TITLE}</title>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700;800&family=Source+Sans+3:ital,wght@0,400;0,500;0,600;1,400&family=JetBrains+Mono:wght@500;600&display=swap">
<link rel="stylesheet" href="kit.css">
</head>
<body>

<div class="toolbar">
  <span class="lbl">{d['toolbar'][0]}</span>
  <button type="button" onclick="window.print()">🖨 Print / Save as PDF</button>
  <span class="hint">{d['toolbar'][1]}</span>
</div>

<div class="sheet">

  <header class="cover">
    <div class="kit-eyebrow">{d['eyebrow']}</div>
    <h1>{KIT_TITLE}</h1>
    <p class="sub">{d['sub']}</p>
    <div class="meta-row">{''.join(d['chips'])}</div>
  </header>

  <nav class="toc">
    <h2>Contents</h2>
    <ol>
        {toc}
    </ol>
  </nav>

{mods}

  <div class="foot">
    <div class="who"><span class="bio">{KIT_TITLE} · {d['role']}</span></div>
    <div class="ver">Complete {d['role']} · {scope} · v1.0 · &copy; 2026 {AUTHOR}</div>
  </div>

</div>
</body>
</html>
"""
    (KIT / d["base"]).write_text(out, encoding="utf-8")
    if skipped:
        print(f"WARNING: {d['base']}: {len(skipped)} session(s) skipped (source doc missing or not cuttable): "
              + ", ".join(f"{n:02d}" for n in skipped))
    print(f"wrote {d['base']}  ({len(out) // 1024} KB, {n_done} of {len(MODULES)} sessions)")
    return skipped


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if any(a in ("-h", "--help") for a in argv):
        print(__doc__)
        return 0
    strict = "--strict" in argv
    if not (KIT / "source").is_dir():
        raise SystemExit(f"source/ folder not found next to {Path(__file__).name}")
    titles = lesson_titles()
    for num, _, _ in MODULES:
        lessons_for(num, titles)          # fail early on a lesson id that left the course
    skipped = set()
    for k in DOCS:
        skipped |= set(build(k, titles, strict))
    if skipped:
        print(f"Built with {len(skipped)} session(s) missing at least one doc: "
              + ", ".join(f"{n:02d}" for n in sorted(skipped)))
        return 1
    print(f"Done: all {SESSIONS} sessions in all three books. Now render the PDFs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

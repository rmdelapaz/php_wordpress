# PHP and WordPress Development: Instructor Kit ("Course-in-a-Box")

A ready-to-teach package that lets another instructor deliver **PHP and WordPress Development** in a
classroom without building it from scratch. The live course site (<https://rays-php-wordpress.netlify.app/>)
is the learner's textbook: 31 lessons in 9 modules (72 h 30 min of learner time), each with real output
under every code block (run on WordPress 7.1.3, PHP 8.5, MySQL 9.7 and WP-CLI 2.12 in the course's Docker
project), a project step for the fictional bookstore Pages & Co., exercises with hidden solutions, a quiz
and a journal prompt. This kit is everything the instructor needs around it.

**Scope:** the whole course, Modules 1 to 9: WordPress as a PHP application and a local Docker site with
WP-CLI, debugging and Mailpit; PHP the WordPress way, the content model, the database and hooks; block
themes (`theme.json`, templates, patterns, style variations, child themes) and classic themes (the Loop,
custom queries, `functions.php`); the `pagesco-books` plugin (custom post types, security, the Settings API,
custom tables, shortcodes); custom blocks (static, dynamic, block bindings, the Interactivity API); the REST
API, custom endpoints, external APIs and WP-Cron; debugging, PHPUnit and PHPCS, performance,
internationalization, accessibility, distribution and deployment; a final project and next steps.
Learners need **PHP Foundations and MySQL Foundations (or equivalent experience)**: Session 1 opens with a
short, ungraded diagnostic.

**Format:** **18 sessions × 3 hours = 54 class hours** in two parts, two lessons per session (Session 7
teaches one lesson and starts the Part 1 project; Session 8 teaches none: it is the Part 1 project studio
and assessment; Sessions 17 and 18 share the final project, Lesson 9.1).

- **Part 1: Themes** (Sessions 1 to 8, Modules 1 to 4, **24 hours**) takes a PHP developer from an empty
  laptop to a local WordPress 7.1 site, the content model and hooks, the Pages & Co. block theme, a child
  theme and a classic/hybrid theme. It **runs on its own as a short course** and ends with the **Part 1
  project and the Part 1 assessment** (Session 8).
- **Part 2: Plugins to Launch** (Sessions 9 to 18, Modules 5 to 9, 30 hours) builds the plugin, the blocks,
  the APIs, tests and a deployment, and ends with the **final project**: Lesson 9.1's "Reserve & Pick Up",
  a hold-a-book feature built into the plugin, released and deployed to the rehearsal server.

Run it weekly (18 weeks; Part 1 alone: 8 weeks), twice a week (about 9 weeks), or as intensive days (two
sessions a day). In the file layout a session is called a "module": `source/module-09/` is Session 9. In
prose, "Module 5" always means a course module (Plugins).

Learners start each lesson project in the room and finish it at home, so "leave with" below means "have
started in class and finish before the next session".

| Session | Lessons | Learners leave with |
|---------|---------|---------------------|
| **Part 1: Themes** | | |
| S1 · WordPress for Developers and Your Local Environment | 1.1 WordPress for Developers · 1.2 Your Local Development Environment (+ welcome, environment check, diagnostic, install clinic) | The `pagesco-dev` Docker project running WordPress 7.1.3 on PHP 8.5 (`check_environment.sh` says READY); the Pages & Co. site plan; the dev-site health check |
| S2 · PHP the WordPress Way and the Content Model | 1.3 PHP the WordPress Way · 2.1 The Content Model | The Book Card Helper (escaping, i18n, PHPCS-clean); the site stocked: users maria and devon, pages 12 to 14, News posts 15 to 17 |
| S3 · Core Architecture, the Database and Hooks | 2.2 Core Architecture & the Database · 2.3 The Hooks System | A database inventory of the site (SQL and `$wpdb`); the store notice, `mu-plugins/pagesco-site.php`, with hooks of its own |
| S4 · Theme Anatomy and Building a Block Theme | 3.1 Theme Anatomy & the Template Hierarchy · 3.2 Building a Block Theme + **Checkpoint 1** (30 min) | The template map; the `pagesco` block theme active (theme.json, six templates, two parts); a scored checkpoint |
| S5 · Patterns, Style Variations and Child Themes | 3.3 Patterns, Style Variations & the Site Editor · 3.4 Child Themes & Customizing Existing Themes | The Pages & Co. front page from patterns, a synced pattern and the Evening variation; `pagesco-tt5-child` |
| S6 · The Loop and Custom Queries | 4.1 The Loop & Template Tags · 4.2 Custom Queries | `pagesco-classic` (index, singular, 404, template parts); a front page with several loops and `pre_get_posts` |
| S7 · functions.php: Supports, Assets, Menus & Widgets | 4.3 functions.php (+ Part 1 project kickoff and studio) | The classic theme finished, `pagesco` active again; the Fernhill project started (Milestone 1) |
| S8 · Part 1 Project and Assessment | — (Part 1 review, project studio, the **Part 1 assessment**, 60 min, review and showcase) | The Fernhill Community Garden theme nearly done (due a week later); a scored Part 1 assessment. Part 1 alone: the course closes here |
| **Part 2: Plugins to Launch** | | |
| S9 · Your First Plugin and Custom Post Types | 5.1 Your First Plugin · 5.2 Custom Post Types, Taxonomies & Meta (+ Part 1 refresher, "starting with Part 2", the Part 2 check) | `pagesco-books` with Composer autoloading and the store notice moved in; the `book` type, `genre`, six meta keys, eleven books seeded |
| S10 · Security and the Settings API | 5.3 Security in WordPress · 5.4 Admin Pages, Settings API & Options | The plugin hardened (nonces, capabilities, sanitize/escape, prepared SQL); a settings page the shop can change |
| S11 · Custom Tables, Shortcodes and Block Setup | 5.5 Shortcodes, $wpdb & Custom Tables · 6.1 Block Development Setup | The events table and `[pagesco_events]`; the Book Card's first build with Node 24 and `@wordpress/scripts` |
| S12 · Static and Dynamic Blocks | 6.2 Static Blocks · 6.3 Dynamic Blocks & Block Bindings | A staff pick on the Staff picks post; book pages with live details (Book List, bindings) |
| S13 · The Interactivity API and Using the REST API | 6.4 The Interactivity API · 7.1 Using the REST API + **Checkpoint 2** (30 min) | A Find a Book page; Stock at a Glance with application passwords; a scored checkpoint |
| S14 · Custom Endpoints, External APIs and Cron | 7.2 Custom REST Endpoints · 7.3 External APIs, Transients & WP-Cron | The `pagesco/v1` events API; the supplier sync (transients, a daily cron job, an ability) |
| S15 · Debugging, Testing and Performance | 8.1 Debugging & Testing · 8.2 Performance & Caching | PHPCS clean and twelve PHPUnit tests in wp-env; a faster shop, with numbers |
| S16 · Distribution and Deployment | 8.3 Internationalization, Accessibility & Distribution · 8.4 Deployment & Maintenance (+ final-project brief) | Release 1.1.0 (Spanish, accessibility fixes, a ZIP, Plugin Check); launch day rehearsed on the `pagesco-live` server; the brief read |
| S17 · Final Project Kickoff and Studio I | 9.1 Final Project (plan, holds table, rules, the first doors) | Reserve & Pick Up Milestones 1 to 4 (5 and 6 at home) |
| S18 · Final Project Studio II, Showcase and Next Steps | 9.1 (quality, release 1.2.0, the deploy, showcase) · 9.2 Next Steps | Milestones 7 to 9 and a three-minute showcase; the next-steps plan. Submit within a week |

**Why this shape (and the timing trade-off):** the lessons were written and timed honestly for a solo
learner at 100 to 150 minutes each (the final project, 300), so two of them come to more than the roughly
150 room minutes left once the warm-up, break and wrap-up are out. They do not fit whole, and the kit does
not pretend they do. The room protects what is hardest alone: the **mental model**, a **live demo**
learners type along with, the **guided lab** (new practice on the Pages & Co. site, never the lesson's own
project), and **starting** each lesson project together. Home gets the rest: finishing the two projects,
the lesson's exercises, quiz and journal, about two to three hours between sessions (three after Session
13). Every facilitator guide says, for its session, what is done in the room, what goes home, what to
protect and what to cut first if you run long.

Every session runs 0:00 to 3:00 with one 10-minute break: a warm-up (retrieval questions and a site
check that proves every laptop is at the state the session starts from; Session 1 opens with 30 minutes of
welcome, environment check and diagnostic, Session 9 with a 30-minute Part 1 refresher, "starting with Part
2" note and Part 2 check), the lessons (frame, demo, guided lab, project start), and a 10-minute wrap-up
(exit ticket, homework, the next session's bring list). Checkpoint 1 sits in Session 4, Checkpoint 2 at
2:20 in Session 13; Session 8 runs a 50-minute project studio, then the 60-minute Part 1 assessment at 1:35.

### Teaching Part 1 only

Part 1 (Sessions 1 to 8) is a complete short course of 8 × 3 hours = 24 hours: a local development site,
WordPress's content model, database and hooks, and three kinds of theme. Nothing in it depends on Part 2.
Session 8's facilitator guide closes either the course (completion, next steps, evaluation) or Part 1
(Part 2 preparation as homework). The Part 1 project (the Fernhill Community Garden block theme) and the
Part 1 assessment (the Brightwater Swim School classic theme), with their rubrics, scoring sheets and
notes, are in `final-assessment.html`. The sell sheet prices the full program and the Part 1 option
separately.

Programs can also run **Part 2 on its own** for learners who already build themes: Session 9's guide has a
"Starting with Part 2" note (send the setup guide, including its Part 2 section, a week ahead). Learners who
did not do Part 1 (or whose Part 1 site is broken) install the **Part 2 starting site**,
`downloads/pagesco-part2-start.zip` on the course site: the site exactly as Lesson 4.3 leaves it (three
themes, the store-notice must-use plugin, the database), imported into their Lesson 1.2 project by one
command (`docker compose run --rm wpcli sh pagesco-part2-start/install.sh`, which saves the old database
first; its README.txt has the steps).

### Primary documents: the combined books (start here)

| File | Audience | Contents |
|------|----------|----------|
| `participant-workbook.{html,pdf}` | Learner | The complete workbook: all 18 sessions as chapters with Part dividers (goals, key ideas, a new worked example per lesson, guided-lab steps, predict-then-run items, a 12-item self-check, homework checklist, glossary; Start Here pages in Sessions 1 and 9; the checkpoint pages; the Part 1 project and the final project pages) |
| `facilitator-guide.{html,pdf}` | Instructor | The complete teaching manual: per session, Before the Session (prep checklist, files, known environment traps), the 0:00–3:00 agenda, warm-up with answers and the site check, lesson plans with live-demo scripts (every command run on WordPress 7.1.3 / PHP 8.5, with its real output), the three mistakes to expect, checks for understanding, closing (exit ticket, homework, next bring list) and "If you run long or short" |
| `answer-key.{html,pdf}` | Instructor | Every self-check item answered with reasons (including why each wrong option is wrong), lab solution notes with the solutions' real output, the lesson pages' own quiz answers, warm-up, diagnostic, exit-ticket and checkpoint answers with rubrics (confidential) |

**Self-check items:** 12 per session, 18 × 12 = **216**, every one answered in the answer key. The
workbook quiz, the answer key and the guide's compact answers are generated from one item list per
session and are checked to match word for word, with the correct letters balanced across A to D.

The editable per-session docs live in `source/module-NN/`. **They are generated** (see "Editing and
building"): change a session through its generator, then run `python3 build-combined.py` to regenerate the
three books and re-render their PDFs.

### Kit-wide documents

| File | Audience | Purpose |
|------|----------|---------|
| `setup-guide.html` | Learner (+ a facilitator page) | Before-you-begin guide, the same steps as Lesson 1.2: Docker (Windows with WSL 2, macOS, Linux), the `pagesco-dev` project and the Linux/WSL file-owner setup, the install, the `wp` shortcut, the Mailpit plugin, where `labs/` goes, the environment check, common install problems, the images and downloads per session (and `docker save` / `docker load` for an offline room), a **Part 2** section (Node 24 or the node:24 image, composer:2, the Part 2 starting site, `check_environment.sh --part2`) and a room-setup checklist. Send it a week before Session 1 |
| `quick-setup.html` | Learner | Two-page quick setup: Docker, the project, install, Mailpit and labs, the check. Send it with the full setup guide |
| `final-assessment.html` | Instructor | The **Part 1 project** (Fernhill: brief, milestones, rubric, scoring, model-solution notes), the **Part 1 assessment** (Brightwater: 60 minutes, open book, alone, rubric, scoring sheet, answer notes) and the **final project** (Lesson 9.1's Reserve & Pick Up: brief, timeline, the lesson's rubric reproduced exactly, scoring guidance, the grading run, submission rules and reference numbers measured on the reference solution `downloads/pagesco-final`) (confidential) |
| `sell-sheet.html` | Prospective instructors | One-page overview: who it is for, outcomes, format (full program and Part 1 only), what is included, prerequisites, license tiers |
| `README.md` · `LICENSE.md` | — | This overview and the tiered license template |

**Slide decks:** one per session in `slides/` (`module-NN-<slug>.html`), 566 slides in all (27 to 37 per
session). Each deck is one self-contained file: open it in a browser, arrow keys or space to advance.
Every code slide shows the real output and fits a 1280×720 projector without scrolling.

**Labs:** 78 starter/solution pairs (55 single files, 36 `.php` and 19 `.sh`; 21 folder pairs, themes,
plugins and must-use plugins with a `test_*` script; plus the Session 8 review pair and the Checkpoint 2
script) and 33 `debug_*` "find the bug" handouts across `labs/module-01/` … `labs/module-18/`, each session
with its own `README.md` (files, what each lab practices, timing, what "done" looks like, how to remove a
lab from the site afterwards, network needs). Session 1 adds the environment check and the diagnostic
pair (`labs/module-01/l1_0-orientation/`); Session 4 the Checkpoint 1 theme (`labs/module-04/checkpoint-1/`);
Session 8 the Part 1 project (`labs/module-08/p1-project/`, with `BRIEF.md`), the Part 1 assessment
(`labs/module-08/p1-assessment/`) and the review labs (`p1-review/`); Session 13 the Checkpoint 2 pair
(`labs/module-13/checkpoint-2/`). Starters run without a single PHP or WordPress message as handed out
(TODOs in comments, placeholder results) and end with an "Expected when done" comment that quotes the
solution's real output; solutions print the answers.

**Downloads on the course site** (public, used by the lessons and the kit): `pagesco-dev.zip` (the Lesson
1.2 Docker project), `pagesco-seed.zip` (Lesson 5.2's catalog seeder), `pagesco-live.zip` (Lesson 8.4's
rehearsal server), `pagesco-final.zip` (the final project's reference solution, Lesson 9.1) and
`pagesco-part2-start.zip` (the Part 2 starting site, above).

The public **syllabus** lives in the course root, one level up from `instructor-kit/`, so it stays public:
`syllabus.html` (screen, light/dark), `syllabus-print.html` (print-first, with the Part 1 option noted) and
`PHP-and-WordPress-Syllabus-18-sessions.pdf`. They are generated (see "Editing and building").

**Still to do before selling:** `LICENSE.md` is a plain-language **template**: have it reviewed by a
lawyer before commercial distribution. Pricing in the sell sheet and the license is a **suggested
anchor**: the bracketed prices are placeholders set at point of sale.

---

## Folder layout

```
instructor-kit/
├─ participant-workbook.{html,pdf}   ← canonical hand-out books (all 18 sessions, Part dividers)
├─ facilitator-guide.{html,pdf}
├─ answer-key.{html,pdf}
├─ setup-guide / quick-setup / final-assessment / sell-sheet  (.html + .pdf)
├─ slides/            one self-contained deck per session: module-NN-<slug>.html (NN = 01 … 18)
├─ labs/              check_labs.py, README.md (the lab rules and header lines),
│                     and module-01/ … module-18/: per lesson a folder lM_N-<slug>/ with
│                     *_starter + *_solution pairs (.php, .sh, or theme/plugin folders with a test_* script)
│                     and debug_* handouts;
│                     module-01/l1_0-orientation/ = environment check + diagnostic;
│                     module-04/checkpoint-1/, module-08/p1-project/, module-08/p1-assessment/,
│                     module-08/p1-review/, module-13/checkpoint-2/
├─ source/            module-01/ … module-18/ per-session docs (generated; they build the books)
├─ _parts/            the Part 1 project and assessment fragments final-assessment.html includes
├─ kit.css            shared print-first stylesheet
├─ build-combined.py  regenerate the 3 books from source/
└─ README.md · LICENSE.md
```

Every document is print-ready (a **Print / Save as PDF** button and a tuned print layout, US Letter) and
readable on a phone.

The whole `instructor-kit/` folder is kept **off the live site**: the course root's `_redirects` returns
404 for `/instructor-kit/*`. It lives in the repository only.

## How to teach from it

1. **A week before Session 1**, send learners the **setup guide** (and the two-page quick setup) with the
   `labs/` folder **without the `*_solution*` files and folders** and without `module-08/p1-assessment/`;
   ask each learner to put `labs/` inside the project folder (`~/pagesco-dev/labs/`, next to
   `compose.yaml`, not inside `wordpress/`), run `bash labs/module-01/l1_0-orientation/check_environment.sh`
   and reply with its last line (`READY for PHP and WordPress Development`). No reply means an install
   risk: chase it.
2. **Hand out** each session's `labs/module-NN/` the same way (also on a USB stick with `pagesco-dev.zip`
   and, for an offline room, the saved Docker images: the setup guide's facilitator page). Hold back the
   checkpoint and assessment folders until the moment they are used.
3. **Before each session**, read that session's facilitator guide: Before the Session (files, the site
   state the session starts from, known environment traps), the agenda, each lesson's live-demo script, the
   three mistakes to expect, and "If you run long or short". Run `python3 labs/check_labs.py module-NN`
   once.
4. **Present** from the session's deck in `slides/`; type the demos live in your own `pagesco-dev` project
   (two terminals: one for commands, one for `tail -f wordpress/wp-content/debug.log`; font 18 pt or more).
   Your projector site follows the lessons like the learners' sites do.
5. Learners work in the **participant workbook** and keep a **learning journal**.
6. Check self-checks, warm-ups and exit tickets with the **answer key**; score Checkpoints 1 and 2, the
   Part 1 project and assessment and the final project with their rubrics.
7. **After Session 8** (when Part 2 follows), send the setup guide's **Part 2** section: Node 24 (or the
   node:24 image) and the composer:2 image; learners new in Part 2 also get the Part 2 starting site.
   Session 9 opens with `check_environment.sh --part2`.

### The site a session starts from

There is one course site all the way through: the learner's own `pagesco-dev` project, which every lesson
changes a little (the "Before the Next Lesson" list on each lesson page says what it must look like).
Every session's warm-up has a **site check**: one or two commands whose output on the projector must match
every laptop, with the fix for the usual differences. The facilitator guides name the state each session
starts from (`after:lesson_NN` in the kit's own checks = what that lesson's project leaves), and every lab
header says the state it needs. Lesson 2.1 fixes the post IDs the rest of the course names (pages 12 to
14, posts 15 to 17, books from 30): its next-ID check runs before the project in Session 2.

All data is fictional: Pages & Co., its staff (Maria Lopez, Devon Park), customers and events, the Fernhill
Community Garden (Part 1 project), the Brightwater Swim School (Part 1 assessment) and Reserve & Pick Up
(final project). Book titles and authors are real classics (the catalog of MySQL Foundations' `bookstore`);
every user, email address and password is invented (`@example.com`, development passwords such as
`password` and `maria-pass` that the course replaces before launch, Lesson 8.4).

## Checkpoints and assessments

- **Checkpoint 1 (Session 4, 30 minutes):** an individual, open-book task on Modules 1 and 2 built on the
  Lesson 2.3 hooks (`labs/module-04/checkpoint-1/`, with a `test_checkpoint.sh` self-check). Five-row rubric
  and model answer in the guide and the answer key. Formative: it does not count toward completion.
- **Part 1 project (briefed in Session 7, studio in Session 8, due a week later):** the Fernhill Community
  Garden block theme (`labs/module-08/p1-project/`: BRIEF.md, a starter theme, a 12-check self-test
  `test_fernhill.php`, a model solution verified on a real site). Practice with feedback.
- **Part 1 assessment (Session 8, 1:35, 60 minutes + review):** alone, open book, a classic-theme task on a
  theme that already runs: the Brightwater Swim School (bug reports and tasks T1 to T5, a self-check
  `test_brightwater.php`). Rubric, scoring sheet and answer notes in `final-assessment.html`. When Part 1
  runs alone, it is the course's final assessment.
- **Checkpoint 2 (Session 13, 2:20, 30 minutes):** Modules 5 and 6 (`labs/module-13/checkpoint-2/`: a
  script plus a written Part D). Rubric in the answer key; returned in the Session 14 warm-up.
- **Final project:** the brief (Lesson 9.1's Reserve & Pick Up) is handed out at the end of **Session
  16**. **Session 17** is kickoff, plan, the holds table, the rules and the first doors (Milestones 1 to
  4) in a studio with check-ins; Milestones 5 and 6 go home; **Session 18** is quality, release 1.2.0 and
  the code-only deploy (Milestones 7 to 9), then the showcase. Learners submit within a week.
  `final-assessment.html` holds the lesson's rubric and reference numbers for every milestone, measured on
  `downloads/pagesco-final`.

## Requirements

- **A computer that runs Docker:** Docker Desktop on Windows 10/11 (with WSL 2: keep the project in the
  Linux file system) or macOS, or Docker Engine with Compose v2 on Linux; 8 GB of memory or more. The
  course images (`wordpress:7.1-php8.5-apache`, `mysql:9.7`, `wordpress:cli-php8.5` for the locally built
  WP-CLI image, `axllent/mailpit`) are about 3 GB on disk; Part 2 adds `composer:2` and `node:24` (about 2
  GB). Every output in the kit was produced on WordPress 7.1.3, PHP 8.5.12, MySQL 9.7.2 and WP-CLI 2.12.0.
  - **PHP 8.4** (`wordpress:7.1-php8.4-apache`) runs the course; two early lessons print PHP-8.5-only
    output, and the environment check says `READY WITH NOTES`.
- **Part 2 also needs:** Node.js 24 on the computer (or the `node:24` image, Lesson 6.1), the `composer:2`
  image, Git (Lesson 8.4), and the internet for npm and Composer installs (Lesson 1.3's translation and
  coding standards, Modules 6 to 9), wp-env's first start (Lesson 8.1) and Lesson 8.3's language pack and
  Plugin Check. Each session's README says which labs need the network.
- **A code editor** (VS Code with a PHP extension works well), a browser with developer tools, and two
  terminals. No accounts, no paid tools.
- **For the facilitator's lab check:** Python 3.8 or newer (standard library only) and Docker.

## Checking the labs (`labs/check_labs.py`)

```bash
cd instructor-kit
python3 labs/check_labs.py                 # every session
python3 labs/check_labs.py module-09       # one session (also 09 or 9; several allowed)
python3 labs/check_labs.py module-09 -v    # also show what each file printed
python3 labs/check_labs.py --file labs/module-01/l1_2-local-environment/site_report_solution.sh -v
python3 labs/check_labs.py --no-host       # skip the environment check's throwaway Compose project
```

For every lab file it installs the lab on a site at the state the lab declares (`// state: fresh` or
`after:lesson_NN`), runs it the way a learner does (`wp eval-file --use-include <file>` for PHP, `sh <file>`
in the WP-CLI container for shell labs; folder labs are copied into `wp-content/` and activated, then their
`test_*` script runs once per folder) and prints one `PASS` / `FAIL` line per file. A file fails on any PHP
or WordPress message (Warning, Notice, Deprecated, a fatal error, "called incorrectly", a WP-CLI `Error:`)
that a `debug_*` handout did not declare in its `// expect-error:` header, in the output or newly in
`debug.log`; on a non-zero exit, a timeout, a missing `// expect:` text, or files it leaves behind in the
WordPress tree. The full rules are in `labs/README.md` and at the top of `check_labs.py`.

**Buyer mode: run the checks on your own course project.** Point the checker at your Lesson 1.2 project
(running, `docker compose up -d`):

```bash
WP_LABS_COMPOSE=~/pagesco-dev python3 labs/check_labs.py module-01
```

Every lab then runs on your site through `docker compose run --rm wpcli ...`: before each file the checker
exports your database, installs and runs the lab, removes what it installed and imports the database again,
so the site is left as it was. Your site must be at the state each lab declares (the checker prints it):
check a session's labs when your projector site is where that session starts. The environment check
(`# host: compose`) runs in your project folder. Without `WP_LABS_COMPOSE` the checker uses the course
author's runner (fresh throwaway sites per file) when it is installed.

## Editing and building

```bash
cd instructor-kit
python3 build-combined.py                 # regenerate the 3 books from source/ (with Part dividers)
python3 labs/check_labs.py                # run every lab file
```

The author's tools in `~/projects/_kit_tools/php_wordpress/` (not shipped with a licensed kit):

```bash
python3 check_kit_wp.py 01 … 18           # per-session consistency: agenda sums to 180 with contiguous clocks
                                          # and one Break, checkpoint rows, lesson titles match
                                          # course-config.json, quiz identical across workbook/key/guide,
                                          # lesson-quiz letters match the pages, lab paths, pairs and headers,
                                          # decks fit 1280x720, nothing wider than 390 px, no console errors
python3 gen_syllabus_wp.py --course ~/projects/php_wordpress    # rebuild ../syllabus{,-print}.html
python3 render_pdfs_wp.py --course ~/projects/php_wordpress PHP-and-WordPress-Syllabus-18-sessions.pdf
                                          # the seven kit PDFs + the syllabus PDF, page counts, a 390 px check
bash verify_all.sh                        # the course itself: every lesson's blocks run on WordPress 7.1.3 /
                                          # PHP 8.5 and compared with its printed output
```

**The generators are the source of truth.** Each session's three documents and deck are generated: the
generator for Session N is `~/projects/_kit_tools/php_wordpress/kit_generators/SNN/gen_SNN.py`, with the
blocks it shows in `blocks_SNN.py` (demo code is read from the lesson pages themselves), run for real on a
WordPress 7.1.3 / PHP 8.5 site through `kitlib_wp.py`, with results cached next to the generator
(`--fresh` reruns everything). Lab outputs in the answer keys come from running the lab files exactly as
`check_labs.py` does. `final-assessment.html` comes from `kit_generators/final/gen_final.py` (Session 8's
generator writes the `_parts/` fragments it includes). To change a session, edit its generator, run it from
its own folder (`python3 -I gen_SNN.py`), then rebuild the books, the syllabus and the PDFs; hand edits to
the generated HTML are lost the next time the generator runs. The lab files, their READMEs and the
kit-wide documents (this file, `LICENSE.md`, the setup guide, the quick setup, the sell sheet) are edited
directly. The Part 2 starting site is rebuilt from the saved Lesson 4.3 state with
`agents/int/part2_start.py build` (and checked end to end with `verify`).

Or open any document and use **Print / Save as PDF** (Letter, 0.5 in margins, background graphics on).

---

## License

See `LICENSE.md`. Short version: licensed to a **single instructor or organization** to teach the kit;
**not** for resale; the facilitator guide, answer key and final assessment are **not** for learner
distribution. The Pages & Co., Fernhill, Brightwater and Reserve & Pick Up materials are part of the
licensed materials. Tiers (Solo / Organization / White-label, for the full program or Part 1 only, plus an
optional updates add-on) are set at point of sale. WordPress (GPLv2 or later), PHP, MySQL, Docker images,
Node.js, Composer and the npm and Composer packages the lessons install are not part of the kit: learners
get them from their publishers under their own licenses; the course's theme and plugin code is GPL-2.0-or-later,
as code that runs in WordPress must be (`LICENSE.md`, Third-party).

© 2026 Ray de la Paz. PHP and WordPress Development. All rights reserved.

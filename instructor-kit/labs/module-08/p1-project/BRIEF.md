# Part 1 Project: a block theme for the Fernhill Community Garden

Session 7 to one week after Session 8 · about 3 h 45 min of work · Modules 1 to 4 · open book

## The client

Odette Marsh, the garden's volunteer coordinator, writes:

> Our website runs on a free theme from 2019 that nobody dares to touch. We would like our own theme, made for us: green and calm, our news on the front page three at a time, a big welcome at the top, a call for Saturday volunteers, and an autumn look we can switch on in October. Our volunteers write news and edit pages in the editor; none of us writes code. And please: nothing that breaks when WordPress updates itself.

The garden's own news is not written yet: build and test on your course site's posts and pages (four posts, three of them in News; About Us, Events, Contact). Your theme must not care whose content it shows.

## What you build

A block theme in its own folder, `wordpress/wp-content/themes/fernhill/`, prefix `fernhill_`, text domain `fernhill`. Requirements:

- **R1 Design system** (Lesson 3.2; self-check 1 to 4). `style.css` names the theme: Theme Name `Fernhill`, Text Domain `fernhill`, Version `1.0.0`, Requires at least `7.1`, Requires PHP (the version you test on, at least `8.1`), Tested up to `7.1`. `theme.json` is version 3 with the 7.1 `$schema` and holds the design: exactly five colors named by role, in this order: `base` #f7f5ee, `contrast` #23301f, `primary` #3f6b35, `secondary` #e4ecd9, `accent` #9c4426 (`defaultPalette` off); content width `680px`, wide width `1100px`; a serif for text and a sans-serif for headings (system font stacks, no font files); links and buttons in primary, text in contrast on base.
- **R2 Templates and parts** (Lessons 3.1, 3.2; self-check 5, 6). Templates `index`, `front-page`, `single` and `page` (and `404`, R7). Two template parts declared in `theme.json` with their areas: `header` (the site title and a Navigation block) and `footer` (two lines: "Fernhill Community Garden · 48 Orchard Lane · 555-0187" and "Workdays every Saturday, 9 a.m. to noon"). Every template is the header part (tagName `header`), one group with tagName `main`, and the footer part (tagName `footer`): the landmarks screen readers and the skip link need.
- **R3 Patterns and the front page** (Lessons 3.3, 1.3; self-check 7, 9). Two PHP patterns in `patterns/`: `fernhill/hero` (an h1 "Grow food, grow friendships", the welcome paragraph, a button "About the garden" to `/about/`, the leaf drawing `assets/images/leaf.svg` with its alt text) and `fernhill/volunteer-call` (an h2 "Volunteer on Saturday mornings", a paragraph, a button "Sign up for a workday" to `/contact/` in the accent color). Both in the theme's category `fernhill`; every visible string through `esc_html_e()` or `esc_attr_e()` with the `fernhill` text domain; URLs through `esc_url( home_url( ... ) )`. `front-page.html`: the hero, an h2 "News from the garden", a Query Loop that inherits the main query (title, date, excerpt, pagination), the volunteer call.
- **R4 Style variation** (Lesson 3.3; self-check 8). `styles/autumn.json`, titled `Autumn`: the same five slugs with autumn colors (the brief suggests base #fbf4ea, contrast #3a2318, primary #8a3b1e, secondary #f1dfc6, accent #4f6b2a). Odette switches it on in Styles; nothing else changes.
- **R5 functions.php** (Lessons 4.3, 2.3; self-check 7, 10). Registers the pattern category `fernhill` (label "Fernhill Garden") on `init`, and enqueues `assets/css/fernhill.css` (shipped in the starter) with the handle `fernhill-style`, versioned with the theme's own Version, on `wp_enqueue_scripts`. One prefixed function (`fernhill_`) per job, each with a docblock.
- **R6 The main query** (Lesson 4.2; self-check 11). The blog home (the front page of this site, which shows the latest posts) lists **three** posts per page and paginates the rest (the fourth course post on `/page/2/`). Change the main query in `pre_get_posts` with the three guards of Lesson 4.2: not in the admin, the main query only, the blog home only. No second query in the template.
- **R7 404 page** (Lesson 3.1; self-check 12). `templates/404.html`: an h1 "This path is overgrown", one sentence, and a Search block, between the same header and footer. WordPress answers with status 404.
- **R8 Quality** (Lessons 1.3, 3.2; self-check every line). No PHP message on any page with debugging on (`debug.log` stays quiet); WordPress coding standards (tabs, spaces inside parentheses, docblocks: Lesson 1.3); every function prefixed; no edits to core, the course themes or another theme's files; no Site Editor copies left in the database (Lesson 3.2: they win over your files); the per-URL check of Lesson 3.2 passes for `/`, `/page/2/`, `/hello-world/`, `/about/`, `/category/news/`, `/?s=garden` (200) and `/no-such-path/` (404); a short `NOTES.md` in the theme folder.

Stretch, if you have time (evidence for Exemplary):

- **A section style** (`styles/sections/`, Lesson 3.3) for the volunteer band instead of hand-set colors.
- **`search.html`** with a Query Title of the search type and the Query No Results block (Lesson 3.2).
- **A child theme** `fernhill-kids` for the children's garden page: `Template: fernhill`, a theme.json that only changes the accent color and one `page-kids.html` template (Lesson 3.4).
- **`screenshot.png`** (1200 by 900) so the theme looks right in Appearance > Themes.

## Files

Everything is in `labs/module-08/p1-project/` (in your project folder):

- `fernhill_starter/`: your starting theme. Ready: `assets/css/fernhill.css`, `assets/images/leaf.svg`, `parts/header.html`. Half done: `patterns/hero.php`, the model for R3. TODOs: `style.css`, `functions.php`. Bare: `theme.json`, `templates/index.html`.
- `fernhill_front.png`: what the finished front page looks like on the course site (the thin line at the very top is the course's own store notice, printed by a must-use plugin: not your theme's job).
- `test_fernhill.php`: the self-check. Twelve lines, OK or TODO, and `Checks passed: N of 12`. Run it as often as you like. It helps; it is not your score (R8 and the rubric are read by your instructor).

## Set up (Milestone 1)

From your project folder (`~/pagesco-dev`):

```
cp -r labs/module-08/p1-project/fernhill_starter wordpress/wp-content/themes/fernhill
wp theme activate fernhill
cp labs/module-08/p1-project/test_fernhill.php wordpress/
wp eval-file --use-include test_fernhill.php
```

The last line says `Checks passed: 1 of 12`. Edit the files in `wordpress/wp-content/themes/fernhill/` in VS Code. When you stop for the day:

```
wp theme activate pagesco
```

and when you are done with the project, `rm wordpress/test_fernhill.php` (keep your theme folder: it is yours, and it does not disturb the course site while pagesco is active).

## Milestones

| | Minutes | What | Requirements | Where |
|---|---|---|---|---|
| M1 | 15 | Set up: copy the starter to `wordpress/wp-content/themes/fernhill/`, activate it, run the self-check (`Checks passed: 1 of 12`), read every starter file and its TODOs. | – | Session 7 studio |
| M2 | 45 | The design system: the style.css header and theme.json (palette, layout, fonts, element styles). | R1 | Session 7 studio (start), home |
| M3 | 60 | Templates and parts: header and footer parts, index, single, page, 404; the per-URL check. | R2, R7 | home |
| M4 | 45 | Patterns and the front page: the two PHP patterns, front-page.html. | R3 | home, Session 8 studio |
| M5 | 30 | functions.php: the pattern category, the stylesheet, the main query. | R5, R6 | Session 8 studio |
| M6 | 30 | The Autumn variation, NOTES.md, the per-URL check and the self-check (`Checks passed: 12 of 12`), the hand-in. | R4, R8 | Session 8 studio, home |

## Rules

- Open book: the lesson pages, your notes, your workbook, your own course code (the pagesco theme is the closest model). Talk ideas through with other learners; write your own code.
- AI assistants may explain an error message; they do not write the theme. Be ready to explain any line of it: the review in Session 8 and the feedback may ask.
- Work on your course site. The test switches nothing: you activate `fernhill` yourself, and when you stop for the day you run `wp theme activate pagesco` (Session 9 and Lesson 5.1 start from pagesco active).
- Edit the theme's FILES. If you try something in the Site Editor, export it or copy its markup into the file, then delete the database copy (Lesson 3.2, Mistake 3): a copy left behind hides your files and is not in your zip.

## Hand-in

- **One zip,** `fernhill-<yourname>.zip`, of the theme folder `wordpress/wp-content/themes/fernhill/` (the folder itself, not its parent), made on your computer.
- **`NOTES.md` in the theme folder:** what is unfinished (or "nothing"); one decision you made and why (a color, a template, where a piece of code lives); the last lines of the self-check.
- **Due one week after Session 8**, to the address your instructor gives you. Feedback comes back within a week, on the rubric below.

## Rubric

| Criterion | 4 Exemplary | 3 Met | 2 Partly | 1 Not yet |
|---|---|---|---|---|
| **Design system (R1, R4)** (Lessons 3.2, 3.3) | All of Met, and the styles live in theme.json only (no hard-coded colors in templates or patterns), plus a stretch item done well. | Header complete; theme.json version 3 with the five role colors in order, default palette off, both widths, two font stacks, link and button styles; the Autumn variation changes only the palette. | theme.json works but a color, a width or the variation is missing or misnamed; or colors are hard-coded hex in markup. | theme.json does not load (a decode notice) or the theme falls back to core styles. |
| **Templates and parts (R2, R7)** (Lessons 3.1, 3.2) | All of Met, and the markup is valid in the Site Editor (no "unexpected or invalid content"), plus search.html or the child theme. | index, front-page, single, page and 404 present; header and footer parts with their areas; every page has one header, one main and one footer; the 404 page answers 404 with its heading and a search. | A template or a part missing, a part slug typo, or a landmark missing on some pages. | Pages fall back to index everywhere, or a part does not render. |
| **Patterns and front page (R3)** (Lessons 3.3, 1.3) | All of Met, and the patterns use only theme presets (spacing, colors) and are useful from the inserter on any page. | Both patterns registered in the fernhill category; every string translatable with the fernhill domain and escaped; URLs with esc_url( home_url() ); the front page shows hero, news (inherit) and the call. | One pattern missing, or strings not translatable, or a URL hard-coded to localhost. | No PHP patterns; the front page is plain markup with hard-coded text. |
| **functions.php and the main query (R5, R6)** (Lessons 2.3, 4.2, 4.3) | All of Met, and the learner can say why pre_get_posts beats a second query here (paging, one query, the Query Loop inherits). | Category on init; fernhill-style enqueued on wp_enqueue_scripts with the theme's Version; pre_get_posts with all three guards; 3 posts on /, 1 on /page/2/. | Works, but a guard is missing (admin lists change too), the version is hard-coded or missing, or a hook is wrong but happens to work. | Code runs at the top level of functions.php, a second query replaces the main one, or a fatal error. |
| **Quality and verification (R8)** (Lessons 1.3, 3.2) | All of Met, and NOTES.md explains a real trade-off; the code would pass PHPCS (Lesson 8.1) without changes. | No PHP messages; coding standards and prefixes; the per-URL check passes; no Site Editor copies; NOTES.md complete; the self-check output included. | A notice on one page, unprefixed names, or NOTES.md missing a part. | Warnings on several pages, edits outside the theme folder, or no NOTES.md. |

**Met** = at least 14 of 20 points with no row at 1. Below that, the learner revises once, within a week of the feedback.

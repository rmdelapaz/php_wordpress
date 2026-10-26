# Session 4 labs · Lessons 3.1 + 3.2 · Checkpoint 1

**Theme Anatomy and Building a Block Theme.** The labs run on the course site as the lessons leave it:

- `checkpoint-1/` and `l3_1-theme-anatomy/` start from **the end of Lesson 2.3** (`// state: after:lesson_06`):
  Twenty Twenty-Five active, `mailpit-smtp.php` and `pagesco-site.php` in `wp-content/mu-plugins/`, the users,
  pages and News posts of Lesson 2.1. That is the site learners bring to Session 4.
- `l3_2-block-theme/` starts from **the end of Lesson 3.1** (`// state: after:lesson_07`): the same site, Twenty
  Twenty-Five active again. The two theme labs switch themes: note your active theme first
  (`wp theme list --status=active --field=name`; `pagesco` once you have built it in Lesson 3.2) and switch back
  to it at the end.

Copy the kit's `labs/` folder into your project folder (`~/pagesco-dev/labs/`, next to `compose.yaml`) and type
every command below in the project folder. `wp` is the shortcut from Lesson 1.2.

| Folder | File | What it practices | Time | Done when |
|---|---|---|---|---|
| `checkpoint-1/` | `checkpoint_starter/` → `checkpoint_solution/` + `test_checkpoint.sh` | **Checkpoint 1 (Modules 1 and 2), in class, alone, open site and closed notes.** A must-use plugin that adds the newest News post and a link to Maria's author archive to the store notice (Lesson 2.3's own filter and action, with priorities) and counts the published pages with a prepared `$wpdb` query | 23 min | the test prints `Latest news: Book club: Dune.`, `Ask Maria Lopez` and `Published pages: 4` with no message |
| `l3_1-theme-anatomy/` | `which_template_starter.php` → `which_template_solution.php` | **Guided lab.** The template hierarchy, both halves: the candidate list (`get_template_hierarchy()`) and the first template the active theme has (`get_block_templates()`) | 15 min | the output matches "Expected when done" |
| | `theme_inspector_starter.sh` → `theme_inspector_solution.sh` | Theme anatomy for every installed theme: version, `Requires at least`, block or classic, how many templates, parts and patterns, a functions.php or not | 10 min | the output matches "Expected when done" |
| | `debug_theme_report.php` | A report on the active theme with two loud bugs (Warnings) and a silent one (a theme header read with the wrong key) | 10 min | name, `Needs WordPress: 6.7`, the eight palette colors and `Colors in the palette: 8`, no message |
| `l3_2-block-theme/` | `book_fair_starter/` → `book_fair_solution/` + `test_book_fair.sh` | **Guided lab.** A small block theme of your own (`pagesco-fair`): a palette color, a styles section, a Query Loop and a footer part | 20 min | the test prints the three colors, the page colors, `posts listed: 4` and `footer parts: 1` |
| | `theme_json_reader_starter.php` → `theme_json_reader_solution.php` | theme.json read with PHP: settings (widths, palette, font sizes) and styles, and the `var:preset\|color\|x` shorthand turned into the CSS WordPress prints | 10 min | the output matches "Expected when done" |
| | `debug_cafe_theme/` + `test_debug_cafe_theme.sh` | A café theme with a trailing comma in theme.json (Notice), a filter that forgets to return (Deprecated) and a template part slug typo (silent) | 15 min | the test prints no message, both colors, `header parts: 1` and the titles with their cup |

## Commands

```bash
cd ~/pagesco-dev

# a PHP lab: copy it into the WordPress root, edit THAT copy, run it with WordPress loaded, delete it
cp labs/module-04/l3_1-theme-anatomy/which_template_starter.php wordpress/
wp eval-file --use-include which_template_starter.php
rm wordpress/which_template_starter.php

# a shell lab: the same, run in the WP-CLI container
cp labs/module-04/l3_1-theme-anatomy/theme_inspector_starter.sh wordpress/
docker compose run --rm wpcli sh theme_inspector_starter.sh
rm wordpress/theme_inspector_starter.sh

# the checkpoint: a must-use plugin and its test
cp labs/module-04/checkpoint-1/checkpoint_starter/pagesco-checkpoint.php wordpress/wp-content/mu-plugins/
cp labs/module-04/checkpoint-1/test_checkpoint.sh wordpress/
docker compose run --rm wpcli sh test_checkpoint.sh
rm wordpress/test_checkpoint.sh wordpress/wp-content/mu-plugins/pagesco-checkpoint.php

# a theme lab: note your theme, install and activate the lab theme, run its test, switch back, remove both
wp theme list --status=active --field=name
cp -r labs/module-04/l3_2-block-theme/book_fair_starter wordpress/wp-content/themes/pagesco-fair
wp theme activate pagesco-fair
cp labs/module-04/l3_2-block-theme/test_book_fair.sh wordpress/
docker compose run --rm wpcli sh test_book_fair.sh
wp theme activate pagesco          # or twentytwentyfive: the theme the first command printed
wp theme delete pagesco-fair
rm wordpress/test_book_fair.sh
```

`debug_theme_report.php` and `theme_json_reader_starter.php` run like `which_template_starter.php`. The café
handout installs like the book-fair theme, as `wordpress/wp-content/themes/pagesco-cafe` (`wp theme activate
pagesco-cafe`, test `test_debug_cafe_theme.sh`, then switch back and `wp theme delete pagesco-cafe`).

## Notes for the instructor

- **Expected outputs** are in each starter's "Expected when done" comment (the solutions' real output) and, with
  explanations, in the Answer Key's "Lab Reference Solutions". The pattern counts in `theme_inspector` are the
  default themes' as shipped with WordPress 7.1.3 and change when those themes update: the commands, not the
  numbers, are the skill.
- **Theme labs and the database.** Switching themes makes WordPress write options (`theme_mods_pagesco-fair`,
  `theme_switched`), exactly as Lesson 3.1's sketch theme did; they are harmless and stay after the theme is
  deleted. Nothing else in the database changes. Never delete or rename `pagesco` for a lab: the lab themes are
  their own folders.
- **`which_template` and the hierarchy.** `get_template_hierarchy()` works from slugs, so it never lists the
  ID-based names (`author-3`, `page-13`) that a real request adds (Lesson 3.1, Exercise 1). With `pagesco` active
  (after Lesson 3.2) the front page answers `index`, because pagesco has no `home` template: a good question to ask.
- **`theme_json_reader`** reads Twenty Twenty-Five's file whatever theme is active; set `$pagesco_slug = 'pagesco'`
  after Lesson 3.2 to read your own (`680px`, `1180px`, `paper, ink, oxblood, sage, slate`, `var(--wp--preset--color--ink)`).
- **The checkpoint** expects the site of Lesson 2.3 (pagesco-site.php in mu-plugins/, the News posts and the user
  maria of Lesson 2.1). Its rubric and model answer are in the facilitator guide and the answer key.
- **PHP 8.4:** every lab runs the same.
- **Checking the labs:** `python3 labs/check_labs.py module-04` (15 results in about a minute and a half). On your own
  project: `WP_LABS_COMPOSE=~/pagesco-dev python3 labs/check_labs.py module-04` (your site must be at the state
  each file names: the 3.1 labs and the checkpoint before Lesson 3.1, the 3.2 labs with Twenty Twenty-Five active).

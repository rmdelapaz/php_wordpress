# Session 6 labs · Lessons 4.1 + 4.2

**The Loop and Custom Queries.** The labs run on the course site at the states the lessons start from (each
file's `state:` line):

| State | What your site has | Which labs |
|---|---|---|
| `after:lesson_10` | the end of Lesson 3.4: `pagesco` active, `pagesco-tt5-child` installed, the four posts and three pages of Lesson 2.1 | everything in `l4_1-loop-template-tags/` (none of it needs pagesco-classic) |
| `after:lesson_11` | the end of Lesson 4.1: `pagesco-classic` active (index.php, singular.php, 404.php, two template parts, theme.json) | everything in `l4_2-custom-queries/` |

Copy the kit's `labs/` folder into your project folder (`~/pagesco-dev/labs/`, next to `compose.yaml`) and type
every command below in the project folder; `wp` is the shortcut from Lesson 1.2. Every lab removes itself again.

| Folder | File | What it practices | Time | Done when |
|---|---|---|---|---|
| `l4_1-loop-template-tags/` | `shelf_theme_starter/` → `shelf_theme_solution/` + `test_shelf_theme.sh` | **Guided lab.** A one-template classic theme: the Loop, template tags (printed and returned, escaped), `the_title_attribute()`, a heading chosen by conditional tags, an empty-list message. One file draws five kinds of page | 20 min | the test shows `Shelf: News`, `Book club: Dune · 2026-10-01 · Maria Lopez` and `Nothing on this shelf.` |
| | `template_tags_starter.php` → `template_tags_solution.php` | The the_/get_ table outside the Loop, on one post: raw and filtered title, the attribute version, permalink, date, author, categories, raw vs rendered content, excerpt, classes | 15 min | eleven lines without TODO |
| | `debug_loop_report.php` | A Loop run on a real main query (`wp( 's=dune' )`): a typo (Warning), a conditional tag asked too early and a template tag concatenated into a string (both silent) | 10 min | the heading, two `- <title> (<date>)` lines, `2 result(s) for "dune"` |
| `l4_2-custom-queries/` | `query_shelf_starter.php` → `query_shelf_solution.php` | **Guided lab.** Five shop questions as WP_Query arguments (author_name, category_name + paged, date_query, post_name__in + orderby, fields ids) and what post_count, found_posts and max_num_pages say | 20 min | five lines without TODO |
| | `archive_rules_starter/` → `archive_rules_solution/` + `test_archive_rules.sh` | A must-use plugin with a guarded `pre_get_posts` callback: author archives oldest first, date archives one post per page (so `/2026/09/page/2/` exists), secondary queries untouched | 15 min | `/2026/09/page/2/    200` and `a September box:    2 posts` |
| | `debug_related_box.php` | A related-posts box on a real main query: a `for` loop that walks past the end (Warning), `wp_list_pluck()` on the query instead of its posts, and a missing `wp_reset_postdata()` (both silent) | 10 min | two titles, a `Titles:` line, `This page is about: Book club: Dune` |

## Commands

```bash
cd ~/pagesco-dev

# the theme lab of Lesson 4.1: install, activate, test, switch back, remove
cp -r labs/module-06/l4_1-loop-template-tags/shelf_theme_starter wordpress/wp-content/themes/pagesco-lab-shelf
wp theme activate pagesco-lab-shelf
cp labs/module-06/l4_1-loop-template-tags/test_shelf_theme.sh wordpress/
docker compose run --rm wpcli sh test_shelf_theme.sh
wp theme activate pagesco                 # or pagesco-classic, if you are past Lesson 4.1
rm -r wordpress/wp-content/themes/pagesco-lab-shelf wordpress/test_shelf_theme.sh

# a PHP lab: copy it into the WordPress root, edit THAT copy, run it with WordPress loaded, delete it
cp labs/module-06/l4_2-custom-queries/query_shelf_starter.php wordpress/
wp eval-file --use-include query_shelf_starter.php
rm wordpress/query_shelf_starter.php

# the must-use plugin lab of Lesson 4.2
cp labs/module-06/l4_2-custom-queries/archive_rules_starter/pagesco-archive-rules.php wordpress/wp-content/mu-plugins/
cp labs/module-06/l4_2-custom-queries/test_archive_rules.sh wordpress/
docker compose run --rm wpcli sh test_archive_rules.sh
rm wordpress/test_archive_rules.sh wordpress/wp-content/mu-plugins/pagesco-archive-rules.php
```

`template_tags_starter.php`, `debug_loop_report.php` and `debug_related_box.php` run like `query_shelf_starter.php`.

## Notes for the instructor

- **Expected outputs** are in each starter's "Expected when done" comment (the solutions' real output) and, with
  explanations, in the Answer Key's "Lab Reference Solutions".
- **`wp( '...' )` in the PHP labs.** WP-CLI runs no main query (Lesson 4.1), so the two debug handouts run one
  themselves: `wp()` parses the query string and runs the main query exactly as a request for that address
  does (WordPress's own tests do the same). Conditional tags and the Loop then behave as in a template.
- **Dates.** Every date the labs print is a post date from Lesson 2.1 (September and October 2026). `Hello
  world!` carries the date your site was installed, which is why no lab prints it with a date, and why
  `before October` in `query_shelf` lists only the two September posts on any course site installed after
  October 1, 2026.
- **Theme switches** (the Shelf lab) create a `theme_mods_pagesco-lab-shelf` option: harmless (Lessons 3.1, 3.4).
- **`archive_rules`** changes the main query only while the file is in `mu-plugins/`; the last command removes it.
- **No network needed. PHP 8.4:** every lab prints the same.
- **Checking the labs:** `python3 labs/check_labs.py module-06` (about a minute and a half). On your own project:
  `WP_LABS_COMPOSE=~/pagesco-dev python3 labs/check_labs.py module-06` (your site must be at the states above).

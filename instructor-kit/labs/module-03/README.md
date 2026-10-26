# Session 3 labs · Lessons 2.2 + 2.3

**Core Architecture, the Database and Hooks.** Every file runs on the course site as Lesson 2.1 leaves it
(`// state: after:lesson_04`): WordPress 7.1.3, PHP 8.5, MySQL 9.7, WP-CLI 2.12, Twenty Twenty-Five active, the users
`maria` (editor, ID 2) and `devon` (author, ID 3), the pages About Us, Contact and Events (12 to 14), three posts in
News (15 to 17), `mailpit-smtp.php` in `wp-content/mu-plugins/`. That is also where Lessons 2.2 and 2.3 start, so a
learner who has finished Session 2's homework is there. The labs work the same on a site that already has Lesson 2.3's
`pagesco-site.php`: none of them reads the store notice.

Copy the kit's `labs/` folder into your project folder (`~/pagesco-dev/labs/`, next to `compose.yaml`) and type every
command below in the project folder. `wp` is the shortcut from Lesson 1.2. No lab writes to the database, and every
lab removes itself again: the last command of each is an `rm`.

| Folder | File | What it practices | Time | Done when |
|---|---|---|---|---|
| `l2_2-core-database/` | `meta_pivot_starter.sh` → `meta_pivot_solution.sh` | **Guided lab.** The key-value pattern read back as columns: a join with the key in `ON`, a `MAX(CASE ...)` pivot, the same through `wp user list`, a `GROUP BY` count | 20 min | the output matches "Expected when done" |
| | `wpdb_report_starter.php` → `wpdb_report_solution.php` | `$wpdb->get_var()`, `get_col()` and `get_row()` with `{$wpdb->...}` table names and `prepare()`, each answer checked against the API | 15 min | six lines without TODO |
| | `debug_meta_report.php` | Three metadata questions with two loud bugs (Warnings) and a silent one | 10 min | `Post 15 waiting for pings: yes`, `Maria's role: editor`, `Published pages: 4` |
| `l2_3-hooks/` | `filter_chain_starter.php` → `filter_chain_solution.php` | **Guided lab.** Three callbacks on one filter: priorities, two accepted arguments, a removal with the right priority, `has_filter()` | 20 min | `Line: Fahrenheit 451 by Ray Bradbury` |
| | `hook_finder_starter.sh` → `hook_finder_solution.sh` | Find hooks in core with exact `grep` patterns, then ask the running site (`has_filter()`, `$wp_filter`) | 10 min | the output matches "Expected when done" |
| | `title_parts_starter/` → `title_parts_solution/` + `test_title_parts.sh` | A must-use plugin on the `document_title_parts` filter: a tagline on the front page, "News:" on news posts | 15 min | the test prints the tagline title and `News: Book club: Dune` |
| | `debug_price_tag.php` | A price through four filters: a callback with no `return`, a variable out of scope, a removal with the wrong priority | 10 min | the last line reads `Pages & Co. price: $14.99` |

## Commands

```bash
cd ~/pagesco-dev

# a shell lab: copy it into the WordPress root, run it in the WP-CLI container, delete it
cp labs/module-03/l2_2-core-database/meta_pivot_starter.sh wordpress/
docker compose run --rm wpcli sh meta_pivot_starter.sh
rm wordpress/meta_pivot_starter.sh

# a PHP lab: copy it, edit THAT copy, run it with WordPress loaded, delete it
cp labs/module-03/l2_3-hooks/filter_chain_starter.php wordpress/
wp eval-file --use-include filter_chain_starter.php
rm wordpress/filter_chain_starter.php

# the folder lab: install the must-use plugin, run its test, remove both
cp labs/module-03/l2_3-hooks/title_parts_starter/pagesco-title.php wordpress/wp-content/mu-plugins/
cp labs/module-03/l2_3-hooks/test_title_parts.sh wordpress/
docker compose run --rm wpcli sh test_title_parts.sh
rm wordpress/test_title_parts.sh wordpress/wp-content/mu-plugins/pagesco-title.php
```

`wpdb_report_starter.php`, `debug_meta_report.php` and `debug_price_tag.php` run like `filter_chain_starter.php`;
`hook_finder_starter.sh` like `meta_pivot_starter.sh`. Try every SQL query of `meta_pivot` at the `wp db cli` prompt
first (it draws tables there); in the script, `wp db query` prints tab-separated rows with the column names first.

## Notes for the instructor

- **Expected outputs** are in each starter's "Expected when done" comment (the solutions' real output) and, with
  explanations, in the Answer Key's "Lab Reference Solutions". Line numbers in `hook_finder` are WordPress 7.1.3's
  and move between releases; the exact pattern, not the number, is the skill.
- **Learners whose site differs.** A learner who opened posts in the editor after Lesson 2.1 has more usermeta rows
  (`meta_pivot` Step 5 counts more for that user) and may have more revisions; the queries are the answer, not the
  numbers. A learner who skipped Session 2's homework has no `maria` or `devon`: `meta_pivot` then shows only `admin`,
  `wpdb_report` finds no pages for user 2, and `test_title_parts.sh` shows a 404 title for `/book-club-dune/`.
  Finish Lesson 2.1's project first (it creates both users, the three pages and the News posts).
- **The title-parts plugin** is a must-use plugin: while it is in `mu-plugins/`, every page of the learner's site
  shows the tagline. Remove it at the end (the `rm` above); `mu-plugins/` must hold only `mailpit-smtp.php` and, after
  Lesson 2.3's project, `pagesco-site.php`.
- **A fatal error in a must-use plugin** takes down the whole site, the admin and WP-CLI included (Lesson 2.3, Common
  Mistakes 3). If a learner's edit of `pagesco-title.php` breaks everything, `rm` the file from
  `wordpress/wp-content/mu-plugins/` and start again from the starter.
- **PHP 8.4:** every lab runs the same and prints the same.
- **Checking the labs:** `python3 labs/check_labs.py module-03` (14 results in about a minute). On your own project:
  `WP_LABS_COMPOSE=~/pagesco-dev python3 labs/check_labs.py module-03` (your site must be at the end of Lesson 2.1 or
  later; the checker restores your database after every file).

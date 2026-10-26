# Session 13 labs · Lessons 6.4 + 7.1 · Checkpoint 2

**The Interactivity API and Using the REST API.** Lesson 6.4's labs run on the site as Lesson 6.3 left it
(`// state: after:lesson_21`), Lesson 7.1's on the site after Lesson 6.4 (`after:lesson_22`: the Book Filter, the
Find a Book page). Checkpoint 2 runs on `after:lesson_21` (the Book List must exist). Copy the kit's `labs/` folder
into your project folder (`~/pagesco-dev/labs/`, next to `compose.yaml`) and type every command below in the project
folder. `wp` is the shortcut from Lesson 1.2. No lab needs Node, a build, a browser or the internet.

| Folder | File | What it practices | Time | Done when |
|---|---|---|---|---|
| `l6_4-interactivity-api/` | `open_today_starter.php` → `open_today_solution.php` | **Guided lab.** An opening-hours box: two derived-state closures and the directives; `wp_interactivity_process_directives()` does what WordPress does for an interactive block, on the server | 15 min | the output matches "Expected when done" |
| | `event_list_starter.php` → `event_list_solution.php` | `data-wp-each`: the server repeats a `<template>` per event in the state, with per-item context and derived state | 15 min | the output matches "Expected when done" |
| | `debug_stock_badges.php` | Stock badges with a "called incorrectly" Notice, a Warning and a silent wrong count | 10 min | Dune's badge hidden, `In stock: 1`, no message |
| `l7_1-rest-api/` | `catalog_queries_starter.sh` → `catalog_queries_solution.sh` | **Guided lab.** Six questions for the catalog, one curl request each (`_fields`, `genres`, `search`, `orderby`, a status code, a header) | 15 min | the output matches "Expected when done" |
| | `who_may_starter.sh` → `who_may_solution.sh` | Five GET requests as anonymous, Devon, Maria and admin (throwaway application passwords, revoked at the end): 200, 400, 401 or 403 | 15 min | the table matches "Expected when done" |
| | `debug_stock_list.php` | A stock list read from the REST API over HTTP: two kinds of Warning and a silent first-page-only list | 10 min | eleven books listed, `Listed 11 of 11` |
| `checkpoint-2/` | `checkpoint_starter.php` → `checkpoint_solution.php` | **Checkpoint 2 (Modules 5 and 6), instructor only until 2:20.** The Weekly Picks report: a meta query, a prepared COUNT, a Book List rendered with do_blocks(), the cards of a post | 25 min | four lines, no message (rubric in the Answer Key) |

## Commands

```bash
cd ~/pagesco-dev

# a PHP lab: copy it into the WordPress root, edit THAT copy, run it with WordPress loaded, delete it
cp labs/module-13/l6_4-interactivity-api/open_today_starter.php wordpress/
wp eval-file --use-include open_today_starter.php
rm wordpress/open_today_starter.php

# a shell lab: the same, run in the WP-CLI container (curl is there; http://localhost:8080 is the site)
cp labs/module-13/l7_1-rest-api/catalog_queries_starter.sh wordpress/
docker compose run --rm wpcli sh catalog_queries_starter.sh
rm wordpress/catalog_queries_starter.sh

# the checkpoint (at 2:20, from the instructor): under your own name, run, hand in
cp labs/module-13/checkpoint-2/checkpoint_starter.php wordpress/checkpoint_YOURNAME.php
wp eval-file --use-include checkpoint_YOURNAME.php
```

`event_list_starter.php` and the two `debug_*.php` handouts run like `open_today_starter.php`; `who_may_starter.sh`
like `catalog_queries_starter.sh`.

## Notes for the instructor

- **Hand out** `labs/module-13/` without the `*_solution.*` files and without the `checkpoint-2/` folder; at 2:20 hand
  out `checkpoint-2/checkpoint_starter.php` only. The model answer and the rubric are in the Answer Key.
- **The 6.4 labs are the server half.** `wp_interactivity_process_directives()` runs the same directive processor
  WordPress runs for a block with `"interactivity": true`; the browser half (a store with getters and actions in
  view.js) is Lesson 6.4's project. The Answer Key sketches the store a learner would add to `open_today`.
- **Credentials.** `who_may_*.sh` creates application passwords named "Who may lab" for devon, maria and admin and
  deletes them at the end; if a learner stops it halfway:
  `wp user application-password list maria --name="Who may lab" --field=uuid` and `wp user application-password delete`.
  No lab changes content; the checkpoint script changes nothing.
- **States.** The 7.1 labs list the Find a Book page (Lesson 6.4); on a site without it that line differs.
- **PHP 8.4:** every lab runs the same.
- **Checking the labs:** `python3 labs/check_labs.py module-13` (13 results, about two minutes). On your own
  project: `WP_LABS_COMPOSE=~/pagesco-dev python3 labs/check_labs.py module-13`.

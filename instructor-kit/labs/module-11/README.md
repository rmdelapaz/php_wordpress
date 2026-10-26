# Session 11 labs · Lessons 5.5 + 6.1

**Custom Tables, Shortcodes and Block Setup.** Every lab says in its header which site it needs (`// state:`):

- **`after:lesson_17`** (Lesson 5.5's labs): the site as Lesson 5.4 leaves it: pagesco-books with nine features,
  eleven books (IDs 30 to 40), the settings page; no events table yet.
- **`after:lesson_18`** (Lesson 6.1's labs, and `debug_events_report`): the finished Lesson 5.5 site: twelve
  features, the table `wp_pagesco_events` at version 2 with six events (IDs 1 to 6), the two shortcodes. No Node
  files in the plugin yet.

Copy the kit's `labs/` folder into your project folder (`~/pagesco-dev/labs/`, next to `compose.yaml`) and type every
command below in the project folder. `wp` is the shortcut from Lesson 1.2. Every lab removes itself again.

| Folder | File | What it practices | Time | Done when |
|---|---|---|---|---|
| `l5_5-custom-tables/` | `wishlist_table_starter.php` → `wishlist_table_solution.php` | **Guided lab.** A throwaway table's whole life: `dbDelta()`, `$wpdb->insert()` with formats, a JOIN through `prepare()` and `%i`, `update()`, `DROP TABLE` | 15 min | the output matches "Expected when done" and ends with `tables left: 0` |
| | `open_hours_starter/` → `open_hours_solution/` + `test_open_hours.sh` | A `[pagesco_open_hours day="..."]` shortcode (a must-use plugin): `shortcode_atts()`, return instead of echo, empty output for bad input | 10 min | the test prints each case with its HTML inside the quotes, `''` for "holiday" |
| | `debug_events_report.php` | An events report: a `prepare()` without placeholders, a column that was never selected, and a silent COUNT that should be a SUM | 10 min | no message; 20/15/40 seats, then Café 70 ... Front of the shop 0 |
| `l6_1-block-setup/` | `shelf_label_starter/` → `shelf_label_solution/` + `test_shelf_label.sh` | **Guided lab.** A small plugin with one prebuilt static block, `pagesco/shelf-label`: register the build from its manifest (TODO 1); with Node, add keywords and rebuild (TODO 2) | 15 min | the test prints `Shelf Label (text, icon tag)`, `keywords: shelf, sign` and `front end: 1 stylesheet(s)` |
| | `core_blocks_tour_starter.sh` → `core_blocks_tour_solution.sh` | WordPress's own blocks built the same way: 115 block.json files, core's manifest, apiVersion 3, the one bundle, the one block without block.json | 10 min | the output matches "Expected when done" |
| | `debug_block_registration.php` | Three block names registered in PHP: two refused ("called incorrectly"), one silently on an old apiVersion | 10 min | no message; all three `registered, apiVersion 3` |

## Commands

```bash
cd ~/pagesco-dev

# a PHP lab: copy it into the WordPress root, edit THAT copy, run it with WordPress loaded, delete it
cp labs/module-11/l5_5-custom-tables/wishlist_table_starter.php wordpress/
wp eval-file --use-include wishlist_table_starter.php
rm wordpress/wishlist_table_starter.php

# the must-use plugin lab
cp labs/module-11/l5_5-custom-tables/open_hours_starter/pagesco-lab-hours-shortcode.php wordpress/wp-content/mu-plugins/
cp labs/module-11/l5_5-custom-tables/test_open_hours.sh wordpress/
docker compose run --rm wpcli sh test_open_hours.sh
rm wordpress/test_open_hours.sh wordpress/wp-content/mu-plugins/pagesco-lab-hours-shortcode.php

# the block plugin lab (build/ is prebuilt: no Node needed for TODO 1)
cp -r labs/module-11/l6_1-block-setup/shelf_label_starter wordpress/wp-content/plugins/pagesco-shelf-label
wp plugin activate pagesco-shelf-label
cp labs/module-11/l6_1-block-setup/test_shelf_label.sh wordpress/
docker compose run --rm wpcli sh test_shelf_label.sh
wp plugin deactivate pagesco-shelf-label
rm -r wordpress/wp-content/plugins/pagesco-shelf-label wordpress/test_shelf_label.sh

# TODO 2 of shelf_label (Node 24 on your computer, in the plugin's folder)
cd wordpress/wp-content/plugins/pagesco-shelf-label && npm install && npm run build && cd ~/pagesco-dev
```

`core_blocks_tour_starter.sh` runs like any shell lab (`docker compose run --rm wpcli sh core_blocks_tour_starter.sh`);
the `debug_*` files run like `wishlist_table_starter.php`.

## Notes for the instructor

- **wishlist_table** creates and drops `wp_pagesco_lab_wishlist`. If a learner's run stops half-way (a typo after
  the CREATE), the table is left behind: `wp db query "DROP TABLE IF EXISTS wp_pagesco_lab_wishlist"`.
- **open_hours' starter ECHOES its list**: in the test the HTML appears before the quotes and `''` inside them,
  which is exactly the "shortcode that echoes" mistake of Lesson 5.5 seen from do_shortcode().
- **shelf_label ships `build/` prebuilt** (built for real with @wordpress/scripts 37 on Node 24 by the kit author's
  `kit_generators/S11/build_shelf_label.py`); the starter's build has no keywords, the solution's has. Without TODO 1
  the block is not registered, yet the test page still shows the saved HTML: it lives in the post. Only the block's
  stylesheet is missing. `npm install` in the lab plugin downloads about 540 MB; learners who did Lesson 6.1 can
  instead link pagesco-books' copy: `ln -s ../pagesco-books/node_modules node_modules` in the lab plugin's folder
  (remove the link with the plugin).
- **`debug_events_report.php` needs the events table** (`after:lesson_18`); its "undefined property" Warning prints
  once per event in the learner's terminal.
- **Network:** none of the checked labs needs it; shelf_label's TODO 2 does (npm install).
- **Checking the labs:** `python3 labs/check_labs.py module-11` (19 results in about two minutes). On your own
  project: `WP_LABS_COMPOSE=~/pagesco-dev python3 labs/check_labs.py module-11`.

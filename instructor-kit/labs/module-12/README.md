# Session 12 labs · Lessons 6.2 + 6.3

**Static and Dynamic Blocks.** Lesson 6.2's labs run on the site as Lesson 6.1 left it (`// state: after:lesson_19`:
the 6.1 Book Card, the plugin's build), Lesson 6.3's on the site after Lesson 6.2 (`after:lesson_20`: the finished
card, the staff pick). A learner who followed the lessons is there. Copy the kit's `labs/` folder into your project
folder (`~/pagesco-dev/labs/`, next to `compose.yaml`) and type every command below in the project folder. `wp` is
the shortcut from Lesson 1.2. No lab needs Node or a build: the block labs register their block from PHP.

| Folder | File | What it practices | Time | Done when |
|---|---|---|---|---|
| `l6_2-static-blocks/` | `attribute_sources_starter.php` → `attribute_sources_solution.php` | **Guided lab.** Where core/heading, core/quote and core/button keep each attribute (registry: source + selector, or the comment and its default), and what `parse_blocks()` sees of a stored heading and image | 15 min | the output matches "Expected when done" |
| | `card_price_starter/` → `card_price_solution/` + `test_card_price.sh` | A must-use plugin: `render_block_pagesco/book-card` reads a static card's link with `WP_HTML_Tag_Processor`, finds the book, adds today's price after the card | 15 min | the test prints `Today: $10.99` after The Hobbit and `price lines: 1` |
| | `debug_card_report.php` | A report of stored Book Cards: two Warnings (one with a Deprecated) and a silent wrong heading level | 10 min | both cards right, no message |
| `l6_3-dynamic-blocks/` | `next_events_starter/` → `next_events_solution/` + `test_next_events.php` | **Guided lab.** A plugin with a dynamic block `pagesco/next-events` (block.json + render.php, registered from PHP): an attribute without a default that falls back to a setting, a clamp, `EventsTable::find()`, `get_block_wrapper_attributes()`, escaping | 20 min | five events, two Café events, the empty sentence, `count 99: 6 events` |
| | `core_sources_starter.php` → `core_sources_solution.php` | What `core/post-meta` and `core/post-data` give a bound paragraph: raw values, empty strings, the fallback (rendered with `new WP_Block( $parsed, $context )`) | 10 min | the output matches "Expected when done" |
| | `debug_genre_counts.php` | A dynamic block (a `render_callback`) with two Warnings and a silent reversed clamp | 10 min | three and four genres, no message |

## Commands

```bash
cd ~/pagesco-dev

# a PHP lab: copy it into the WordPress root, edit THAT copy, run it with WordPress loaded, delete it
cp labs/module-12/l6_2-static-blocks/attribute_sources_starter.php wordpress/
wp eval-file --use-include attribute_sources_starter.php
rm wordpress/attribute_sources_starter.php

# the must-use plugin lab (6.2): install the file, run the test in the WP-CLI container, remove both
cp labs/module-12/l6_2-static-blocks/card_price_starter/pagesco-card-price.php wordpress/wp-content/mu-plugins/
cp labs/module-12/l6_2-static-blocks/test_card_price.sh wordpress/
docker compose run --rm wpcli sh test_card_price.sh
rm wordpress/test_card_price.sh wordpress/wp-content/mu-plugins/pagesco-card-price.php

# the plugin lab (6.3): copy the folder as a plugin, activate it, run the test, deactivate and remove it
cp -r labs/module-12/l6_3-dynamic-blocks/next_events_starter wordpress/wp-content/plugins/pagesco-next-events
wp plugin activate pagesco-next-events
cp labs/module-12/l6_3-dynamic-blocks/test_next_events.php wordpress/
wp eval-file --use-include test_next_events.php
wp plugin deactivate pagesco-next-events
rm -r wordpress/wp-content/plugins/pagesco-next-events wordpress/test_next_events.php
```

`core_sources_starter.php` and the two `debug_*.php` handouts run like `attribute_sources_starter.php`.
`--use-include` makes PHP's messages name your file (`/var/www/html/debug_card_report.php on line 28`, which is
`wordpress/debug_card_report.php`) instead of WP-CLI's `eval()'d code`.

## Notes for the instructor

- **Expected outputs** are in each starter's "Expected when done" comment (the solutions' real output) and, with
  explanations, in the Answer Key's "Lab Reference Solutions".
- **No build, no editor.** `pagesco/next-events` registers block.json from PHP and has no editor script, so it is not
  in the inserter; the test renders it with `do_blocks()`, which is exactly what a page view does with the comment.
  Making it insertable is Lesson 6.1's build (an `editorScript`), deliberately left out of a 20-minute lab.
- **Content.** `test_card_price.sh` creates a post "Card price lab" and force-deletes it again; no other lab changes
  content. The plugin and must-use plugin labs are removed with the commands above.
- **Learners whose site is behind.** The 6.3 labs need only the plugin's EventsTable and book meta (Lessons 5.2 and
  5.5) and work on any later state too; the 6.2 labs need the Book Card block registered (Lesson 6.1).
- **PHP 8.4:** every lab runs the same.
- **Checking the labs:** `python3 labs/check_labs.py module-12` (15 results, about two minutes). On your own project:
  `WP_LABS_COMPOSE=~/pagesco-dev python3 labs/check_labs.py module-12` (your site must be at the states above).

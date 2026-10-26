# Session 15 labs · Lessons 8.1 + 8.2

**Debugging, Testing and Performance.** The labs run on the course site as Lessons 7.3 and 8.1 leave it. Each file
says which in its header (`// state:` or `# state:`):

- `after:lesson_25` (the end of Lesson 7.3): pagesco-books with its twenty features, the supplier sandbox in the
  WordPress folder and its address and key in wp-config.php, the daily job.
- `after:lesson_26` (the end of Lesson 8.1's project): the same, plus the plugin's development packages
  (`composer update`: PHPUnit, PHPCS with the WordPress Coding Standards), `phpcs.xml.dist` and the tests folder.
  `test_next_event.sh` needs it: it runs PHPCS from the plugin's `vendor/` folder.

Copy the kit's `labs/` folder into your project folder (`~/pagesco-dev/labs/`, next to `compose.yaml`) and type every
command below in the project folder. `wp` is the shortcut from Lesson 1.2. Every lab removes itself again, and
`cheapest_cache` puts Dune's price back: nothing else changes on your site. No lab needs the internet.

| Folder | File | What it practices | Time | Done when |
|---|---|---|---|---|
| `l8_1-debugging-testing/` | `fake_supplier_starter.php` → `fake_supplier_solution.php` | **Guided lab.** The supplier client against four fake answers with `pre_http_request`, the idea of Lesson 8.1's SupplierClientTest without PHPUnit: exact error codes, the status in the error's data | 15 min | `4 of 4 checks passed, 4 requests answered by the fake, none by the network` |
| | `next_event_starter/` → `next_event_solution/` + `test_next_event.sh` | A must-use plugin brought to zero PHPCS findings with the plugin's own ruleset (`after:lesson_26`): file and function DocBlocks, escaping, the text domain, a translators comment | 15 min | `PHPCS: no findings` and the same footer line as before |
| | `debug_supplier_log.php` | A quick look at the supplier with an `http_api_debug` logger: two Warnings, and a silent bug in what it writes to the log | 10 min | three book lines without a message, and a log line without the whole key |
| `l8_2-performance-caching/` | `query_count_starter.php` → `query_count_solution.php` | **Guided lab.** What five everyday calls cost the database, first and second time (`$wpdb->num_queries`): autoloaded and missing options, meta, WP_Query, N+1 and `update_postmeta_cache()` | 15 min | the six rows of "Expected when done" |
| | `cheapest_cache_starter.php` → `cheapest_cache_solution.php` | A cached query of your own with the last-changed pattern: the key knows when the data changed | 15 min | `second call: 0 queries`, the price drop seen at once, Dune's price restored |
| | `page_weight_starter.sh` → `page_weight_solution.sh` | What four pages make the browser download (inline styles, stylesheets, modules, images) and the hero image's two problems, with curl and grep | 10 min | the table and the three hero lines (after Lesson 8.2's project: `yes`, `yes`) |
| | `debug_events_cache.php` | A cache in front of the events table: two Warnings and a key that forgets an argument | 10 min | one, three and five events, and their seats, without a message |

## Commands

```bash
cd ~/pagesco-dev

# a PHP lab: copy it into the WordPress root, edit THAT copy, run it with WordPress loaded, delete it
cp labs/module-15/l8_1-debugging-testing/fake_supplier_starter.php wordpress/
wp eval-file --use-include fake_supplier_starter.php
rm wordpress/fake_supplier_starter.php

# a shell lab: the same, run in the WP-CLI container
cp labs/module-15/l8_2-performance-caching/page_weight_starter.sh wordpress/
docker compose run --rm wpcli sh page_weight_starter.sh
rm wordpress/page_weight_starter.sh

# the folder lab (after Lesson 8.1's Step 2): the must-use plugin and its test, then remove both
cp labs/module-15/l8_1-debugging-testing/next_event_starter/pagesco-books-next-event.php wordpress/wp-content/mu-plugins/
cp labs/module-15/l8_1-debugging-testing/test_next_event.sh wordpress/
docker compose run --rm wpcli sh test_next_event.sh
rm wordpress/test_next_event.sh wordpress/wp-content/mu-plugins/pagesco-books-next-event.php
```

The other `.php` files (`debug_supplier_log.php`, `query_count_starter.php`, `cheapest_cache_starter.php`,
`debug_events_cache.php`) run like `fake_supplier_starter.php`. `--use-include` makes PHP's messages name your
file (`/var/www/html/debug_events_cache.php on line 36`, which is `wordpress/debug_events_cache.php`).

## Notes for the instructor

- **Expected outputs** are in each starter's "Expected when done" comment (the solutions' real output) and, with
  explanations, in the Answer Key's "Lab Reference Solutions".
- **Variables in lab scripts are local.** `wp eval-file --use-include` includes the file inside a function, so a
  variable at the top of a lab file is not a global: `fake_supplier` counts with a `static` variable in a function
  instead of `$GLOBALS` (a learner who tries `global $pagesco_x;` gets "Undefined global variable"). A good
  question for fast finishers: why does `global $wpdb;` still work?
- **PHPUnit and wp-env are not in these labs.** The lesson's tests run in a wp-env test environment that needs
  Node.js on the computer and a minute to start; its outputs in the lesson are recordings. `fake_supplier` practices
  the same `pre_http_request` idea on the course site, and the Facilitator Guide's 8.1 demo shows the recorded run.
- **Numbers move with the state.** `query_count` and `page_weight` count on the site as Lesson 8.1 leaves it.
  After Lesson 8.2's project (the empty settings row, the hero image's aspect ratio and preload) `page_weight`'s
  hero lines say `yes`, and the page sizes change by about a kilobyte: the commands, not the numbers, are the answer.
- **Dates.** `test_next_event.sh` and `debug_events_cache.php` read the events table, whose sample events are in
  November and December 2027 (Lesson 5.5). From 2028 the daily job deletes them as past events and both labs show
  other titles (or none): add a future event with `PagesCo\Books\EventsTable::add()` (Lesson 7.3's tip).
- **PHP 8.4:** every lab runs the same.
- **Checking the labs:** `python3 labs/check_labs.py module-15` (14 results in about two minutes). On your own
  project: `WP_LABS_COMPOSE=~/pagesco-dev python3 labs/check_labs.py module-15` (your site must be at the state each
  file declares).

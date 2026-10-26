# Session 9 labs · Lessons 5.1 + 5.2

**Your First Plugin and Custom Post Types.** Session 9 opens Part 2. Every lab says in its header which site it
needs (`// state:`):

- **`after:lesson_13`** (Lesson 5.1's labs): the Part 2 starting site, as Lesson 4.3 leaves it: the `pagesco`
  block theme active, `pagesco-classic` installed, `mu-plugins/pagesco-site.php` 1.0.0 with the store notice and its
  three hooks, the users maria (editor) and devon (author), the pages About Us, Contact and Events. No plugin active.
- **`after:lesson_14`**: the same site with `pagesco-books` active (Lesson 5.1's skeleton and its StoreNotice feature).
- **`after:lesson_15`**: the finished Lesson 5.2 site: the `book` type, the `genre` taxonomy, the six book meta keys,
  eleven books (IDs 30 to 40) in five genres. Only `shelf_report` needs it: it is homework after the project.

Copy the kit's `labs/` folder into your project folder (`~/pagesco-dev/labs/`, next to `compose.yaml`) and type every
command below in the project folder. `wp` is the shortcut from Lesson 1.2. Every lab removes itself again.
The Part 2 environment check is Session 1's script with `--part2` (nothing to copy):
`bash labs/module-01/l1_0-orientation/check_environment.sh --part2`.

| Folder | File | What it practices | Time | Done when |
|---|---|---|---|---|
| `l5_1-first-plugin/` | `gift_wrap_starter/` → `gift_wrap_solution/` + `test_gift_wrap.sh` | **Guided lab.** A one-file plugin with the whole life cycle: the requirement headers, the ABSPATH guard, an activation hook that stores an option, a filter on the store notice, and `uninstall.php` | 15 min | the test prints `requires WordPress 6.8, PHP 8.2`, `direct request: 200`, the notice with `Gift wrapping: $2.50.` and `after uninstall: (not stored)` |
| | `psr4_paths_starter.php` → `psr4_paths_solution.php` | The PSR-4 rule written by hand: class name in, file name out, and why case matters | 10 min | the output matches "Expected when done" |
| | `debug_plugin_audit.php` | A plugin audit (`get_plugins()`, `Requires PHP`): two Warnings and a silent wrong answer about which plugins run here | 10 min | no message, both plugins `runs here`, `2 plugin(s) installed, 2 inactive` |
| `l5_2-custom-post-types/` | `book_quotes_starter/` → `book_quotes_solution/` + `test_book_quotes.sh` | **Guided lab.** A second post type (`pagesco_quote`) with an archive, REST, a public meta key and an activator that registers before it flushes | 15 min | the test prints `archive /quotes/: 200` and the quote with `"pagesco_quote_source":"Pride and Prejudice"` |
| | `shelf_report_starter.php` → `shelf_report_solution.php` | Questions about the catalog: term counts, a `meta_query` with `meta_value_num`, an average, a `DATE` comparison (homework, after the project) | 15 min | the output matches "Expected when done" |
| | `debug_meeting_type.php` | A post type, a taxonomy and an array meta key registered with three bugs (two "called incorrectly" notices, a Warning, a silent typo) | 10 min | no message; `taxonomies on meetings: pagesco_room` |

## Commands

```bash
cd ~/pagesco-dev

# the Part 2 environment check (on your computer, in the project folder)
bash labs/module-01/l1_0-orientation/check_environment.sh --part2

# a folder lab: install the plugin, activate it, run its test, remove both
cp -r labs/module-09/l5_1-first-plugin/gift_wrap_starter wordpress/wp-content/plugins/pagesco-gift-wrap
wp plugin activate pagesco-gift-wrap
cp labs/module-09/l5_1-first-plugin/test_gift_wrap.sh wordpress/
docker compose run --rm wpcli sh test_gift_wrap.sh
rm -r wordpress/wp-content/plugins/pagesco-gift-wrap wordpress/test_gift_wrap.sh   # the test already uninstalled it

cp -r labs/module-09/l5_2-custom-post-types/book_quotes_starter wordpress/wp-content/plugins/pagesco-quotes
wp plugin activate pagesco-quotes
cp labs/module-09/l5_2-custom-post-types/test_book_quotes.sh wordpress/
docker compose run --rm wpcli sh test_book_quotes.sh
wp plugin deactivate pagesco-quotes
rm -r wordpress/wp-content/plugins/pagesco-quotes wordpress/test_book_quotes.sh

# a PHP lab: copy it into the WordPress root, edit THAT copy, run it with WordPress loaded, delete it
cp labs/module-09/l5_1-first-plugin/psr4_paths_starter.php wordpress/
wp eval-file --use-include psr4_paths_starter.php
rm wordpress/psr4_paths_starter.php
```

`debug_plugin_audit.php`, `debug_meeting_type.php` and `shelf_report_starter.php` run like `psr4_paths_starter.php`.

**Trying the solution folder after the starter:** deactivate and delete the starter's copy first
(`wp plugin deactivate pagesco-quotes && rm -r wordpress/wp-content/plugins/pagesco-quotes`), then copy the
solution folder to the same place and activate it: the activation hook runs only on activation.

## Notes for the instructor

- **Expected outputs** are in each starter's "Expected when done" comment (the solutions' real output) and, with
  explanations, in the Answer Key's "Lab Reference Solutions".
- **gift_wrap and the direct request.** The starter has no ABSPATH guard, so `curl` of its main file runs it without
  WordPress and dies on `add_filter()`: a 500 (the Fatal error goes to the web server's log, `docker compose logs
  wordpress`, not to debug.log, because WordPress never loaded). With the guard the request ends quietly with 200.
- **gift_wrap's test ends with `wp plugin uninstall pagesco-gift-wrap --deactivate --skip-delete`**, so the option is
  gone and the plugin is inactive afterwards; only the files are left to delete.
- **book_quotes' starter registers the type** (not public, no REST) but its activator flushes nothing: the archive is
  a 404 and REST has no route. With the solution, deactivating unregisters the type and flushes again, so
  `/quotes/` stops answering; the test deletes the quote it creates.
- **`debug_meeting_type.php` registers for one run only** (nothing is stored), on `after:lesson_14`; its first bug
  (a 24-character post type name) also causes the Warning that follows it.
- **Network:** none of these labs needs the network. The Part 2 check pulls `composer:2` and `node:24` if they are
  missing (about 0.5 GB): run it at home first.
- **Checking the labs:** `python3 labs/check_labs.py module-09` (16 results in about a minute and a half).
  On your own project: `WP_LABS_COMPOSE=~/pagesco-dev python3 labs/check_labs.py module-09`; your site must be at the
  state each file declares (the 5.1 labs before you start Lesson 5.1, the others after the lesson named).

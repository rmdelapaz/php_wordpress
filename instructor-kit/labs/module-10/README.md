# Session 10 labs · Lessons 5.3 + 5.4

**Security and the Settings API.** Every lab says in its header which site it needs (`// state:`):

- **`after:lesson_15`** (Lesson 5.3's labs): the site as Lesson 5.2 leaves it: pagesco-books with six features
  (StoreNotice, BookPostType, GenreTaxonomy, BookMeta, Admin\BookMetaBox, Admin\BookColumns), eleven books (IDs 30
  to 40; Dune is 30, by Frank Herbert, in stock), the users maria (2, editor) and devon (3, author).
- **`after:lesson_16`** (Lesson 5.4's starting site): the same plus the hardened meta box and Admin\StockAction.
- **`after:lesson_17`**: the finished Lesson 5.4 site: Settings and Admin\SettingsPage, the option
  `pagesco_books_settings` registered (no row: the defaults apply). Only `settings_probe` needs it: it is homework
  after the project.

Copy the kit's `labs/` folder into your project folder (`~/pagesco-dev/labs/`, next to `compose.yaml`) and type every
command below in the project folder. `wp` is the shortcut from Lesson 1.2. Every lab removes itself again.

| Folder | File | What it practices | Time | Done when |
|---|---|---|---|---|
| `l5_3-security/` | `staff_note_starter.php` → `staff_note_solution.php` | **Guided lab.** A save handler for a staff note, attacked by four requests (no token, a forged token, the wrong user, a script tag): add the nonce, the capability check and the sanitizing | 15 min | the output matches "Expected when done": three refusals and one clean save |
| | `prepared_search_starter.php` → `prepared_search_solution.php` | `$wpdb->prepare()` with `%f` and `%s`, `esc_like()` for LIKE, and a hostile value that stays a string | 10 min | the output matches "Expected when done" |
| | `debug_book_search.php` | A price report with two misused `prepare()` calls ("called incorrectly") and a silent wrong sanitizer | 10 min | no message; `Under $9.99: 5 book(s)`, `Cheapest: $7.99` |
| `l5_4-settings-api/` | `newsletter_settings_starter/` → `newsletter_settings_solution/` + `test_newsletter_settings.sh` | **Guided lab.** A Settings > Newsletter screen with the Settings API (a must-use plugin): the sanitize callback, two more fields, a value refused with `add_settings_error()`; the test saves the form the way a browser does | 15 min | the test prints `rows: 3`, `Frequency must be weekly or monthly.` and the cleaned option |
| | `settings_probe_starter.php` → `settings_probe_solution.php` | What WordPress knows about `pagesco_books_settings`: its registration, `sanitize_option()` and its errors, the two filters register_setting() adds (homework, after the project) | 10 min | the output matches "Expected when done" |
| | `debug_newsletter_sanitize.php` | A setting and its sanitize callback with three bugs ("called incorrectly", a Warning, a silent one) | 10 min | no message; the tags are gone and `daily` became `monthly` |

## Commands

```bash
cd ~/pagesco-dev

# a PHP lab: copy it into the WordPress root, edit THAT copy, run it with WordPress loaded, delete it
cp labs/module-10/l5_3-security/staff_note_starter.php wordpress/
wp eval-file --use-include staff_note_starter.php
rm wordpress/staff_note_starter.php

# the folder lab: install the must-use plugin, run its test, remove both
cp labs/module-10/l5_4-settings-api/newsletter_settings_starter/pagesco-lab-newsletter.php wordpress/wp-content/mu-plugins/
cp labs/module-10/l5_4-settings-api/test_newsletter_settings.sh wordpress/
docker compose run --rm wpcli sh test_newsletter_settings.sh
rm wordpress/test_newsletter_settings.sh wordpress/wp-content/mu-plugins/pagesco-lab-newsletter.php
```

`prepared_search_starter.php`, `settings_probe_starter.php` and the two `debug_*` files run like
`staff_note_starter.php`. Open http://localhost:8080/wp-admin/options-general.php?page=pagesco-lab-newsletter in
your browser while the must-use plugin is installed to see the screen the test saves.

## Notes for the instructor

- **Expected outputs** are in each starter's "Expected when done" comment (the solutions' real output) and, with
  explanations, in the Answer Key's "Lab Reference Solutions".
- **staff_note** plays the four requests with `wp_set_current_user()` and `wp_create_nonce()`: a nonce made in the
  same WP-CLI run verifies, exactly as the browser's would on the next request. It deletes the note it saves.
- **prepared_search** prints SQL with `$wpdb->remove_placeholder_escape()`: `prepare()` hides every literal `%`
  behind a long random string until the query runs, so the raw prepared string would differ on every run.
- **The newsletter test** logs in as admin and maria with curl (cookie jars in the container's `/tmp`, deleted
  again), posts the form to options.php like Lesson 5.4's `pagesco-save.sh`, and deletes the option it saved
  (`wp option delete pagesco_lab_newsletter`), so the site is as it was.
- **`debug_book_search.php`'s last bug has a nasty side effect:** a `prepare()` with too few arguments returns
  nothing, and `$wpdb->get_var( null )` hands back a value of the PREVIOUS query. Say so before learners trust the
  "Cheapest" line.
- **Checking the labs:** `python3 labs/check_labs.py module-10` (12 results in about a minute). On your own project:
  `WP_LABS_COMPOSE=~/pagesco-dev python3 labs/check_labs.py module-10`; your site must be at the state each file
  declares.

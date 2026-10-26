# Session 14 labs · Lessons 7.2 + 7.3

**Custom Endpoints, External APIs and Cron.** Lesson 7.2's labs run on the site as Lesson 7.1 left it
(`// state: after:lesson_23`), Lesson 7.3's on the site after Lesson 7.2 (`after:lesson_24`: the pagesco/v1 routes).
A learner who followed the lessons is there. Copy the kit's `labs/` folder into your project folder
(`~/pagesco-dev/labs/`, next to `compose.yaml`) and type every command below in the project folder. `wp` is the
shortcut from Lesson 1.2. No lab needs the internet: the 7.3 labs call the site's own REST API over HTTP, as if it
were another company's service, and `.invalid`, a domain that never exists.

| Folder | File | What it practices | Time | Done when |
|---|---|---|---|---|
| `l7_2-custom-endpoints/` | `opening_hours_starter/` → `opening_hours_solution/` + `test_opening_hours.sh` | **Guided lab.** A plugin with `GET /pagesco/v1/opening-hours`: `register_rest_route()` on rest_api_init, an argument with a type and an enum and no default, a prepared response | 20 min | Saturday's hours, Sunday closed, a 400 for funday, seven days, the argument in OPTIONS |
| | `schema_rules_starter.php` → `schema_rules_solution.php` | What `rest_validate_value_from_schema()` accepts and `rest_sanitize_value_from_schema()` turns a query string into: types, ranges, enums, lists, lengths, dates | 10 min | the output matches "Expected when done" |
| | `debug_staff_picks_route.php` | A route called with `rest_do_request()`: a "called incorrectly" Notice, a Warning, and a silent maximum that is not enforced | 10 min | 200, 200, then 400 for limit=50, no message |
| `l7_3-external-apis-cron/` | `remote_answers_starter.php` → `remote_answers_solution.php` | **Guided lab.** One careful client (`wp_remote_get()` with a timeout) and its three failure checks, on five answers: data, 400, 404, HTML, no host | 20 min | the output matches "Expected when done" |
| | `events_cache_starter.php` → `events_cache_solution.php` | A read-through transient (10 minutes; a failure for 1 minute; never false), counting the requests that really go out | 15 min | one request for three views, two after a simulated failure, 0 rows left |
| | `cron_plan_starter.sh` → `cron_plan_solution.sh` | WP-Cron from WP-CLI: a guarded recurring event at 04:30 site time, a one-time event with an argument, both cleared | 10 min | the output matches "Expected when done" |
| | `debug_event_counts.php` | Cached event counts per location: two kinds of Warning and a silent cache that never hits for 0 | 10 min | Café 2 (asked once), Rooftop 0 (asked once), no message |

## Commands

```bash
cd ~/pagesco-dev

# the plugin lab (7.2): copy the folder as a plugin, activate it, run the test, deactivate and remove it
cp -r labs/module-14/l7_2-custom-endpoints/opening_hours_starter wordpress/wp-content/plugins/pagesco-opening-hours
wp plugin activate pagesco-opening-hours
cp labs/module-14/l7_2-custom-endpoints/test_opening_hours.sh wordpress/
docker compose run --rm wpcli sh test_opening_hours.sh
wp plugin deactivate pagesco-opening-hours
rm -r wordpress/wp-content/plugins/pagesco-opening-hours wordpress/test_opening_hours.sh

# a PHP lab: copy it into the WordPress root, edit THAT copy, run it with WordPress loaded, delete it
cp labs/module-14/l7_3-external-apis-cron/remote_answers_starter.php wordpress/
wp eval-file --use-include remote_answers_starter.php
rm wordpress/remote_answers_starter.php

# the shell lab: the same, run in the WP-CLI container
cp labs/module-14/l7_3-external-apis-cron/cron_plan_starter.sh wordpress/
docker compose run --rm wpcli sh cron_plan_starter.sh
rm wordpress/cron_plan_starter.sh
```

`schema_rules_starter.php`, `events_cache_starter.php` and the two `debug_*.php` handouts run like
`remote_answers_starter.php`.

## Notes for the instructor

- **Expected outputs** are in each starter's "Expected when done" comment (the solutions' real output) and, with
  explanations, in the Answer Key's "Lab Reference Solutions".
- **The site calls itself.** `wp_remote_get( rest_url( ... ) )` from WP-CLI reaches the site through
  http://localhost:8080 inside the containers (Lesson 1.2's port setup); `wp cron test` says whether that works.
- **Leaves nothing behind.** `events_cache` and `debug_event_counts` delete their transients (the solution proves it:
  `rows left: 0`); `cron_plan` clears its events (if a learner stops it halfway:
  `wp cron event delete pagesco_books_lab_job`). The opening-hours plugin is removed with the commands above.
- **2028 and later.** Lesson 7.3's daily job deletes events that are over; the sample events are in Nov–Dec 2027.
  On a learner's site after that date the event counts in `events_cache` and `debug_event_counts` are smaller (the
  lesson's own tip card says how to add future events). The runner's states keep the 2027 events.
- **PHP 8.4:** every lab runs the same.
- **Checking the labs:** `python3 labs/check_labs.py module-14` (15 results, about two minutes). On your own
  project: `WP_LABS_COMPOSE=~/pagesco-dev python3 labs/check_labs.py module-14`.

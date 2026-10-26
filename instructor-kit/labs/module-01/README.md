# Session 1 labs · Lessons 1.1 + 1.2

**WordPress for Developers and Your Local Environment.** All files run on the course site of Lesson 1.2 as it is
right after setup (`// state: fresh`): WordPress 7.1.3, PHP 8.5, MySQL 9.7, WP-CLI 2.12, Mailpit, Twenty
Twenty-Five active, `mailpit-smtp.php` in `wp-content/mu-plugins/`. Copy the kit's `labs/` folder into your project
folder (`~/pagesco-dev/labs/`, next to `compose.yaml`) and type every command below in the project folder.
`wp` is the shortcut from Lesson 1.2. Every lab removes itself again: the last command of each is an `rm`.

| Folder | File | What it practices | Time | Done when |
|---|---|---|---|---|
| `l1_0-orientation/` | `check_environment.sh` | Is this computer ready? Docker, Compose, the project, WordPress 7.1, PHP 8.5, WP-CLI, permalinks, debugging, Mailpit, the ports. Run it on YOUR computer (not in a container) | 2 min | the last line says `READY for PHP and WordPress Development` (or `READY WITH NOTES`) |
| | `diagnostic_starter.php` → `diagnostic_solution.php` | The Start Here questions D1, D2 and D6 answered by PHP, one small gap each (practice at home) | 10 min | `D1 PHP says: 3 Dune`, the escaped name, `DUNE! EMMA!` |
| `l1_1-wordpress-for-developers/` | `core_tour_starter.sh` → `core_tour_solution.sh` | **Guided lab.** Find the lines of core that do each step of a request (grep -n) | 15 min | the output matches "Expected when done" |
| | `wp_paths_starter.php` → `wp_paths_solution.php` | Where code lives, as WordPress reports it (constants, `get_stylesheet()`, `get_plugins()`) | 10 min | eight lines without TODO |
| | `debug_old_tutorial.php` | An old tutorial: three deprecated calls, each message names its replacement | 10 min | no message left |
| `l1_2-local-environment/` | `site_report_starter.sh` → `site_report_solution.sh` | **Guided lab.** A one-screen site report, one `wp` command per line | 15 min | the output matches "Expected when done" |
| | `store_hours_starter/` → `store_hours_solution/` + `test_store_hours.sh` | A must-use plugin like the lesson's debug demo: Saturday's hours in the footer (escaped) and one line in debug.log | 15 min | the test prints `Open Saturday: 10:00-16:00` and the log line |
| | `debug_health_check.php` | A health check with two loud bugs (Warnings) and a silent one | 10 min | all five checks OK, `All checks passed.` |

## Commands

```bash
cd ~/pagesco-dev

# the environment check (on your computer, in the project folder)
bash labs/module-01/l1_0-orientation/check_environment.sh

# a PHP lab: copy it into the WordPress root, edit THAT copy, run it with WordPress loaded, delete it
cp labs/module-01/l1_1-wordpress-for-developers/wp_paths_starter.php wordpress/
wp eval-file --use-include wp_paths_starter.php
rm wordpress/wp_paths_starter.php

# a shell lab: the same, run in the WP-CLI container
cp labs/module-01/l1_1-wordpress-for-developers/core_tour_starter.sh wordpress/
docker compose run --rm wpcli sh core_tour_starter.sh
rm wordpress/core_tour_starter.sh

# the folder lab: install the must-use plugin, run its test, remove both
cp labs/module-01/l1_2-local-environment/store_hours_starter/pagesco-hours.php wordpress/wp-content/mu-plugins/
cp labs/module-01/l1_2-local-environment/test_store_hours.sh wordpress/
docker compose run --rm wpcli sh test_store_hours.sh
rm wordpress/test_store_hours.sh wordpress/wp-content/mu-plugins/pagesco-hours.php
```

`diagnostic_starter.php`, `debug_old_tutorial.php` and `debug_health_check.php` run like `wp_paths_starter.php`;
`site_report_starter.sh` like `core_tour_starter.sh`. `--use-include` makes PHP's messages name your file
(`/var/www/html/debug_health_check.php on line 28`, which is `wordpress/debug_health_check.php`) instead of WP-CLI's
`eval()'d code`.

## Notes for the instructor

- **Expected outputs** are in each starter's "Expected when done" comment (the solutions' real output) and, with
  explanations, in the Answer Key's "Lab Reference Solutions". Line numbers in `core_tour` are WordPress 7.1.3's:
  a later 7.1.x may move them by a few lines; the grep, not the number, is the skill.
- **`check_environment.sh`** needs bash and the Docker CLI on the learner's computer (Linux, macOS, WSL; on Windows
  run it in the Ubuntu terminal, where the project lives). It changes nothing on the site except sending one test
  email, which Mailpit catches. `--part2` (Session 9) adds Node 24, the `composer:2` image and the Part 2 starting
  site (pagesco active, as Lesson 4.3 leaves it).
- **The store-hours plugin** writes one line to `wordpress/wp-content/debug.log` per page view until it is removed.
  The test counts the plugin's log lines; a learner who reloads the site in the browser sees a higher count, which
  is fine (each view is one line).
- **PHP 8.4:** every lab runs the same; only the PHP version lines differ (`check_environment.sh` says CHECK and
  `READY WITH NOTES`).
- **Checking the labs:** `python3 labs/check_labs.py module-01` (15 results in about two minutes; the environment check builds a
  throwaway copy of the course project, about a minute). On your own project: `WP_LABS_COMPOSE=~/pagesco-dev
  python3 labs/check_labs.py module-01`.

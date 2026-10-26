# Session 16 labs · Lessons 8.3 + 8.4

**Distribution and Deployment.** The labs run on the course site as Lessons 8.2 and 8.3 leave it. Each file says
which in its header (`// state:` or `# state:`):

- `after:lesson_27` (the end of Lesson 8.2): pagesco-books 1.0.0 with the events cache and the settings row, the
  hero image with its aspect ratio and preload. Lesson 8.3's labs start here, like the lesson.
- `after:lesson_28` (the end of Lesson 8.3's project): pagesco-books 1.1.0 with `readme.txt`, `languages/` and
  the release ZIP `pagesco-books.zip` in the plugin's folder, the navigation as four links, Spanish installed.
  `release_check` and every Lesson 8.4 lab need it, like the lesson.

Copy the kit's `labs/` folder into your project folder (`~/pagesco-dev/labs/`, next to `compose.yaml`) and type every
command below in the project folder. `wp` is the shortcut from Lesson 1.2. Every lab removes itself and the files it
writes to the container's `/tmp`; `restore_drill` deletes its marker post again (the post's ID stays used). Nothing
else changes on your site, and no lab needs the internet. The rehearsal server of Lesson 8.4 (`pagesco-live`) is not
used here: every lab runs on your development site.

| Folder | File | What it practices | Time | Done when |
|---|---|---|---|---|
| `l8_3-i18n-a11y-distribution/` | `plural_strings_starter.php` → `plural_strings_solution.php` | **Guided lab.** Four strings rewritten until a translator's file can translate them: `_n()`, numbered placeholders, `_x()`, a whole sentence; English and Spanish side by side | 15 min | every `es` line is Spanish |
| | `a11y_scan_starter.sh` → `a11y_scan_solution.sh` | Seven markup checks an audit makes, with curl and grep, on four pages (language, main landmark, one h1, alt attributes, skip link, the notice landmark, the nested list) | 10 min | the four rows of "Expected when done" (after Lesson 8.3's project, two columns change) |
| | `release_check_starter.sh` → `release_check_solution.sh` | Before shipping: the four version numbers, both "Requires at least", the POT, and what the ZIP contains and must not (`after:lesson_28`) | 15 min | `release check: 0 problems` |
| | `debug_seats_spanish.php` | Events and seats in Spanish: two Warnings, events that all look "open to all", and a silent line that stays English | 10 min | three Spanish event lines and a Spanish total |
| `l8_4-deployment-maintenance/` | `migration_preview_starter.sh` → `migration_preview_solution.sh` | **Guided lab.** A move to a staging address, previewed: registered tables and all tables, a dry run, two exports to `/tmp` compared, serialized options | 15 min | `export with --all-tables-with-prefix: 13 tables`, and the database unchanged |
| | `restore_drill_starter.sh` → `restore_drill_solution.sh` | A backup proven by a restore: a marker post, a dump outside the web root, the accident, the restore, the clean-up (`set -e`) | 10 min | `after the restore: 1 "Restore drill" post` |
| | `cron_audit_starter.php` → `cron_audit_solution.php` | What a server's scheduler takes over from WP-Cron: events by schedule, the shop's job, the crontab line | 10 min | the crontab line with your site's folder |
| | `debug_launch_check.sh` | A pre-launch report with two WP-CLI errors and a table count that looks right and is not | 10 min | the address, the supplier's address and 13 tables, without an `Error:` |

## Commands

```bash
cd ~/pagesco-dev

# a PHP lab: copy it into the WordPress root, edit THAT copy, run it with WordPress loaded, delete it
cp labs/module-16/l8_3-i18n-a11y-distribution/plural_strings_starter.php wordpress/
wp eval-file --use-include plural_strings_starter.php
rm wordpress/plural_strings_starter.php

# a shell lab: the same, run in the WP-CLI container
cp labs/module-16/l8_4-deployment-maintenance/migration_preview_starter.sh wordpress/
docker compose run --rm wpcli sh migration_preview_starter.sh
rm wordpress/migration_preview_starter.sh
```

`debug_seats_spanish.php` and `cron_audit_starter.php` run like `plural_strings_starter.php`; every `.sh` file like
`migration_preview_starter.sh`.

## Notes for the instructor

- **Expected outputs** are in each starter's "Expected when done" comment (the solutions' real output) and, with
  explanations, in the Answer Key's "Lab Reference Solutions".
- **Translations without a language pack.** `plural_strings` and `debug_seats_spanish` write a small `.l10n.php`
  file (the format `wp i18n make-php` builds, WordPress 6.5+) into the container's `/tmp` and load it with
  `load_textdomain()` for their own text domain, `pagesco-lab`: the site's language and the plugin's `languages/`
  stay as they are, and the labs work before Lesson 8.3's `wp language core install es_ES`.
- **Git is not in these labs.** The WP-CLI container has no `git` (Lesson 8.4 runs Git on the computer, the
  runner in the node:24 container), so the repository, the tags and the release builds are the lesson's project,
  done on the learner's own computer. The labs practice what runs on any WordPress server: WP-CLI, `wp db`, cron.
- **The rehearsal server is recorded in the lesson.** Lesson 8.4's Steps 3 to 7 on `pagesco-live` show output
  recorded on the course's machine; the Facilitator Guide quotes those cards. The kit's labs do not start a second
  WordPress.
- **Numbers move with the state.** `migration_preview` counts on the site as Lesson 8.3 leaves it (9 replacements,
  34 GUIDs); edits in the editor add revisions, and with them a few replacements. `cron_audit` counts the events
  WordPress and the plugin scheduled; a site with more plugins has more.
- **PHP 8.4:** every lab runs the same.
- **Checking the labs:** `python3 labs/check_labs.py module-16` (14 results in about two minutes). On your own
  project: `WP_LABS_COMPOSE=~/pagesco-dev python3 labs/check_labs.py module-16` (your site must be at the state each
  file declares).

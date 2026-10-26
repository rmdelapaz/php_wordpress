# Session 8 labs · Part 1 Project and Assessment (no new lesson)

**Part 1 Project and Assessment.** Every file runs on the course site as Lesson 4.3 leaves it
(`// state: after:lesson_13`): WordPress 7.1.3, PHP 8.5, pagesco active, pagesco-classic and pagesco-tt5-child
installed, four published posts (three in News), the pages About Us, Contact and Events. Type every command below
in your project folder (`~/pagesco-dev`); `wp` is the shortcut from Lesson 1.2.

| Folder | File | What it is | Time | Done when |
|---|---|---|---|---|
| `p1-project/` | `BRIEF.md` | **The Part 1 project** (handed out in Session 7): a block theme for the Fernhill Community Garden, requirements R1 to R8, milestones, hand-in, rubric | about 3 h 45 min (Session 7, home, Session 8 studio, home) | handed in one week after Session 8 |
| | `fernhill_starter/` → `fernhill_solution/` + `test_fernhill.php` | The starter theme (activates cleanly; the self-check says `Checks passed: 1 of 12`), the model solution (instructor only) and the self-check, 12 OK/TODO lines | | `Checks passed: 12 of 12`, the per-URL check, NOTES.md |
| | `fernhill_front.png` | The model solution's front page on the course site: what done looks like | | |
| `p1-assessment/` | `BRIEF.md` | **The Part 1 assessment** (Session 8, 60 minutes, alone, open book): finish the Brightwater Swim School classic theme, tasks T1 to T5 | 60 min | handed in at the end of the hour |
| | `brightwater_starter/` → `brightwater_solution/` + `test_brightwater.php` | The half-finished classic theme (`Checks passed: 2 of 10`), the model solution (instructor only), the self-check | | `Checks passed: 10 of 10` |
| `p1-review/` | `request_map_starter.sh` → `request_map_solution.sh` | What WordPress thinks each address is: the status and the request-type body classes of seven addresses (Lessons 3.1 and 4.1) | 10 min | the output matches "Expected when done" |
| | `debug_query_review.php` | A "latest news" list with one loud bug and three silent ones (Lesson 4.2); a warm-up for the assessment's Task 5 | 10 min | the two newest News posts, `News posts in all: 3`, `About Us` again at the end |

## Commands

```bash
cd ~/pagesco-dev

# the project (Session 7 onward): install the starter as YOUR theme, run the self-check
cp -r labs/module-08/p1-project/fernhill_starter wordpress/wp-content/themes/fernhill
wp theme activate fernhill
cp labs/module-08/p1-project/test_fernhill.php wordpress/
wp eval-file --use-include test_fernhill.php
wp theme activate pagesco                          # whenever you stop for the day (Session 9 starts from pagesco)

# the assessment (Session 8, when your instructor says so)
cp -r labs/module-08/p1-assessment/brightwater_starter wordpress/wp-content/themes/brightwater
wp theme activate brightwater
cp labs/module-08/p1-assessment/test_brightwater.php wordpress/
wp eval-file --use-include test_brightwater.php
rm wordpress/test_brightwater.php && wp theme activate pagesco      # after the hand-in

# the review lab and handout
cp labs/module-08/p1-review/request_map_starter.sh wordpress/
docker compose run --rm wpcli sh request_map_starter.sh
rm wordpress/request_map_starter.sh
cp labs/module-08/p1-review/debug_query_review.php wordpress/
wp eval-file --use-include debug_query_review.php
rm wordpress/debug_query_review.php
```

## Notes for the instructor

- **Never hand out** `fernhill_solution/` or `brightwater_solution/` before the feedback. If you can, release the
  `p1-assessment/` folder only at 1:25 in Session 8 (a USB stick or a shared folder).
- **The two themes stay on the learner's site** (`wp-content/themes/fernhill/`, `brightwater/`): they are the
  learner's work and do nothing while inactive. What a theme switch leaves in the database is harmless
  (`theme_mods_fernhill`, `theme_mods_brightwater`, `theme_switched`); `wp theme activate pagesco` is all Lesson 5.1
  needs. The checker removes both folders after its runs; on your own project (`WP_LABS_COMPOSE`) it also restores
  your database.
- **test_brightwater.php** puts the site's "Main menu" into the theme's `primary` location for its own requests and
  puts the old locations back before it prints. The self-checks request pages from inside the WP-CLI container
  (`wp_remote_get( home_url() )`, http://localhost:8080), so they work on any learner's machine.
- **request_map** prints pagesco's statuses (`/page/2/` is a 404 there: ten posts per page). With fernhill active
  page 2 exists (three per page); the body classes are the same with every theme.
- Rubrics, scoring guidance, scoring sheets and the answer notes with the real outputs of every common mistake:
  `final-assessment.html` at the kit root (Part 1 Project, Part 1 Assessment).
- Checked with `python3 labs/check_labs.py module-08`: each self-check runs once with the starter folder and once
  with the solution folder on a fresh after:lesson_13 site.

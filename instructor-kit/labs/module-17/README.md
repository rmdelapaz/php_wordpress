# Session 17 labs · Lesson 9.1 (Milestones 1 to 4)

**Final Project Kickoff and Studio I.** Session 17 starts the final project, Lesson 9.1's Reserve & Pick Up. The
project itself is the main work of the room and of the week; these labs are SHORT practice on the habits the first
four milestones need, for the guided lab and for learners who are stuck on a milestone. They are new practice,
not the project: wish lists, event seats and book requests instead of holds.

All files run on the course site as **Lesson 8.4's project left it** (`// state: after:lesson_29`): pagesco-books
1.1.1 and the pagesco theme 1.1.1, releases release-1 and release-2 in the wp-content Git repository, maria
(editor) and devon (author), the eleven books and the seven events. A learner who has already done Milestone 3
(jordan and priya, a holds table) can run them too: nothing here depends on the holds. Copy the kit's `labs/`
folder into your project folder (`~/pagesco-dev/labs/`, next to `compose.yaml`) and type every command below in
the project folder; `wp` is the shortcut from Lesson 1.2.

| Folder | File | What it practices | Time | Done when |
|---|---|---|---|---|
| `l9_1-final-project/` | `ownership_sql_starter.php` → `ownership_sql_solution.php` | **Guided lab.** Ownership in the query (`$wpdb->update()` with the owner in the WHERE), the user from the login, one 404 for anyone else's row (Milestones 2 and 4; a TEMPORARY table, gone when the script ends) | 15 min | Devon's and the visitor's attempts are `pagesco_wish_not_found (404)`, Maria's wish 1 is closed |
| | `rsvp_rules_starter.php` → `rsvp_rules_solution.php` | One rules function for every door: WP_Error with 401, 404 and 409 in its data, a duplicate and a limit rule, a status computed from the date (Milestone 3) | 15 min | the output matches "Expected when done" |
| | `own_action_starter/` → `own_action_solution/` + `test_own_action.php` | A must-use plugin whose rules function fires its own action; two listeners with a priority and an accepted-arguments count (Milestone 3's `pagesco_books_hold_placed`, Exercise 2) | 10 min | the test prints the customer's note, then the shop's, for each request |
| | `debug_trash_door.php` | A staff door with Common Mistake 2 (a general capability), a `wpdb::prepare()` placeholder mismatch and a mistyped key | 10 min | `devon may trash "Welcome to the new Pages & Co. website": no` and `Reason: duplicate`, no message |

## Commands

```bash
cd ~/pagesco-dev

# a PHP lab: copy it into the WordPress root, edit THAT copy, run it with WordPress loaded, delete it
cp labs/module-17/l9_1-final-project/ownership_sql_starter.php wordpress/
wp eval-file --use-include ownership_sql_starter.php
rm wordpress/ownership_sql_starter.php

# the folder lab: the must-use plugin and its test, then remove both
cp labs/module-17/l9_1-final-project/own_action_starter/pagesco-lab-requests.php wordpress/wp-content/mu-plugins/
cp labs/module-17/l9_1-final-project/test_own_action.php wordpress/
wp eval-file --use-include test_own_action.php
rm wordpress/test_own_action.php wordpress/wp-content/mu-plugins/pagesco-lab-requests.php
```

`rsvp_rules_starter.php` and `debug_trash_door.php` run like `ownership_sql_starter.php`.

## Notes for the instructor

- **Nothing stays behind.** `ownership_sql` uses a TEMPORARY table (MySQL drops it when WP-CLI's connection
  closes); `rsvp_rules` keeps its seats in a PHP array and only READS the events table; `own_action` keeps its
  requests in memory; `debug_trash_door` prints a decision and never trashes anything. The last command of each
  lab is an `rm`.
- **`rsvp_rules` uses the IDs 4 and 5** for Jordan and Priya (the accounts Milestone 3 creates) but adds no users
  and reads no user data: it runs the same before and after Milestone 3.
- **`debug_trash_door.php`, the surprise:** with the broken `prepare()` call, `$wpdb->get_var()` receives an empty
  query and returns the PREVIOUS query's answer, so the title prints as `"3"` (Devon's user ID from
  `get_user_by()`). A wrong value with no error of its own: read the Notice first.
- **Expected outputs** are in each starter's "Expected when done" comment (the solutions' real output) and, with
  explanations, in the Session 17 Answer Key ("Lab Reference Solutions").
- **PHP 8.4:** every lab prints the same.
- **Checking the labs:** `python3 labs/check_labs.py module-17` (9 results, about a minute and a half). On your own project:
  `WP_LABS_COMPOSE=~/pagesco-dev python3 labs/check_labs.py module-17` (your site at the end of Lesson 8.4, or
  later).

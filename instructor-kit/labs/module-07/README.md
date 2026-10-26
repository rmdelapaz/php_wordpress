# Session 7 labs · Lesson 4.3 (+ the Part 1 project kickoff)

**functions.php: Supports, Assets, Menus & Widgets.** The labs run on the course site at the states the lesson
starts from or leaves behind (each file's `state:` line):

| State | What your site has | Which labs |
|---|---|---|
| `after:lesson_12` | the end of Lesson 4.2: `pagesco-classic` active, its functions.php has only the pre_get_posts callback | `corner_theme` (a separate theme: it works on any site from Lesson 4.2 on) |
| `after:lesson_13` | the end of Lesson 4.3: `pagesco` active again; pagesco-classic finished (the Main menu in `primary`, one block widget in `footer`) | `menus_widgets`, `debug_theme_setup` |

**The Part 1 project** that Session 7 kicks off is not in this folder: its brief, starter theme and self-check
are in `labs/module-08/p1-project/` (`BRIEF.md`, `fernhill_starter/`, `test_fernhill.php`; Session 8 finishes
it). Milestone 1 in the room:

```bash
cp -r labs/module-08/p1-project/fernhill_starter wordpress/wp-content/themes/fernhill
wp theme activate fernhill
cp labs/module-08/p1-project/test_fernhill.php wordpress/
wp eval-file --use-include test_fernhill.php      # Checks passed: 1 of 12
wp theme activate pagesco                         # when you stop for the day
```

Copy the kit's `labs/` folder into your project folder (`~/pagesco-dev/labs/`, next to `compose.yaml`) and type
every command below in the project folder; `wp` is the shortcut from Lesson 1.2. Every lab removes itself again.

| Folder | File | What it practices | Time | Done when |
|---|---|---|---|---|
| `l4_3-functions-php/` | `corner_theme_starter/` → `corner_theme_solution/` + `test_corner_theme.sh` | **Guided lab.** A small classic theme whose templates are finished and whose functions.php is empty: title-tag and html5 on after_setup_theme, a versioned stylesheet and a deferred footer script on wp_enqueue_scripts, a menu location, a widget area on widgets_init | 20 min | the test prints `<title>:      1`, `html5`, `style.css?ver=2.0.0`, `corner.js?ver=2.0.0, defer`, the location and the area |
| | `menus_widgets_starter.sh` → `menus_widgets_solution.sh` | WP-CLI for menus and widgets on pagesco-classic: a second menu with a page and a custom link, a second block widget, and the cleanup | 15 min | the Gift cards link is listed, and only `block-7` is left afterwards |
| | `debug_theme_setup.php` | A widget area without an id and html5 without an array (both "called incorrectly"), and a stylesheet without a version (silent) | 10 min | `footer-shop`, no notices, `?ver=` with the theme's version |

## Commands

```bash
cd ~/pagesco-dev

# the theme lab: install, activate, test, switch back, remove
cp -r labs/module-07/l4_3-functions-php/corner_theme_starter wordpress/wp-content/themes/pagesco-lab-corner
wp theme activate pagesco-lab-corner
cp labs/module-07/l4_3-functions-php/test_corner_theme.sh wordpress/
docker compose run --rm wpcli sh test_corner_theme.sh
wp theme activate pagesco-classic        # (pagesco if you are past Lesson 4.3)
rm -r wordpress/wp-content/themes/pagesco-lab-corner wordpress/test_corner_theme.sh

# the WP-CLI lab: it switches to pagesco-classic and back to pagesco itself
cp labs/module-07/l4_3-functions-php/menus_widgets_starter.sh wordpress/
docker compose run --rm wpcli sh menus_widgets_starter.sh
rm wordpress/menus_widgets_starter.sh

# the handout
cp labs/module-07/l4_3-functions-php/debug_theme_setup.php wordpress/
wp eval-file --use-include debug_theme_setup.php
rm wordpress/debug_theme_setup.php
```

## Notes for the instructor

- **Expected outputs** are in each starter's "Expected when done" comment (the solutions' real output) and, with
  explanations, in the Answer Key's "Lab Reference Solutions".
- **`menus_widgets` changes the database and undoes it** (the menu and the widget are deleted at the end, and
  pagesco is active again). Menu, item and widget IDs on a learner's site may differ from the expected output if
  they built extra menus or widgets; the commands, not the numbers, are the answer. A learner who stops the
  script halfway deletes the menu with `wp menu delete shop-links`.
- **`debug_theme_setup.php`** runs its calls after init, so they register only for that one WP-CLI run; nothing is
  saved. pagesco is a block theme, so the html5 list it prints is the block-theme default (Lesson 4.3).
- **Theme switches** (the Reading Corner lab) create a `theme_mods_pagesco-lab-corner` option: harmless.
- **No network needed. PHP 8.4:** every lab prints the same.
- **Checking the labs:** `python3 labs/check_labs.py module-07` (about a minute). On your own project:
  `WP_LABS_COMPOSE=~/pagesco-dev python3 labs/check_labs.py module-07`.

# Session 5 labs · Lessons 3.3 + 3.4

**Patterns, Style Variations and Child Themes.** The labs run on the course site at the states the lessons
themselves start from or leave behind (each file's `state:` line; `handoff` in the course tools describes each):

| State | What your site has | Which labs |
|---|---|---|
| `after:lesson_08` | the end of Lesson 3.2: `pagesco` active, no patterns yet | `hours_band` (works on any site from Lesson 3.2 on, whatever you have done of 3.3) |
| `after:lesson_09` | the end of Lesson 3.3: three patterns, two section styles, `styles/evening.json`, `WP_DEVELOPMENT_MODE` = `theme` | `variation_contrast`, `debug_pattern_files`, `tt4_child` |
| `after:lesson_10` | the end of Lesson 3.4: `pagesco` active again, `pagesco-tt5-child` installed | `merge_layers`, `debug_child_theme` |

Copy the kit's `labs/` folder into your project folder (`~/pagesco-dev/labs/`, next to `compose.yaml`) and type
every command below in the project folder; `wp` is the shortcut from Lesson 1.2. Every lab removes itself again.

| Folder | File | What it practices | Time | Done when |
|---|---|---|---|---|
| `l3_3-patterns-style-variations/` | `hours_band_starter/` → `hours_band_solution/` + `test_hours_band.php` | **Guided lab.** Finish a theme pattern file: header fields, translatable strings in the right text domain, a URL built with `home_url()` and `esc_url()`. The folder is a one-file child theme of pagesco, so pagesco stays untouched | 20 min | the test prints `VISIT THE SHOP` and the `pagesandco.example` link |
| | `variation_contrast_starter.php` → `variation_contrast_solution.php` | Read the palette of the theme and of every style variation from WordPress (`wp_get_global_settings()`, `WP_Theme_JSON_Resolver`) and check WCAG AA contrast for the pairs the theme uses | 20 min | ten lines without TODO; `sage on paper` FAILS (sage is a background, never text) |
| | `debug_pattern_files.sh` | A pattern without a Slug, a style file with a JSON syntax error, and a style variation that turns out to be a section style | 10 min | `pagesco/gift-cards` is listed, and `site variation: Sepia` |
| `l3_4-child-themes/` | `tt4_child_starter/` → `tt4_child_solution/` + `test_tt4_child.sh` | **Guided lab.** A child theme of Twenty Twenty-Four (not the lesson's Twenty Twenty-Five): a full palette with one color changed, the child's stylesheet enqueued (the parent has no handle to depend on), a footer pattern override by slug, a pluggable parent function replaced | 20 min | the test prints `#7a2e2e`, `child CSS:   1`, the shop's footer and only `core/list checkmark-list` |
| | `merge_layers_starter.php` → `merge_layers_solution.php` | Merge the parent's and the child's theme.json with `WP_Theme_JSON`, the class WordPress uses: single values merged, preset lists replaced | 15 min | `merged:  8 colors, accent-3 = #7a2e2e` and `partial: 2 colors` |
| | `debug_child_theme.sh` | A child theme with a JSON syntax error, an enqueue at the top level of functions.php, and a parent hook removed too early | 15 min | link `#7a2e2e`, `child CSS: 1`, `checkmark: no`, nothing new in debug.log |

## Commands

```bash
cd ~/pagesco-dev

# the folder lab of Lesson 3.3: a one-file child theme of pagesco that carries the pattern
cp -r labs/module-05/l3_3-patterns-style-variations/hours_band_starter wordpress/wp-content/themes/pagesco-lab-hours
wp theme activate pagesco-lab-hours
cp labs/module-05/l3_3-patterns-style-variations/test_hours_band.php wordpress/
wp eval-file --use-include test_hours_band.php            # edit wordpress/wp-content/themes/pagesco-lab-hours/patterns/hours-band.php, run again
wp theme activate pagesco
rm -r wordpress/wp-content/themes/pagesco-lab-hours wordpress/test_hours_band.php

# the folder lab of Lesson 3.4: a child theme of Twenty Twenty-Four
cp -r labs/module-05/l3_4-child-themes/tt4_child_starter wordpress/wp-content/themes/pagesco-lab-tt4-child
wp theme activate pagesco-lab-tt4-child
cp labs/module-05/l3_4-child-themes/test_tt4_child.sh wordpress/
docker compose run --rm wpcli sh test_tt4_child.sh
wp theme activate pagesco
rm -r wordpress/wp-content/themes/pagesco-lab-tt4-child wordpress/test_tt4_child.sh

# a PHP lab: copy it into the WordPress root, edit THAT copy, run it with WordPress loaded, delete it
cp labs/module-05/l3_4-child-themes/merge_layers_starter.php wordpress/
wp eval-file --use-include merge_layers_starter.php
rm wordpress/merge_layers_starter.php

# a shell handout: the same, run in the WP-CLI container
cp labs/module-05/l3_4-child-themes/debug_child_theme.sh wordpress/
docker compose run --rm wpcli sh debug_child_theme.sh
rm wordpress/debug_child_theme.sh
```

`variation_contrast_starter.php` runs like `merge_layers_starter.php`; `debug_pattern_files.sh` like
`debug_child_theme.sh`.

## Notes for the instructor

- **Expected outputs** are in each starter's "Expected when done" comment (the solutions' real output) and, with
  explanations, in the Answer Key's "Lab Reference Solutions".
- **Theme switches leave an option behind.** Activating a lab theme creates a `theme_mods_<slug>` option (Lessons
  3.1 and 3.4 call these harmless). The two debug handouts switch back to the theme that was active before; for the
  folder labs the last command of each block above does it. On the checker's runner sites the database is restored
  after every file anyway.
- **The two debug handouts write files into themes/ and delete them at the end** (`debug_pattern_files.sh` into
  `pagesco/patterns/` and `pagesco/styles/`, `debug_child_theme.sh` a whole `pagesco-lab-broken/` theme). A learner
  who stops one halfway (Ctrl+C) deletes those files by hand: the script's last lines name them.
- **`debug_pattern_files.sh` needs `WP_DEVELOPMENT_MODE` = `theme`** (Lesson 3.3). Without it the new pattern file
  waits for the 30-minute pattern cache, and the "Slug field missing" notice appears only when the cache is rebuilt.
- **`hours_band` works before the end of Lesson 3.3** (it needs only pagesco active); the pattern's sage band only
  turns sage once `styles/sections/section-sage.json` exists.
- **No network needed** for any lab (Twenty Twenty-Four ships with WordPress).
- **PHP 8.4:** every lab prints the same.
- **Checking the labs:** `python3 labs/check_labs.py module-05` (about a minute and a half). On your own project:
  `WP_LABS_COMPOSE=~/pagesco-dev python3 labs/check_labs.py module-05` (your site must be at the states above).

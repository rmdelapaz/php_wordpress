# Session 2 labs · Lessons 1.3 + 2.1

**PHP the WordPress Way and the Content Model.** All files run on the course site as Session 1 leaves it
(`// state: fresh`, the end of Lesson 1.2): WordPress 7.1.3, PHP 8.5, MySQL 9.7, WP-CLI 2.12, Mailpit, Twenty
Twenty-Five active, only `mailpit-smtp.php` in `wp-content/mu-plugins/`, no content beyond the install. Copy the
kit's `labs/` folder into your project folder (`~/pagesco-dev/labs/`, next to `compose.yaml`) and type every command
below in the project folder. `wp` is the shortcut from Lesson 1.2.

**Every file in this session only reads:** none of them creates a post, a user or a file that stays, so they never
use up the post IDs that Lesson 2.1's project counts on (pages 12 to 14, posts 15 to 17). Each lab ends with an `rm`
of its own copy.

| Folder | File | What it practices | Time | Done when |
|---|---|---|---|---|
| `l1_3-php-the-wordpress-way/` | `signup_form_starter.php` → `signup_form_solution.php` | **Guided lab.** Sanitize early, escape late, on a book club sign-up form with WordPress's added slashes: `wp_unslash()`, `sanitize_text_field()`, `sanitize_email()` + `is_email()`, `absint()`, a validated shelf, then `esc_attr()`, `esc_url()`, `esc_html()` | 20 min | the output matches "Expected when done" (the `javascript:` link comes back empty) |
| | `event_line_starter.php` → `event_line_solution.php` | An events list: `wp_parse_args()` (array and query string), `sprintf()` + `__()` with translator comments, `_n()`, `number_format_i18n()`, a named sort callback for `usort()`, a `WP_Error` checked with `is_wp_error()` | 15 min | `skipped: The event has no date. (pagesco_no_date)` and three sorted lines |
| | `debug_book_badge.php` | A badge helper: two loud bugs (Warnings, and a Deprecated that blames core) and a silent one (the arguments of `wp_parse_args()` swapped) | 10 min | no message, and the second badge says `New in paperback` |
| `l2_1-content-model/` | `content_census_starter.sh` → `content_census_solution.sh` | **Guided lab.** The site counted the way Lesson 2.1 sees it: posts by status, pages, terms, an option, a role's capabilities, the blocks of a post, one WP-CLI command per line | 15 min | the output matches "Expected when done" |
| | `post_report_starter.php` → `post_report_solution.php` | One row of wp_posts seen through the whole model: the post type object, the author and a capability, terms, revisions, `parse_blocks()`, the address (`is_post_type_viewable()`), for five IDs | 15 min | five reports without TODO, `#999 not found` last |
| | `debug_page_report.php` | A content report: two loud bugs (Warnings: a page's categories, a user who does not exist yet) and a silent one (a WP_Post property that is not there) | 10 min | no message, and every line says what the site really holds |

## Commands

```bash
cd ~/pagesco-dev

# a PHP lab: copy it into the WordPress root, edit THAT copy, run it with WordPress loaded, delete it
cp labs/module-02/l1_3-php-the-wordpress-way/signup_form_starter.php wordpress/
wp eval-file --use-include signup_form_starter.php
rm wordpress/signup_form_starter.php

# a shell lab: the same, run in the WP-CLI container
cp labs/module-02/l2_1-content-model/content_census_starter.sh wordpress/
docker compose run --rm wpcli sh content_census_starter.sh
rm wordpress/content_census_starter.sh
```

`event_line_starter.php`, `debug_book_badge.php`, `post_report_starter.php` and `debug_page_report.php` run like
`signup_form_starter.php`. `--use-include` makes PHP's messages name your file
(`/var/www/html/debug_book_badge.php on line 33`, which is `wordpress/debug_book_badge.php`) instead of WP-CLI's
`eval()'d code`.

## Notes for the instructor

- **Expected outputs** are in each starter's "Expected when done" comment (the solutions' real output) and, with
  explanations, in the Answer Key's "Lab Reference Solutions".
- **Run the 2.1 labs before Lesson 2.1's project** (the room does: the guided lab comes right before it). They read
  the site, so after the project their numbers change and nothing breaks. `content_census_solution.sh` on the
  stocked site (the end of Lesson 2.1) prints:

  ```
  == Pages & Co. content census ==
  Post types: 16
  Published posts: 4
  Pages, any status: 5
  Draft pages: 1
  Categories: News
  Uncategorized
  Home page shows: posts
  Editor capabilities: 34
  Blocks in post 1:
        1 <!-- wp:paragraph
  ```

  `post_report_solution.php` then shows revision counts and Maria as the author of the new IDs (edit its ID list to
  `array( 12, 16 )` to see About Us and Staff picks); `debug_page_report.php` loses its last Warning, because the
  user maria exists (the code is still wrong: the Answer Key says why).
- **`debug_page_report.php`** prints its foreach Warning once although the loop runs twice: PHP does not repeat
  the same message from the same line here.
- **No network needed** for any lab file. (Lesson 1.3's PHPCS and Spanish-translation demos do need it; the labs do
  not use Composer.)
- **PHP 8.4:** every lab prints the same. The Deprecated in `debug_book_badge.php` exists on PHP 8.1 and later.
- **Checking the labs:** `python3 labs/check_labs.py module-02` (10 results in about a minute). On your
  own project, at the end of Session 1: `WP_LABS_COMPOSE=~/pagesco-dev python3 labs/check_labs.py module-02`.

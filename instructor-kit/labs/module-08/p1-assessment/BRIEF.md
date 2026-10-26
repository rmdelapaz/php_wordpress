# Part 1 Assessment: finish the Brightwater Swim School theme

Session 8 · 60 minutes · alone, open book · Module 4 (with Modules 1 to 3)

## The client

Ken Adeyemi, who runs the school, writes:

> A developer started a classic theme for us and left halfway. The site works, sort of: our menu never shows, the news page lists bare titles, there is no stylesheet, the search page did something strange when my nephew typed HTML into it, and the previous and next links under a post point to the wrong posts. Can you finish it this afternoon?

The theme is `brightwater`, a classic theme (PHP templates, no theme.json). The school's own news is not written yet: it runs on your course site's posts and pages.

## Set up (5 minutes, before the clock starts)

From your project folder:

```
cp -r labs/module-08/p1-assessment/brightwater_starter wordpress/wp-content/themes/brightwater
wp theme activate brightwater
cp labs/module-08/p1-assessment/test_brightwater.php wordpress/
wp eval-file --use-include test_brightwater.php
```

The last line says `Checks passed: 2 of 10`. Open `wordpress/wp-content/themes/brightwater/` in VS Code.

## Tasks

| | Minutes | Task | Lessons | Self-check |
|---|---|---|---|---|
| T1 | 10 | **Theme setup** (`functions.php`, `header.php`): WordPress prints the title (`title-tag`; remove the hand-written `<title>`); `wp_body_open()` right after `<body>`; register the menu location `primary` ("Primary menu") and make the header use it. Bug report: "our menu never shows" (the course's Main menu is put into `primary` by the self-check). | 3.1, 4.3 | 2, 3, 5 |
| T2 | 5 | **The stylesheet:** enqueue `style.css` with the handle `brightwater-style`, versioned with the theme's own Version, on the right hook. | 4.3 | 4 |
| T3 | 20 | **The news list** (`index.php`, `functions.php`): inside the Loop, an `<article>` with the post's id and classes (`id="post-<?php the_ID(); ?>"`, `post_class()`), an `h2` with the class `entry-title` whose link goes to the post, the date in a `p` with the class `entry-meta`, the excerpt; after the Loop, the pagination links. Two posts per page on the blog home, by changing the main query (guarded). | 4.1, 4.2 | 6, 7 |
| T4 | 5 | **The search page** (`search.php`). Bug report: "it did something strange when my nephew typed HTML". The heading must print the visitor's words as text. | 1.3, 4.1 | 8 |
| T5 | 10 | **Under a post** (`template-parts/related-news.php`, `singular.php`). Bug report: "previous and next point to the wrong posts". The More news box stays as it is; the links under it must be the post's own neighbors. | 4.2 | 9, 10 |

Stretch: A footer widget area with the id `footer` (footer.php already prints it when it holds widgets): Lesson 4.3.

## Rules

- 60 minutes, alone, open book: the lesson pages, your notes, the workbook, your own course code. No other people, no AI assistants, no code from the web.
- Run the self-check as often as you like (it starts at `Checks passed: 2 of 10`). It is a help, not the score: the instructor reads your code with the rubric.
- Change only files in `wordpress/wp-content/themes/brightwater/`. Keep the prefix `brightwater_` and the text domain `brightwater`.
- Unfinished at the end? Write one line at the top of `functions.php` saying what is missing. A clear note beats half-working code you cannot explain.

## Hand-in

- **At the end of the 60 minutes:** zip `wordpress/wp-content/themes/brightwater/` as `brightwater-<yourname>.zip` and hand it in as your instructor says (shared folder or USB stick), with the last self-check output pasted into the zip as `selfcheck.txt`.
- Then: `rm wordpress/test_brightwater.php` and `wp theme activate pagesco`.

## Rubric

| Criterion | 4 Exemplary | 3 Met | 2 Partly | 1 Not yet |
|---|---|---|---|---|
| **Theme setup and hooks (T1, T2)** (Lessons 3.1, 4.3) | All of Met, and the stretch widget area works (id footer, wrappers with %1$s and %2$s). | title-tag on after_setup_theme and one <title>; wp_body_open() after <body>; primary registered and used by has_nav_menu() and wp_nav_menu(); brightwater-style on wp_enqueue_scripts with the theme's Version. | Two of the four pieces done, or a piece done on the wrong hook (top-level code, init) that happens to work. | Setup and stylesheet untouched, or code that breaks the site. |
| **The Loop and template tags (T3, index.php)** (Lesson 4.1) | All of Met, with the_title_attribute() or an aria-label where a link text could repeat, and the translatable no-posts text kept. | article with the_ID() and post_class(); linked h2.entry-title (the_permalink() or esc_url( get_permalink() )); the date escaped; the excerpt; the_posts_pagination() after the Loop. | Titles linked but a piece missing (classes, date, pagination), or echo with a the_ function (prints in the wrong place). | The Loop still prints bare titles, or the_post() missing (an endless loop). |
| **Main and secondary queries (T3, T5)** (Lesson 4.2) | All of Met, and the learner explains in one line why the bug moved the links (the global $post). | pre_get_posts with is_admin(), is_main_query() and is_home() guards, 2 per page, page 2 works; wp_reset_postdata() after the related loop, so the navigation is Dune's own. | Two per page by a second query in the template, or a guard missing; or the reset in the wrong place. | posts_per_page in index.php's own WP_Query, query_posts(), or the navigation still wrong. |
| **Escaping and safe output (T4, all)** (Lessons 1.3, 4.1) | All of Met, and the learner found and escaped a second spot on their own initiative (or explains why each echo is safe). | The search term printed with esc_html() (or get_search_query() with its default escaping); every new echo escaped for its context. | The search term escaped, but a new unescaped echo elsewhere (a date, a URL). | The search page still prints the visitor's HTML. |
| **Working method (all)** (Lessons 1.2, 1.3) | All of Met, and the code is tidy enough to hand to the next developer as it is. | No PHP messages on any page; prefixes and the text domain kept; WordPress coding standards; the self-check run and handed in; an honest note about anything unfinished. | A notice on one page, a missing prefix, or no self-check output. | Fatal errors, edits outside the theme folder, or nothing handed in. |

**Met** = at least 14 of 20 points with no row at 1. Below that, the learner revises once, within a week of the feedback.

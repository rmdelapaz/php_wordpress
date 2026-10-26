# Instructor Kit License (Summary / Template)

**Kit:** PHP and WordPress Development, an instructor kit for the course PHP and WordPress Development
(<https://rays-php-wordpress.netlify.app/>)
**Author & licensor:** Ray de la Paz

> This is a plain-language template. Replace the bracketed terms at point of sale
> and have final wording reviewed by a lawyer before commercial distribution.

## Licensed materials
"The kit" means everything in the `instructor-kit/` folder and the course data it is taught with:

- the facilitator guides, participant workbooks and answer keys (per session and combined), the slide
  decks, the labs (starters and solutions, theme, plugin and must-use plugin folders with their test
  scripts, debug handouts, the environment check, the checkpoints, the Part 1 project, assessment and
  review files, and the checker `check_labs.py`), the setup guide and quick setup, the final assessment
  and the sell sheet;
- the course's **practice data and starting sites**: the fictional bookstore Pages & Co. (its users,
  pages, posts, events and the eleven-book catalog in `pagesco-seed/books.json`), the course downloads
  `pagesco-dev` (the Docker Compose project), `pagesco-part2-start` (the site as Lesson 4.3 leaves it,
  with its database export), `pagesco-seed`, `pagesco-live` and `pagesco-final` (the final project's
  reference solution), the Fernhill Community Garden (Part 1 project), the Brightwater Swim School (Part 1
  assessment) and the Reserve & Pick Up reference data (final project). These are original works,
  written by the author, and part of the licensed materials when used with the kit (the code in them is
  also licensed under the GPL: see "Third-party software and data").

The kit has two parts: **Part 1, Themes** (Sessions 1 to 8) and **Part 2, Plugins to Launch** (Sessions 9
to 18). A "Part 1 only" license covers Sessions 1 to 8 and their materials (including the Part 1 project
and Part 1 assessment sections of `final-assessment.html`); a full license covers all 18 sessions.

## Grant
You (the "Instructor") are granted a **non-exclusive, non-transferable license** to
use the kit to **teach the course to your own students**, according to the
tier you purchased:

| Tier | Who may teach | Rebranding | Full program (18 sessions) | Part 1 only (8 sessions) |
|------|---------------|------------|----------------------------|--------------------------|
| **Solo** | One named instructor | No | [$1,097] one-time | [$547] one-time |
| **Organization** | Multiple instructors at one org | No | [$3,297] one-time | [$1,647] one-time |
| **White-label** | Multiple instructors at one org | Yes — edit & add your brand | [$6,597] one-time | [$3,297] one-time |
| **Updates add-on** | — | — | [$219 / yr] | [$109 / yr] |

A Part 1 license can be upgraded to the full program for the difference in price [at point of sale].

## You MAY
- Teach the course to an unlimited number of your own students under your tier.
- Print and distribute the **participant workbook**, the **setup guide**, the **quick setup** and the
  **lab starter files** (with the environment check and the lab test scripts) to enrolled students.
- Give enrolled students the course downloads (`pagesco-dev`, `pagesco-part2-start`, `pagesco-seed`,
  `pagesco-live`) and the course data files.
- Hand out lab **solutions** to enrolled students after the lab has been completed in class.
- Adapt timing, examples, and pacing to your audience.
- (White-label only) Edit the materials and add your own branding.

## You MAY NOT
- Resell, sublicense, or redistribute the kit itself to other instructors.
- Distribute the **facilitator guide**, the **answer key** or the **final assessment** (the Part 1
  project and assessment rubrics and model solutions, the final-project rubric and instructor answer
  notes), or the checkpoint, Part 1 project and assessment solution files, to students. These are
  **confidential** instructor materials. (The final project's reference site `pagesco-final` is a public
  download on the course site; point students to it after they submit.)
- Publish the materials publicly (e.g., a public website, repository or file share), including
  republishing the practice data as your own.
- Remove author credit (except under the white-label tier).

## Third-party software and data
**No third-party software is shipped with the kit**, apart from the theme assets and generated files
named below. Everything else is downloaded and installed by each learner and the instructor, from its
usual source, under its own license:

- **WordPress** (7.1; the course was verified on 7.1.3) is free software licensed under the **GNU General
  Public License, version 2 or later (GPLv2+)**. Learners get it from the official `wordpress` Docker image
  (`wordpress:7.1-php8.5-apache`, which the course's Compose project starts) or from wordpress.org. The
  bundled themes and plugins (Twenty Twenty-Five, Twenty Twenty-Four, Twenty Twenty-Three, Akismet, Hello
  Dolly) come with it under their own GPL terms.
- **The course's own theme and plugin code is GPL.** Code that runs inside WordPress is distributed under
  the GPL, as WordPress requires of its derivative works, and the course files say so: the themes
  `pagesco`, `pagesco-classic` and `pagesco-tt5-child` declare `License: GNU General Public License v2 or
  later` in their `style.css`; the plugin `pagesco-books` declares `License: GPL-2.0-or-later` in its main
  file, its `readme.txt`, `composer.json` and `package.json`. Anyone who receives that code may use,
  change and share it under the GPL. This license governs the kit's **teaching materials** (the guides,
  workbooks, answer keys, decks, assessments, rubrics and practice data); it does not take away any GPL
  right in the code. Lab theme and plugin folders follow the same rule.
- **Twenty Twenty-Five assets** reused in the course theme `pagesco` (from Lesson 3.2 on) and listed in its
  `readme.txt`: the **Vollkorn** font (Copyright © 2005-2018 Friedrich Althausen, **SIL Open Font
  License 1.1**) and the image `assets/images/book-image.webp` (public domain, **CC0**), both as credited
  in Twenty Twenty-Five's own `readme.txt`.
- **PHP** (8.5; 8.4 also works) under the **PHP License**, **MySQL Community Server** 9.7 (Oracle, **GPL**),
  **WP-CLI** 2.12 (**MIT License**), **Mailpit** (**MIT License**), **Composer** (**MIT License**) and
  **Node.js** 24 with **npm**, all used through their publishers' Docker images (`mysql:9.7`,
  `wordpress:cli-php8.5`, `axllent/mailpit`, `composer:2`, `node:24`) or the learner's own install, each
  under its publisher's license. The course's WP-CLI image is built on the learner's computer from
  `config/wpcli.Dockerfile`; no image is shipped with the kit.
- **npm and Composer packages** installed by the lessons and labs from the npm registry and Packagist,
  under their own licenses: `@wordpress/scripts`, `@wordpress/create-block`,
  `@wordpress/create-block-interactive-template` and `@wordpress/env` (GPL-2.0-or-later, the WordPress
  project) with their dependencies, and `phpunit/phpunit` (BSD-3-Clause),
  `wp-coding-standards/wpcs` (MIT), `yoast/phpunit-polyfills` (BSD-3-Clause) and their dependencies.
  They are downloaded into each learner's own `node_modules/` and `vendor/` folders; the kit ships the
  `package.json`, `package-lock.json`, `composer.json` and `composer.lock` files that name them, Composer's
  generated autoloader files, and the block `build/` output that `@wordpress/scripts` compiled from the
  course's own sources.

If you copy Docker images to a USB stick for a classroom (as the setup guide suggests, with `docker save`
and `docker load`), you redistribute those publishers' unmodified images under their license terms; they
are not part of the kit and not covered by this license.

VS Code, Docker Desktop, wp-env, WordPress Playground, and the hosting types described in Lesson 8.4 are
mentioned as tools or alternatives; none of them is shipped with the kit. WordPress is a registered
trademark of the WordPress Foundation; PHP is a trademark of The PHP Group, and MySQL a trademark of
Oracle and/or its affiliates. The kit is not affiliated with or endorsed by any of them.

**All data in the kit is the author's own and fictional:** every user, customer, staff member, event,
hold, garden volunteer, swim lesson, account, password and email address in Pages & Co., the Part 1 project
and assessment and the final project is invented (email addresses use example domains such as
`example.com`; the only real addresses in the kit are the package authors' contact details inside
`composer.lock`, as published on Packagist). Book titles and author names are real published works, used
only as catalog entries. The development passwords in the course sites (`password`, `maria-pass`,
`devon-pass`) are for local practice sites only.

## The public course site
The lessons at <https://rays-php-wordpress.netlify.app/>, the course downloads in its `downloads/` folder
and the public syllabus remain freely available to anyone. This license covers the instructor kit and
its use for teaching; it does not restrict anyone's use of the free lessons or the GPL code.

## Ownership
All materials remain the intellectual property of the licensor (the GPL code is the author's copyright,
licensed under the GPL). This license may be revoked for breach of these terms.

---
© 2026 Ray de la Paz. All rights reserved.

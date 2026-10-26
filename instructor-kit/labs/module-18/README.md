# Session 18 labs · Lessons 9.1 (Milestones 7 to 9) + 9.2

**Final Project Studio II, Showcase and Next Steps.** Session 18 finishes the final project in the studio (quality,
the release, the code-only deploy), holds the showcase and closes the course with Lesson 9.2. The project is the
main work; these labs are SHORT practice for the guided lab of 9.2 and for learners who are stuck or done early.
They are new practice, not the project or the lessons' exercises.

- `l9_1-final-project/` runs on the course site as **Lesson 8.4's project left it** (`// state: after:lesson_29`,
  release-2: plugin and theme 1.1.1), the site Lesson 9.1 starts from. A learner who has finished the project
  (1.2.0) sees 1.2.0 instead of 1.1.1 in `version_audit` and the `src/Holds` folder as `shipped` in `files_list`;
  that is the point of both labs.
- `l9_2-next-steps/` runs on the site as **Lesson 9.1's project left it** (`// state: after:lesson_30`: release-3,
  Reserve & Pick Up, jordan and priya).

Copy the kit's `labs/` folder into your project folder (`~/pagesco-dev/labs/`, next to `compose.yaml`) and type
every command below in the project folder; `wp` is the shortcut from Lesson 1.2.

| Folder | File | What it practices | Time | Done when |
|---|---|---|---|---|
| `l9_1-final-project/` | `version_audit_starter.php` → `version_audit_solution.php` | Every place a version lives, read the way WordPress and the tools read it: plugin header, constant, readme Stable tag, package.json, theme Version (Milestone 8) | 10 min | five lines and `All five agree: 1.1.1` (1.2.0 after your release) |
| | `files_list_starter.php` → `files_list_solution.php` | Which `src/` folders a release ZIP would leave out, without Node: package.json's "files" against the folders, plus a planned one (Common Mistake 1) | 10 min | `src/Holds (planned)` is `MISSING`, the block sources are left out on purpose |
| | `smoke_rest_starter.sh` → `smoke_rest_solution.sh` | A smoke test from outside in the shape of holds-smoke.sh: status codes, a REST header, a redirect, exit 1 on failure (Milestones 5 and 9) | 15 min | five `ok` lines, exit status 0 |
| | `debug_release_check.php` | "Can everything move to 1.2.0?": one typo with two messages (a Warning and the Deprecated it causes) and a silent wrong header name | 10 min | three lines `1.1.1 -> 1.2.0 ok`, no message |
| `l9_2-next-steps/` | `cors_headers_starter.sh` → `cors_headers_solution.sh` | **Guided lab.** What a front end on another origin may read: Allow-Origin, credentials, the exposed paging headers, and a protected route that is readable but refused | 15 min | the output matches "Expected when done" |
| | `ai_readiness_starter.php` → `ai_readiness_solution.php` | Five honest lines for a client meeting about AI, and a helper with three guards that never breaks the page (with AI switched off by the `wp_supports_ai` filter too) | 15 min | `A text model available: no` and the fallback answer twice |
| | `publish_scan_starter.sh` → `publish_scan_solution.sh` | Before a repository goes public: secrets and never-publish files in the shop's own code, on disk (the step 4 history search's partner) | 10 min | `0 file(s)` for every secret, 0 never-publish files |
| | `debug_headless_client.php` | A headless client's first draft in PHP: a mistyped key (Warning, then Deprecated) and Common Mistake 3, the first page only (silent) | 10 min | `Pages & Co.: 11 books on 2 pages`, no message |

## Commands

```bash
cd ~/pagesco-dev

# a PHP lab: copy it into the WordPress root, edit THAT copy, run it with WordPress loaded, delete it
cp labs/module-18/l9_1-final-project/version_audit_starter.php wordpress/
wp eval-file --use-include version_audit_starter.php
rm wordpress/version_audit_starter.php

# a shell lab: the same, run in the WP-CLI container
cp labs/module-18/l9_2-next-steps/cors_headers_starter.sh wordpress/
docker compose run --rm wpcli sh cors_headers_starter.sh
rm wordpress/cors_headers_starter.sh
```

`files_list`, `debug_release_check`, `ai_readiness` and `debug_headless_client` run like `version_audit`;
`smoke_rest` and `publish_scan` like `cors_headers`. `smoke_rest_solution.sh` also takes an address, so it can
check the rehearsal server from its own WP-CLI container: `sh /deploy/smoke_rest_solution.sh http://localhost:8081`
(copy it into `pagesco-live/deploy/` first, as Milestone 9 does with holds-smoke.sh).

## Notes for the instructor

- **Nothing stays behind.** Every lab only reads files, options and pages (`ai_readiness` adds a filter for its
  own request and removes it); the last command of each is an `rm`.
- **No network needed,** and no AI provider: `ai_readiness` reports what a fresh 7.1 site has (three providers
  listed, none active, no model) and its helper gives the fallback.
- **`debug_release_check.php`:** the Warning (`Undefined array key "verison"`) causes the Deprecated (null passed
  to `version_compare()`): fix the key and both go. The silent bug is `get( 'version' )`: theme header names are
  case-sensitive, it returns false, and `version_compare()` turns false into an empty string that is "older" than
  1.2.0, so the line says ok for the wrong reason.
- **`debug_headless_client.php`:** fixing the key (`name`) fixes both loud messages; the silent bug is that it
  reads one page of six books while `X-WP-TotalPages` says 2.
- **Expected outputs** are in each starter's "Expected when done" comment and, with explanations, in the Session 18
  Answer Key ("Lab Reference Solutions").
- **PHP 8.4:** every lab prints the same.
- **Checking the labs:** `python3 labs/check_labs.py module-18` (14 results, about two minutes). On your own
  project: `WP_LABS_COMPOSE=~/pagesco-dev python3 labs/check_labs.py module-18` (your site at the end of Lesson 8.4
  for `l9_1-final-project/`, of Lesson 9.1 for `l9_2-next-steps/`; a site past release-3 prints 1.2.0 in
  `version_audit`, which then fails its expect line: that is a correct result for your site, not a broken lab).

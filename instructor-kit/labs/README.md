# Labs

All hands-on labs of the **PHP and WordPress Development** instructor kit (18 sessions, Modules 1 to 9), grouped by
session (one folder per 3-hour session; `module-04` = Session 4). Each session folder has its own `README.md` with
the exact files, what each lab practices, how long it takes and what "done" looks like. This file is the map and
the rules.

```
labs/
├─ check_labs.py    installs and runs every lab on a real WordPress 7.1 site and reports PASS/FAIL
├─ module-01/       Session 1 · lessons 1.1 + 1.2
│   ├─ README.md
│   ├─ l1_0-orientation/            (Session 1 only: check_environment.sh, the diagnostic pair)
│   ├─ l1_1-<slug>/                 one folder per lesson: l<module>_<lesson>-<slug>
│   │   ├─ <name>_starter.php         a handout: a PHP script run with WordPress loaded (wp eval-file)
│   │   ├─ <name>_solution.php        the instructor's reference
│   │   ├─ <name>_starter.sh          a handout: WP-CLI and shell commands, run in the WP-CLI container
│   │   ├─ <name>_solution.sh         ... and its reference
│   │   ├─ debug_<name>.php|.sh       (optional) a deliberately broken "find the bug" handout
│   │   ├─ <name>_starter/            (folder labs) a plugin, must-use plugin or theme the learner writes ...
│   │   ├─ <name>_solution/           ... its reference twin ...
│   │   └─ test_<name>.sh|.php        ... and the test that requests pages and reads the log
├─ module-02/ ... module-18/       (Part 1 "Themes" = module-01 to module-08, Part 2 "Plugins to Launch" = module-09 to module-18)
```

## Where the labs live on a learner's computer

Learners copy this whole `labs/` folder into their **project folder** (`~/pagesco-dev`, Lesson 1.2), next to
`compose.yaml`, so it is NOT inside `wordpress/` (the web root) and never mixes with core files:

```
pagesco-dev/
  compose.yaml   config/   wordpress/   labs/     <- here
```

## How learners run a lab (the pattern of Lesson 1.2's health check)

Every command below is typed in the project folder. `wp` is the course shortcut
(`alias wp='docker compose --progress quiet run --rm wpcli wp'`, Lesson 1.2).

**A PHP lab** (`*.php`) is copied into the WordPress root, edited there, and run by WP-CLI with WordPress loaded:

```
cp labs/module-01/l1_1-wordpress-for-developers/wp_paths_starter.php wordpress/
wp eval-file --use-include wp_paths_starter.php
rm wordpress/wp_paths_starter.php                  # when you are done
```

`--use-include` makes PHP's messages name the file and line (`in /var/www/html/wp_paths_starter.php on line 12`)
instead of WP-CLI's `EvalFile_Command.php(85) : eval()'d code`. Learners edit the copy in `wordpress/` in VS Code.

**A shell lab** (`*.sh`) runs in the WP-CLI container, in the WordPress root, where `wp`, `curl`, `grep` and the
usual tools are available and `http://localhost:8080` is the site:

```
cp labs/module-01/l1_2-local-environment/site_report_starter.sh wordpress/
docker compose run --rm wpcli sh site_report_starter.sh
```

**A folder lab** (`<name>_starter/`) is a plugin, must-use plugin or theme. The session README gives the exact
copy and activate commands (for example `cp labs/.../store_hours_starter/pagesco-hours.php
wordpress/wp-content/mu-plugins/`, or `cp -r labs/.../x_starter wordpress/wp-content/plugins/pagesco-x` then
`wp plugin activate pagesco-x`), and its `test_<name>.sh` or `test_<name>.php` runs like any lab file.
Remove the lab plugin or theme when the lab is done (`wp plugin deactivate ... && rm -r ...`): the course site
must stay the way the next lesson expects it.

**`check_environment.sh`** runs on the learner's own computer (not in a container), in the project folder:
`bash labs/module-01/l1_0-orientation/check_environment.sh` (Session 9: add `--part2`).

Error messages in the answer key show `/var/www/html/...`: that is the learner's `wordpress/` folder as the
containers see it, so their messages show exactly the same paths.

## Header lines: what a lab needs

Every file that runs (starters, solutions, `debug_*`, `test_*`, `check_*`) says in a comment in its first 25 lines
(`//`, `#`, or ` * ` inside a docblock) what it needs:

| Header | Meaning |
|---|---|
| `// state: fresh` | The site the lab starts from: `fresh` (the end of Lesson 1.2) or `after:lesson_NN` (the site exactly as Lesson NN's project left it). A learner who followed the lessons is there; the session README says so |
| `// expect: All checks passed.` | (repeatable) Text the output must contain. A starter's line is what it prints AS SHIPPED (a TODO line); a solution's is the answer |
| `// expect-starter: ...` · `// expect-solution: ...` | (test files) the same, for the starter folder and the solution folder |
| `// expect-error: Deprecated, Warning` | (`debug_*` only) the messages it must produce: PHP levels (`Warning`, `Notice`, `Deprecated`, `Fatal error`, `Parse error`), uncaught exception classes (`TypeError` ...), `doing_it_wrong` (WordPress's "was called incorrectly"), `Error` (a WP-CLI `Error:` line) |
| `// serve: store_hours` | (`test_*` only) the folder pair `store_hours_starter/` + `store_hours_solution/` (or one folder named exactly `store_hours/`) |
| `// install: mu-plugin` · `plugin [slug]` · `theme [slug]` | (`test_*` only) how that folder is installed: its files into `wp-content/mu-plugins/`, or as `wp-content/plugins/<slug>/` then `wp plugin activate <slug>`, or `wp-content/themes/<slug>/` then `wp theme activate <slug>` (slug default: the pair name with `-` for `_`) |
| `// user: admin` · `// args: ...` | `wp eval-file ... --user=admin` / arguments for the script |
| `# host: compose` | (`check_*.sh` only) runs on the host in the project folder (check_environment.sh) |

## Naming and writing rules

| File | Meaning | Run by the checker |
|---|---|---|
| `<name>_starter.php` / `.sh` | The handout. **Runs without any PHP or WordPress message exactly as shipped**: TODOs in comments, placeholder values that print `TODO` or an obviously unfinished result, and an "Expected when done" comment at the end that quotes the solution's real output. | yes |
| `<name>_solution.php` / `.sh` | The reference. Complete; prints its answers. Do not hand out before the lab. | yes |
| `debug_<name>.php` / `.sh` | A deliberately broken handout. It MUST produce messages, and only the kinds its header declares. A good one has two loud bugs and a silent one. | yes |
| `<name>_starter/`, `<name>_solution/` + `test_<name>` | A folder lab: the plugin, must-use plugin or theme, and the test that requests its pages (`curl http://localhost:8080/...` in a `.sh`, `wp_remote_get( home_url( '/...' ) )` in a `.php`) and reads `wp-content/debug.log`. | the test, once per folder |
| `check_*.sh` / `.php` | Support tools (`check_environment.sh`). | yes |
| other `.php` files (the files of a folder lab, includes) | Not run directly. | syntax check (`php -l`, PHP 8.5) |

- Starters and solutions come in **pairs** with the same `<name>` and extension (files or folders).
- Lesson folders are `l<module>_<lesson>-<slug>`: `l1_2-local-environment`, `l5_2-custom-post-types`.
- Labs are NEW practice on the lesson's ideas, never the lesson's own project or exercises.
- Code follows the lessons and WordPress's coding standards (Lesson 1.3): the `pagesco_` prefix on every function
  and every variable a lab script defines (scripts share WordPress's scope), tabs, `esc_html()` and friends on
  output, `$wpdb->prepare()` for any SQL with values. Fictional people, the real classics of the bookstore.
- A lab must leave the learner's site as it found it: no files left behind (the checker fails a lab that creates
  or changes files outside its own copy, its installed folder and `debug.log`), and content it adds is removed
  again or listed in the session README with the command that removes it.
- No `$ ` prompts in `.sh` files (learners copy them); no `shell_exec`, `exec`, `system`, `passthru` or backticks
  in PHP outside `check_*` files.

## Checking the labs

From this kit's folder (any folder works):

```bash
python3 labs/check_labs.py                 # all sessions
python3 labs/check_labs.py module-01       # one session (also 01 or 1; several allowed)
python3 labs/check_labs.py module-01 -v    # also show what each file printed
python3 labs/check_labs.py --file labs/module-01/l1_2-local-environment/site_report_solution.sh -v
python3 labs/check_labs.py --no-host       # skip check_environment.sh (it starts a whole Compose project)
python3 labs/check_labs.py --strict        # all sessions; a session with no labs counts as a failure
```

For every file it prepares a site at the file's `state`, copies the lab in (and installs and activates a folder
lab), runs it exactly as a learner would, removes what it installed, and prints one `PASS` / `FAIL` line, then
`N passed, M failed`. A file fails on any message it did not declare (in its output or newly written to
`wp-content/debug.log`), a WP-CLI `Error:` line, a non-zero exit status, a timeout (120 s), a missing `expect` text,
or files left behind.

**On your own computer (buyers, instructors).** Point the checker at YOUR Lesson 1.2 project, started with
`docker compose up -d`:

```bash
export WP_LABS_COMPOSE=~/pagesco-dev
python3 ~/pagesco-dev/labs/check_labs.py module-01
```

Every lab then runs on your site through `docker compose run --rm wpcli`. Before each file the checker saves your
database (`wp db export` into `wordpress/.wp-labs-snapshot.sql`), and afterwards it removes what it installed and
imports the snapshot again, so your site is left as it was. Your site must be at the state each lab declares
(Session 1: a freshly set-up site; later sessions: the end of the lesson named in the header). Without
`WP_LABS_COMPOSE` the checker uses the course author's throwaway runner sites (`wpkit.py`), which build every
state from the lessons themselves.

The expected outputs were produced on **WordPress 7.1.3, PHP 8.5, MySQL 9.7, WP-CLI 2.12**; on PHP 8.4
(`WP_LABS_PHP=8.4` for the runner) the version lines differ and the session READMEs say where else.

**How the documents refer to labs:** the facilitator guide, workbook and answer key use paths like
`labs/module-03/l2_3-hooks/`, relative to this kit's folder (where the combined books live). Keep the whole kit
folder together so those pointers hold.

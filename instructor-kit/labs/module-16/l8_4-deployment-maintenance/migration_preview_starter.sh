# migration_preview_starter.sh: a migration to a staging address, previewed without changing anything (Session 16, Lesson 8.4, lab A)
# state: after:lesson_28
# expect: dry run, every table with the prefix, GUIDs left alone: TODO
#
# Before a staging copy gets your database (Lesson 8.4's "staging" FAQ), find out what the move changes, with
# dry runs and an export to /tmp: nothing in the site's database changes. The staging address here is
# https://staging.pagesco.example. The script runs in the WP-CLI container. From your project folder:
#     cp labs/module-16/l8_4-deployment-maintenance/migration_preview_starter.sh wordpress/
#     docker compose run --rm wpcli sh migration_preview_starter.sh
# The table lists and the last line are done for you. Each TODO is one wp search-replace or grep: never without
# --dry-run or --export (this is your development site). Compare with "Expected when done" at the end.
# When you are done: rm wordpress/migration_preview_starter.sh

old='http://localhost:8080'
new='https://staging.pagesco.example'

echo "tables WordPress registers: $(wp db tables | wc -l), all with the prefix: $(wp db tables --all-tables-with-prefix | wc -l)"
echo "the tables only the second list has: $(wp db tables --all-tables-with-prefix | grep -v -x -F "$(wp db tables)" | xargs)"

# TODO 1: how many replacements would a move to $new make? wp search-replace with --all-tables-with-prefix,
#         --skip-columns=guid, --dry-run and --format=count (which prints only the number).
echo "dry run, every table with the prefix, GUIDs left alone: TODO"

# TODO 2: export the replaced database twice into /tmp, once without and once with --all-tables-with-prefix
#         (--export=/tmp/<name>.sql; > /dev/null hides the table), and count the CREATE TABLE lines of each.
echo "export without --all-tables-with-prefix: TODO"
echo "export with --all-tables-with-prefix: TODO"
# TODO 3: in the second export, count the new address and the old one (grep -o ... | wc -l). Then rm both files.
echo "new address in the export: TODO"

# TODO 4: count the options whose value is a serialized array (it starts with a:) and contains localhost:8080,
#         with wp db query "SELECT COUNT(*) ..." --skip-column-names.
echo "options with the address inside a serialized value: TODO"
echo "the database still says: $(wp option get home)"

# Expected when done (migration_preview_solution.sh, the course site after Lesson 8.3):
# tables WordPress registers: 12, all with the prefix: 13
# the tables only the second list has: wp_pagesco_events
# dry run, every table with the prefix, GUIDs left alone: 9 replacements
# export without --all-tables-with-prefix: 12 tables
# export with --all-tables-with-prefix: 13 tables
# new address in the export: 15, old address left (the GUIDs): 34
# options with the address inside a serialized value: 0
# the database still says: http://localhost:8080

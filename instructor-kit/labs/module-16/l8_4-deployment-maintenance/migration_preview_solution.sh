# migration_preview_solution.sh: a migration to a staging address, previewed without changing anything (Session 16, Lesson 8.4, lab A)
# state: after:lesson_28
# expect: export with --all-tables-with-prefix: 13 tables
# expect: the database still says: http://localhost:8080
#
# Before a staging copy gets your database (Lesson 8.4's "staging" FAQ), find out what the move changes, with
# dry runs and an export to /tmp: nothing in the site's database changes. The staging address here is
# https://staging.pagesco.example. The script runs in the WP-CLI container. From your project folder:
#     cp labs/module-16/l8_4-deployment-maintenance/migration_preview_solution.sh wordpress/
#     docker compose run --rm wpcli sh migration_preview_solution.sh
#     rm wordpress/migration_preview_solution.sh

old='http://localhost:8080'
new='https://staging.pagesco.example'

echo "tables WordPress registers: $(wp db tables | wc -l), all with the prefix: $(wp db tables --all-tables-with-prefix | wc -l)"
echo "the tables only the second list has: $(wp db tables --all-tables-with-prefix | grep -v -x -F "$(wp db tables)" | xargs)"

echo "dry run, every table with the prefix, GUIDs left alone: $(wp search-replace "$old" "$new" --all-tables-with-prefix --skip-columns=guid --dry-run --format=count) replacements"

wp search-replace "$old" "$new" --skip-columns=guid --export=/tmp/pagesco-staging-core.sql > /dev/null
wp search-replace "$old" "$new" --all-tables-with-prefix --skip-columns=guid --export=/tmp/pagesco-staging.sql > /dev/null
echo "export without --all-tables-with-prefix: $(grep -c '^CREATE TABLE' /tmp/pagesco-staging-core.sql) tables"
echo "export with --all-tables-with-prefix: $(grep -c '^CREATE TABLE' /tmp/pagesco-staging.sql) tables"
echo "new address in the export: $(grep -o "$new" /tmp/pagesco-staging.sql | wc -l), old address left (the GUIDs): $(grep -o "$old" /tmp/pagesco-staging.sql | wc -l)"
rm /tmp/pagesco-staging-core.sql /tmp/pagesco-staging.sql

echo "options with the address inside a serialized value: $(wp db query "SELECT COUNT(*) FROM wp_options WHERE option_value LIKE 'a:%' AND option_value LIKE '%localhost:8080%'" --skip-column-names)"
echo "the database still says: $(wp option get home)"

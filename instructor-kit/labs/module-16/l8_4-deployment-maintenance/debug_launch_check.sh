# debug_launch_check.sh: a pre-launch report typed the night before (Session 16, Lesson 8.4, find-the-bug handout)
# state: after:lesson_28
# expect-error: Error
#
# Before the launch database is exported, the report should print the site's address, the supplier's address
# (which must change for the live site), and the tables a launch export would contain: 13, the events table
# included. From your project folder:
#     cp labs/module-16/l8_4-deployment-maintenance/debug_launch_check.sh wordpress/
#     docker compose run --rm wpcli sh debug_launch_check.sh
# Two bugs announce themselves with a WP-CLI "Error:" line (and the script carries on: a shell script does not stop
# at a failed command unless it says set -e). The third is SILENT: a number that looks fine and is not. Fix them
# one at a time and run again after each fix. Nothing in the database changes. Then delete the copy:
# rm wordpress/debug_launch_check.sh

echo "== Pre-launch report =="
echo "Site address: $(wp option get homeurl)"
echo "Supplier address: $(wp config get PAGESCO_BOOKS_SUPPLIER_ULR)"
wp search-replace 'http://localhost:8080' 'https://www.pagesco.example' --skip-columns=guid --export=/tmp/pagesco-launch.sql > /dev/null
echo "Tables in the launch export: $(grep -c '^CREATE TABLE' /tmp/pagesco-launch.sql)"
rm /tmp/pagesco-launch.sql
echo "== End of report =="

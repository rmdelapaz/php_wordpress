# restore_drill_starter.sh: a backup is only a backup once you have restored it (Session 16, Lesson 8.4, lab B)
# state: after:lesson_28
# expect: after the restore: TODO
#
# A fire drill for the database, on your development site: a marker post, a backup outside the web root, the
# "accident", the restore, the proof. The marker is deleted again at the end (its ID stays used). From your
# project folder:
#     cp labs/module-16/l8_4-deployment-maintenance/restore_drill_starter.sh wordpress/
#     docker compose run --rm wpcli sh restore_drill_starter.sh
# The marker, the backup and the clean-up at the end are done for you. TODO 1 is the accident, TODO 2 the restore
# (and the object cache: Lesson 8.4, Step 6). set -e stops the script at the first command that fails: a drill
# that cannot fail quietly. Compare with "Expected when done" at the end.
# When you are done: rm wordpress/restore_drill_starter.sh
set -e
backup=/tmp/pagesco-drill.sql

marker=$(wp post create --post_title='Restore drill' --post_status=draft --porcelain)
echo "marker post created"
wp db export "$backup" --quiet
echo "backup: $(grep -c '^CREATE TABLE' "$backup") tables, events table included: $(grep -c 'CREATE TABLE `wp_pagesco_events`' "$backup")"

# TODO 1: the accident. Delete the marker post for good (wp post delete with --force), then count the drafts titled
#         'Restore drill' (wp post list --post_type=post --post_status=draft --title='Restore drill' --format=count).
echo "after the accident: TODO"

# TODO 2: the restore. Import $backup, empty the object cache, and count the marker posts again.
echo "after the restore: TODO"

# The clean-up (done for you): the marker goes, and so does the dump. On a real server the dump would be copied
# somewhere else, not deleted.
wp post delete "$marker" --force --quiet
rm "$backup"
echo "drill over: $(wp post list --post_type=post --post_status=draft --title='Restore drill' --format=count) \"Restore drill\" posts, the dump deleted"

# Expected when done (restore_drill_solution.sh):
# marker post created
# backup: 13 tables, events table included: 1
# after the accident: 0 "Restore drill" posts
# after the restore: 1 "Restore drill" post
# drill over: 0 "Restore drill" posts, the dump deleted

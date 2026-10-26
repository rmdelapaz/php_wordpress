# restore_drill_solution.sh: a backup is only a backup once you have restored it (Session 16, Lesson 8.4, lab B)
# state: after:lesson_28
# expect: after the restore: 1 "Restore drill" post
# expect: drill over: 0 "Restore drill" posts, the dump deleted
#
# A fire drill for the database, on your development site: a marker post, a backup outside the web root, the
# "accident", the restore, the proof. The marker is deleted again at the end (its ID stays used). From your
# project folder:
#     cp labs/module-16/l8_4-deployment-maintenance/restore_drill_solution.sh wordpress/
#     docker compose run --rm wpcli sh restore_drill_solution.sh
#     rm wordpress/restore_drill_solution.sh
set -e
backup=/tmp/pagesco-drill.sql

marker=$(wp post create --post_title='Restore drill' --post_status=draft --porcelain)
echo "marker post created"
wp db export "$backup" --quiet
echo "backup: $(grep -c '^CREATE TABLE' "$backup") tables, events table included: $(grep -c 'CREATE TABLE `wp_pagesco_events`' "$backup")"

wp post delete "$marker" --force --quiet
echo "after the accident: $(wp post list --post_type=post --post_status=draft --title='Restore drill' --format=count) \"Restore drill\" posts"

wp db import "$backup" --quiet
wp cache flush --quiet
echo "after the restore: $(wp post list --post_type=post --post_status=draft --title='Restore drill' --format=count) \"Restore drill\" post"

wp post delete "$marker" --force --quiet
rm "$backup"
echo "drill over: $(wp post list --post_type=post --post_status=draft --title='Restore drill' --format=count) \"Restore drill\" posts, the dump deleted"

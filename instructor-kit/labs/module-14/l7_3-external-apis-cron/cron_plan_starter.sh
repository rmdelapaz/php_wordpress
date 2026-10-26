# cron_plan_starter.sh: schedule a job once, a reminder once, and take both away again (Session 14, Lesson 7.3, lab C)
# state: after:lesson_24
# expect: Events of pagesco_books_lab_job after three schedule calls: 0
# expect: Left: 0
#
# Lesson 7.3's rules for WP-Cron, from the WP-CLI container: schedule a recurring event only when
# wp_next_scheduled() says there is none, start it at a quiet hour in the site's time zone, give one-time events
# their arguments, and clear what you scheduled. Each wp command is one request, like a page view. From your
# project folder:
#     cp labs/module-14/l7_3-external-apis-cron/cron_plan_starter.sh wordpress/
#     docker compose run --rm wpcli sh cron_plan_starter.sh
# Fill in the TODOs, run again after each one, compare with "Expected when done". The script removes its events
# at the end; if you stop it halfway: wp cron event delete pagesco_books_lab_job (and pagesco_books_lab_reminder).
# When you are done: rm wordpress/cron_plan_starter.sh

for run in 1 2 3; do
	# TODO 1: one wp eval that schedules the hook pagesco_books_lab_job twice a day ('twicedaily'), first at
	#         04:30 tomorrow in the site's time zone (new DateTimeImmutable( "tomorrow 04:30", wp_timezone() )),
	#         but only if wp_next_scheduled() finds none. Run three times, it must still be ONE event.
	:
done
printf 'Events of pagesco_books_lab_job after three schedule calls: '
wp cron event list --hook=pagesco_books_lab_job --format=count; echo
wp cron event list --hook=pagesco_books_lab_job --fields=hook,recurrence
printf 'First run (site time): '
wp eval 'echo wp_next_scheduled( "pagesco_books_lab_job" ) ? wp_date( "H:i", wp_next_scheduled( "pagesco_books_lab_job" ) ) : "TODO", "\n";'

# TODO 2: a one-time event, the hook pagesco_books_lab_reminder with the argument 7, an hour from now
#         (wp_schedule_single_event()), then list it: wp cron event list --hook=... --fields=hook,recurrence,args

# Clean up (keep this part): wp_clear_scheduled_hook() returns how many events it removed.
printf 'Removed: '
wp eval 'echo wp_clear_scheduled_hook( "pagesco_books_lab_job" ), " + ", wp_clear_scheduled_hook( "pagesco_books_lab_reminder", array( 7 ) ), "\n";'
printf 'Left: '
wp eval 'echo (int) wp_next_scheduled( "pagesco_books_lab_job" ) + (int) wp_next_scheduled( "pagesco_books_lab_reminder", array( 7 ) ), "\n";'

# Expected when done (cron_plan_solution.sh):
# Events of pagesco_books_lab_job after three schedule calls: 1
# +-----------------------+------------+
# | hook                  | recurrence |
# +-----------------------+------------+
# | pagesco_books_lab_job | 12 hours   |
# +-----------------------+------------+
# First run (site time): 04:30
# +----------------------------+---------------+------+
# | hook                       | recurrence    | args |
# +----------------------------+---------------+------+
# | pagesco_books_lab_reminder | Non-repeating | [7]  |
# +----------------------------+---------------+------+
# Removed: 1 + 1
# Left: 0

# cron_plan_solution.sh: the instructor's reference for cron_plan_starter.sh (Session 14, Lesson 7.3, lab C)
# state: after:lesson_24
# expect: Events of pagesco_books_lab_job after three schedule calls: 1
# expect: Removed: 1 + 1
# expect: Left: 0

# One "schedule" call, guarded the way DailySync::schedule() is: run it three times, as three requests would.
for run in 1 2 3; do
	wp eval '$hook = "pagesco_books_lab_job"; if ( ! wp_next_scheduled( $hook ) ) { wp_schedule_event( ( new DateTimeImmutable( "tomorrow 04:30", wp_timezone() ) )->getTimestamp(), "twicedaily", $hook ); }'
done
printf 'Events of pagesco_books_lab_job after three schedule calls: '
wp cron event list --hook=pagesco_books_lab_job --format=count; echo
wp cron event list --hook=pagesco_books_lab_job --fields=hook,recurrence
printf 'First run (site time): '
wp eval 'echo wp_date( "H:i", wp_next_scheduled( "pagesco_books_lab_job" ) ), "\n";'

# A one-time event with an argument (a reminder for event 7), an hour from now.
wp eval 'wp_schedule_single_event( time() + HOUR_IN_SECONDS, "pagesco_books_lab_reminder", array( 7 ) );'
wp cron event list --hook=pagesco_books_lab_reminder --fields=hook,recurrence,args

# Clean up: wp_clear_scheduled_hook() returns how many events it removed (args must match for the reminder).
printf 'Removed: '
wp eval 'echo wp_clear_scheduled_hook( "pagesco_books_lab_job" ), " + ", wp_clear_scheduled_hook( "pagesco_books_lab_reminder", array( 7 ) ), "\n";'
printf 'Left: '
wp eval 'echo (int) wp_next_scheduled( "pagesco_books_lab_job" ) + (int) wp_next_scheduled( "pagesco_books_lab_reminder", array( 7 ) ), "\n";'

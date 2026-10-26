<?php
/**
 * cron_audit_starter.php: what the server's scheduler would have to run, read from WP-Cron (Session 16, Lesson 8.4, lab C)
 * state: after:lesson_28
 * expect: the shop's job: TODO
 *
 * Before a live site gets DISABLE_WP_CRON (Lesson 8.4, "Scheduled tasks"), know what it schedules: how many events,
 * how often, the shop's own job, and the one line the server's crontab needs. From your project folder:
 *     cp labs/module-16/l8_4-deployment-maintenance/cron_audit_starter.php wordpress/
 *     wp eval-file --use-include cron_audit_starter.php
 * The count by schedule is done for you (_get_cron_array(): timestamp => hook => runs, each with its 'schedule').
 * TODO 1 to 3 each need one WordPress function or constant. Compare with "Expected when done" at the end.
 * When you are done: rm wordpress/cron_audit_starter.php
 */

$pagesco_by_schedule = array();
$pagesco_events      = 0;
foreach ( _get_cron_array() as $pagesco_hooks ) {
	foreach ( $pagesco_hooks as $pagesco_runs ) {
		foreach ( $pagesco_runs as $pagesco_run ) {
			$pagesco_name                          = $pagesco_run['schedule'] ? $pagesco_run['schedule'] : 'once';
			$pagesco_by_schedule[ $pagesco_name ] = ( $pagesco_by_schedule[ $pagesco_name ] ?? 0 ) + 1;
			++$pagesco_events;
		}
	}
}
ksort( $pagesco_by_schedule );
echo "scheduled events: $pagesco_events\n";
foreach ( $pagesco_by_schedule as $pagesco_name => $pagesco_count ) {
	printf( "  %-12s %d\n", $pagesco_name, $pagesco_count );
}

// TODO 1: the shop's job: its recurrence (wp_get_schedule()) and whether its next run (wp_next_scheduled()) is in the
//         future: print "the shop's job: pagesco_books_daily_sync, daily, next run scheduled: yes".
echo "the shop's job: TODO\n";

// TODO 2: "off" when DISABLE_WP_CRON is defined and true, else "on (the development default)".
echo "WP-Cron spawning on page views: TODO\n";

// TODO 3: the crontab line, with this site's WordPress folder (ABSPATH without its trailing slash).
echo "on the live server, its crontab needs:\n";
echo "TODO\n";

// Expected when done (cron_audit_solution.php, the course site after Lesson 8.3):
// scheduled events: 13
//   daily        6
//   hourly       1
//   twicedaily   4
//   weekly       2
// the shop's job: pagesco_books_daily_sync, daily, next run scheduled: yes
// WP-Cron spawning on page views: on (the development default)
// on the live server, its crontab needs:
// */5 * * * * cd /var/www/html && wp cron event run --due-now --quiet


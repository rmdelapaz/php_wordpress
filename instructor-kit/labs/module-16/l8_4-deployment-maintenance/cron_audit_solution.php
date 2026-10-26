<?php
/**
 * cron_audit_solution.php: what the server's scheduler would have to run, read from WP-Cron (Session 16, Lesson 8.4, lab C)
 * state: after:lesson_28
 * expect: the shop's job: pagesco_books_daily_sync, daily, next run scheduled: yes
 * expect: cd /var/www/html && wp cron event run --due-now --quiet
 *
 * Before a live site gets DISABLE_WP_CRON (Lesson 8.4, "Scheduled tasks"), know what it schedules: how many events,
 * how often, the shop's own job, and the one line the server's crontab needs. From your project folder:
 *     cp labs/module-16/l8_4-deployment-maintenance/cron_audit_solution.php wordpress/
 *     wp eval-file --use-include cron_audit_solution.php
 *     rm wordpress/cron_audit_solution.php
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

$pagesco_next = wp_next_scheduled( 'pagesco_books_daily_sync' );
printf(
	"the shop's job: pagesco_books_daily_sync, %s, next run scheduled: %s\n",
	wp_get_schedule( 'pagesco_books_daily_sync' ),
	$pagesco_next > time() ? 'yes' : 'no'
);

printf( "WP-Cron spawning on page views: %s\n", defined( 'DISABLE_WP_CRON' ) && DISABLE_WP_CRON ? 'off' : 'on (the development default)' );
echo "on the live server, its crontab needs:\n";
printf( "*/5 * * * * cd %s && wp cron event run --due-now --quiet\n", untrailingslashit( ABSPATH ) );

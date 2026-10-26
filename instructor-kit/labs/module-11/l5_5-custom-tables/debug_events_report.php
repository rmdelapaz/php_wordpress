<?php
/**
 * debug_events_report.php: an events report with three bugs (Session 11, Lesson 5.5, find-the-bug handout)
 * state: after:lesson_18
 * expect-error: doing_it_wrong, Warning
 *
 * A report on the events table of Lesson 5.5: the next three events with their seats, then the seats per location.
 * On the course site the six events have 125 seats in all (Café 70, Reading corner 40, Children's corner 15,
 * Front of the shop 0). It only reads. From your project folder:
 *     cp labs/module-11/l5_5-custom-tables/debug_events_report.php wordpress/
 *     wp eval-file --use-include debug_events_report.php
 * WordPress and PHP report two bugs. The third is SILENT: compare the seat numbers with the line above.
 * Fix all three; when you are done: rm wordpress/debug_events_report.php
 */
global $wpdb;
$pagesco_table = PagesCo\Books\EventsTable::name();

$pagesco_next = $wpdb->get_results(
	$wpdb->prepare( "SELECT title, starts_at FROM {$pagesco_table} ORDER BY starts_at LIMIT 3" )
);
foreach ( $pagesco_next as $pagesco_event ) {
	printf( "%s  %-26s %d seats\n", $pagesco_event->starts_at, $pagesco_event->title, $pagesco_event->capacity );
}

$pagesco_places = $wpdb->get_results(
	$wpdb->prepare( 'SELECT location, COUNT(capacity) AS seats FROM %i GROUP BY location ORDER BY seats DESC, location', $pagesco_table )
);
foreach ( $pagesco_places as $pagesco_place ) {
	printf( "%s: %d seats\n", $pagesco_place->location, $pagesco_place->seats );
}

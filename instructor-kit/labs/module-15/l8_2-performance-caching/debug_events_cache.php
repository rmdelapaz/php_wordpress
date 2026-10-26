<?php
/**
 * debug_events_cache.php: a cache in front of the events table, written in a hurry (Session 15, Lesson 8.2, find-the-bug handout)
 * state: after:lesson_26
 * expect-error: Warning
 *
 * pagesco_lab_events() keeps the events table's answers in the object cache, with the last-changed value of
 * Lesson 8.2 in the key. On a working course site the script prints the next event, the next three, the next
 * five (five titles) and the seats of those five. From your project folder:
 *     cp labs/module-15/l8_2-performance-caching/debug_events_cache.php wordpress/
 *     wp eval-file --use-include debug_events_cache.php
 * Two bugs announce themselves with a Warning. The third is SILENT: no message, just an answer that is wrong
 * (count the titles). Find all three, fix them one at a time, and run again after each fix. Then delete the copy:
 * rm wordpress/debug_events_cache.php
 */

/**
 * The next events, cached until the events table changes.
 *
 * @param int $limit How many events.
 * @return object[]
 */
function pagesco_lab_events( int $limit ): array {
	$key    = 'events:' . wp_cache_get_last_changed( 'pagesco_events' );
	$cached = wp_cache_get( $key, 'pagesco_lab' );
	if ( is_array( $cached ) ) {
		return $cached;
	}

	$events = PagesCo\Books\EventsTable::find( $limit );
	wp_cache_set( $key, $events, 'pagesco_lab' );

	return $events;
}

echo 'Next event: ', pagesco_lab_events( 1 )[0]->titel, "\n";
echo 'Next three: ', implode( ', ', wp_list_pluck( pagesco_lab_events( 3 ), 'title' ) ), "\n";
echo 'Next five:  ', implode( ', ', wp_list_pluck( pagesco_lab_events( 5 ), 'title' ) ), "\n";

foreach ( pagesco_lab_events( 5 ) as $pagesco_event ) {
	$pagesco_seats += (int) $pagesco_event->capacity;
}
echo 'Seats in those five: ', $pagesco_seats, "\n";

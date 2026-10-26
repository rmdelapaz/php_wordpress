<?php
/**
 * debug_event_counts.php: cached event counts per location, with three bugs (Session 14, Lesson 7.3, find-the-bug handout)
 * state: after:lesson_24
 * expect-error: Warning
 *
 * How many events are at the Café, and on the Rooftop? Each count comes from GET /pagesco/v1/events?location=...
 * (Lesson 7.2) over HTTP and is cached in a transient for ten minutes, so three page views should ask the API
 * once per location. From your project folder:
 *     cp labs/module-14/l7_3-external-apis-cron/debug_event_counts.php wordpress/
 *     wp eval-file --use-include debug_event_counts.php
 * Two bugs announce themselves with Warnings. The third is SILENT: it shows once the others are fixed, in the
 * "asked the API" number of one location. Find all three, fix them one at a time, run again after each fix.
 * When you are done: rm wordpress/debug_event_counts.php
 */
global $pagesco_asked;   // WP-CLI runs this file inside a function: the counter is global on purpose

/**
 * The number of events at a location, cached for ten minutes.
 */
function pagesco_lab_count_at( string $place ): int {
	global $pagesco_asked;

	$key    = 'pagesco_books_lab_count_' . sanitize_key( $place );
	$cached = get_transient( $key );
	if ( $cached ) {
		return (int) $cached;
	}

	++$pagesco_asked;
	$response = wp_remote_get( add_query_arg( 'location', rawurlencode( $place ), rest_url( 'pagesco/v1/events' ) ), array( 'timeout' => 3 ) );
	$data     = json_decode( wp_remote_retrieve_body( $response ), true );

	$count = 0;
	foreach ( $data['items'] as $event ) {
		++$count;
	}
	set_transient( $key, $count, 10 * MINUTE_IN_SECONDS );

	return $count;
}

foreach ( array( 'Café', 'Rooftop' ) as $pagesco_place ) {
	$pagesco_asked = 0;
	for ( $pagesco_view = 1; $pagesco_view <= 3; $pagesco_view++ ) {
		$pagesco_total = pagesco_lab_count_at( $pagesco_place );
	}
	printf( "%s: %d events (asked the API %d times in 3 views)\n", $pagesco_place, $pagesco_totals, $pagesco_asked );
	delete_transient( 'pagesco_books_lab_count_' . sanitize_key( $pagesco_place ) );
}

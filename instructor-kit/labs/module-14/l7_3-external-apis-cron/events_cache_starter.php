<?php
/**
 * events_cache_starter.php: a read-through cache in a transient, failures included (Session 14, Lesson 7.3, lab B)
 * state: after:lesson_24
 * expect: View 3: 5 events, error "TODO: no cache yet", requests so far: 3
 *
 * Lesson 7.3's sticky note: ask the API only when there is no fresh answer in the transient, cache a failure
 * briefly too, and never store false. The API is your own GET /pagesco/v1/events (Lesson 7.2), asked over HTTP;
 * the script counts the requests that really go out, then simulates a day without a connection.
 * From your project folder:
 *     cp labs/module-14/l7_3-external-apis-cron/events_cache_starter.php wordpress/
 *     wp eval-file --use-include events_cache_starter.php
 * As shipped every view asks again. Fill in the TODOs and compare with "Expected when done".
 * When you are done: rm wordpress/events_cache_starter.php
 */
const PAGESCO_LAB_TRANSIENT = 'pagesco_books_lab_events';

/**
 * The next events from the shop's own API, cached: 10 minutes for an answer, 1 minute for a failure.
 */
function pagesco_lab_events(): array {
	global $pagesco_requests;

	// TODO 1: get_transient( PAGESCO_LAB_TRANSIENT ): when it is an array, return it (no request).

	++$pagesco_requests;   // count the requests that really go out
	$response = wp_remote_get( rest_url( 'pagesco/v1/events' ), array( 'timeout' => 3 ) );
	$data     = is_wp_error( $response ) ? null : json_decode( wp_remote_retrieve_body( $response ), true );

	// TODO 2: a WP_Error, a status other than 200 or a body that is not an array: build
	//         array( 'items' => array(), 'error' => <the WP_Error's message, or 'Unexpected answer.'> ),
	//         store it for MINUTE_IN_SECONDS and return it. (Why not cache nothing? Why never false?)
	// TODO 3: success: array( 'items' => $data, 'error' => '' ), stored for 10 * MINUTE_IN_SECONDS, returned.
	return array(
		'items' => is_array( $data ) ? $data : array(),
		'error' => 'TODO: no cache yet',
	);
}

global $pagesco_requests;   // WP-CLI runs this file inside a function: make the counter global on purpose
$pagesco_requests = 0;
for ( $pagesco_view = 1; $pagesco_view <= 3; $pagesco_view++ ) {
	$pagesco_events = pagesco_lab_events();
	printf( "View %d: %d events, error \"%s\", requests so far: %d\n", $pagesco_view, count( $pagesco_events['items'] ), $pagesco_events['error'], $pagesco_requests );
}

// A bad day: the next request gets no connection (pre_http_request answers instead of the network).
delete_transient( PAGESCO_LAB_TRANSIENT );
add_filter( 'pre_http_request', fn() => new WP_Error( 'http_request_failed', 'cURL error 7: Failed to connect' ) );
for ( $pagesco_view = 1; $pagesco_view <= 2; $pagesco_view++ ) {
	$pagesco_events = pagesco_lab_events();
	printf( "After the failure, view %d: %d events, error \"%s\", requests so far: %d\n", $pagesco_view, count( $pagesco_events['items'] ), $pagesco_events['error'], $pagesco_requests );
}

// Clean up, and prove it: a transient is two rows in wp_options.
delete_transient( PAGESCO_LAB_TRANSIENT );
global $wpdb;
echo 'rows left: ', $wpdb->get_var( $wpdb->prepare( 'SELECT COUNT(*) FROM %i WHERE option_name LIKE %s', $wpdb->options, '%' . $wpdb->esc_like( PAGESCO_LAB_TRANSIENT ) ) ), "\n";

// Expected when done (events_cache_solution.php, the site after Lesson 7.2):
// View 1: 5 events, error "", requests so far: 1
// View 2: 5 events, error "", requests so far: 1
// View 3: 5 events, error "", requests so far: 1
// After the failure, view 1: 0 events, error "cURL error 7: Failed to connect", requests so far: 2
// After the failure, view 2: 0 events, error "cURL error 7: Failed to connect", requests so far: 2
// rows left: 0

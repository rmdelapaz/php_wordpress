<?php
/**
 * events_cache_solution.php: the instructor's reference for events_cache_starter.php (Session 14, Lesson 7.3, lab B)
 * state: after:lesson_24
 * expect: View 3: 5 events, error "", requests so far: 1
 * expect: After the failure, view 2: 0 events, error "cURL error 7: Failed to connect", requests so far: 2
 * expect: rows left: 0
 */
const PAGESCO_LAB_TRANSIENT = 'pagesco_books_lab_events';

/**
 * The next events from the shop's own API, cached: 10 minutes for an answer, 1 minute for a failure.
 * Never false in the cache: the value is always array( 'items' => ..., 'error' => ... ).
 */
function pagesco_lab_events(): array {
	global $pagesco_requests;

	$cached = get_transient( PAGESCO_LAB_TRANSIENT );
	if ( is_array( $cached ) ) {
		return $cached;
	}

	++$pagesco_requests;   // count the requests that really go out
	$response = wp_remote_get( rest_url( 'pagesco/v1/events' ), array( 'timeout' => 3 ) );
	$data     = is_wp_error( $response ) ? null : json_decode( wp_remote_retrieve_body( $response ), true );

	if ( is_wp_error( $response ) || 200 !== wp_remote_retrieve_response_code( $response ) || ! is_array( $data ) ) {
		$value = array(
			'items' => array(),
			'error' => is_wp_error( $response ) ? $response->get_error_message() : 'Unexpected answer.',
		);
		set_transient( PAGESCO_LAB_TRANSIENT, $value, MINUTE_IN_SECONDS );
		return $value;
	}

	$value = array(
		'items' => $data,
		'error' => '',
	);
	set_transient( PAGESCO_LAB_TRANSIENT, $value, 10 * MINUTE_IN_SECONDS );
	return $value;
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

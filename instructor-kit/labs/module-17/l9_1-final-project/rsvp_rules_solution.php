<?php
/**
 * rsvp_rules_solution.php: one rules function, answers with an HTTP status, a computed status (Session 17, Lesson 9.1, lab B)
 * state: after:lesson_29
 * expect: Jordan books Story time again    pagesco_rsvp_duplicate (409)
 * expect: Book club: Dune on 2027-11-05    past
 *
 * The reference for rsvp_rules_starter.php: seats at the shop's events (Lesson 5.5's events table, read only),
 * kept in memory, so the script changes nothing on your site.
 */
global $wpdb;

/**
 * The house rules for a seat at an event, in ONE place. Every door (a form, a REST route, a block) would call it.
 * It returns the event's title, or a WP_Error whose data names the HTTP status a door should answer with.
 *
 * @param int   $event_id The event.
 * @param int   $user_id  The customer, from the login (0 = a visitor).
 * @param array $seats    The seats so far, by reference: user ID => list of event IDs.
 * @return string|WP_Error
 */
function pagesco_lab_book_seat( int $event_id, int $user_id, array &$seats ) {
	global $wpdb;

	if ( ! $user_id ) {
		return new WP_Error( 'pagesco_rsvp_login_required', 'Log in to book a seat.', array( 'status' => 401 ) );
	}

	$pagesco_event = $wpdb->get_row(
		$wpdb->prepare( 'SELECT id, title, starts_at FROM %i WHERE id = %d', $wpdb->prefix . 'pagesco_events', $event_id )
	);
	if ( ! $pagesco_event ) {
		return new WP_Error( 'pagesco_rsvp_no_event', 'No event was found with that ID.', array( 'status' => 404 ) );
	}

	$pagesco_mine = $seats[ $user_id ] ?? array();
	if ( in_array( $event_id, $pagesco_mine, true ) ) {
		return new WP_Error( 'pagesco_rsvp_duplicate', 'You already have a seat at this event.', array( 'status' => 409 ) );
	}
	if ( count( $pagesco_mine ) >= 2 ) {
		return new WP_Error( 'pagesco_rsvp_limit', 'You already have 2 seats booked.', array( 'status' => 409 ) );
	}

	$seats[ $user_id ][] = $event_id;

	return $pagesco_event->title;
}

/**
 * Upcoming or past, computed from the start time and a moment ("now"), never stored.
 *
 * @param object $event An events row (starts_at in the site's time zone).
 * @param string $now   Y-m-d H:i:s in the site's time zone.
 */
function pagesco_lab_event_status( object $event, string $now ): string {
	return $event->starts_at < $now ? 'past' : 'upcoming';
}

$pagesco_seats  = array();
$pagesco_jordan = 4;   // Milestone 3's customer accounts: the script needs only their IDs, it adds no users
$pagesco_priya  = 5;

$pagesco_show = function ( $label, $result ) {
	printf( "%-32s %s\n", $label, is_wp_error( $result ) ? $result->get_error_code() . ' (' . $result->get_error_data()['status'] . ')' : $result );
};

$pagesco_show( 'A visitor books event 1', pagesco_lab_book_seat( 1, 0, $pagesco_seats ) );
$pagesco_show( 'Jordan books event 99', pagesco_lab_book_seat( 99, $pagesco_jordan, $pagesco_seats ) );
$pagesco_show( 'Jordan books event 2', pagesco_lab_book_seat( 2, $pagesco_jordan, $pagesco_seats ) );
$pagesco_show( 'Jordan books Story time again', pagesco_lab_book_seat( 2, $pagesco_jordan, $pagesco_seats ) );
$pagesco_show( 'Jordan books event 5', pagesco_lab_book_seat( 5, $pagesco_jordan, $pagesco_seats ) );
$pagesco_show( 'Jordan books event 7', pagesco_lab_book_seat( 7, $pagesco_jordan, $pagesco_seats ) );
$pagesco_show( 'Priya books event 7', pagesco_lab_book_seat( 7, $pagesco_priya, $pagesco_seats ) );

$pagesco_event = $wpdb->get_row( $wpdb->prepare( 'SELECT id, title, starts_at FROM %i WHERE id = %d', $wpdb->prefix . 'pagesco_events', 1 ) );
foreach ( array( '2027-11-04 18:00:00', '2027-11-05 09:00:00' ) as $pagesco_now ) {
	printf( "%s on %s    %s\n", $pagesco_event->title, substr( $pagesco_now, 0, 10 ), pagesco_lab_event_status( $pagesco_event, $pagesco_now ) );
}

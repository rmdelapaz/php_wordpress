<?php
/**
 * Plugin Name: Pages & Co. Opening Hours API (Session 14 lab)
 * Description: GET /wp-json/pagesco/v1/opening-hours: the shop's week, or one day with ?day=.
 * Text Domain: pagesco-opening-hours
 */

/**
 * The shop's week: opening and closing time, or null for a closed day.
 */
function pagesco_lab_week(): array {
	return array(
		'monday'    => array( '9:00', '18:00' ),
		'tuesday'   => array( '9:00', '18:00' ),
		'wednesday' => array( '9:00', '18:00' ),
		'thursday'  => array( '9:00', '21:00' ),
		'friday'    => array( '9:00', '18:00' ),
		'saturday'  => array( '10:00', '16:00' ),
		'sunday'    => null,
	);
}

/**
 * Registers the route on rest_api_init. Done for you: the method, the callback and the permission (a public read).
 */
function pagesco_lab_register_opening_hours() {
	register_rest_route(
		'pagesco/v1',
		'/opening-hours',
		array(
			'methods'             => WP_REST_Server::READABLE,
			'callback'            => 'pagesco_lab_get_opening_hours',
			'permission_callback' => '__return_true',
			// TODO 1: 'args' with one argument, day: a description, 'type' => 'string' and an 'enum' of the seven
			//         day names (array_keys( pagesco_lab_week() )), and NO default: "not sent" means the whole week.
			//         With a type and no callbacks, WordPress validates and sanitizes it for you (Lesson 7.2).
		)
	);
}
add_action( 'rest_api_init', 'pagesco_lab_register_opening_hours' );

/**
 * GET /pagesco/v1/opening-hours.
 *
 * @param WP_REST_Request $request The request.
 * @return WP_REST_Response
 */
function pagesco_lab_get_opening_hours( WP_REST_Request $request ) {
	// TODO 2: a helper pagesco_lab_prepare_day( string $day, ?array $hours ): array that returns
	//         array( 'day' => ..., 'closed' => true ) for a closed day (null), otherwise
	//         array( 'day' => ..., 'closed' => false, 'opens' => ..., 'closes' => ... ).
	// TODO 3: $request['day'] is already valid, or null when not sent: a day -> that one day; null -> all seven, in order
	//         (array_map( 'pagesco_lab_prepare_day', array_keys( $week ), $week )). Wrap with rest_ensure_response().
	return rest_ensure_response( array( 'todo' => 'TODO: the hours' ) );
}

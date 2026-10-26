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
 * Registers the route on rest_api_init, with its argument described by a schema.
 */
function pagesco_lab_register_opening_hours() {
	register_rest_route(
		'pagesco/v1',
		'/opening-hours',
		array(
			'methods'             => WP_REST_Server::READABLE,
			'callback'            => 'pagesco_lab_get_opening_hours',
			'permission_callback' => '__return_true',
			'args'                => array(
				'day' => array(
					'description' => __( 'One day of the week, in lowercase English. Without it: the whole week.', 'pagesco-opening-hours' ),
					'type'        => 'string',
					'enum'        => array_keys( pagesco_lab_week() ),
				),
			),
		)
	);
}
add_action( 'rest_api_init', 'pagesco_lab_register_opening_hours' );

/**
 * One day as the API shows it.
 */
function pagesco_lab_prepare_day( string $day, ?array $hours ): array {
	return null === $hours
		? array(
			'day'    => $day,
			'closed' => true,
		)
		: array(
			'day'    => $day,
			'closed' => false,
			'opens'  => $hours[0],
			'closes' => $hours[1],
		);
}

/**
 * GET /pagesco/v1/opening-hours: the whole week, or the day the (already validated) argument names.
 * An argument without a default is null when the client did not send it.
 *
 * @param WP_REST_Request $request The request.
 * @return WP_REST_Response
 */
function pagesco_lab_get_opening_hours( WP_REST_Request $request ) {
	$week = pagesco_lab_week();

	if ( null !== $request['day'] ) {
		return rest_ensure_response( pagesco_lab_prepare_day( $request['day'], $week[ $request['day'] ] ) );
	}

	return rest_ensure_response( array_map( 'pagesco_lab_prepare_day', array_keys( $week ), $week ) );
}

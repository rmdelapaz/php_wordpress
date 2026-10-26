<?php
/**
 * debug_staff_picks_route.php: a small route with three bugs, called without HTTP (Session 14, Lesson 7.2, find-the-bug handout)
 * state: after:lesson_23
 * expect-error: doing_it_wrong, Warning
 *
 * GET /pagesco/v1/picks?limit=2 should answer with the titles of the first books by title, at most 5, and a
 * request for a limit of 50 should be refused with 400. The script registers the route the way a plugin does
 * (on rest_api_init) and sends three requests internally with rest_do_request() (Lesson 7.2, Exercise 1).
 * From your project folder:
 *     cp labs/module-14/l7_2-custom-endpoints/debug_staff_picks_route.php wordpress/
 *     wp eval-file --use-include debug_staff_picks_route.php
 * WordPress reports one bug as "called incorrectly" (outside a REST request it prints the Notice), one is a
 * Warning. The third is SILENT: look at the status of the last request. Find all three, fix them one at a time,
 * run again after each fix. When you are done: rm wordpress/debug_staff_picks_route.php
 */
function pagesco_lab_register_picks() {
	register_rest_route(
		'pagesco/v1',
		'/picks',
		array(
			'methods'  => WP_REST_Server::READABLE,
			'callback' => 'pagesco_lab_get_picks',
			'args'     => array(
				'limit' => array(
					'type'              => 'integer',
					'default'           => 3,
					'minimum'           => 1,
					'maximum'           => 5,
					'sanitize_callback' => 'absint',
				),
			),
		)
	);
}
add_action( 'rest_api_init', 'pagesco_lab_register_picks' );

function pagesco_lab_get_picks( WP_REST_Request $request ) {
	$pagesco_params = $request->get_query_params();
	$pagesco_books  = get_posts(
		array(
			'post_type'      => 'book',
			'posts_per_page' => $pagesco_params['limit'],
			'orderby'        => 'title',
			'order'          => 'ASC',
		)
	);

	return rest_ensure_response( wp_list_pluck( $pagesco_books, 'post_title' ) );
}

foreach ( array( '?limit=2', '', '?limit=50' ) as $pagesco_query ) {
	$pagesco_request = new WP_REST_Request( 'GET', '/pagesco/v1/picks' );
	parse_str( ltrim( $pagesco_query, '?' ), $pagesco_args );
	$pagesco_request->set_query_params( $pagesco_args );

	$pagesco_response = rest_do_request( $pagesco_request );
	printf( "%-10s %d %s\n", $pagesco_query ? $pagesco_query : '(none)', $pagesco_response->get_status(), wp_json_encode( $pagesco_response->get_data() ) );
}

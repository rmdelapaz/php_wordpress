<?php
/**
 * Plugin Name: Pages & Co. Book Requests (Session 17 lab)
 * Description: A customer asks the shop to order a book. The rules function fires its own action; two listeners attach to it.
 */

/**
 * Saves a request (in memory, for the lab) and announces it: the function knows nothing about emails.
 *
 * @param string $title The book the customer wants.
 * @param string $login The customer's login.
 */
function pagesco_lab_save_request( string $title, string $login ): array {
	$request = array(
		'id'    => count( $GLOBALS['pagesco_lab_requests'] ?? array() ) + 1,
		'title' => $title,
		'login' => $login,
	);
	$GLOBALS['pagesco_lab_requests'][] = $request;

	/**
	 * Fires after a book request is saved.
	 *
	 * @param array  $request The saved request.
	 * @param string $title   The book's title.
	 */
	do_action( 'pagesco_lab_request_saved', $request, $title );

	return $request;
}

// The customer's note: priority 10 (the default), one argument is all it needs.
add_action(
	'pagesco_lab_request_saved',
	function ( $request ) {
		$GLOBALS['pagesco_lab_heard'][] = sprintf( '10 customer note: %s for %s', $request['title'], $request['login'] );
	}
);

// The shop's note runs AFTER the customer's (priority 20) and wants both arguments (accepted_args 2).
add_action(
	'pagesco_lab_request_saved',
	function ( $request, $title ) {
		$GLOBALS['pagesco_lab_heard'][] = sprintf( '20 shop note: order "%s" (request %d)', $title, $request['id'] );
	},
	20,
	2
);

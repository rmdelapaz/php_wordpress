<?php
/**
 * Plugin Name: Pages & Co. Book Requests (Session 17 lab)
 * Description: A customer asks the shop to order a book. The rules function should fire its own action; two listeners attach to it.
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

	// TODO 1: fire your own action 'pagesco_lab_request_saved' here, with two arguments: $request and $title
	// (the moment others may want to act at, like pagesco_books_hold_placed in Milestone 3). Give it a docblock.

	return $request;
}

// The customer's note: priority 10 (the default), one argument is all it needs.
add_action(
	'pagesco_lab_request_saved',
	function ( $request ) {
		$GLOBALS['pagesco_lab_heard'][] = sprintf( '10 customer note: %s for %s', $request['title'], $request['login'] );
	}
);

// TODO 2: the shop's note. Add a second listener to the same action that stores
//     sprintf( '20 shop note: order "%s" (request %d)', $title, $request['id'] )
// in $GLOBALS['pagesco_lab_heard'][]. It must run AFTER the customer's note and needs BOTH arguments: give
// add_action() a priority and an accepted-arguments count (Lesson 2.3). Without the count, PHP stops with an
// ArgumentCountError: try it once.

<?php
/**
 * test_own_action.php: saves two requests and prints what the listeners heard (Session 17, Lesson 9.1, lab C)
 * serve: own_action
 * install: mu-plugin
 * state: after:lesson_29
 * expect-starter: Listeners heard: nothing yet (TODO 1)
 * expect-solution: 20 shop note: order "Dune" (request 1)
 *
 * The rules function fires an action; the notes are listeners. From your project folder, with the plugin and
 * this test copied in:
 *     cp labs/module-17/l9_1-final-project/own_action_starter/pagesco-lab-requests.php wordpress/wp-content/mu-plugins/
 *     cp labs/module-17/l9_1-final-project/test_own_action.php wordpress/
 *     wp eval-file --use-include test_own_action.php
 * When you are done: rm wordpress/test_own_action.php wordpress/wp-content/mu-plugins/pagesco-lab-requests.php
 */
if ( ! function_exists( 'pagesco_lab_save_request' ) ) {
	echo "pagesco_lab_save_request() is missing: is pagesco-lab-requests.php in wp-content/mu-plugins/?\n";
	return;
}

$GLOBALS['pagesco_lab_heard'] = array();
pagesco_lab_save_request( 'Dune', 'jordan' );
pagesco_lab_save_request( 'Emma', 'priya' );

$pagesco_hook = $GLOBALS['wp_filter']['pagesco_lab_request_saved'] ?? null;
printf( "Listeners on the action: %d\n", $pagesco_hook ? array_sum( array_map( 'count', $pagesco_hook->callbacks ) ) : 0 );
if ( ! $GLOBALS['pagesco_lab_heard'] ) {
	echo "Listeners heard: nothing yet (TODO 1)\n";
}
foreach ( $GLOBALS['pagesco_lab_heard'] as $pagesco_line ) {
	echo $pagesco_line, "\n";
}

<?php
/**
 * Plugin Name: Pages & Co. Next Event (Session 15 lab)
 * Description: The next event from the events table, in the footer of every page. Written in a hurry.
 *
 * TODO: bring PHPCS to "no findings" (test_next_event.sh runs it with the plugin's own ruleset from Lesson 8.1),
 * without changing what a visitor sees. Read each message from the left: the line, ERROR or WARNING, the message,
 * and the rule in brackets. [x] marks what phpcbf could fix for you; fix those by hand too.
 */

function pagesco_books_lab_next_event() {
	$events = PagesCo\Books\EventsTable::find( 1 );
	if ( ! $events ) {
		return;
	}
	$event = $events[0];
	echo '<p class="pagesco-next-event">' . sprintf( __( 'Next event: %s', 'pagesco' ), $event->title ) . '</p>';
}
add_action( 'wp_footer', 'pagesco_books_lab_next_event' );

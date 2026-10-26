<?php
/**
 * Plugin Name: Pages & Co. Next Event (Session 15 lab)
 * Description: The next event from the events table, in the footer of every page.
 *
 * @package PagesCo\Books
 */

/**
 * Prints the next event from the events table (Lesson 5.5) in the footer.
 */
function pagesco_books_lab_next_event() {
	$events = PagesCo\Books\EventsTable::find( 1 );
	if ( ! $events ) {
		return;
	}
	$event = $events[0];

	printf(
		'<p class="pagesco-next-event">%s</p>',
		/* translators: %s: the event's title. */
		esc_html( sprintf( __( 'Next event: %s', 'pagesco-books' ), $event->title ) )
	);
}
add_action( 'wp_footer', 'pagesco_books_lab_next_event' );

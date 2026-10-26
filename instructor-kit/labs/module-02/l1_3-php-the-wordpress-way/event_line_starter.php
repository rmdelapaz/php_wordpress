<?php
/**
 * event_line_starter.php: an array of arguments, translatable strings and WP_Error (Session 2, Lesson 1.3, lab B)
 * state: fresh
 * expect: TODO: Book club: Dune
 *
 * Lesson 1.3's "Arrays of Arguments and WP_Error", "Strings Ready for Translation" and "Callbacks in Every
 * Shape", on the shop's events list. From your project folder:
 *     cp labs/module-02/l1_3-php-the-wordpress-way/event_line_starter.php wordpress/
 *     wp eval-file --use-include event_line_starter.php
 * Do the TODOs in order, run again after each one, and compare with "Expected when done" at the end.
 * When you are done: rm wordpress/event_line_starter.php
 */

/**
 * Returns one line of the events list, escaped for HTML text.
 *
 * @param array        $event { @type string $title  @type string $date Y-m-d  @type int $seats }
 * @param array|string $args  { @type bool $show_seats Default true. @type string $date_format Default 'l, F j'.
 *                              @type string $before Text in front of the line. Default ''. }
 * @return string|WP_Error The line, or a WP_Error when the event has no date.
 */
function pagesco_lab_event_line( $event, $args = array() ) {
	// TODO 1: merge $args over the three defaults of the DocBlock with wp_parse_args().
	// TODO 2: an event without a date: return new WP_Error( 'pagesco_no_date', __( 'The event has no date.', 'pagesco' ) );
	// TODO 3: the line: $args['before'] . sprintf( __( '%1$s on %2$s', 'pagesco' ), title, date ), with a
	//         translators comment above the __() line; the date is date_i18n( $args['date_format'], strtotime( ... ) ).
	// TODO 4: when show_seats is true, add ' · ' and the seats: sprintf( _n( '%s seat left', '%s seats left',
	//         $count, 'pagesco' ), number_format_i18n( $count ) ), with its own translators comment.
	// TODO 5: return the line escaped for HTML text.
	return 'TODO: ' . $event['title'];
}

/**
 * Sort callback: the earlier event first (usort() calls it with two events).
 *
 * @param array $a One event.
 * @param array $b Another event.
 * @return int Negative, zero or positive.
 */
function pagesco_lab_by_date( $a, $b ) {
	return 0; // TODO 6: compare the two dates (Y-m-d strings sort like text: strcmp()).
}

$pagesco_events = array(
	array( 'title' => 'Author reading: Ada Quill', 'date' => '2026-11-12', 'seats' => 24 ),
	array( 'title' => 'Book club: Dune', 'date' => '2026-10-01', 'seats' => 1 ),
	array( 'title' => 'Story time & cocoa', 'date' => '2026-10-17', 'seats' => 0 ),
	array( 'title' => 'Poetry night', 'date' => '', 'seats' => 30 ),
);

usort( $pagesco_events, 'pagesco_lab_by_date' );

foreach ( $pagesco_events as $pagesco_event ) {
	$pagesco_line = pagesco_lab_event_line( $pagesco_event );
	// TODO 7: when $pagesco_line is a WP_Error, print "skipped: <message> (<code>)" and continue.
	echo $pagesco_line, "\n";
}

// Two more calls: options as an array, and as a query string (wp_parse_args() accepts both).
echo pagesco_lab_event_line( $pagesco_events[1], array( 'show_seats' => false ) ), "\n";
echo pagesco_lab_event_line( $pagesco_events[3], 'before=New: &date_format=M j' ), "\n";

// Expected when done (event_line_solution.php, the course site):
// skipped: The event has no date. (pagesco_no_date)
// Book club: Dune on Thursday, October 1 · 1 seat left
// Story time &amp; cocoa on Saturday, October 17 · 0 seats left
// Author reading: Ada Quill on Thursday, November 12 · 24 seats left
// Book club: Dune on Thursday, October 1
// New: Author reading: Ada Quill on Nov 12 · 24 seats left

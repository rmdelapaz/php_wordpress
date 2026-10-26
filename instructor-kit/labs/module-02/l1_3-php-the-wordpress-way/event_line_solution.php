<?php
/**
 * event_line_solution.php: the instructor's reference for event_line_starter.php (Session 2, Lesson 1.3, lab B)
 * state: fresh
 * expect: Book club: Dune on Thursday, October 1 · 1 seat left
 * expect: skipped: The event has no date. (pagesco_no_date)
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
	$args = wp_parse_args(
		$args,
		array(
			'show_seats'  => true,
			'date_format' => 'l, F j',
			'before'      => '',
		)
	);

	if ( empty( $event['date'] ) ) {
		return new WP_Error( 'pagesco_no_date', __( 'The event has no date.', 'pagesco' ) );
	}

	$line = $args['before'] . sprintf(
		/* translators: 1: event title, 2: date. */
		__( '%1$s on %2$s', 'pagesco' ),
		$event['title'],
		date_i18n( $args['date_format'], strtotime( $event['date'] ) )
	);
	if ( $args['show_seats'] ) {
		$line .= ' · ' . sprintf(
			/* translators: %s: number of seats left. */
			_n( '%s seat left', '%s seats left', (int) $event['seats'], 'pagesco' ),
			number_format_i18n( (int) $event['seats'] )
		);
	}
	return esc_html( $line );
}

/**
 * Sort callback: the earlier event first (usort() calls it with two events).
 *
 * @param array $a One event.
 * @param array $b Another event.
 * @return int Negative, zero or positive.
 */
function pagesco_lab_by_date( $a, $b ) {
	return strcmp( $a['date'], $b['date'] );
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
	if ( is_wp_error( $pagesco_line ) ) {
		echo 'skipped: ', esc_html( $pagesco_line->get_error_message() ), ' (', esc_html( $pagesco_line->get_error_code() ), ")\n";
		continue;
	}
	echo $pagesco_line, "\n"; // phpcs:ignore WordPress.Security.EscapeOutput -- escaped inside the function.
}

echo pagesco_lab_event_line( $pagesco_events[1], array( 'show_seats' => false ) ), "\n"; // phpcs:ignore WordPress.Security.EscapeOutput
echo pagesco_lab_event_line( $pagesco_events[3], 'before=New: &date_format=M j' ), "\n"; // phpcs:ignore WordPress.Security.EscapeOutput

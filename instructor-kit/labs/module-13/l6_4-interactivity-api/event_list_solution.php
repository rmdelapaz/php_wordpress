<?php
/**
 * event_list_solution.php: the instructor's reference for event_list_starter.php (Session 13, Lesson 6.4, lab B)
 * state: after:lesson_21
 * expect: <li data-wp-each-child="pagesco/events::state.events" hidden data-wp-bind--hidden="state.isElsewhere"><time data-wp-text="context.event.when">Nov 4</time>
 * expect: Showing 2 of 5 events
 */
$pagesco_events = array();
foreach ( PagesCo\Books\EventsTable::find( 5 ) as $pagesco_row ) {
	$pagesco_events[] = array(
		'id'    => (int) $pagesco_row->id,
		'title' => $pagesco_row->title,
		'where' => $pagesco_row->location,
		'when'  => mysql2date( 'M j', $pagesco_row->starts_at ),
	);
}

wp_interactivity_state(
	'pagesco/events',
	array(
		'events'      => $pagesco_events,
		'location'    => 'Café',
		'total'       => count( $pagesco_events ),
		// Derived: an event is hidden when a location is chosen and the event is somewhere else.
		'isElsewhere' => function () {
			$pagesco_state = wp_interactivity_state();
			return '' !== $pagesco_state['location'] && $pagesco_state['location'] !== wp_interactivity_get_context()['event']['where'];
		},
		'shown'       => function () {
			$pagesco_state = wp_interactivity_state();
			return count( wp_list_filter( $pagesco_state['events'], array( 'where' => $pagesco_state['location'] ) ) );
		},
	)
);

$pagesco_html = '<div data-wp-interactive="pagesco/events">'
	. '<p>Showing <span data-wp-text="state.shown"></span> of <span data-wp-text="state.total"></span> events</p><ul>'
	. '<template data-wp-each--event="state.events" data-wp-each-key="context.event.id">'
	. '<li data-wp-bind--hidden="state.isElsewhere"><time data-wp-text="context.event.when"></time> <span data-wp-text="context.event.title"></span></li>'
	. '</template></ul></div>';

$pagesco_out = wp_interactivity_process_directives( $pagesco_html );
// The <template> stays (the browser uses it to add items); the server also printed one <li> per event after it.
echo wp_strip_all_tags( explode( '<ul>', $pagesco_out )[0] ), "\n";
preg_match_all( '#<li[^>]*>.*?</li>#', explode( '</template>', $pagesco_out )[1], $pagesco_items );
echo implode( "\n", $pagesco_items[0] ), "\n";

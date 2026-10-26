<?php
/**
 * event_list_starter.php: a list the server repeats from state with data-wp-each (Session 13, Lesson 6.4, lab B)
 * state: after:lesson_21
 * expect: (no <li> yet: TODO 1)
 *
 * Lesson 6.4's directive table lists data-wp-each: a <template> repeated once per item of a list in the state.
 * The server runs it too, so the events are in the HTML before any JavaScript, and a store could later push more
 * (the "Load more" design of Lesson 7.2). Here: the next five events, with only the Café's shown.
 * From your project folder:
 *     cp labs/module-13/l6_4-interactivity-api/event_list_starter.php wordpress/
 *     wp eval-file --use-include event_list_starter.php
 * Fill in the TODOs, run again after each one, and compare with "Expected when done".
 * When you are done: rm wordpress/event_list_starter.php
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
		'events'   => array(),   // TODO 1: the state's list is $pagesco_events (plain data: it travels as JSON).
		'location' => 'Café',
		'total'    => count( $pagesco_events ),
		// TODO 2: 'isElsewhere' => a closure: true when the state's location is not '' and differs from the
		//         context's event's where. Inside data-wp-each, the context is array( 'event' => <one item> ).
		// TODO 3: 'shown' => a closure: how many events are at the state's location
		//         (count( wp_list_filter( $state['events'], array( 'where' => ... ) ) )).
	)
);

// TODO 4: give the <li> the directive data-wp-bind--hidden="state.isElsewhere".
$pagesco_html = '<div data-wp-interactive="pagesco/events">'
	. '<p>Showing <span data-wp-text="state.shown"></span> of <span data-wp-text="state.total"></span> events</p><ul>'
	. '<template data-wp-each--event="state.events" data-wp-each-key="context.event.id">'
	. '<li><time data-wp-text="context.event.when"></time> <span data-wp-text="context.event.title"></span></li>'
	. '</template></ul></div>';

$pagesco_out = wp_interactivity_process_directives( $pagesco_html );
// The <template> stays (the browser uses it to add items); the server also printed one <li> per event after it.
echo wp_strip_all_tags( explode( '<ul>', $pagesco_out )[0] ), "\n";
preg_match_all( '#<li[^>]*>.*?</li>#', explode( '</template>', $pagesco_out )[1], $pagesco_items );
echo $pagesco_items[0] ? implode( "\n", $pagesco_items[0] ) : '(no <li> yet: TODO 1)', "\n";

// Expected when done (event_list_solution.php, the site after Lesson 6.3):
// Showing 2 of 5 events
// <li data-wp-each-child="pagesco/events::state.events" hidden data-wp-bind--hidden="state.isElsewhere"><time data-wp-text="context.event.when">Nov 4</time> <span data-wp-text="context.event.title">Book club: Dune</span></li>
// <li data-wp-each-child="pagesco/events::state.events" hidden data-wp-bind--hidden="state.isElsewhere"><time data-wp-text="context.event.when">Nov 6</time> <span data-wp-text="context.event.title">Story time: The Hobbit</span></li>
// <li data-wp-each-child="pagesco/events::state.events" data-wp-bind--hidden="state.isElsewhere"><time data-wp-text="context.event.when">Nov 11</time> <span data-wp-text="context.event.title">An evening with Ana Ruiz</span></li>
// <li data-wp-each-child="pagesco/events::state.events" data-wp-bind--hidden="state.isElsewhere"><time data-wp-text="context.event.when">Nov 18</time> <span data-wp-text="context.event.title">Poetry open mic</span></li>
// <li data-wp-each-child="pagesco/events::state.events" hidden data-wp-bind--hidden="state.isElsewhere"><time data-wp-text="context.event.when">Dec 2</time> <span data-wp-text="context.event.title">Book club: Fahrenheit 451</span></li>

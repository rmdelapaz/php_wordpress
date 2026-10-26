<?php
/**
 * Renders pagesco/next-events on the server, on every view. WordPress passes $attributes, $content and $block.
 *
 * @package PagesCo\Books
 */

use PagesCo\Books\EventsTable;
use PagesCo\Books\Settings;

// TODO 1: the count. count has NO default in block.json, so it is missing when nobody chose one: use isset().
//         No count: (int) Settings::get( 'events_limit' ) (Lesson 5.4). Then clamp it to 1 to 10.
// TODO 2: $events = EventsTable::find( $count, ... ) with the location attribute through sanitize_text_field().
// TODO 3: no events: print <p WRAPPER>No events at this location yet.</p> (esc_html__) and return.
// TODO 4: otherwise <ul WRAPPER> with one <li> per event:
//         <li><time datetime="2027-11-04T19:00">Nov 4</time> Book club: Dune</li>
//         mysql2date( 'Y-m-d\TH:i', $event->starts_at, false ) for datetime, mysql2date( 'M j', ... ) for the text;
//         escape every value. WRAPPER = get_block_wrapper_attributes() (already escaped: print it as it is).
printf( '<p %s>TODO: the next events</p>', get_block_wrapper_attributes() );

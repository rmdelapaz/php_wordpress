<?php
/**
 * checkpoint_starter.php: Checkpoint 2 (Modules 5 and 6), the Weekly Picks report (Session 13)
 * state: after:lesson_21
 * expect: A  Under $10, in stock: TODO
 * expect: C2 Staff picks post: 0 Book Card, comment attributes {"TODO":true}
 *
 * 25 minutes, on your own, open notes (the lesson pages, your plugin's code). The shop wants a weekly report for
 * its newsletter, built from the plugin's data. Write the bodies of the four functions below (Parts A to C); do
 * not change the main section at the end. Part D (three written answers) is on your workbook's Checkpoint page.
 * The script must change nothing on the site. From your project folder:
 *     cp labs/module-13/checkpoint-2/checkpoint_starter.php wordpress/checkpoint_YOURNAME.php
 *     wp eval-file --use-include checkpoint_YOURNAME.php
 * Hand in the file (and leave it in wordpress/ until your instructor has run it; then delete it).
 */

/**
 * Part A (Lessons 5.2, 5.3): books in stock that cost at most $max, cheapest first, as "Title ($8.49)".
 * One query: meta_query for the price (a number: 'type' => 'DECIMAL(10,2)') and the stock ('1'), sorted by
 * meta_value_num on pagesco_price.
 *
 * @param float $max The highest price.
 * @return string[]
 */
function pagesco_cp_cheap_books( float $max ): array {
	return array( 'TODO' );
}

/**
 * Part B (Lesson 5.5): how many events take place at a location: one COUNT query on the events table
 * (PagesCo\Books\EventsTable::name()). The location comes from anyone: never put it into SQL yourself.
 *
 * @param string $location The exact location, as typed by anyone.
 */
function pagesco_cp_events_at( string $location ): int {
	return -1;
}

/**
 * Part C1 (Lesson 6.3): render a Book List block for a genre, cheapest first (its comment with the attributes
 * genre and orderBy, through do_blocks()), and return the book titles from its links.
 *
 * @param string $genre A genre slug.
 * @return string[]
 */
function pagesco_cp_list_titles( string $genre ): array {
	return array( 'TODO' );
}

/**
 * Part C2 (Lesson 6.2): how many Book Cards the post stores, and the comment attributes of the first one.
 *
 * @param string $slug A post slug.
 * @return array{count: int, attrs: array}
 */
function pagesco_cp_cards_in( string $slug ): array {
	return array(
		'count' => 0,
		'attrs' => array( 'TODO' => true ),
	);
}

// ---------------------------------------------------------------- main: the same in the starter
echo 'A  Under $10, in stock: ', esc_html( implode( ', ', pagesco_cp_cheap_books( 10.0 ) ) ), "\n";

$pagesco_places = array( 'Café', 'Rooftop', "Reading corner'; DROP TABLE x; --" );
echo 'B  ', implode( ' · ', array_map( fn( $place ) => $place . ': ' . pagesco_cp_events_at( $place ) . ' events', $pagesco_places ) ), "\n";

echo 'C1 Fantasy, cheapest first: ', esc_html( implode( ', ', pagesco_cp_list_titles( 'fantasy' ) ) ), "\n";

$pagesco_cards = pagesco_cp_cards_in( 'staff-picks' );
printf( "C2 Staff picks post: %d Book Card, comment attributes %s\n", $pagesco_cards['count'], wp_json_encode( $pagesco_cards['attrs'] ) );

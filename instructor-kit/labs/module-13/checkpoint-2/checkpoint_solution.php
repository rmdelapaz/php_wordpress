<?php
/**
 * checkpoint_solution.php: Checkpoint 2 (Modules 5 and 6), the Weekly Picks report: MODEL ANSWER (Session 13)
 * state: after:lesson_21
 * expect: A  Under $10, in stock: Pride and Prejudice ($7.99), Animal Farm ($8.49), Brave New World ($9.49), 1984 ($9.99)
 * expect: B  Café: 2 events · Rooftop: 0 events · Reading corner'; DROP TABLE x; --: 0 events
 * expect: C1 Fantasy, cheapest first: The Hobbit, Lord of the Rings
 * expect: C2 Staff picks post: 1 Book Card, comment attributes {"backgroundColor":"sage"}
 *
 * Instructor copy. The shop wants a weekly report for its newsletter, built from the plugin's data: Parts A to C
 * are the scored code (three functions); Part D (three written answers) is on the workbook's Checkpoint page.
 * The main section at the end is the same in the starter, and the script changes nothing on the site.
 * Run: wp eval-file --use-include checkpoint_solution.php
 */

/**
 * Part A (Lessons 5.2, 5.3): books in stock that cost at most $max, cheapest first, as "Title ($8.49)".
 *
 * @param float $max The highest price.
 * @return string[]
 */
function pagesco_cp_cheap_books( float $max ): array {
	$books = get_posts(
		array(
			'post_type'      => 'book',
			'post_status'    => 'publish',
			'posts_per_page' => -1,
			'meta_key'       => 'pagesco_price',
			'orderby'        => 'meta_value_num',
			'order'          => 'ASC',
			'meta_query'     => array(
				array(
					'key'     => 'pagesco_price',
					'value'   => $max,
					'compare' => '<=',
					'type'    => 'DECIMAL(10,2)',
				),
				array(
					'key'   => 'pagesco_in_stock',
					'value' => '1',
				),
			),
		)
	);

	$lines = array();
	foreach ( $books as $book ) {
		$lines[] = sprintf( '%s ($%s)', $book->post_title, number_format_i18n( (float) get_post_meta( $book->ID, 'pagesco_price', true ), 2 ) );
	}

	return $lines;
}

/**
 * Part B (Lesson 5.5): how many events take place at a location: one prepared COUNT query on the events table.
 *
 * @param string $location The exact location, as typed by anyone.
 */
function pagesco_cp_events_at( string $location ): int {
	global $wpdb;

	return (int) $wpdb->get_var(
		$wpdb->prepare( 'SELECT COUNT(*) FROM %i WHERE location = %s', PagesCo\Books\EventsTable::name(), $location )
	);
}

/**
 * Part C (Lessons 6.2, 6.3): C1 renders a Book List block for a genre, cheapest first, and returns its titles;
 * C2 describes the Book Cards stored in a post.
 *
 * @param string $genre A genre slug.
 * @return string[]
 */
function pagesco_cp_list_titles( string $genre ): array {
	$attributes = array(
		'genre'   => $genre,
		'orderBy' => 'price',
	);
	$html       = do_blocks( '<!-- wp:pagesco/book-list ' . wp_json_encode( $attributes ) . ' /-->' );

	preg_match_all( '#<a href="[^"]*">([^<]*)</a>#', $html, $found );

	return $found[1];
}

/**
 * @param string $slug A post slug.
 * @return array{count: int, attrs: array}
 */
function pagesco_cp_cards_in( string $slug ): array {
	$post  = get_page_by_path( $slug, OBJECT, 'post' );
	$cards = array_values( wp_list_filter( parse_blocks( $post ? $post->post_content : '' ), array( 'blockName' => 'pagesco/book-card' ) ) );

	return array(
		'count' => count( $cards ),
		'attrs' => $cards ? $cards[0]['attrs'] : array(),
	);
}

// ---------------------------------------------------------------- main: the same in the starter
echo 'A  Under $10, in stock: ', esc_html( implode( ', ', pagesco_cp_cheap_books( 10.0 ) ) ), "\n";

$pagesco_places = array( 'Café', 'Rooftop', "Reading corner'; DROP TABLE x; --" );
echo 'B  ', implode( ' · ', array_map( fn( $place ) => $place . ': ' . pagesco_cp_events_at( $place ) . ' events', $pagesco_places ) ), "\n";

echo 'C1 Fantasy, cheapest first: ', esc_html( implode( ', ', pagesco_cp_list_titles( 'fantasy' ) ) ), "\n";

$pagesco_cards = pagesco_cp_cards_in( 'staff-picks' );
printf( "C2 Staff picks post: %d Book Card, comment attributes %s\n", $pagesco_cards['count'], wp_json_encode( $pagesco_cards['attrs'] ) );

<?php
/**
 * cheapest_cache_solution.php: a cached query whose key knows when the data changed (Session 15, Lesson 8.2, lab B)
 * state: after:lesson_26
 * expect: after Dune's price drop: 1 query, Dune at $1.99
 * expect: Dune's price restored to 14.99
 *
 * The last-changed pattern of Lesson 8.2's EventsTable, on a query of your own: "the cheapest book". One group
 * timestamp in the cache key; every write renews it, so no old answer is ever read again. From your project folder:
 *     cp labs/module-15/l8_2-performance-caching/cheapest_cache_solution.php wordpress/
 *     wp eval-file --use-include cheapest_cache_solution.php
 *     rm wordpress/cheapest_cache_solution.php
 * The script changes Dune's price and sets it back at the end.
 */

/**
 * The cheapest book and its price, from the database or from the object cache.
 */
function pagesco_lab_cheapest(): string {
	global $wpdb;

	$key    = 'cheapest:' . wp_cache_get_last_changed( 'pagesco_lab' );
	$cached = wp_cache_get( $key, 'pagesco_lab' );
	if ( is_string( $cached ) ) {
		return $cached;
	}

	$row = $wpdb->get_row(
		$wpdb->prepare(
			"SELECT p.post_title, m.meta_value FROM %i AS p INNER JOIN %i AS m ON m.post_id = p.ID
			WHERE p.post_type = 'book' AND p.post_status = 'publish' AND m.meta_key = 'pagesco_price'
			ORDER BY m.meta_value + 0 ASC LIMIT 1",
			$wpdb->posts,
			$wpdb->postmeta
		)
	);
	$answer = sprintf( '%s at $%s', $row->post_title, $row->meta_value );
	wp_cache_set( $key, $answer, 'pagesco_lab' );

	return $answer;
}

/**
 * Changes a book's price: every write to the data the cache depends on renews the group's last-changed value.
 *
 * @param int    $book_id The book.
 * @param string $price   The new price.
 */
function pagesco_lab_set_price( int $book_id, string $price ): void {
	update_post_meta( $book_id, 'pagesco_price', $price );
	wp_cache_set_last_changed( 'pagesco_lab' );
}

/**
 * Prints one call of pagesco_lab_cheapest() with the queries it made.
 *
 * @param string $label When the call happens.
 */
function pagesco_lab_ask( string $label ): void {
	global $wpdb;

	$before = $wpdb->num_queries;
	$answer = pagesco_lab_cheapest();
	$count  = $wpdb->num_queries - $before;
	printf( "%s: %d %s, %s\n", $label, $count, 1 === $count ? 'query' : 'queries', $answer );
}

$pagesco_dune  = get_page_by_path( 'dune', OBJECT, 'book' )->ID;
$pagesco_price = get_post_meta( $pagesco_dune, 'pagesco_price', true );

pagesco_lab_ask( 'first call' );
pagesco_lab_ask( 'second call' );
pagesco_lab_set_price( $pagesco_dune, '1.99' );
pagesco_lab_ask( "after Dune's price drop" );
pagesco_lab_set_price( $pagesco_dune, $pagesco_price );
pagesco_lab_ask( 'after the price is back' );
printf( "Dune's price restored to %s\n", get_post_meta( $pagesco_dune, 'pagesco_price', true ) );

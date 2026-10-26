<?php
/**
 * shelf_report_solution.php: four questions about the catalog, asked in PHP (Session 9, Lesson 5.2, lab B, reference)
 * state: after:lesson_15
 * expect: Cheapest in stock: Pride and Prejudice ($7.99)
 * expect: Published before 1950:
 */

// 1. Every genre with the number of books filed under it (the term's count column).
foreach ( get_terms( array( 'taxonomy' => 'genre', 'hide_empty' => false, 'orderby' => 'term_id' ) ) as $pagesco_term ) {
	printf( "%-16s %d\n", $pagesco_term->name . ':', $pagesco_term->count );
}

// 2. The cheapest book in stock: a meta_query to filter, meta_value_num to sort as a number.
$pagesco_cheapest = get_posts(
	array(
		'post_type'   => 'book',
		'numberposts' => 1,
		'meta_query'  => array(
			array(
				'key'   => 'pagesco_in_stock',
				'value' => '1',
			),
		),
		'meta_key'    => 'pagesco_price',
		'orderby'     => 'meta_value_num',
		'order'       => 'ASC',
	)
);
printf( "Cheapest in stock: %s ($%s)\n", $pagesco_cheapest[0]->post_title, get_post_meta( $pagesco_cheapest[0]->ID, 'pagesco_price', true ) );

// 3. The average price of all books.
$pagesco_ids    = get_posts( array( 'post_type' => 'book', 'numberposts' => -1, 'fields' => 'ids' ) );
$pagesco_prices = array_map( fn( $pagesco_id ) => (float) get_post_meta( $pagesco_id, 'pagesco_price', true ), $pagesco_ids );
echo 'Average price: $', number_format( array_sum( $pagesco_prices ) / count( $pagesco_prices ), 2 ), "\n";

// 4. Books first published before 1950: compare the Y-m-d strings as dates.
$pagesco_old = get_posts(
	array(
		'post_type'   => 'book',
		'numberposts' => -1,
		'fields'      => 'ids',
		'meta_query'  => array(
			array(
				'key'     => 'pagesco_published',
				'value'   => '1950-01-01',
				'compare' => '<',
				'type'    => 'DATE',
			),
		),
	)
);
echo 'Published before 1950: ', count( $pagesco_old ), "\n";

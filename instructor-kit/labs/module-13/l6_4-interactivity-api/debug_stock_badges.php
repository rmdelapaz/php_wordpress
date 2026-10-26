<?php
/**
 * debug_stock_badges.php: server-rendered stock badges with three bugs (Session 13, Lesson 6.4, find-the-bug handout)
 * state: after:lesson_21
 * expect-error: doing_it_wrong, Warning
 *
 * Three books, each with a "Sold out" badge that must be hidden while the book is in stock, a heading that names
 * the shop, and the number of books in stock. The server processes the directives, as for an interactive block.
 * From your project folder:
 *     cp labs/module-13/l6_4-interactivity-api/debug_stock_badges.php wordpress/
 *     wp eval-file --use-include debug_stock_badges.php
 * One bug makes WordPress say it was "called incorrectly" (a Notice), one is a Warning. The third is SILENT:
 * look at the count. Find all three, fix them one at a time, run again after each fix. When you are done:
 *     rm wordpress/debug_stock_badges.php
 */
$pagesco_books = array();
foreach ( array( 30, 33, 37 ) as $pagesco_id ) {
	$pagesco_books[] = array(
		'title'   => get_the_title( $pagesco_id ),
		'inStock' => (bool) get_post_meta( $pagesco_id, 'pagesco_in_stock', true ),
	);
}

wp_interactivity_state(
	'pagesco/badges',
	array(
		'shop'    => 'Pages & Co.',
		'books'   => $pagesco_books,
		'isSold'  => function () {
			return ! wp_interactivity_get_context()['instock'];
		},
		'inStock' => function () {
			return count( wp_list_filter( wp_interactivity_state( 'pagesco/badge' )['books'] ?? array(), array( 'inStock' => true ) ) );
		},
	)
);

$pagesco_html = '<h2 data-wp-text="state.shop"></h2><div data-wp-interactive="pagesco/badges">'
	. '<p>In stock: <span data-wp-text="state.inStock"></span></p><ul>';
foreach ( $pagesco_books as $pagesco_book ) {
	$pagesco_html .= '<li ' . wp_interactivity_data_wp_context( $pagesco_book ) . '>' . esc_html( $pagesco_book['title'] )
		. ' <span class="badge" data-wp-bind--hidden="!state.isSold">Sold out</span></li>';
}
$pagesco_html .= '</ul></div>';

echo str_replace( array( '<div', '<li' ), array( "\n<div", "\n<li" ), wp_interactivity_process_directives( $pagesco_html ) ), "\n";

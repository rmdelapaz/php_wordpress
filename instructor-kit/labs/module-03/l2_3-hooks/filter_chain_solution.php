<?php
/**
 * filter_chain_solution.php: the instructor's reference for filter_chain_starter.php (Session 3, Lesson 2.3, lab A)
 * state: after:lesson_04
 * expect: Removed the sale badge: true
 * expect: Line: Fahrenheit 451 by Ray Bradbury
 */

// Already in the site: a "plugin" that marks every book line as on sale.
function pagesco_lab_sale_badge( $line ) {
	return $line . ' [SALE]';
}
add_filter( 'pagesco_lab_book_line', 'pagesco_lab_sale_badge', 30 );

function pagesco_lab_capitalize( $line ) {
	return ucwords( $line );
}
add_filter( 'pagesco_lab_book_line', 'pagesco_lab_capitalize', 5 );

function pagesco_lab_add_author( $line, $author ) {
	return $line . ' by ' . $author;
}
add_filter( 'pagesco_lab_book_line', 'pagesco_lab_add_author', 10, 2 );

echo 'Removed the sale badge: ', var_export( remove_filter( 'pagesco_lab_book_line', 'pagesco_lab_sale_badge', 30 ), true ), "\n";

echo 'pagesco_lab_capitalize: ', var_export( has_filter( 'pagesco_lab_book_line', 'pagesco_lab_capitalize' ), true ), "\n";
echo 'pagesco_lab_add_author: ', var_export( has_filter( 'pagesco_lab_book_line', 'pagesco_lab_add_author' ), true ), "\n";
echo 'pagesco_lab_sale_badge: ', var_export( has_filter( 'pagesco_lab_book_line', 'pagesco_lab_sale_badge' ), true ), "\n";

echo 'Line: ', apply_filters( 'pagesco_lab_book_line', 'fahrenheit 451', 'Ray Bradbury' ), "\n";

<?php
/**
 * debug_price_tag.php: a price passed through four filters, with three hook bugs (Session 3, Lesson 2.3, find-the-bug handout)
 * state: after:lesson_04
 * expect-error: Deprecated, Warning
 *
 * A shelf price of 14.987 (after a discount) goes through the filter pagesco_lab_price: rounded, formatted,
 * labeled. A holiday markup the shop no longer wants is removed. From your project folder:
 *     cp labs/module-03/l2_3-hooks/debug_price_tag.php wordpress/
 *     wp eval-file --use-include debug_price_tag.php
 * Two bugs are loud (a Deprecated and a Warning), one is silent. Read each message from the left, and when a
 * message points at a line that looks fine, ask what the callback BEFORE it handed over (Lesson 2.3, Common
 * Mistakes 1). Done: no message, and the last line reads
 *     Pages & Co. price: $14.99
 * Then delete the copy: rm wordpress/debug_price_tag.php
 */

$pagesco_shop_name = 'Pages & Co.';

function pagesco_lab_round_price( $price ) {
	$price = round( $price, 2 );
}
add_filter( 'pagesco_lab_price', 'pagesco_lab_round_price', 5 );

function pagesco_lab_format_price( $price ) {
	return number_format( $price, 2 );
}
add_filter( 'pagesco_lab_price', 'pagesco_lab_format_price', 10 );

function pagesco_lab_holiday_markup( $price ) {
	return $price . ' (holiday price)';
}
add_filter( 'pagesco_lab_price', 'pagesco_lab_holiday_markup', 15 );

function pagesco_lab_price_label( $price ) {
	return $pagesco_shop_name . ' price: $' . $price;
}
add_filter( 'pagesco_lab_price', 'pagesco_lab_price_label', 20 );

// The holidays are over: no more markup.
remove_filter( 'pagesco_lab_price', 'pagesco_lab_holiday_markup' );

echo apply_filters( 'pagesco_lab_price', 14.987 ), "\n";

<?php
/**
 * debug_book_search.php: a price search with three bugs (Session 10, Lesson 5.3, find-the-bug handout)
 * state: after:lesson_15
 * expect-error: doing_it_wrong
 *
 * A report for the shop's "under $10" shelf, typed in a hurry: the books under a price, and how many of them are in
 * stock. On the Lesson 5.2 catalog the first query should find the five books under $9.99. From your project folder:
 *     cp labs/module-10/l5_3-security/debug_book_search.php wordpress/
 *     wp eval-file --use-include debug_book_search.php
 * WordPress reports two of the bugs ("wpdb::prepare was called incorrectly"). The third is SILENT: the count is
 * wrong without any message. Fix all three; when you are done: rm wordpress/debug_book_search.php
 */
global $wpdb;
$pagesco_max = absint( '9.99' );   // what a visitor typed into the price box

$pagesco_titles = $wpdb->get_col(
	$wpdb->prepare(
		"SELECT p.post_title FROM {$wpdb->posts} p INNER JOIN {$wpdb->postmeta} m ON m.post_id = p.ID WHERE m.meta_key = 'pagesco_price' AND m.meta_value + 0 < %f ORDER BY m.meta_value + 0",
		$pagesco_max
	)
);
echo 'Under $', $pagesco_max, ': ', count( $pagesco_titles ), ' book(s): ', implode( ', ', $pagesco_titles ), "\n";

$pagesco_in_stock = $wpdb->get_var(
	$wpdb->prepare(
		"SELECT COUNT(*) FROM {$wpdb->postmeta} WHERE meta_key = 'pagesco_in_stock' AND meta_value = '1'",
		$pagesco_max
	)
);
echo 'In stock (whole catalog): ', $pagesco_in_stock, "\n";

$pagesco_cheapest = $wpdb->get_var(
	$wpdb->prepare(
		"SELECT MIN(meta_value + 0) FROM {$wpdb->postmeta} WHERE meta_key = %s AND meta_value + 0 < %f",
		'pagesco_price'
	)
);
echo 'Cheapest: $', $pagesco_cheapest, "\n";

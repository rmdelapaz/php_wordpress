<?php
/**
 * debug_stock_list.php: a stock list read from the REST API, with three bugs (Session 13, Lesson 7.1, find-the-bug handout)
 * state: after:lesson_22
 * expect-error: Warning
 *
 * A script that a partner shop might run: ask the public REST API for the catalog and print every book with
 * "in stock" or "sold out", then the total the API reports. It calls the site over HTTP, like any outside program.
 * From your project folder:
 *     cp labs/module-13/l7_1-rest-api/debug_stock_list.php wordpress/
 *     wp eval-file --use-include debug_stock_list.php
 * Two bugs announce themselves with Warnings. The third is SILENT: count the books, and compare with the total
 * (the partner wants every book, four per request).
 * Find all three, fix them one at a time, run again after each fix. When you are done:
 *     rm wordpress/debug_stock_list.php
 */
$pagesco_response = wp_remote_get( rest_url( 'wp/v2/books?per_page=4&orderby=title&order=asc&_fields=id,title' ) );
$pagesco_books    = json_decode( wp_remote_retrieve_body( $pagesco_response ), true );

foreach ( $pagesco_books as $pagesco_book ) {
	$pagesco_stock = $pagesco_book['meta']['pagesco_in_stock'] ? 'in stock' : 'sold out';
	echo $pagesco_book['title'], ': ', $pagesco_stock, "\n";
}
echo 'Total in the catalog: ', wp_remote_retrieve_header( $pagesco_response, 'x-wp-total' ), "\n";

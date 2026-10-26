<?php
/**
 * debug_supplier_log.php: a quick look at the supplier, with a log line per request (Session 15, Lesson 8.1, find-the-bug handout)
 * state: after:lesson_25
 * expect-error: Warning
 *
 * A colleague wanted to see what the supplier says about three books, and how the requests look, so the script
 * logs every outgoing request with the http_api_debug action (as Lesson 8.1's case did). On a working course site it
 * should print three lines with the number of copies, and write one line to wp-content/debug.log. From your
 * project folder:
 *     cp labs/module-15/l8_1-debugging-testing/debug_supplier_log.php wordpress/
 *     wp eval-file --use-include debug_supplier_log.php
 *     tail -n 3 wordpress/wp-content/debug.log
 * Two bugs announce themselves with Warnings (read each from the left: level, message, file, line). The third
 * makes no message at all: it is in what the script writes to the log once the first Warning is gone. Fix them one
 * at a time, run again after each fix, and read the log each time. Then delete the copy:
 * rm wordpress/debug_supplier_log.php
 */

// Log each request to the supplier: method, address and the key it sends.
add_action(
	'http_api_debug',
	function ( $response, $context, $transport, $args, $url ) {
		error_log( sprintf( 'supplier %s %s, key %s', $args['method'], strtok( $url, '?' ), $args['headers']['X-API-Key'] ) );
	},
	10,
	5
);

// Three books by their slugs, and their ISBNs.
$pagesco_isbns = array();
foreach ( array( 'dune', '1984', 'hobbit' ) as $pagesco_slug ) {
	$pagesco_book                   = get_page_by_path( $pagesco_slug, OBJECT, 'book' );
	$pagesco_isbns[ $pagesco_slug ] = get_post_meta( $pagesco_book->ID, 'pagesco_isbn', true );
}

// One request for all three, then one line per book.
$pagesco_answer = ( new PagesCo\Books\Supplier\Client() )->availability( array_values( array_filter( $pagesco_isbns ) ) );
foreach ( $pagesco_isbns as $pagesco_slug => $pagesco_isbn ) {
	printf( "%-12s %d copies at the supplier\n", $pagesco_slug, $pagesco_answer[ $pagesco_isbn ]['available'] ?? 0 );
}

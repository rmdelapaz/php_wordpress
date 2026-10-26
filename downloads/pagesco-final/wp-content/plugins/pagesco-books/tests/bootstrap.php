<?php
/**
 * Starts WordPress for the plugin's PHPUnit tests. Run them inside wp-env (see .wp-env.json).
 *
 * @package PagesCo\Books
 */

$pagesco_books_tests_dir = getenv( 'WP_TESTS_DIR' );

if ( ! $pagesco_books_tests_dir || ! file_exists( $pagesco_books_tests_dir . '/includes/functions.php' ) ) {
	echo "The WordPress test library was not found. Run the tests inside wp-env.\n";
	exit( 1 );
}

// The plugin's Composer autoloader, which also loads the PHPUnit Polyfills the test library needs.
require_once dirname( __DIR__ ) . '/vendor/autoload.php';

// The supplier in tests: an address that is never called, because the tests answer for it.
define( 'PAGESCO_BOOKS_SUPPLIER_URL', 'https://api.riverside.example/v1/' );
define( 'PAGESCO_BOOKS_SUPPLIER_KEY', 'test-key' );

require_once $pagesco_books_tests_dir . '/includes/functions.php';

// Load the plugin as early as a must-use plugin, before WordPress starts.
tests_add_filter(
	'muplugins_loaded',
	function () {
		require dirname( __DIR__ ) . '/pagesco-books.php';
	}
);

require $pagesco_books_tests_dir . '/includes/bootstrap.php';

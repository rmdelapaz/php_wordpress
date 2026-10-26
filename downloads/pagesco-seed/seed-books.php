<?php
/**
 * Seeds the Pages & Co. catalog: the genres and the 11 books from books.json.
 *
 * Run from the WordPress root with WP-CLI: wp eval-file pagesco-seed/seed-books.php
 * Safe to run twice: books and genres that already exist are skipped.
 *
 * @package PagesCo\Books
 */

defined( 'ABSPATH' ) || exit;

if ( ! post_type_exists( 'book' ) || ! taxonomy_exists( 'genre' ) ) {
	WP_CLI::error( 'Activate the pagesco-books plugin first: the book post type and the genre taxonomy are missing.' );
}

$pagesco_data = json_decode( file_get_contents( __DIR__ . '/books.json' ), true );

// The genres, in this order, so their IDs are the same on every site.
foreach ( array( 'Fiction', 'Science Fiction', 'Classic', 'Fantasy', 'Dystopian' ) as $pagesco_genre ) {
	if ( ! term_exists( $pagesco_genre, 'genre' ) ) {
		$pagesco_term = wp_insert_term( $pagesco_genre, 'genre' );
		WP_CLI::log( sprintf( 'Genre %d: %s', $pagesco_term['term_id'], $pagesco_genre ) );
	}
}

$pagesco_editor = get_user_by( 'login', 'maria' );

foreach ( $pagesco_data['books'] as $pagesco_book ) {
	$pagesco_slug = sanitize_title( $pagesco_book['title'] );

	if ( get_page_by_path( $pagesco_slug, OBJECT, 'book' ) ) {
		WP_CLI::log( "Skipped {$pagesco_book['title']}: it already exists." );
		continue;
	}

	$pagesco_id = wp_insert_post(
		array(
			'post_type'   => 'book',
			'post_status' => 'publish',
			'post_title'  => $pagesco_book['title'],
			'post_name'   => $pagesco_slug,
			'post_author' => $pagesco_editor ? $pagesco_editor->ID : 1,
			// Fixed IDs (Dune is 30 ... Animal Farm is 40) so the whole class matches.
			'import_id'   => 29 + $pagesco_book['bookstore_id'],
			// One minute apart, so "newest first" lists are the same on every site.
			'post_date'   => gmdate( 'Y-m-d H:i:s', strtotime( '2026-10-01 10:00:00' ) + 60 * $pagesco_book['bookstore_id'] ),
			'meta_input'  => array(
				'pagesco_author'    => $pagesco_book['author'],
				'pagesco_price'     => $pagesco_book['price'],
				'pagesco_pages'     => $pagesco_book['pages'],
				'pagesco_published' => $pagesco_book['published'],
				'pagesco_in_stock'  => $pagesco_book['in_stock'],
			),
		),
		true
	);

	if ( is_wp_error( $pagesco_id ) ) {
		WP_CLI::warning( "{$pagesco_book['title']}: " . $pagesco_id->get_error_message() );
		continue;
	}

	// wp_set_object_terms(), not tax_input: see Common Mistakes.
	wp_set_object_terms( $pagesco_id, $pagesco_book['genres'], 'genre' );

	WP_CLI::log( sprintf( 'Book %d: %s', $pagesco_id, $pagesco_book['title'] ) );
}

WP_CLI::success( sprintf( '%d books in the catalog.', wp_count_posts( 'book' )->publish ) );

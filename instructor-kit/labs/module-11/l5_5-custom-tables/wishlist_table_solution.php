<?php
/**
 * wishlist_table_solution.php: a custom table's whole life in one script (Session 11, Lesson 5.5, lab A, reference)
 * state: after:lesson_17
 * expect: Created table wp_pagesco_lab_wishlist
 * expect: Dune: 2 reader(s)
 * expect: tables left: 0
 *
 * A throwaway {prefix}pagesco_lab_wishlist table: which reader wants which book. Created with dbDelta(), filled
 * with $wpdb->insert() and its formats, read with prepare() and %i, changed, then dropped again.
 */
require_once ABSPATH . 'wp-admin/includes/upgrade.php';
global $wpdb;
$pagesco_table = $wpdb->prefix . 'pagesco_lab_wishlist';

// 1. Create it: one column or index per line, PRIMARY KEY with two spaces, the site's collation.
$pagesco_collate = $wpdb->get_charset_collate();
$pagesco_result  = dbDelta(
	"CREATE TABLE {$pagesco_table} (
	id bigint unsigned NOT NULL AUTO_INCREMENT,
	book_id bigint unsigned NOT NULL,
	reader varchar(100) NOT NULL,
	added_at datetime NOT NULL,
	PRIMARY KEY  (id),
	KEY book_id (book_id)
) {$pagesco_collate};"
);
echo implode( "\n", $pagesco_result ), "\n";

// 2. Four wishes: every value through the format array.
foreach ( array( array( 30, 'Priya Shah' ), array( 35, 'Tomas Berg' ), array( 30, 'Lena Ortiz' ), array( 39, 'Priya Shah' ) ) as list( $pagesco_book, $pagesco_reader ) ) {
	$wpdb->insert(
		$pagesco_table,
		array(
			'book_id'  => $pagesco_book,
			'reader'   => $pagesco_reader,
			'added_at' => current_time( 'mysql', true ),
		),
		array( '%d', '%s', '%s' )
	);
}
echo 'rows: ', $wpdb->get_var( $wpdb->prepare( 'SELECT COUNT(*) FROM %i', $pagesco_table ) ), ', last ID ', $wpdb->insert_id, "\n";

// 3. The most wished-for books, with their titles from wp_posts.
$pagesco_rows = $wpdb->get_results(
	$wpdb->prepare(
		'SELECT p.post_title, COUNT(*) AS readers FROM %i w INNER JOIN %i p ON p.ID = w.book_id GROUP BY p.ID, p.post_title ORDER BY readers DESC, p.post_title',
		$pagesco_table,
		$wpdb->posts
	)
);
foreach ( $pagesco_rows as $pagesco_row ) {
	printf( "%s: %d reader(s)\n", $pagesco_row->post_title, $pagesco_row->readers );
}

// 4. Priya changes her mind about Fahrenheit 451 (book 39): it becomes Brave New World (36).
$pagesco_changed = $wpdb->update( $pagesco_table, array( 'book_id' => 36 ), array( 'reader' => 'Priya Shah', 'book_id' => 39 ), array( '%d' ), array( '%s', '%d' ) );
echo "updated: {$pagesco_changed} row(s)\n";

// 5. Drop it again, and check that it is gone.
$wpdb->query( $wpdb->prepare( 'DROP TABLE IF EXISTS %i', $pagesco_table ) );
echo 'tables left: ', $wpdb->get_var( $wpdb->prepare( 'SELECT COUNT(*) FROM information_schema.TABLES WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s', $pagesco_table ) ), "\n";

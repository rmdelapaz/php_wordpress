<?php
/**
 * Removes the plugin's data when an administrator deletes the plugin.
 *
 * Always: the role, the settings, the events and holds tables and the supplier transient (Lessons 5.4, 5.5, 7.3, 9.1).
 * Only when an administrator turned on "Delete all books, genres and book details": the shop's content too (Lesson 8.3).
 *
 * @package PagesCo\Books
 */

defined( 'WP_UNINSTALL_PLUGIN' ) || exit;

global $wpdb;

// Read the choice before the settings are deleted below. The plugin is not loaded: no Settings class here.
$pagesco_books_settings = get_option( 'pagesco_books_settings', array() );

if ( is_array( $pagesco_books_settings ) && ! empty( $pagesco_books_settings['delete_data'] ) ) {
	// Every book in every status, trash included. wp_delete_post() also deletes its meta and term links.
	$pagesco_books_ids = get_posts(
		array(
			'post_type'   => 'book',
			'post_status' => array_keys( get_post_stati() ),
			'numberposts' => -1,
			'fields'      => 'ids',
		)
	);
	foreach ( $pagesco_books_ids as $pagesco_books_id ) {
		wp_delete_post( $pagesco_books_id, true );
	}

	// The taxonomy is not registered while the plugin is uninstalled: register it, or get_terms() fails.
	register_taxonomy( 'genre', 'book' );
	$pagesco_books_terms = get_terms(
		array(
			'taxonomy'   => 'genre',
			'hide_empty' => false,
			'fields'     => 'ids',
		)
	);
	foreach ( is_array( $pagesco_books_terms ) ? $pagesco_books_terms : array() as $pagesco_books_term ) {
		wp_delete_term( $pagesco_books_term, 'genre' );
	}
}

remove_role( 'pagesco_bookseller' );
delete_option( 'pagesco_books_settings' );
delete_option( 'pagesco_books_db_version' );
delete_option( 'pagesco_books_holds_db_version' );

$wpdb->query( $wpdb->prepare( 'DROP TABLE IF EXISTS %i', $wpdb->prefix . 'pagesco_events' ) );
$wpdb->query( $wpdb->prepare( 'DROP TABLE IF EXISTS %i', $wpdb->prefix . 'pagesco_holds' ) );

delete_transient( 'pagesco_books_supplier_availability' );

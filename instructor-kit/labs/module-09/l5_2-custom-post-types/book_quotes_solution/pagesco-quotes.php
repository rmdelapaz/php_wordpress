<?php
/**
 * Plugin Name:       Pages & Co. Book Quotes (Session 9 lab)
 * Description:       A "quote" post type: favorite lines from the shop's books, each with the book it comes from.
 * Version:           0.1.0
 * Requires at least: 6.8
 * Requires PHP:      8.2
 * Text Domain:       pagesco-quotes
 */
defined( 'ABSPATH' ) || exit;

/**
 * Registers the quote post type and its meta key. Runs on init.
 */
function pagesco_quotes_register() {
	register_post_type(
		'pagesco_quote',
		array(
			'labels'       => array(
				'name'          => __( 'Quotes', 'pagesco-quotes' ),
				'singular_name' => __( 'Quote', 'pagesco-quotes' ),
			),
			'public'       => true,
			'has_archive'  => 'quotes',
			'rewrite'      => array( 'slug' => 'quotes' ),
			'show_in_rest' => true,
			'rest_base'    => 'quotes',
			'supports'     => array( 'title', 'editor', 'custom-fields' ),
		)
	);
	register_post_meta(
		'pagesco_quote',
		'pagesco_quote_source',
		array(
			'type'         => 'string',
			'single'       => true,
			'show_in_rest' => true,
		)
	);
}
add_action( 'init', 'pagesco_quotes_register' );

/**
 * Runs once, on activation: init has already run on this request, so register first, then flush.
 */
function pagesco_quotes_activate() {
	pagesco_quotes_register();
	flush_rewrite_rules();
}
register_activation_hook( __FILE__, 'pagesco_quotes_activate' );

/**
 * Runs once, on deactivation: the type's URLs stop answering while the plugin is off.
 */
function pagesco_quotes_deactivate() {
	unregister_post_type( 'pagesco_quote' );
	flush_rewrite_rules();
}
register_deactivation_hook( __FILE__, 'pagesco_quotes_deactivate' );

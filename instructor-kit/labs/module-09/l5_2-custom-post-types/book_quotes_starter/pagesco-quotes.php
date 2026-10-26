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
 * Registers the quote post type (and, after TODO 3, its meta key). Runs on init.
 */
function pagesco_quotes_register() {
	register_post_type(
		'pagesco_quote',
		array(
			'labels'       => array(
				'name'          => __( 'Quotes', 'pagesco-quotes' ),
				'singular_name' => __( 'Quote', 'pagesco-quotes' ),
			),
			'public'       => false,   // TODO 1: public, with an archive at /quotes/ (has_archive and the rewrite slug)
			'show_in_rest' => false,   // TODO 2: in the REST API, at /wp/v2/quotes (rest_base)
			'supports'     => array( 'title', 'editor', 'custom-fields' ),
		)
	);
	// TODO 3: register the meta key pagesco_quote_source for this type: a string (the book the quote comes from),
	// one value per quote, shown in REST. No leading underscore: why not? (Lesson 5.2, "Book Meta")
}
add_action( 'init', 'pagesco_quotes_register' );

/**
 * Runs once, on activation.
 */
function pagesco_quotes_activate() {
	// TODO 4: on this request init has already run: register the type yourself, THEN flush the rewrite rules.
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

<?php
/**
 * Pages & Co. TT5 Child functions and definitions.
 *
 * @package pagesco-tt5-child
 */

/**
 * Loads the child theme's style.css after the parent's styles.
 */
function pagesco_tt5_child_enqueue_styles() {
	wp_enqueue_style(
		'pagesco-tt5-child-style',
		get_stylesheet_uri(),
		array( 'twentytwentyfive-style' ),
		wp_get_theme()->get( 'Version' )
	);
}
add_action( 'wp_enqueue_scripts', 'pagesco_tt5_child_enqueue_styles' );

/**
 * Replaces the parent's post format support: the shop only uses asides and quotes.
 *
 * Twenty Twenty-Five wraps this function in function_exists(), and the child's
 * functions.php loads first, so this definition wins.
 */
function twentytwentyfive_post_format_setup() {
	add_theme_support( 'post-formats', array( 'aside', 'quote' ) );
}

/**
 * Removes parent features the shop does not want.
 *
 * Runs on after_setup_theme, when the parent's functions.php has added its hooks.
 */
function pagesco_tt5_child_remove_parent_features() {
	remove_action( 'init', 'twentytwentyfive_block_styles' );
}
add_action( 'after_setup_theme', 'pagesco_tt5_child_remove_parent_features' );

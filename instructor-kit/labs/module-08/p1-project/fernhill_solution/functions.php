<?php
/**
 * Fernhill functions and definitions.
 *
 * @package fernhill
 */

/**
 * Registers the theme's own pattern category.
 */
function fernhill_register_pattern_categories() {
	register_block_pattern_category(
		'fernhill',
		array(
			'label'       => __( 'Fernhill Garden', 'fernhill' ),
			'description' => __( 'Sections designed for the Fernhill Community Garden website.', 'fernhill' ),
		)
	);
}
add_action( 'init', 'fernhill_register_pattern_categories' );

/**
 * Loads the theme's small stylesheet, versioned with the theme.
 */
function fernhill_enqueue_assets() {
	wp_enqueue_style(
		'fernhill-style',
		get_theme_file_uri( 'assets/css/fernhill.css' ),
		array(),
		wp_get_theme( get_template() )->get( 'Version' )
	);
}
add_action( 'wp_enqueue_scripts', 'fernhill_enqueue_assets' );

/**
 * Shows three news posts per page on the blog home (the front page of this site).
 *
 * @param WP_Query $query The query WordPress is about to run.
 */
function fernhill_adjust_main_query( $query ) {
	if ( is_admin() || ! $query->is_main_query() ) {
		return;
	}

	if ( $query->is_home() ) {
		$query->set( 'posts_per_page', 3 );
	}
}
add_action( 'pre_get_posts', 'fernhill_adjust_main_query' );

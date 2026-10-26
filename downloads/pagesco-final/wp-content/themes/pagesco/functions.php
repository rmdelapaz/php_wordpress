<?php
/**
 * Pages & Co. functions and definitions.
 *
 * @package pagesco
 */

/**
 * Registers the theme's own pattern category.
 */
function pagesco_register_pattern_categories() {
	register_block_pattern_category(
		'pagesco',
		array(
			'label'       => __( 'Pages & Co.', 'pagesco' ),
			'description' => __( 'Sections designed for the Pages & Co. website.', 'pagesco' ),
		)
	);
}
add_action( 'init', 'pagesco_register_pattern_categories' );

/**
 * Tells the browser, in the head of the front page, to fetch the hero image early and first:
 * it is the page's largest element, so it decides the Largest Contentful Paint (Lesson 8.2).
 *
 * @param array $resources Resources to preload, each an array of link attributes.
 * @return array
 */
function pagesco_preload_hero_image( $resources ) {
	if ( is_front_page() ) {
		$resources[] = array(
			'href'          => get_theme_file_uri( 'assets/images/book-image.webp' ),
			'as'            => 'image',
			'fetchpriority' => 'high',
		);
	}
	return $resources;
}
add_filter( 'wp_preload_resources', 'pagesco_preload_hero_image' );

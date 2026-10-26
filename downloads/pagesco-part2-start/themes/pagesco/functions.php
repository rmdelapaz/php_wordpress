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

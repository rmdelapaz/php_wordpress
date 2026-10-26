<?php
/**
 * Pages & Co. Lab: TT4 Child functions (Session 5, Lesson 3.4, lab A: the reference solution).
 *
 * @package pagesco-lab-tt4-child
 */

/**
 * Loads the child's style.css. Twenty Twenty-Four enqueues no stylesheet of its own (its CSS is theme.json
 * plus per-block files), so there is no parent handle to depend on.
 */
function pagesco_lab_tt4_child_enqueue_styles() {
	wp_enqueue_style(
		'pagesco-lab-tt4-child-style',
		get_stylesheet_uri(),
		array(),
		wp_get_theme()->get( 'Version' )
	);
}
add_action( 'wp_enqueue_scripts', 'pagesco_lab_tt4_child_enqueue_styles' );

/**
 * Replaces the parent's pluggable block styles: the reading corner keeps only the checkmark list.
 *
 * The child's functions.php loads first, so when the parent reaches its function_exists() check, this
 * function already exists and the parent's five styles are never registered.
 */
function twentytwentyfour_block_styles() {
	register_block_style(
		'core/list',
		array(
			'name'  => 'checkmark-list',
			'label' => __( 'Checkmark', 'pagesco-lab-tt4-child' ),
		)
	);
}

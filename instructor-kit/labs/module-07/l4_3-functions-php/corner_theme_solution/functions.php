<?php
/**
 * Pages & Co. Lab: Reading Corner functions (Session 7, Lesson 4.3, lab A: the reference solution).
 *
 * @package pagesco-lab-corner
 */

/**
 * The features WordPress should provide: the <title> and HTML5 search forms.
 */
function pagesco_lab_corner_setup() {
	add_theme_support( 'title-tag' );
	add_theme_support( 'html5', array( 'search-form' ) );
}
add_action( 'after_setup_theme', 'pagesco_lab_corner_setup' );

/**
 * The stylesheet and the script, versioned with the theme.
 */
function pagesco_lab_corner_assets() {
	$version = wp_get_theme( get_template() )->get( 'Version' );

	wp_enqueue_style( 'pagesco-lab-corner-style', get_parent_theme_file_uri( 'style.css' ), array(), $version );
	wp_enqueue_script(
		'pagesco-lab-corner-script',
		get_parent_theme_file_uri( 'assets/corner.js' ),
		array(),
		$version,
		array(
			'strategy'  => 'defer',
			'in_footer' => true,
		)
	);
}
add_action( 'wp_enqueue_scripts', 'pagesco_lab_corner_assets' );

/**
 * The menu location the header prints.
 */
function pagesco_lab_corner_menus() {
	register_nav_menus( array( 'corner' => __( 'Reading corner menu', 'pagesco-lab-corner' ) ) );
}
add_action( 'after_setup_theme', 'pagesco_lab_corner_menus' );

/**
 * The footer widget area.
 */
function pagesco_lab_corner_widgets() {
	register_sidebar(
		array(
			'id'            => 'corner-footer',
			'name'          => __( 'Reading corner footer', 'pagesco-lab-corner' ),
			'before_widget' => '<section id="%1$s" class="widget %2$s">',
			'after_widget'  => '</section>',
		)
	);
}
add_action( 'widgets_init', 'pagesco_lab_corner_widgets' );

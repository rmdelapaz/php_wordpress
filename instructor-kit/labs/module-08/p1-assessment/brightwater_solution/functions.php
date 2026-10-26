<?php
/**
 * Brightwater functions and definitions.
 *
 * @package brightwater
 */

/**
 * Sets up the theme features WordPress should provide, and the menu location.
 */
function brightwater_setup() {
	add_theme_support( 'title-tag' );
	add_theme_support( 'html5', array( 'search-form', 'comment-form', 'comment-list', 'gallery', 'caption' ) );

	register_nav_menus(
		array(
			'primary' => __( 'Primary menu', 'brightwater' ),
		)
	);
}
add_action( 'after_setup_theme', 'brightwater_setup' );

/**
 * Loads the theme's stylesheet, versioned with the theme.
 */
function brightwater_enqueue_assets() {
	wp_enqueue_style(
		'brightwater-style',
		get_stylesheet_uri(),
		array(),
		wp_get_theme( get_template() )->get( 'Version' )
	);
}
add_action( 'wp_enqueue_scripts', 'brightwater_enqueue_assets' );

/**
 * Shows two posts per page on the blog home.
 *
 * @param WP_Query $query The query WordPress is about to run.
 */
function brightwater_adjust_main_query( $query ) {
	if ( is_admin() || ! $query->is_main_query() ) {
		return;
	}

	if ( $query->is_home() ) {
		$query->set( 'posts_per_page', 2 );
	}
}
add_action( 'pre_get_posts', 'brightwater_adjust_main_query' );

/**
 * Registers the footer widget area (stretch task).
 */
function brightwater_widgets_init() {
	register_sidebar(
		array(
			'id'            => 'footer',
			'name'          => __( 'Footer', 'brightwater' ),
			'before_widget' => '<section id="%1$s" class="widget %2$s">',
			'after_widget'  => '</section>',
			'before_title'  => '<h2 class="widget-title">',
			'after_title'   => '</h2>',
		)
	);
}
add_action( 'widgets_init', 'brightwater_widgets_init' );

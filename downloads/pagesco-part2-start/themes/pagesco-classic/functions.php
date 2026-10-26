<?php
/**
 * Pages & Co. Classic functions and definitions.
 *
 * @package pagesco-classic
 */

/**
 * Sets up translations and the theme features WordPress should provide.
 */
function pagesco_classic_setup() {
	load_theme_textdomain( 'pagesco-classic', get_template_directory() . '/languages' );

	add_theme_support( 'title-tag' );
	add_theme_support( 'automatic-feed-links' );
	add_theme_support( 'post-thumbnails' );
	add_theme_support( 'responsive-embeds' );
	add_theme_support(
		'html5',
		array( 'search-form', 'comment-form', 'comment-list', 'gallery', 'caption', 'navigation-widgets' )
	);
}
add_action( 'after_setup_theme', 'pagesco_classic_setup' );

/**
 * Shows three posts per page on the blog home.
 *
 * @param WP_Query $query The query WordPress is about to run.
 */
function pagesco_classic_adjust_main_query( $query ) {
	if ( is_admin() || ! $query->is_main_query() ) {
		return;
	}

	if ( $query->is_home() ) {
		$query->set( 'posts_per_page', 3 );
	}
}
add_action( 'pre_get_posts', 'pagesco_classic_adjust_main_query' );

/**
 * Loads the theme's stylesheet and its menu script.
 */
function pagesco_classic_enqueue_assets() {
	$version = wp_get_theme( get_template() )->get( 'Version' );

	wp_enqueue_style(
		'pagesco-classic-style',
		get_parent_theme_file_uri( 'style.css' ),
		array(),
		$version
	);

	wp_enqueue_script(
		'pagesco-classic-navigation',
		get_parent_theme_file_uri( 'assets/js/navigation.js' ),
		array(),
		$version,
		array(
			'strategy'  => 'defer',
			'in_footer' => true,
		)
	);
}
add_action( 'wp_enqueue_scripts', 'pagesco_classic_enqueue_assets' );

/**
 * Registers the menu location the header prints.
 */
function pagesco_classic_register_menus() {
	register_nav_menus(
		array(
			'primary' => __( 'Primary menu', 'pagesco-classic' ),
		)
	);
}
add_action( 'after_setup_theme', 'pagesco_classic_register_menus' );

/**
 * Registers the footer widget area.
 */
function pagesco_classic_widgets_init() {
	register_sidebar(
		array(
			'id'            => 'footer',
			'name'          => __( 'Footer', 'pagesco-classic' ),
			'description'   => __( 'Shown in the site footer, above the address.', 'pagesco-classic' ),
			'before_widget' => '<section id="%1$s" class="widget %2$s">',
			'after_widget'  => '</section>',
			'before_title'  => '<h2 class="widget-title">',
			'after_title'   => '</h2>',
		)
	);
}
add_action( 'widgets_init', 'pagesco_classic_widgets_init' );

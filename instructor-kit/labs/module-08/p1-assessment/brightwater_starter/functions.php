<?php
/**
 * Brightwater functions and definitions.
 *
 * One prefixed function per job (brightwater_), each on the hook where it belongs.
 *
 * @package brightwater
 */

/**
 * Sets up the theme features WordPress should provide, and the menu location.
 */
function brightwater_setup() {
	add_theme_support( 'html5', array( 'search-form', 'comment-form', 'comment-list', 'gallery', 'caption' ) );

	// TODO T1: let WordPress print the <title> (and remove the hand-written one in header.php).
	// TODO T1: register the menu location primary ("Primary menu").
}
add_action( 'after_setup_theme', 'brightwater_setup' );

// TODO T2: enqueue style.css with the handle brightwater-style, versioned with the theme's own Version.

// TODO T3: two posts per page on the blog home (main query only, never in the admin).

// Stretch: a footer widget area with the id footer (footer.php already prints it when it has widgets).

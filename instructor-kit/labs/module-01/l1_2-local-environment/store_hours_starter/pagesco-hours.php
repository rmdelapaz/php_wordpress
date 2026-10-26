<?php
/**
 * Plugin Name: Pages & Co. Opening Hours (Session 1 lab)
 * Description: Saturday's opening hours at the bottom of every page, and one line in the debug log per page view.
 *
 * Install it like the lesson's debug demo: copy this file into wordpress/wp-content/mu-plugins/ (every PHP
 * file there runs on every request, Lesson 1.1). Reload http://localhost:8080/ and look at the bottom of the page.
 */
function pagesco_lab_hours_footer() {
	$pagesco_hours = array(
		'Monday to Friday' => '9:00-18:00',
		'Saturday'         => '10:00-16:00',
		'Sunday'           => 'closed',
	);
	// TODO 1: print Saturday's hours from $pagesco_hours instead of TODO, wrapped in esc_html() like the lesson's
	//         fixed debug demo does.
	echo '<p class="pagesco-hours">Open Saturday: TODO</p>';
	// TODO 2: write one line to wp-content/debug.log with error_log(): "pagesco-hours: footer printed".
}
add_action( 'wp_footer', 'pagesco_lab_hours_footer' );

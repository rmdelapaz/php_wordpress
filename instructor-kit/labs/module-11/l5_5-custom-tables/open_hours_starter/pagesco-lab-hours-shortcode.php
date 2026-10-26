<?php
/**
 * Plugin Name: Pages & Co. Opening Hours Shortcode (Session 11 lab)
 * Description: [pagesco_open_hours] lists the week; [pagesco_open_hours day="saturday"] prints one day.
 *
 * Session 11 lab starter: TODO 1 to 3 below. A must-use plugin: copy this file into wordpress/wp-content/mu-plugins/.
 */

/**
 * The shop's opening hours, by day.
 *
 * @return array<string, string>
 */
function pagesco_lab_hours() {
	return array(
		'monday'    => '9:00-18:00',
		'tuesday'   => '9:00-18:00',
		'wednesday' => '9:00-18:00',
		'thursday'  => '9:00-21:00',
		'friday'    => '9:00-18:00',
		'saturday'  => '10:00-16:00',
		'sunday'    => 'closed',
	);
}

/**
 * Renders [pagesco_open_hours]: returns escaped HTML, never echoes.
 *
 * @param array|string $atts day (default: every day).
 * @return string
 */
function pagesco_lab_hours_shortcode( $atts ) {
	// TODO 1: fill the attributes with shortcode_atts( array( 'day' => '' ), $atts, 'pagesco_open_hours' ).
	// TODO 2: with a day (lowercased: sanitize_key() does it), return '<span class="pagesco-hours">Saturday: 10:00-16:00</span>'
	//         for a known day and '' for an unknown one (never an error message in a public page).
	// TODO 3: the list below is ECHOED: build the same <ul> as a string and return it.
	echo '<ul class="pagesco-hours">';
	foreach ( pagesco_lab_hours() as $name => $time ) {
		printf( '<li>%s: %s</li>', esc_html( ucfirst( $name ) ), esc_html( $time ) );
	}
	echo '</ul>';
	return '';
}

/**
 * Registers the shortcode on init.
 */
function pagesco_lab_hours_register() {
	add_shortcode( 'pagesco_open_hours', 'pagesco_lab_hours_shortcode' );
}
add_action( 'init', 'pagesco_lab_hours_register' );

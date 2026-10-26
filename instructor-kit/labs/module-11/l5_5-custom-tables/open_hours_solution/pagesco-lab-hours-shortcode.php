<?php
/**
 * Plugin Name: Pages & Co. Opening Hours Shortcode (Session 11 lab)
 * Description: [pagesco_open_hours] lists the week; [pagesco_open_hours day="saturday"] prints one day.
 *
 * A must-use plugin: copy this file into wordpress/wp-content/mu-plugins/.
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
	$atts  = shortcode_atts( array( 'day' => '' ), $atts, 'pagesco_open_hours' );
	$hours = pagesco_lab_hours();
	$day   = strtolower( sanitize_key( $atts['day'] ) );
	if ( '' !== $day ) {
		if ( ! isset( $hours[ $day ] ) ) {
			return '';
		}
		return sprintf( '<span class="pagesco-hours">%s: %s</span>', esc_html( ucfirst( $day ) ), esc_html( $hours[ $day ] ) );
	}
	$items = '';
	foreach ( $hours as $name => $time ) {
		$items .= sprintf( '<li>%s: %s</li>', esc_html( ucfirst( $name ) ), esc_html( $time ) );
	}
	return '<ul class="pagesco-hours">' . $items . '</ul>';
}

/**
 * Registers the shortcode on init.
 */
function pagesco_lab_hours_register() {
	add_shortcode( 'pagesco_open_hours', 'pagesco_lab_hours_shortcode' );
}
add_action( 'init', 'pagesco_lab_hours_register' );

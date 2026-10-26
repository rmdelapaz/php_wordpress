<?php
/**
 * Plugin Name: Pages & Co. Opening Hours (Session 1 lab)
 * Description: Saturday's opening hours at the bottom of every page, and one line in the debug log per page view.
 */
function pagesco_lab_hours_footer() {
	$pagesco_hours = array(
		'Monday to Friday' => '9:00-18:00',
		'Saturday'         => '10:00-16:00',
		'Sunday'           => 'closed',
	);
	echo '<p class="pagesco-hours">Open Saturday: ' . esc_html( $pagesco_hours['Saturday'] ) . '</p>';
	error_log( 'pagesco-hours: footer printed' );
}
add_action( 'wp_footer', 'pagesco_lab_hours_footer' );

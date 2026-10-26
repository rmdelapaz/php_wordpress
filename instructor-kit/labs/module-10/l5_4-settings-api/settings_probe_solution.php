<?php
/**
 * settings_probe_solution.php: what WordPress knows about pagesco_books_settings (Session 10, Lesson 5.4, lab B,
 * reference)
 * state: after:lesson_17
 * expect: books_per_page: Books per list must be between 1 and 24.
 * expect: rows in wp_options: 0
 * expect: sanitize_option filter: yes, default_option filter: yes
 */
global $wpdb;

// 1. The registration, as register_setting() stored it.
$pagesco_reg = get_registered_settings()['pagesco_books_settings'];
printf( "group %s, type %s, sanitized by %s()\n", $pagesco_reg['group'], $pagesco_reg['type'], $pagesco_reg['sanitize_callback'][1] );

// 2. What the sanitize callback makes of a hostile submission, and the errors it queues.
$pagesco_clean = sanitize_option(
	'pagesco_books_settings',
	array(
		'notice_extra'   => '<em>Signed copies</em> this week.',
		'books_per_page' => '30',
		'events_limit'   => '3',
	)
);
echo wp_json_encode( $pagesco_clean ), "\n";
foreach ( get_settings_errors( 'pagesco_books_settings' ) as $pagesco_error ) {
	echo $pagesco_error['code'], ': ', $pagesco_error['message'], "\n";
}

// 3. Sanitizing stored nothing: the row still does not exist (defaults apply).
echo 'rows in wp_options: ', $wpdb->get_var( $wpdb->prepare( "SELECT COUNT(*) FROM {$wpdb->options} WHERE option_name = %s", 'pagesco_books_settings' ) ), "\n";

// 4. register_setting() works through two filters: one cleans every write, one hands out the default.
printf(
	"sanitize_option filter: %s, default_option filter: %s\n",
	has_filter( 'sanitize_option_pagesco_books_settings' ) ? 'yes' : 'no',
	has_filter( 'default_option_pagesco_books_settings' ) ? 'yes' : 'no'
);

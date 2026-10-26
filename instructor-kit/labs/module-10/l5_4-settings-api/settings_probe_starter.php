<?php
/**
 * settings_probe_starter.php: what WordPress knows about pagesco_books_settings (Session 10, Lesson 5.4, lab B)
 * state: after:lesson_17
 * expect: group pagesco_books
 * expect: TODO
 *
 * Run it on your site after the lesson project. Four questions about the setting Lesson 5.4 registered, asked of
 * WordPress itself. Nothing is stored. From your project folder:
 *     cp labs/module-10/l5_4-settings-api/settings_probe_starter.php wordpress/
 *     wp eval-file --use-include settings_probe_starter.php
 * When you are done: rm wordpress/settings_probe_starter.php
 */
global $wpdb;

// 1. Done for you: the registration, as register_setting() stored it (get_registered_settings()).
$pagesco_reg = get_registered_settings()['pagesco_books_settings'];
printf( "group %s, type %s, sanitized by %s()\n", $pagesco_reg['group'], $pagesco_reg['type'], $pagesco_reg['sanitize_callback'][1] );

// TODO 2: run the submission below through sanitize_option( 'pagesco_books_settings', ... ) (the function
// options.php calls), print the result with wp_json_encode(), then every queued error from
// get_settings_errors( 'pagesco_books_settings' ) as "code: message".
//     array( 'notice_extra' => '<em>Signed copies</em> this week.', 'books_per_page' => '30', 'events_limit' => '3' )
echo "TODO\n";

// TODO 3: did sanitizing store anything? Count the rows named pagesco_books_settings in wp_options with a
// prepared query ($wpdb->options is the table): "rows in wp_options: N".
echo "rows in wp_options: TODO\n";

// TODO 4: register_setting() does its work through two filters named after the option:
// sanitize_option_pagesco_books_settings (runs your callback on every write) and
// default_option_pagesco_books_settings (hands out the default while there is no row). Is each one hooked?
// has_filter( $name ) answers true or false: print "sanitize_option filter: yes, default_option filter: yes".
echo "filters: TODO\n";

// Expected when done (settings_probe_solution.php):
// group pagesco_books, type object, sanitized by sanitize()
// {"notice_extra":"Signed copies this week.","show_events_link":false,"books_per_page":6,"events_limit":3}
// books_per_page: Books per list must be between 1 and 24.
// rows in wp_options: 0
// sanitize_option filter: yes, default_option filter: yes

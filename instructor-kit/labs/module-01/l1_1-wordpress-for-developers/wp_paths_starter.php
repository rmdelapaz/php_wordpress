<?php
/**
 * wp_paths_starter.php: where your code lives, as WordPress itself reports it (Session 1, Lesson 1.1, lab B)
 * state: fresh
 * expect: wp-content      TODO
 *
 * Lesson 1.1's table of folders, asked of the running site. WordPress is loaded when WP-CLI runs a file, so its
 * constants and functions are all there. From your project folder:
 *     cp labs/module-01/l1_1-wordpress-for-developers/wp_paths_starter.php wordpress/
 *     wp eval-file --use-include wp_paths_starter.php
 * Replace each 'TODO' with the constant or function its comment names (look them up in the Code Reference,
 * developer.wordpress.org/reference), run again, and compare with "Expected when done" at the end.
 * When you are done: rm wordpress/wp_paths_starter.php
 */
$pagesco_rows = array(
	'WordPress root' => ABSPATH,  // done for you: the constant wp-load.php defines first
	'wp-content'     => 'TODO',   // TODO 1: the constant that holds the full path of wp-content
	'plugins'        => 'TODO',   // TODO 2: the constant for the plugins folder
	'must-use'       => 'TODO',   // TODO 3: the constant for the mu-plugins folder
	'active theme'   => 'TODO',   // TODO 4: the function that returns the active theme's folder name
	'its URL'        => 'TODO',   // TODO 5: the function that returns that folder's URL (..._directory_uri)
);
foreach ( $pagesco_rows as $pagesco_label => $pagesco_value ) {
	printf( "%-15s %s\n", $pagesco_label, $pagesco_value );
}

// TODO 6: get_plugins() lists every installed plugin (its keys are their main files). It lives in an admin file
// that WP-CLI does not load by itself: require_once ABSPATH . 'wp-admin/includes/plugin.php'; first.
echo "installed plugins: TODO\n";
// TODO 7: get_mu_plugins() lists the must-use plugins the same way (no extra file needed).
echo "must-use plugins: TODO\n";

// Expected when done (wp_paths_solution.php, the course site):
// WordPress root  /var/www/html/
// wp-content      /var/www/html/wp-content
// plugins         /var/www/html/wp-content/plugins
// must-use        /var/www/html/wp-content/mu-plugins
// active theme    twentytwentyfive
// its URL         http://localhost:8080/wp-content/themes/twentytwentyfive
// installed plugins: akismet/akismet.php, hello.php
// must-use plugins: mailpit-smtp.php

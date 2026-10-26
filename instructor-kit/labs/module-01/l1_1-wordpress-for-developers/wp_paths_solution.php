<?php
/**
 * wp_paths_solution.php: the instructor's reference for wp_paths_starter.php (Session 1, Lesson 1.1, lab B)
 * state: fresh
 * expect: must-use        /var/www/html/wp-content/mu-plugins
 * expect: installed plugins: akismet/akismet.php, hello.php
 */
$pagesco_rows = array(
	'WordPress root' => ABSPATH,
	'wp-content'     => WP_CONTENT_DIR,
	'plugins'        => WP_PLUGIN_DIR,
	'must-use'       => WPMU_PLUGIN_DIR,
	'active theme'   => get_stylesheet(),
	'its URL'        => get_stylesheet_directory_uri(),
);
foreach ( $pagesco_rows as $pagesco_label => $pagesco_value ) {
	printf( "%-15s %s\n", $pagesco_label, $pagesco_value );
}

require_once ABSPATH . 'wp-admin/includes/plugin.php';
echo 'installed plugins: ', implode( ', ', array_keys( get_plugins() ) ), "\n";
echo 'must-use plugins: ', implode( ', ', array_keys( get_mu_plugins() ) ), "\n";

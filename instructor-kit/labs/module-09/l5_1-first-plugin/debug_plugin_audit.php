<?php
/**
 * debug_plugin_audit.php: a plugin audit with three bugs (Session 9, Lesson 5.1, find-the-bug handout)
 * state: after:lesson_13
 * expect-error: Warning
 *
 * For every installed plugin, the audit prints its name, whether it is active, the PHP version its header asks for
 * and whether this server meets it, then a total. Typed in a hurry. From your project folder:
 *     cp labs/module-09/l5_1-first-plugin/debug_plugin_audit.php wordpress/
 *     wp eval-file --use-include debug_plugin_audit.php
 * Two bugs announce themselves with Warnings (read each one from the left). The third is SILENT: a wrong answer
 * about which plugins can run here. Fix all three, one at a time, running again after each fix.
 * When you are done: rm wordpress/debug_plugin_audit.php
 */
require_once ABSPATH . 'wp-admin/includes/plugin.php';   // get_plugins() lives in an admin file

$pagesco_totals = array();
foreach ( get_plugins() as $pagesco_file => $pagesco_data ) {
	$pagesco_status = is_plugin_active( $pagesco_file ) ? 'active' : 'inactive';
	$pagesco_needs  = $pagesco_data['RequiresPhp'] ? $pagesco_data['RequiresPhp'] : '7.4';
	$pagesco_runs   = version_compare( PHP_VERSION, $pagesco_needs, '<' );
	printf( "%-12s %-8s needs PHP %-4s %s\n", $pagesco_data['Name'], $pagesco_status, $pagesco_needs, $pagesco_runs ? 'runs here' : 'TOO OLD for this plugin' );
	++$pagesco_totals[ $pagesco_status ];
}
printf( "%d plugin(s) installed, %d inactive\n", array_sum( $pagesco_totals ), $pagesco_totals['inactive'] );

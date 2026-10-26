<?php
/**
 * debug_release_check.php: "can everything move to 1.2.0?", typed in a hurry (Session 18, Lesson 9.1, find-the-bug handout)
 * state: after:lesson_29
 * expect-error: Warning, Deprecated
 *
 * Before Milestone 8's bump: is each version older than the next release? On the course site after Lesson 8.4
 * all three are 1.1.1, so every line should print 1.1.1 and "ok". From your project folder:
 *     cp labs/module-18/l9_1-final-project/debug_release_check.php wordpress/
 *     wp eval-file --use-include debug_release_check.php
 * One typo produces two messages (read both from the left: which one is the cause?). A second bug is SILENT: a
 * line looks fine, prints "ok", and is wrong. Fix both, run again after each fix.
 * When you are done: rm wordpress/debug_release_check.php
 */
require_once ABSPATH . 'wp-admin/includes/plugin.php';

$pagesco_dir  = WP_PLUGIN_DIR . '/pagesco-books';
$pagesco_next = '1.2.0';
$pagesco_pkg  = json_decode( (string) file_get_contents( $pagesco_dir . '/package.json' ), true );

$pagesco_current = array(
	'plugin header'   => get_plugin_data( $pagesco_dir . '/pagesco-books.php', false, false )['Version'],
	'package.json'    => $pagesco_pkg['verison'],
	'theme style.css' => wp_get_theme( 'pagesco' )->get( 'version' ),
);

foreach ( $pagesco_current as $pagesco_label => $pagesco_version ) {
	printf(
		"%-16s %-6s -> %s %s\n",
		$pagesco_label,
		$pagesco_version,
		$pagesco_next,
		version_compare( $pagesco_version, $pagesco_next, '<' ) ? 'ok' : 'NOT OLDER'
	);
}

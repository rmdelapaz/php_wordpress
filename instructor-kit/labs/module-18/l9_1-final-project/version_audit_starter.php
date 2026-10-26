<?php
/**
 * version_audit_starter.php: every place a version lives, read from the files (Session 18, Lesson 9.1, lab A)
 * state: after:lesson_29
 * expect: readme.txt Stable tag      TODO
 *
 * Milestone 8 bumps five places for release 1.2.0. This script reads all five the way WordPress and the tools do,
 * so a forgotten one shows before you tag. From your project folder:
 *     cp labs/module-18/l9_1-final-project/version_audit_starter.php wordpress/
 *     wp eval-file --use-include version_audit_starter.php
 * Replace each 'TODO' with the call its comment names, run again, and compare with "Expected when done".
 * When you are done: rm wordpress/version_audit_starter.php
 */
require_once ABSPATH . 'wp-admin/includes/plugin.php';

$pagesco_dir = WP_PLUGIN_DIR . '/pagesco-books';

$pagesco_versions = array(
	// Done for you: the header WordPress shows on the Plugins screen (false, false: no markup, no translation).
	'pagesco-books.php header' => get_plugin_data( $pagesco_dir . '/pagesco-books.php', false, false )['Version'],
	// TODO 1: the plugin's own constant, PAGESCO_BOOKS_VERSION.
	'PAGESCO_BOOKS_VERSION'    => 'TODO',
	// TODO 2: readme.txt's "Stable tag" line: get_file_data( <file>, array( 'stable' => 'Stable tag' ) )['stable'].
	'readme.txt Stable tag'    => 'TODO',
	// TODO 3: package.json's "version": json_decode() the file's contents as an array.
	'package.json version'     => 'TODO',
	// TODO 4: the theme's Version header: wp_get_theme( 'pagesco' )->get( ... ). Header names are case-sensitive.
	'theme style.css Version'  => 'TODO',
);

foreach ( $pagesco_versions as $pagesco_label => $pagesco_version ) {
	printf( "%-26s %s\n", $pagesco_label, $pagesco_version );
}

// TODO 5: when all five values are the same (array_unique() leaves one), print "All five agree: <version>";
// otherwise "They disagree: " and the different values, comma-separated.
echo "Verdict: TODO\n";

// Expected when done (version_audit_solution.php, the course site after Lesson 8.4):
// pagesco-books.php header   1.1.1
// PAGESCO_BOOKS_VERSION      1.1.1
// readme.txt Stable tag      1.1.1
// package.json version       1.1.1
// theme style.css Version    1.1.1
// All five agree: 1.1.1

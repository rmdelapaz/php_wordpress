<?php
/**
 * version_audit_solution.php: every place a version lives, read from the files (Session 18, Lesson 9.1, lab A)
 * state: after:lesson_29
 * expect: All five agree: 1.1.1
 *
 * The reference for version_audit_starter.php. Milestone 8 bumps five places for release 1.2.0; this script reads
 * all five the way WordPress and the tools do, so a forgotten one shows before you tag.
 */
require_once ABSPATH . 'wp-admin/includes/plugin.php';

$pagesco_dir = WP_PLUGIN_DIR . '/pagesco-books';

$pagesco_versions = array(
	// The header WordPress shows on the Plugins screen (no translation: the Version line is not translated).
	'pagesco-books.php header' => get_plugin_data( $pagesco_dir . '/pagesco-books.php', false, false )['Version'],
	// The constant the plugin uses for cache busting and upgrades.
	'PAGESCO_BOOKS_VERSION'    => PAGESCO_BOOKS_VERSION,
	// The directory's "Stable tag": get_file_data() reads any "Name: value" header line.
	'readme.txt Stable tag'    => get_file_data( $pagesco_dir . '/readme.txt', array( 'stable' => 'Stable tag' ) )['stable'],
	// npm's version, which plugin-zip and package-lock.json follow.
	'package.json version'     => json_decode( (string) file_get_contents( $pagesco_dir . '/package.json' ), true )['version'],
	// The theme's Version: the live site's pattern cache notices a new one (Lesson 8.4).
	'theme style.css Version'  => wp_get_theme( 'pagesco' )->get( 'Version' ),
);

foreach ( $pagesco_versions as $pagesco_label => $pagesco_version ) {
	printf( "%-26s %s\n", $pagesco_label, $pagesco_version );
}

$pagesco_unique = array_unique( $pagesco_versions );
if ( 1 === count( $pagesco_unique ) ) {
	printf( "All five agree: %s\n", reset( $pagesco_unique ) );
} else {
	printf( "They disagree: %s\n", implode( ', ', $pagesco_unique ) );
}

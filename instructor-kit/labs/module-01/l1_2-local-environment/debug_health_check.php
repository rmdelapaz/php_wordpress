<?php
/**
 * debug_health_check.php: a health check with three bugs (Session 1, Lesson 1.2, find-the-bug handout)
 * state: fresh
 * expect-error: Warning
 *
 * A shorter cousin of the lesson's pagesco-check.php, typed in a hurry. On a working course site every check
 * should say OK and the last line "All checks passed." From your project folder:
 *     cp labs/module-01/l1_2-local-environment/debug_health_check.php wordpress/
 *     wp eval-file --use-include debug_health_check.php
 * Two bugs announce themselves with a Warning (read each one from the left: level, message, file, line). The
 * third is SILENT: no message at all, just a wrong answer. Find all three, fix them one at a time, and run again
 * after each fix. Then delete the copy: rm wordpress/debug_health_check.php
 */
$pagesco_checks = array(
	'WordPress 7.1'        => str_starts_with( get_bloginfo( 'version' ), '7.1' ),
	'Site address'         => 'http://localhost:8080' === home_url(),
	'Pretty permalinks'    => '/%postname%/' === get_option( 'permalink' ),
	'Environment is local' => 'local' === wp_get_environment_type(),
	'Mail plugin present'  => file_exists( WPMU_PLUGIN_DIR . '/mailpit-smtp.php' ),
);
$pagesco_words  = array(
	'ok'     => 'OK',
	'failed' => 'FAILED',
);
$pagesco_failes = 0;
foreach ( $pagesco_checks as $pagesco_label => $pagesco_ok ) {
	printf( "%-22s %s\n", $pagesco_label, $pagesco_words[ $pagesco_ok ? 'ok' : 'fail' ] );
	if ( ! $pagesco_ok ) {
		++$pagesco_failes;
	}
}
echo 0 === $pagesco_failed ? "All checks passed.\n" : "{$pagesco_failed} check(s) failed.\n";

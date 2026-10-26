<?php
/**
 * Plugin Name: Pages & Co. Local Mail (Mailpit)
 * Description: On a local site, send all WordPress email to Mailpit (http://localhost:8025) instead of the internet.
 *
 * Copy this file to wordpress/wp-content/mu-plugins/ (Lesson 1.2). Lesson 2.3 explains how it works: hooks.
 */

// WordPress sends from wordpress@<site domain>. On http://localhost:8080 that is wordpress@localhost, which the
// mailer rejects ("Invalid address:  (From): wordpress@localhost") so wp_mail() returns false. Use a valid one.
add_filter( 'wp_mail_from', function ( $from ) {
	return str_ends_with( $from, '@localhost' ) ? 'wordpress@example.com' : $from;
} );

add_action( 'phpmailer_init', function ( $phpmailer ) {
	if ( 'local' !== wp_get_environment_type() ) {
		return;
	}
	$phpmailer->isSMTP();
	$phpmailer->Host        = 'mailpit';
	$phpmailer->Port        = 1025;
	$phpmailer->SMTPAuth    = false;
	$phpmailer->SMTPAutoTLS = false;
} );

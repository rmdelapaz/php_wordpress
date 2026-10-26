<?php
/**
 * debug_newsletter_sanitize.php: a setting and its sanitize callback, with three bugs (Session 10, Lesson 5.4,
 * find-the-bug handout)
 * state: after:lesson_16
 * expect-error: doing_it_wrong, Warning
 *
 * A newsletter setting registered for this one run, then fed two submissions the way options.php would feed it:
 * the form with the box ticked, and the form with the box unticked. Nothing is stored. From your project folder:
 *     cp labs/module-10/l5_4-settings-api/debug_newsletter_sanitize.php wordpress/
 *     wp eval-file --use-include debug_newsletter_sanitize.php
 * WordPress and PHP report two bugs. The third is SILENT: look closely at the stored sign-up text. Fix all three;
 * when you are done: rm wordpress/debug_newsletter_sanitize.php
 */

/**
 * Cleans a submitted newsletter setting.
 *
 * @param mixed $input The submitted values.
 * @return array
 */
function pagesco_lab_debug_sanitize( $input ) {
	$clean              = $input;
	$clean['show_form'] = (bool) $input['show_form'];
	$clean['frequency'] = in_array( $input['frequency'], array( 'weekly', 'monthly' ), true ) ? $input['frequency'] : 'monthly';
	return $input;
}

register_setting(
	'pagesco_lab_debug',
	'pagesco_lab_debug_newsletter',
	array(
		'type'              => 'array',
		'show_in_rest'      => true,
		'sanitize_callback' => 'pagesco_lab_debug_sanitize',
	)
);
$pagesco_forms = array(
	'box ticked'   => array( 'signup_text' => '<b>Join</b> our list', 'frequency' => 'weekly', 'show_form' => '1' ),
	'box unticked' => array( 'signup_text' => 'Join our list', 'frequency' => 'daily' ),
);
foreach ( $pagesco_forms as $pagesco_label => $pagesco_form ) {
	echo $pagesco_label, ': ', wp_json_encode( sanitize_option( 'pagesco_lab_debug_newsletter', $pagesco_form ) ), "\n";
}

<?php
/**
 * Plugin Name: Pages & Co. Newsletter Settings (Session 10 lab)
 * Description: A Settings > Newsletter screen with the Settings API: one array option, three fields, a sanitize callback.
 *
 * A must-use plugin: copy this file into wordpress/wp-content/mu-plugins/ (no activation needed).
 */

/**
 * The option's values when nothing is saved.
 *
 * @return array
 */
function pagesco_lab_newsletter_defaults() {
	return array(
		'signup_text' => 'Join the Pages & Co. newsletter.',
		'frequency'   => 'monthly',
		'show_form'   => true,
	);
}

/**
 * One value with its default filled in.
 *
 * @param string $key A key of the defaults.
 * @return mixed
 */
function pagesco_lab_newsletter_get( $key ) {
	$settings = wp_parse_args( get_option( 'pagesco_lab_newsletter', array() ), pagesco_lab_newsletter_defaults() );
	return $settings[ $key ] ?? null;
}

/**
 * Registers the option on init, so its sanitizing and default apply everywhere.
 */
function pagesco_lab_newsletter_register() {
	register_setting(
		'pagesco_lab_newsletter',
		'pagesco_lab_newsletter',
		array(
			'type'              => 'object',
			'default'           => pagesco_lab_newsletter_defaults(),
			'sanitize_callback' => 'pagesco_lab_newsletter_sanitize',
		)
	);
}
add_action( 'init', 'pagesco_lab_newsletter_register' );

/**
 * Cleans a submitted value: returns the COMPLETE option, keeps the saved frequency when the new one is not allowed.
 *
 * @param mixed $input The submitted settings.
 * @return array
 */
function pagesco_lab_newsletter_sanitize( $input ) {
	$input = is_array( $input ) ? $input : array();
	$clean = array(
		'signup_text' => sanitize_text_field( $input['signup_text'] ?? '' ),
		'frequency'   => $input['frequency'] ?? '',
		'show_form'   => ! empty( $input['show_form'] ),
	);
	if ( ! in_array( $clean['frequency'], array( 'weekly', 'monthly' ), true ) ) {
		add_settings_error( 'pagesco_lab_newsletter', 'frequency', 'Frequency must be weekly or monthly.' );
		$clean['frequency'] = pagesco_lab_newsletter_get( 'frequency' );
	}
	return $clean;
}

/**
 * Adds Settings > Newsletter for users who can manage options.
 */
function pagesco_lab_newsletter_menu() {
	add_options_page( 'Newsletter Settings', 'Newsletter', 'manage_options', 'pagesco-lab-newsletter', 'pagesco_lab_newsletter_render' );
}
add_action( 'admin_menu', 'pagesco_lab_newsletter_menu' );

/**
 * Describes the form: one section, three fields.
 */
function pagesco_lab_newsletter_fields() {
	add_settings_section( 'pagesco_lab_newsletter_main', 'Newsletter', '__return_false', 'pagesco-lab-newsletter' );
	add_settings_field( 'signup_text', 'Sign-up text', 'pagesco_lab_newsletter_text_field', 'pagesco-lab-newsletter', 'pagesco_lab_newsletter_main', array( 'label_for' => 'pagesco-lab-signup-text' ) );
	add_settings_field( 'frequency', 'Frequency', 'pagesco_lab_newsletter_frequency_field', 'pagesco-lab-newsletter', 'pagesco_lab_newsletter_main', array( 'label_for' => 'pagesco-lab-frequency' ) );
	add_settings_field( 'show_form', 'Sign-up form', 'pagesco_lab_newsletter_checkbox_field', 'pagesco-lab-newsletter', 'pagesco_lab_newsletter_main', array( 'label_for' => 'pagesco-lab-show-form' ) );
}
add_action( 'admin_init', 'pagesco_lab_newsletter_fields' );

/**
 * The sign-up text input.
 */
function pagesco_lab_newsletter_text_field() {
	printf( '<input type="text" id="pagesco-lab-signup-text" name="pagesco_lab_newsletter[signup_text]" value="%s" class="regular-text">', esc_attr( pagesco_lab_newsletter_get( 'signup_text' ) ) );
}

/**
 * The frequency select.
 */
function pagesco_lab_newsletter_frequency_field() {
	echo '<select id="pagesco-lab-frequency" name="pagesco_lab_newsletter[frequency]">';
	foreach ( array( 'weekly', 'monthly' ) as $value ) {
		printf( '<option value="%1$s"%2$s>%1$s</option>', esc_attr( $value ), selected( pagesco_lab_newsletter_get( 'frequency' ), $value, false ) );
	}
	echo '</select>';
}

/**
 * The sign-up form checkbox.
 */
function pagesco_lab_newsletter_checkbox_field() {
	printf( '<label><input type="checkbox" id="pagesco-lab-show-form" name="pagesco_lab_newsletter[show_form]" value="1"%s> Show the sign-up form</label>', checked( pagesco_lab_newsletter_get( 'show_form' ), true, false ) );
}

/**
 * Prints the page: the form posts to options.php.
 */
function pagesco_lab_newsletter_render() {
	if ( ! current_user_can( 'manage_options' ) ) {
		return;
	}
	echo '<div class="wrap"><h1>' . esc_html( get_admin_page_title() ) . '</h1><form action="options.php" method="post">';
	settings_fields( 'pagesco_lab_newsletter' );
	do_settings_sections( 'pagesco-lab-newsletter' );
	submit_button();
	echo '</form></div>';
}

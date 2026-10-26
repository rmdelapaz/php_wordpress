<?php
/**
 * Plugin Name: Pages & Co. Site
 * Description: Site-wide features of the Pages & Co. bookstore: the store notice bar.
 * Version:     1.2.0
 * Author:      Pages & Co.
 */

/**
 * Prints the store notice at the top of every front-end page.
 */
function pagesco_render_store_notice() {
	/**
	 * Filters the text of the store notice.
	 *
	 * @since 1.0.0
	 *
	 * @param string $text Plain text; it is escaped when printed. Return '' to hide the notice.
	 */
	$text = apply_filters( 'pagesco_store_notice', 'Free shipping on orders over $35.' );

	if ( '' === $text ) {
		return;
	}

	/**
	 * Fires before the store notice bar is printed.
	 *
	 * @since 1.0.0
	 */
	do_action( 'pagesco_before_store_notice' );

	echo '<div class="pagesco-notice" role="region" aria-label="Store notice">' . esc_html( $text );

	/**
	 * Fires inside the store notice bar, after the text.
	 *
	 * @since 1.0.0
	 */
	do_action( 'pagesco_store_notice_end' );

	echo '</div>';
}
add_action( 'wp_body_open', 'pagesco_render_store_notice' );

remove_action( 'wp_head', 'wp_generator' );

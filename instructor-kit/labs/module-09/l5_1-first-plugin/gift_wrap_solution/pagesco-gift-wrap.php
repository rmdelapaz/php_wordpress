<?php
/**
 * Plugin Name:       Pages & Co. Gift Wrap (Session 9 lab)
 * Description:       Adds a gift-wrapping line to the store notice; the price is stored once, on activation.
 * Version:           0.1.0
 * Requires at least: 6.8
 * Requires PHP:      8.2
 * Text Domain:       pagesco-gift-wrap
 */
defined( 'ABSPATH' ) || exit;

/**
 * Runs once, when the plugin is activated: stores the gift-wrapping price.
 */
function pagesco_gift_wrap_activate() {
	add_option( 'pagesco_gift_wrap_price', '2.50' );
}
register_activation_hook( __FILE__, 'pagesco_gift_wrap_activate' );

/**
 * Adds the gift-wrapping sentence to the store notice (the pagesco_store_notice filter of Lesson 2.3).
 *
 * @param string $text The notice text so far.
 * @return string
 */
function pagesco_gift_wrap_notice( $text ) {
	$price = get_option( 'pagesco_gift_wrap_price' );
	if ( false === $price ) {
		return $text;
	}
	return $text . ' Gift wrapping: $' . $price . '.';
}
add_filter( 'pagesco_store_notice', 'pagesco_gift_wrap_notice', 30 );

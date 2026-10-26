<?php
/**
 * Plugin Name:       Pages & Co. Gift Wrap (Session 9 lab)
 * Description:       Adds a gift-wrapping line to the store notice; the price is stored once, on activation.
 * Version:           0.1.0
 * Text Domain:       pagesco-gift-wrap
 *
 * TODO 1: add the two requirement lines of Lesson 5.1's header (WordPress 6.8, PHP 8.2), aligned like the others.
 */
// TODO 2: the guard line that stops a direct request from a browser (Lesson 5.1, Common Mistakes 1).

/**
 * Runs once, when the plugin is activated: stores the gift-wrapping price.
 */
function pagesco_gift_wrap_activate() {
	add_option( 'pagesco_gift_wrap_price', '2.50' );
}
// TODO 3: register pagesco_gift_wrap_activate() as the activation callback: at the top level, with __FILE__.

/**
 * Adds the gift-wrapping sentence to the store notice (the pagesco_store_notice filter of Lesson 2.3).
 *
 * @param string $text The notice text so far.
 * @return string
 */
function pagesco_gift_wrap_notice( $text ) {
	// TODO 4: read the stored price with get_option() and append " Gift wrapping: $2.50." (with the stored price).
	return $text;
}
add_filter( 'pagesco_store_notice', 'pagesco_gift_wrap_notice', 30 );

<?php
/**
 * Plugin Name:       Pages & Co. Shelf Label (Session 11 lab)
 * Description:       One static block, pagesco/shelf-label: a small sign for a shelf ("Staff picks", "New arrivals").
 * Version:           0.1.0
 * Requires at least: 6.8
 * Requires PHP:      8.2
 * Text Domain:       pagesco-shelf-label
 *
 * The block's sources are in src/blocks/shelf-label/; npm run build writes build/blocks/ and its manifest.
 * The built files ship with the lab, so it works without Node; rebuild after a change to src/ (Lesson 6.1).
 */
defined( 'ABSPATH' ) || exit;

/**
 * Registers every block in build/blocks/ from the manifest that npm run build writes.
 */
function pagesco_shelf_label_register_blocks() {
	wp_register_block_types_from_metadata_collection(
		__DIR__ . '/build/blocks',
		__DIR__ . '/build/blocks/blocks-manifest.php'
	);
}
add_action( 'init', 'pagesco_shelf_label_register_blocks' );

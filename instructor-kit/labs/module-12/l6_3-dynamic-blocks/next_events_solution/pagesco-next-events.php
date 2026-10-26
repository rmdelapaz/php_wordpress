<?php
/**
 * Plugin Name: Pages & Co. Next Events (Session 12 lab)
 * Description: A dynamic block, pagesco/next-events: the next events from the events table, rendered by render.php on every view.
 * Requires Plugins: pagesco-books
 * Text Domain: pagesco-next-events
 */

/**
 * Registers the block from block/block.json, whose "render" names block/render.php. No JavaScript: this lab
 * block is for the front end only (an editor script needs Lesson 6.1's build), so test it with do_blocks().
 */
function pagesco_lab_register_next_events() {
	register_block_type( __DIR__ . '/block' );
}
add_action( 'init', 'pagesco_lab_register_next_events' );

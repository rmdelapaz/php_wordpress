<?php
/**
 * Pages & Co. Cafe: theme functions.
 *
 * Adds a coffee cup in front of every post title on the café's pages.
 */

/**
 * Prefixes post titles with a cup.
 *
 * @param string $title The post title.
 */
function pagesco_cafe_title_cup( $title ) {
	$title = '☕ ' . $title;
}
add_filter( 'the_title', 'pagesco_cafe_title_cup' );

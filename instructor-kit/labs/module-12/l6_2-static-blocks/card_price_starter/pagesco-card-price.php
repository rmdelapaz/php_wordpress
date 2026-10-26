<?php
/**
 * Plugin Name: Pages & Co. Card Price (Session 12 lab)
 * Description: Adds today's price under every Book Card that links to a book, read from the book's meta at view time.
 */

/**
 * A static Book Card is finished HTML: read its link with the HTML API, find the book, and add one line after it.
 *
 * @param string $block_content The card's stored HTML.
 * @param array  $block         The parsed block (its attrs hold only the comment, Lesson 6.2).
 * @return string
 */
function pagesco_lab_card_price( $block_content, $block ) {
	// TODO 1: new WP_HTML_Tag_Processor( $block_content ), then next_tag() with
	//         array( 'class_name' => 'wp-block-pagesco-book-card__link' ). No link found: return the card unchanged.
	// TODO 2: url_to_postid() of the link's href (get_attribute( 'href' )) gives the book's ID. Not a 'book'
	//         (get_post_type()): return the card unchanged.
	// TODO 3: read pagesco_price (a float), and return the card followed by
	//         <p class="pagesco-card-price">Today: $10.99</p>   (number_format_i18n( $price, 2 ), escaped)
	return $block_content;
}
add_filter( 'render_block_pagesco/book-card', 'pagesco_lab_card_price', 10, 2 );

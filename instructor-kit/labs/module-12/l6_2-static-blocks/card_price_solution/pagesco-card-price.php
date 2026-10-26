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
	$pagesco_tags = new WP_HTML_Tag_Processor( $block_content );
	if ( ! $pagesco_tags->next_tag( array( 'class_name' => 'wp-block-pagesco-book-card__link' ) ) ) {
		return $block_content;
	}

	$pagesco_book_id = url_to_postid( (string) $pagesco_tags->get_attribute( 'href' ) );
	if ( ! $pagesco_book_id || 'book' !== get_post_type( $pagesco_book_id ) ) {
		return $block_content;
	}

	$pagesco_price = (float) get_post_meta( $pagesco_book_id, 'pagesco_price', true );

	return $block_content . '<p class="pagesco-card-price">' . esc_html( 'Today: $' . number_format_i18n( $pagesco_price, 2 ) ) . '</p>';
}
add_filter( 'render_block_pagesco/book-card', 'pagesco_lab_card_price', 10, 2 );

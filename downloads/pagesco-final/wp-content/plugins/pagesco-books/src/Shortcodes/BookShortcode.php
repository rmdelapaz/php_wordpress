<?php
/**
 * The [pagesco_book id="30"] shortcode.
 *
 * @package PagesCo\Books
 */

namespace PagesCo\Books\Shortcodes;

use PagesCo\Books\BookPostType;
use PagesCo\Books\Feature;

/**
 * Prints a one-line card for a book: title (linked), author, price and stock.
 */
final class BookShortcode implements Feature {

	/**
	 * The shortcode's tag, the name inside the brackets.
	 */
	public const TAG = 'pagesco_book';

	/**
	 * Registers the shortcode on init.
	 */
	public function register(): void {
		add_action( 'init', array( $this, 'add_shortcode' ) );
	}

	/**
	 * Tells WordPress which callback renders [pagesco_book].
	 */
	public function add_shortcode(): void {
		add_shortcode( self::TAG, array( $this, 'render' ) );
	}

	/**
	 * Returns the card's HTML; never echoes.
	 *
	 * @param array|string $atts The attributes written in the shortcode ('' when there are none).
	 * @return string
	 */
	public function render( $atts ) {
		$atts = shortcode_atts( array( 'id' => 0 ), $atts, self::TAG );
		$book = get_post( absint( $atts['id'] ) );

		if ( ! $book || BookPostType::NAME !== $book->post_type || 'publish' !== $book->post_status ) {
			return '';
		}

		$author   = get_post_meta( $book->ID, 'pagesco_author', true );
		$price    = (float) get_post_meta( $book->ID, 'pagesco_price', true );
		$in_stock = (bool) get_post_meta( $book->ID, 'pagesco_in_stock', true );

		return sprintf(
			'<span class="pagesco-book"><a href="%1$s">%2$s</a> %3$s, <span class="pagesco-book__price">%4$s</span> <span class="pagesco-book__stock">%5$s</span></span>',
			esc_url( get_permalink( $book ) ),
			esc_html( get_the_title( $book ) ),
			/* translators: %s: the book's author. */
			esc_html( sprintf( __( 'by %s', 'pagesco-books' ), $author ) ),
			esc_html( '$' . number_format_i18n( $price, 2 ) ),
			$in_stock ? esc_html__( 'In stock', 'pagesco-books' ) : esc_html__( 'Sold out', 'pagesco-books' )
		);
	}
}

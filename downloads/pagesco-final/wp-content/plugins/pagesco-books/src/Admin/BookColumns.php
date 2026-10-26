<?php
/**
 * Extra columns on the Books screen.
 *
 * @package PagesCo\Books
 */

namespace PagesCo\Books\Admin;

use PagesCo\Books\BookPostType;
use PagesCo\Books\Feature;

/**
 * Shows each book's author, price and stock in the list of books.
 */
final class BookColumns implements Feature {

	/**
	 * Hooks into the list table of the book post type.
	 */
	public function register(): void {
		add_filter( 'manage_' . BookPostType::NAME . '_posts_columns', array( $this, 'add_columns' ) );
		add_action( 'manage_' . BookPostType::NAME . '_posts_custom_column', array( $this, 'print_column' ), 10, 2 );
	}

	/**
	 * Adds the columns after the title.
	 *
	 * @param string[] $columns Column keys and headings.
	 * @return string[]
	 */
	public function add_columns( $columns ) {
		$new = array();
		foreach ( $columns as $key => $heading ) {
			$new[ $key ] = $heading;
			if ( 'title' === $key ) {
				$new['pagesco_author']   = __( 'Author', 'pagesco-books' );
				$new['pagesco_price']    = __( 'Price', 'pagesco-books' );
				$new['pagesco_in_stock'] = __( 'Stock', 'pagesco-books' );
			}
		}
		return $new;
	}

	/**
	 * Prints one cell of a custom column.
	 *
	 * @param string $column  The column key.
	 * @param int    $post_id The book in this row.
	 */
	public function print_column( $column, $post_id ): void {
		switch ( $column ) {
			case 'pagesco_author':
				echo esc_html( get_post_meta( $post_id, 'pagesco_author', true ) );
				break;
			case 'pagesco_price':
				echo esc_html( '$' . number_format_i18n( (float) get_post_meta( $post_id, 'pagesco_price', true ), 2 ) );
				break;
			case 'pagesco_in_stock':
				echo get_post_meta( $post_id, 'pagesco_in_stock', true )
					? esc_html__( 'In stock', 'pagesco-books' )
					: esc_html__( 'Sold out', 'pagesco-books' );
				break;
		}
	}
}

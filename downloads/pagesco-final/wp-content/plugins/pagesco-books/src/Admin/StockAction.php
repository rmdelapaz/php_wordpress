<?php
/**
 * A "Mark sold out" / "Mark in stock" link for each book on the Books screen.
 *
 * @package PagesCo\Books
 */

namespace PagesCo\Books\Admin;

use PagesCo\Books\BookPostType;
use PagesCo\Books\Feature;

/**
 * Adds the row action and handles the request it sends to admin-post.php.
 */
final class StockAction implements Feature {

	/**
	 * The admin-post.php action name, also the start of the nonce action.
	 */
	private const ACTION = 'pagesco_books_toggle_stock';

	/**
	 * Hooks the link into the list and the handler into admin-post.php.
	 */
	public function register(): void {
		add_filter( 'post_row_actions', array( $this, 'add_link' ), 10, 2 );
		add_action( 'admin_post_' . self::ACTION, array( $this, 'handle' ) );
	}

	/**
	 * Adds the link to rows of books the current user may edit.
	 *
	 * @param string[] $actions Row action links.
	 * @param \WP_Post $post    The post in this row.
	 * @return string[]
	 */
	public function add_link( $actions, $post ) {
		if ( BookPostType::NAME !== $post->post_type || ! current_user_can( 'edit_post', $post->ID ) ) {
			return $actions;
		}

		$url = add_query_arg(
			array(
				'action' => self::ACTION,
				'book'   => $post->ID,
			),
			admin_url( 'admin-post.php' )
		);
		$url = wp_nonce_url( $url, self::ACTION . '_' . $post->ID );

		$label = get_post_meta( $post->ID, 'pagesco_in_stock', true )
			? __( 'Mark sold out', 'pagesco-books' )
			: __( 'Mark in stock', 'pagesco-books' );

		$actions['pagesco_stock'] = sprintf( '<a href="%s">%s</a>', esc_url( $url ), esc_html( $label ) );
		return $actions;
	}

	/**
	 * Flips the book's stock flag, then goes back to the Books screen.
	 */
	public function handle(): void {
		$book_id = isset( $_GET['book'] ) ? absint( $_GET['book'] ) : 0;

		check_admin_referer( self::ACTION . '_' . $book_id );

		if ( BookPostType::NAME !== get_post_type( $book_id ) || ! current_user_can( 'edit_post', $book_id ) ) {
			wp_die( esc_html__( 'Sorry, you are not allowed to change this book.', 'pagesco-books' ), 403 );
		}

		$in_stock = (bool) get_post_meta( $book_id, 'pagesco_in_stock', true );
		update_post_meta( $book_id, 'pagesco_in_stock', ! $in_stock );

		wp_safe_redirect( admin_url( 'edit.php?post_type=' . BookPostType::NAME ) );
		exit;
	}
}

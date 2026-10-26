<?php
/**
 * The email a customer gets when a hold is placed.
 *
 * @package PagesCo\Books
 */

namespace PagesCo\Books\Holds;

use PagesCo\Books\Feature;

/**
 * Listens to pagesco_books_hold_placed and sends the confirmation. Other code can listen too.
 */
final class HoldMail implements Feature {

	/**
	 * Hooks into the plugin's own action (Lesson 2.3: an action for a moment).
	 */
	public function register(): void {
		add_action( 'pagesco_books_hold_placed', array( $this, 'send' ), 10, 2 );
	}

	/**
	 * Sends the confirmation. A failed email does not undo the hold: the book is put aside either way.
	 *
	 * @param object   $hold The new hold.
	 * @param \WP_Post $book The book.
	 */
	public function send( $hold, $book ): void {
		$user = get_userdata( (int) $hold->user_id );
		if ( ! $user ) {
			return;
		}

		// Plain text: the raw title, not the HTML version get_the_title() prints in pages.
		$title = $book->post_title;

		/* translators: %s: the book's title. */
		$subject = sprintf( __( 'Your hold at Pages & Co.: %s', 'pagesco-books' ), $title );

		$lines = array(
			/* translators: %s: the customer's name. */
			sprintf( __( 'Hello %s,', 'pagesco-books' ), $user->first_name ? $user->first_name : $user->display_name ),
			'',
			/* translators: %s: the book's title. */
			sprintf( __( 'We have put %s aside for you. Pick it up at the counter by:', 'pagesco-books' ), $title ),
			wp_date( get_option( 'date_format' ), strtotime( $hold->pickup_by . ' 12:00:00' ) ),
			'',
			/* translators: %s: the address of the My holds page. */
			sprintf( __( 'Your holds: %s', 'pagesco-books' ), home_url( '/my-holds/' ) ),
			'',
			__( 'See you soon at Pages & Co.', 'pagesco-books' ),
		);

		wp_mail( $user->user_email, $subject, implode( "\n", $lines ) );
	}
}

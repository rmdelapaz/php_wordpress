<?php
/**
 * The rules of Reserve & Pick Up: who may hold which book, for how long.
 *
 * @package PagesCo\Books
 */

namespace PagesCo\Books\Holds;

use PagesCo\Books\BookPostType;
use PagesCo\Books\Settings;
use WP_Error;

/**
 * Places, cancels and collects holds. The REST API, the forms and the tests all go through these methods,
 * so every rule lives in one place. Each method returns the hold or a WP_Error, never both.
 */
final class Holds {

	/**
	 * Places a hold on a book for a customer, if the shop's rules allow it.
	 *
	 * @param int $book_id The book.
	 * @param int $user_id The customer, a logged-in user.
	 * @return object|WP_Error The new hold.
	 */
	public function place( int $book_id, int $user_id ) {
		if ( ! $user_id ) {
			return new WP_Error( 'pagesco_hold_login_required', __( 'Log in to reserve books.', 'pagesco-books' ), array( 'status' => 401 ) );
		}

		$book = get_post( $book_id );
		if ( ! $book || BookPostType::NAME !== $book->post_type || 'publish' !== $book->post_status ) {
			return new WP_Error( 'pagesco_book_not_found', __( 'No book was found with that ID.', 'pagesco-books' ), array( 'status' => 404 ) );
		}

		if ( ! get_post_meta( $book_id, 'pagesco_in_stock', true ) ) {
			return new WP_Error( 'pagesco_hold_sold_out', __( 'This book is sold out, so it cannot be reserved right now.', 'pagesco-books' ), array( 'status' => 409 ) );
		}

		if ( $this->waiting_hold( $book_id, $user_id ) ) {
			return new WP_Error( 'pagesco_hold_duplicate', __( 'This book is already waiting for you at the counter.', 'pagesco-books' ), array( 'status' => 409 ) );
		}

		$limit = (int) Settings::get( 'max_holds' );
		if ( count( HoldsTable::waiting( self::today(), $user_id ) ) >= $limit ) {
			return new WP_Error(
				'pagesco_hold_limit',
				/* translators: %d: the most books a customer may have waiting at once. */
				sprintf( _n( 'You already have %d book waiting. Collect or cancel it first.', 'You already have %d books waiting. Collect or cancel one first.', $limit, 'pagesco-books' ), $limit ),
				array( 'status' => 409 )
			);
		}

		$days      = (int) Settings::get( 'hold_days' );
		$pickup_by = wp_date( 'Y-m-d', time() + $days * DAY_IN_SECONDS );
		$hold_id   = HoldsTable::add( $book_id, $user_id, $pickup_by );
		if ( ! $hold_id ) {
			return new WP_Error( 'pagesco_hold_not_saved', __( 'The hold could not be saved. Please try again.', 'pagesco-books' ), array( 'status' => 500 ) );
		}

		$hold = HoldsTable::get( $hold_id );

		/**
		 * Fires after a customer placed a hold.
		 *
		 * @since 1.2.0
		 *
		 * @param object   $hold The new hold: id, book_id, user_id, status, pickup_by, created_at.
		 * @param \WP_Post $book The book.
		 */
		do_action( 'pagesco_books_hold_placed', $hold, $book );

		return $hold;
	}

	/**
	 * Cancels one of the customer's own waiting holds. Someone else's hold is "not found", not "forbidden".
	 *
	 * @param int $hold_id The hold.
	 * @param int $user_id The customer asking.
	 * @return object|WP_Error The cancelled hold.
	 */
	public function cancel( int $hold_id, int $user_id ) {
		if ( ! $user_id || ! HoldsTable::finish( $hold_id, 'cancelled', $user_id ) ) {
			return new WP_Error( 'pagesco_hold_not_found', __( 'You have no waiting hold with that ID.', 'pagesco-books' ), array( 'status' => 404 ) );
		}

		return HoldsTable::get( $hold_id );
	}

	/**
	 * Marks a waiting hold as collected at the counter. The caller checks that the user is staff.
	 *
	 * @param int $hold_id The hold.
	 * @return object|WP_Error The collected hold.
	 */
	public function collect( int $hold_id ) {
		if ( ! HoldsTable::finish( $hold_id, 'collected' ) ) {
			return new WP_Error( 'pagesco_hold_not_found', __( 'No waiting hold was found with that ID.', 'pagesco-books' ), array( 'status' => 404 ) );
		}

		return HoldsTable::get( $hold_id );
	}

	/**
	 * The customer's hold on a book that is still waiting at the counter, or null.
	 *
	 * @param int $book_id The book.
	 * @param int $user_id The customer.
	 */
	public function waiting_hold( int $book_id, int $user_id ): ?object {
		$holds = HoldsTable::waiting( self::today(), $user_id, $book_id );

		return $holds ? $holds[0] : null;
	}

	/**
	 * Today in the site's time zone, Y-m-d: a hold is expired once its pickup date is before it.
	 */
	public static function today(): string {
		return wp_date( 'Y-m-d' );
	}

	/**
	 * The status a customer sees: waiting, expired (computed, never stored), collected or cancelled.
	 *
	 * @param object $hold A row from HoldsTable.
	 */
	public static function status( object $hold ): string {
		if ( 'waiting' === $hold->status && $hold->pickup_by < self::today() ) {
			return 'expired';
		}

		return $hold->status;
	}

	/**
	 * The status in words, for pages and the API.
	 *
	 * @param object $hold A row from HoldsTable.
	 */
	public static function label( object $hold ): string {
		$date = wp_date( get_option( 'date_format' ), strtotime( $hold->pickup_by . ' 12:00:00' ) );

		switch ( self::status( $hold ) ) {
			case 'waiting':
				/* translators: %s: the last day of pickup, such as November 5, 2026. */
				return sprintf( __( 'Waiting for you at the counter until %s.', 'pagesco-books' ), $date );
			case 'expired':
				/* translators: %s: the last day of pickup, such as November 5, 2026. */
				return sprintf( __( 'Expired: it was waiting until %s.', 'pagesco-books' ), $date );
			case 'collected':
				return __( 'Collected. Enjoy the book!', 'pagesco-books' );
		}

		return __( 'Cancelled.', 'pagesco-books' );
	}

	/**
	 * The message for a result code that a form handler put in the address (?pagesco_hold=...), or ''.
	 * Only known codes have a message, so the address cannot put any other text on the page.
	 *
	 * @param string $code A result code.
	 */
	public static function message( string $code ): string {
		$messages = array(
			'placed'                 => __( 'Reserved! The book is waiting for you at the counter.', 'pagesco-books' ),
			'cancelled'              => __( 'Your hold was cancelled.', 'pagesco-books' ),
			'collected'              => __( 'The hold was marked as collected.', 'pagesco-books' ),
			'pagesco_hold_sold_out'  => __( 'This book is sold out, so it cannot be reserved right now.', 'pagesco-books' ),
			'pagesco_hold_duplicate' => __( 'This book is already waiting for you at the counter.', 'pagesco-books' ),
			'pagesco_hold_limit'     => __( 'You have reached the most books you can have waiting. Collect or cancel one first.', 'pagesco-books' ),
			'pagesco_hold_not_found' => __( 'That hold is no longer waiting.', 'pagesco-books' ),
		);

		return $messages[ $code ] ?? '';
	}
}

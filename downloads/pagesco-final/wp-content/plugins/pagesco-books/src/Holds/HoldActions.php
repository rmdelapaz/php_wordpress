<?php
/**
 * The form handlers of Reserve & Pick Up, on admin-post.php: they work without JavaScript.
 *
 * @package PagesCo\Books
 */

namespace PagesCo\Books\Holds;

use PagesCo\Books\Feature;

/**
 * Reserve and cancel for customers, collect for staff. Each handler checks the nonce and the capability,
 * asks Holds to do the work, and redirects back with a result code (Lesson 5.3's admin-post.php pattern).
 */
final class HoldActions implements Feature {

	/**
	 * The admin-post.php actions; each is also the start of its nonce action.
	 */
	public const PLACE   = 'pagesco_books_place_hold';
	public const CANCEL  = 'pagesco_books_cancel_hold';
	public const COLLECT = 'pagesco_books_collect_hold';

	/**
	 * The capability a customer needs: every logged-in role has it, Subscribers included.
	 */
	public const CUSTOMER_CAP = 'read';

	/**
	 * The capability staff need to mark holds as collected (editors and administrators).
	 */
	public const STAFF_CAP = 'edit_others_posts';

	/**
	 * Only logged-in users: there is no admin_post_nopriv_ handler, so admin-post.php refuses visitors.
	 */
	public function register(): void {
		add_action( 'admin_post_' . self::PLACE, array( $this, 'place' ) );
		add_action( 'admin_post_' . self::CANCEL, array( $this, 'cancel' ) );
		add_action( 'admin_post_' . self::COLLECT, array( $this, 'collect' ) );
	}

	/**
	 * Prints the hidden fields of a form that runs one of these actions on one ID: the action, the ID, a nonce.
	 *
	 * @param string $action One of the constants.
	 * @param string $field  The name of the ID field: book or hold.
	 * @param int    $id     The book or hold ID.
	 */
	public static function print_fields( string $action, string $field, int $id ): void {
		printf( '<input type="hidden" name="action" value="%s">', esc_attr( $action ) );
		printf( '<input type="hidden" name="%s" value="%d">', esc_attr( $field ), absint( $id ) );
		// Not wp_nonce_field(): it gives every field id="_wpnonce", and a page with several forms would repeat the ID.
		printf( '<input type="hidden" name="_wpnonce" value="%s">', esc_attr( wp_create_nonce( $action . '_' . $id ) ) );
	}

	/**
	 * POST book=ID: places a hold, then goes back to the book's page.
	 */
	public function place(): void {
		$book_id = $this->posted_id( 'book', self::PLACE, self::CUSTOMER_CAP );
		$result  = ( new Holds() )->place( $book_id, get_current_user_id() );

		$this->back( is_wp_error( $result ) ? $result->get_error_code() : 'placed', get_permalink( $book_id ) );
	}

	/**
	 * POST hold=ID: cancels one of the user's own holds, then goes back to the page the form was on.
	 */
	public function cancel(): void {
		$hold_id = $this->posted_id( 'hold', self::CANCEL, self::CUSTOMER_CAP );
		$result  = ( new Holds() )->cancel( $hold_id, get_current_user_id() );

		$this->back( is_wp_error( $result ) ? $result->get_error_code() : 'cancelled', home_url( '/my-holds/' ) );
	}

	/**
	 * POST hold=ID: staff mark a hold as collected, then go back to Books > Holds.
	 */
	public function collect(): void {
		$hold_id = $this->posted_id( 'hold', self::COLLECT, self::STAFF_CAP );
		$result  = ( new Holds() )->collect( $hold_id );

		$this->back( is_wp_error( $result ) ? $result->get_error_code() : 'collected', admin_url( 'edit.php?post_type=book&page=pagesco-holds' ) );
	}

	/**
	 * Reads the posted ID, then checks the nonce for that ID and the capability. Stops with 403 if either fails.
	 *
	 * @param string $field      The ID field: book or hold.
	 * @param string $action     The nonce action's start.
	 * @param string $capability What the user must be able to do.
	 */
	private function posted_id( string $field, string $action, string $capability ): int {
		$id = isset( $_POST[ $field ] ) ? absint( wp_unslash( $_POST[ $field ] ) ) : 0;

		check_admin_referer( $action . '_' . $id );

		if ( ! current_user_can( $capability ) ) {
			wp_die( esc_html__( 'Sorry, you are not allowed to do that.', 'pagesco-books' ), 403 );
		}

		return $id;
	}

	/**
	 * Redirects to a page of this site with the result code in the address, and stops.
	 *
	 * @param string       $code The result: placed, cancelled, collected or an error code.
	 * @param string|false $url  Where to go.
	 */
	private function back( string $code, $url ): void {
		wp_safe_redirect( add_query_arg( 'pagesco_hold', $code, $url ? $url : home_url( '/' ) ), 303 );
		exit;
	}
}

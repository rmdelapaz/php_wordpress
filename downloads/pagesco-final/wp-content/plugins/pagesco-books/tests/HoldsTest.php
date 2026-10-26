<?php
/**
 * Tests of Reserve & Pick Up: the rules in Holds, and the REST route's door.
 *
 * @package PagesCo\Books
 */

namespace PagesCo\Books\Tests;

use PagesCo\Books\Holds\Holds;
use PagesCo\Books\Holds\HoldsTable;

/**
 * Each rule of the brief, broken on purpose once.
 */
final class HoldsTest extends \WP_UnitTestCase {

	/**
	 * A customer.
	 *
	 * @var int
	 */
	private int $jordan;

	/**
	 * Another customer.
	 *
	 * @var int
	 */
	private int $priya;

	/**
	 * Four books in stock and one sold out.
	 *
	 * @var int[]
	 */
	private array $books = array();

	/**
	 * Two customers, five books. The test library empties the tables between tests, the holds table too.
	 */
	public function set_up(): void {
		parent::set_up();

		$this->jordan = self::factory()->user->create( array( 'role' => 'subscriber' ) );
		$this->priya  = self::factory()->user->create( array( 'role' => 'subscriber' ) );

		foreach ( array( 'Dune', '1984', 'Emma', 'Persuasion', 'The Great Gatsby' ) as $title ) {
			$this->books[ $title ] = self::factory()->post->create(
				array(
					'post_type'  => 'book',
					'post_title' => $title,
					'meta_input' => array( 'pagesco_in_stock' => 'The Great Gatsby' !== $title ),
				)
			);
		}
	}

	/**
	 * A hold waits for the number of days in the settings, and the confirmation email goes out.
	 */
	public function test_place_keeps_the_book_for_the_set_days_and_sends_an_email(): void {
		// Catch the email before it is sent: pre_wp_mail gets wp_mail()'s arguments, and a non-null answer stops it.
		$mail = array();
		add_filter(
			'pre_wp_mail',
			function ( $result, $atts ) use ( &$mail ) {
				$mail = $atts;
				return true;
			},
			10,
			2
		);

		$hold = ( new Holds() )->place( $this->books['Dune'], $this->jordan );

		$this->assertIsObject( $hold );
		$this->assertSame( 'waiting', Holds::status( $hold ) );
		$this->assertSame( wp_date( 'Y-m-d', time() + 3 * DAY_IN_SECONDS ), $hold->pickup_by );
		$this->assertSame( get_userdata( $this->jordan )->user_email, $mail['to'] );
		$this->assertStringContainsString( 'Dune', $mail['subject'] );
	}

	/**
	 * The same book twice, a sold-out book, and one book too many are all refused.
	 */
	public function test_refuses_duplicates_sold_out_books_and_too_many_holds(): void {
		$holds = new Holds();

		$holds->place( $this->books['Dune'], $this->jordan );
		$this->assertWPError( $holds->place( $this->books['Dune'], $this->jordan ) );
		$this->assertSame( 'pagesco_hold_duplicate', $holds->place( $this->books['Dune'], $this->jordan )->get_error_code() );
		$this->assertSame( 'pagesco_hold_sold_out', $holds->place( $this->books['The Great Gatsby'], $this->jordan )->get_error_code() );

		$holds->place( $this->books['1984'], $this->jordan );
		$holds->place( $this->books['Emma'], $this->jordan );
		$this->assertSame( 'pagesco_hold_limit', $holds->place( $this->books['Persuasion'], $this->jordan )->get_error_code() );
	}

	/**
	 * An expired hold no longer counts: the customer may reserve the same book again.
	 */
	public function test_an_expired_hold_is_computed_and_frees_the_book(): void {
		$old = HoldsTable::add( $this->books['Dune'], $this->jordan, wp_date( 'Y-m-d', time() - DAY_IN_SECONDS ) );

		$this->assertSame( 'expired', Holds::status( HoldsTable::get( $old ) ) );
		$this->assertIsObject( ( new Holds() )->place( $this->books['Dune'], $this->jordan ) );
	}

	/**
	 * Priya cannot cancel Jordan's hold: for her it does not exist. Jordan can.
	 */
	public function test_only_the_customer_can_cancel_their_hold(): void {
		$hold = ( new Holds() )->place( $this->books['Dune'], $this->jordan );

		$refused = ( new Holds() )->cancel( (int) $hold->id, $this->priya );
		$this->assertWPError( $refused );
		$this->assertSame( 'pagesco_hold_not_found', $refused->get_error_code() );
		$this->assertSame( 'waiting', HoldsTable::get( (int) $hold->id )->status );
		$this->assertSame( 'cancelled', ( new Holds() )->cancel( (int) $hold->id, $this->jordan )->status );
	}

	/**
	 * The REST route turns visitors away with 401, and gives a customer 201 Created.
	 */
	public function test_the_rest_route_needs_a_logged_in_customer(): void {
		$request = new \WP_REST_Request( 'POST', '/pagesco/v1/holds' );
		$request->set_param( 'book', $this->books['Dune'] );

		$this->assertSame( 401, rest_do_request( $request )->get_status() );

		wp_set_current_user( $this->jordan );
		$this->assertSame( 201, rest_do_request( $request )->get_status() );
	}
}

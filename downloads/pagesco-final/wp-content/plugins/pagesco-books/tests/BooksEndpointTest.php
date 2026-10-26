<?php
/**
 * Tests of GET /pagesco/v1/books, through the REST server without HTTP.
 *
 * @package PagesCo\Books
 */

namespace PagesCo\Books\Tests;

use PagesCo\Books\Plugin;
use PagesCo\Books\Rest\BooksEndpoint;

/**
 * The books route filters, sorts and keeps the promise of its schema.
 */
final class BooksEndpointTest extends \WP_UnitTestCase {

	/**
	 * Three books: two fantasy books and Dune.
	 */
	public function set_up(): void {
		parent::set_up();

		$fantasy = self::factory()->term->create(
			array(
				'taxonomy' => 'genre',
				'name'     => 'Fantasy',
				'slug'     => 'fantasy',
			)
		);

		$prices = array(
			'Lord of the Rings' => 15.99,
			'The Hobbit'        => 10.99,
			'Dune'              => 14.99,
		);

		foreach ( $prices as $title => $price ) {
			$book_id = self::factory()->post->create(
				array(
					'post_type'  => 'book',
					'post_title' => $title,
					'meta_input' => array( 'pagesco_price' => $price ),
				)
			);
			if ( 'Dune' !== $title ) {
				wp_set_object_terms( $book_id, $fantasy, 'genre' );
			}
		}
	}

	/**
	 * Runs GET /pagesco/v1/books with these query parameters.
	 *
	 * @param array $params Query parameters.
	 * @return \WP_REST_Response
	 */
	private function get_books( array $params ): \WP_REST_Response {
		$request = new \WP_REST_Request( 'GET', '/pagesco/v1/books' );
		$request->set_query_params( $params );

		return rest_do_request( $request );
	}

	/**
	 * The fantasy books, cheapest first, with the total in a header.
	 */
	public function test_filters_by_genre_and_sorts_by_price(): void {
		$response = $this->get_books(
			array(
				'genre'   => 'fantasy',
				'orderby' => 'price',
			)
		);

		$this->assertSame( 200, $response->get_status() );
		$this->assertSame( array( 'The Hobbit', 'Lord of the Rings' ), wp_list_pluck( $response->get_data(), 'title' ) );
		$this->assertSame( '2', $response->get_headers()['X-WP-Total'] );
	}

	/**
	 * A genre that does not exist is a 400 with the plugin's own error code.
	 */
	public function test_rejects_an_unknown_genre(): void {
		$response = $this->get_books( array( 'genre' => 'romance' ) );

		$this->assertSame( 400, $response->get_status() );
		$this->assertSame( 'pagesco_unknown_genre', $response->get_data()['data']['details']['genre']['code'] );
	}

	/**
	 * Every book the route returns is valid against the route's own schema.
	 */
	public function test_every_book_matches_the_schema(): void {
		$endpoint = Plugin::instance()->feature( BooksEndpoint::class );

		foreach ( $this->get_books( array() )->get_data() as $book ) {
			$this->assertTrue( rest_validate_value_from_schema( $book, $endpoint->get_schema(), 'book' ) );
		}
	}
}

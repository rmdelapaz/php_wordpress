<?php
/**
 * Tests of the supplier client, without the network.
 *
 * @package PagesCo\Books
 */

namespace PagesCo\Books\Tests;

use PagesCo\Books\Supplier\Client;

/**
 * Every test answers in place of the supplier with the pre_http_request filter.
 */
final class SupplierClientTest extends \WP_UnitTestCase {

	/**
	 * The requests the client tried to send: URL and arguments.
	 *
	 * @var array[]
	 */
	private array $requests = array();

	/**
	 * Answers every HTTP request with this status code and body, and records the request.
	 *
	 * @param int    $code The HTTP status code.
	 * @param string $body The response body.
	 */
	private function fake_supplier( int $code, string $body ): void {
		add_filter(
			'pre_http_request',
			function ( $preempt, $args, $url ) use ( $code, $body ) {
				$this->requests[] = array(
					'url'  => $url,
					'args' => $args,
				);

				return array(
					'headers'  => array(),
					'body'     => $body,
					'response' => array(
						'code'    => $code,
						'message' => get_status_header_desc( $code ),
					),
					'cookies'  => array(),
					'filename' => null,
				);
			},
			10,
			3
		);
	}

	/**
	 * A good answer becomes an array keyed by ISBN, and the request carries the key.
	 */
	public function test_reads_availability_by_isbn(): void {
		$this->fake_supplier( 200, '{"items":[{"isbn":"9780743273565","available":0,"next_delivery":"2027-11-15"}],"unknown":[]}' );

		$result = ( new Client() )->availability( array( '9780743273565' ) );

		$this->assertSame(
			array(
				'9780743273565' => array(
					'available'     => 0,
					'next_delivery' => '2027-11-15',
				),
			),
			$result
		);
		$this->assertSame( 'https://api.riverside.example/v1/availability?isbns=9780743273565', $this->requests[0]['url'] );
		$this->assertSame( 'test-key', $this->requests[0]['args']['headers']['X-Api-Key'] );
	}

	/**
	 * An error status is a WP_Error with the status in its data, even when the body is HTML.
	 */
	public function test_turns_an_error_status_into_a_wp_error(): void {
		$this->fake_supplier( 503, '<h1>Service Unavailable</h1>' );

		$result = ( new Client() )->availability( array( '9780743273565' ) );

		$this->assertWPError( $result );
		$this->assertSame( 'pagesco_supplier_http_error', $result->get_error_code() );
		$this->assertSame( 503, $result->get_error_data()['status'] );
	}

	/**
	 * A 200 without the expected items is not trusted.
	 */
	public function test_rejects_an_answer_without_items(): void {
		$this->fake_supplier( 200, '{"supplier":"Riverside Books"}' );

		$result = ( new Client() )->availability( array( '9780743273565' ) );

		$this->assertWPError( $result );
		$this->assertSame( 'pagesco_supplier_bad_response', $result->get_error_code() );
	}

	/**
	 * No answer at all: the transport's WP_Error comes back unchanged.
	 */
	public function test_passes_on_a_network_failure(): void {
		add_filter(
			'pre_http_request',
			function () {
				return new \WP_Error( 'http_request_failed', 'cURL error 28: Operation timed out' );
			}
		);

		$result = ( new Client() )->availability( array( '9780743273565' ) );

		$this->assertWPError( $result );
		$this->assertSame( 'http_request_failed', $result->get_error_code() );
	}
}

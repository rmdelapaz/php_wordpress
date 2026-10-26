<?php
/**
 * The supplier's API (Riverside Books), over HTTP.
 *
 * @package PagesCo\Books
 */

namespace PagesCo\Books\Supplier;

use WP_Error;

/**
 * Asks the supplier what it has, and places orders. Every method returns data or a WP_Error, never both.
 *
 * The address and the API key come from wp-config.php: PAGESCO_BOOKS_SUPPLIER_URL and PAGESCO_BOOKS_SUPPLIER_KEY.
 * Outside a local development site, the address must use HTTPS, because the key is sent with every request.
 */
final class Client {

	/**
	 * Seconds to wait for the supplier before giving up.
	 */
	private const TIMEOUT = 5;

	/**
	 * GET /availability: copies at the supplier and the next delivery date, keyed by ISBN.
	 *
	 * @param string[] $isbns ISBN-13s without dashes.
	 * @return array<string, array{available: int, next_delivery: string}>|WP_Error
	 */
	public function availability( array $isbns ) {
		$url = $this->url( 'availability' );
		if ( is_wp_error( $url ) ) {
			return $url;
		}

		$response = wp_remote_get(
			add_query_arg( 'isbns', rawurlencode( implode( ',', $isbns ) ), $url ),
			array(
				'timeout' => self::TIMEOUT,
				'headers' => $this->headers(),
			)
		);

		$data = $this->decode( $response );
		if ( is_wp_error( $data ) ) {
			return $data;
		}
		if ( ! isset( $data['items'] ) || ! is_array( $data['items'] ) ) {
			return new WP_Error( 'pagesco_supplier_bad_response', __( 'The supplier answered without a list of items.', 'pagesco-books' ) );
		}

		$availability = array();
		foreach ( $data['items'] as $item ) {
			$availability[ (string) ( $item['isbn'] ?? '' ) ] = array(
				'available'     => (int) ( $item['available'] ?? 0 ),
				'next_delivery' => (string) ( $item['next_delivery'] ?? '' ),
			);
		}

		return $availability;
	}

	/**
	 * POST /orders: orders copies of a book. Returns the supplier's order confirmation.
	 *
	 * @param string $isbn     ISBN-13 without dashes.
	 * @param int    $quantity How many copies.
	 * @return array|WP_Error
	 */
	public function order( string $isbn, int $quantity ) {
		$url = $this->url( 'orders' );
		if ( is_wp_error( $url ) ) {
			return $url;
		}

		$response = wp_remote_post(
			$url,
			array(
				'timeout' => self::TIMEOUT,
				'headers' => $this->headers() + array( 'Content-Type' => 'application/json' ),
				'body'    => wp_json_encode(
					array(
						'isbn'     => $isbn,
						'quantity' => $quantity,
					)
				),
			)
		);

		return $this->decode( $response );
	}

	/**
	 * The full address of one of the supplier's endpoints, from the URL in wp-config.php.
	 *
	 * @param string $endpoint The endpoint's path, such as availability.
	 * @return string|WP_Error
	 */
	private function url( string $endpoint ) {
		if ( ! defined( 'PAGESCO_BOOKS_SUPPLIER_URL' ) || ! defined( 'PAGESCO_BOOKS_SUPPLIER_KEY' ) ) {
			return new WP_Error( 'pagesco_supplier_not_configured', __( 'The supplier is not configured in wp-config.php.', 'pagesco-books' ) );
		}

		// The API key goes with every request: only over HTTPS, except on a local development site (Lesson 8.4).
		if ( 'https' !== wp_parse_url( PAGESCO_BOOKS_SUPPLIER_URL, PHP_URL_SCHEME ) && 'local' !== wp_get_environment_type() ) {
			return new WP_Error( 'pagesco_supplier_insecure', __( 'The supplier address must start with https:// on this site.', 'pagesco-books' ) );
		}

		return trailingslashit( PAGESCO_BOOKS_SUPPLIER_URL ) . $endpoint;
	}

	/**
	 * The headers every request sends: what we accept, and who we are.
	 */
	private function headers(): array {
		return array(
			'Accept'    => 'application/json',
			'X-Api-Key' => PAGESCO_BOOKS_SUPPLIER_KEY,
		);
	}

	/**
	 * Turns an HTTP response into data, or into a WP_Error for each way it can go wrong.
	 *
	 * @param array|WP_Error $response What wp_remote_get() or wp_remote_post() returned.
	 * @return array|WP_Error
	 */
	private function decode( $response ) {
		// 1. No answer at all: DNS, connection refused, timeout.
		if ( is_wp_error( $response ) ) {
			return $response;
		}

		$code = wp_remote_retrieve_response_code( $response );
		$data = json_decode( wp_remote_retrieve_body( $response ), true );

		// 2. An answer, but not a success: 401, 404, 422, 503...
		if ( $code < 200 || $code > 299 ) {
			return new WP_Error(
				'pagesco_supplier_http_error',
				sprintf(
					/* translators: 1: HTTP status code, 2: the supplier's message. */
					__( 'The supplier answered %1$d: %2$s', 'pagesco-books' ),
					$code,
					is_array( $data ) && isset( $data['message'] ) ? $data['message'] : wp_remote_retrieve_response_message( $response )
				),
				array(
					'status'      => $code,
					'retry_after' => wp_remote_retrieve_header( $response, 'retry-after' ),
				)
			);
		}

		// 3. A success that is not the JSON we expect.
		if ( ! is_array( $data ) ) {
			return new WP_Error( 'pagesco_supplier_bad_response', __( 'The supplier\'s answer is not JSON.', 'pagesco-books' ) );
		}

		return $data;
	}
}

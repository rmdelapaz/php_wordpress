<?php
/**
 * remote_answers_solution.php: the instructor's reference for remote_answers_starter.php (Session 14, Lesson 7.3, lab A)
 * state: after:lesson_24
 * expect: genre=fantasy     2 books: The Hobbit, Lord of the Rings
 * expect: books/99          pagesco_remote_http_error (404): No book was found with that ID.
 * expect: shop.invalid      http_request_failed: cURL error 6: Could not resolve host: shop.invalid
 */
/**
 * Asks a JSON API and returns the decoded data, or a WP_Error for each way the call can fail.
 *
 * @param string $url The full URL.
 * @return array|WP_Error
 */
function pagesco_lab_ask( string $url ) {
	$response = wp_remote_get(
		$url,
		array(
			'timeout' => 3,
			'headers' => array( 'Accept' => 'application/json' ),
		)
	);

	// 1. No answer at all.
	if ( is_wp_error( $response ) ) {
		return $response;
	}

	$code = wp_remote_retrieve_response_code( $response );
	$data = json_decode( wp_remote_retrieve_body( $response ), true );

	// 2. An answer, but not a success.
	if ( $code < 200 || $code > 299 ) {
		$message = is_array( $data ) && isset( $data['message'] ) ? $data['message'] : wp_remote_retrieve_response_message( $response );
		return new WP_Error( 'pagesco_remote_http_error', $message, array( 'status' => $code ) );
	}

	// 3. A success that is not the JSON we expect.
	if ( ! is_array( $data ) ) {
		return new WP_Error( 'pagesco_remote_bad_response', 'The answer is not JSON.' );
	}

	return $data;
}

$pagesco_api   = rest_url( 'pagesco/v1/' );
$pagesco_tries = array(
	'genre=fantasy' => $pagesco_api . 'books?genre=fantasy&orderby=price',
	'genre=romance' => $pagesco_api . 'books?genre=romance',
	'books/99'      => $pagesco_api . 'books/99',
	'a web page'    => home_url( '/about/' ),
	'shop.invalid'  => 'http://shop.invalid/v1/books',
);

foreach ( $pagesco_tries as $pagesco_label => $pagesco_url ) {
	$pagesco_result = pagesco_lab_ask( $pagesco_url );

	if ( is_wp_error( $pagesco_result ) ) {
		$pagesco_status = $pagesco_result->get_error_data()['status'] ?? null;
		printf( "%-17s %s%s: %s\n", $pagesco_label, $pagesco_result->get_error_code(), $pagesco_status ? " ($pagesco_status)" : '', $pagesco_result->get_error_message() );
	} else {
		printf( "%-17s %d books: %s\n", $pagesco_label, count( $pagesco_result ), implode( ', ', wp_list_pluck( $pagesco_result, 'title' ) ) );
	}
}

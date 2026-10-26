<?php
/**
 * remote_answers_starter.php: one careful API client, five kinds of answer (Session 14, Lesson 7.3, lab A)
 * state: after:lesson_24
 * expect: genre=fantasy     pagesco_todo: TODO: ask and check the answer
 *
 * Lesson 7.3's three ways to fail, practiced on an API you already know: your own pagesco/v1 (Lesson 7.2), called
 * over HTTP like a stranger's service. A 400 or a 404 is not a WP_Error, a web page is not JSON, and a host that
 * does not exist gives no answer at all. No internet needed (.invalid never exists). From your project folder:
 *     cp labs/module-14/l7_3-external-apis-cron/remote_answers_starter.php wordpress/
 *     wp eval-file --use-include remote_answers_starter.php
 * Write pagesco_lab_ask(), run after each TODO, and compare with "Expected when done".
 * When you are done: rm wordpress/remote_answers_starter.php
 */
/**
 * Asks a JSON API and returns the decoded data, or a WP_Error for each way the call can fail.
 *
 * @param string $url The full URL.
 * @return array|WP_Error
 */
function pagesco_lab_ask( string $url ) {
	// TODO 1: wp_remote_get( $url ) with a timeout of 3 seconds and the header Accept: application/json.
	// TODO 2: no answer at all (is_wp_error()): return that WP_Error as it is.
	// TODO 3: a status outside 200 to 299: return new WP_Error( 'pagesco_remote_http_error', <the JSON's message, or
	//         wp_remote_retrieve_response_message()>, array( 'status' => <the code> ) ).
	// TODO 4: the body does not decode to an array: return new WP_Error( 'pagesco_remote_bad_response', 'The answer is not JSON.' ).
	//         Otherwise return the decoded array.
	return new WP_Error( 'pagesco_todo', 'TODO: ask and check the answer' );
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

// Expected when done (remote_answers_solution.php, the site after Lesson 7.2):
// genre=fantasy     2 books: The Hobbit, Lord of the Rings
// genre=romance     pagesco_remote_http_error (400): Invalid parameter(s): genre
// books/99          pagesco_remote_http_error (404): No book was found with that ID.
// a web page        pagesco_remote_bad_response: The answer is not JSON.
// shop.invalid      http_request_failed: cURL error 6: Could not resolve host: shop.invalid (Domain name not found)

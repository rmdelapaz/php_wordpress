<?php
/**
 * fake_supplier_starter.php: the supplier client checked against four fake answers (Session 15, Lesson 8.1, lab A)
 * state: after:lesson_25
 * expect: TODO check 2: a 401 becomes pagesco_supplier_http_error with the status in its data
 *
 * The idea of Lesson 8.1's SupplierClientTest without PHPUnit: the pre_http_request filter answers in place of the
 * network, so the script decides exactly what "the supplier" says, bad days included. From your project folder:
 *     cp labs/module-15/l8_1-debugging-testing/fake_supplier_starter.php wordpress/
 *     wp eval-file --use-include fake_supplier_starter.php
 * Check 1 is done for you. For checks 2 to 4, replace each TODO line with a pagesco_lab_fake() call (the answer)
 * and a pagesco_lab_check() call (what the client must return: is_wp_error(), get_error_code(),
 * get_error_data()). Run again after each one and compare with "Expected when done" at the end.
 * When you are done: rm wordpress/fake_supplier_starter.php
 */

$pagesco_client = new PagesCo\Books\Supplier\Client();

/**
 * Adds to one of the script's two counters and returns its value (wp eval-file runs this file inside a function,
 * so a static variable is simpler than a global).
 *
 * @param string $name requests or passed.
 * @param int    $add  How much to add.
 */
function pagesco_lab_tally( string $name, int $add = 0 ): int {
	static $counts = array(
		'requests' => 0,
		'passed'   => 0,
	);
	$counts[ $name ] += $add;
	return $counts[ $name ];
}

/**
 * Answers every HTTP request with this status code and body (or with $error, a WP_Error), and counts the requests.
 *
 * @param int           $code  The HTTP status code.
 * @param string        $body  The response body.
 * @param WP_Error|null $error An answer that never came: the transport's error.
 */
function pagesco_lab_fake( int $code, string $body, ?WP_Error $error = null ): void {
	remove_all_filters( 'pre_http_request' );
	add_filter(
		'pre_http_request',
		function () use ( $code, $body, $error ) {
			pagesco_lab_tally( 'requests', 1 );
			return $error ?? array(
				'headers'  => array(),
				'body'     => $body,
				'response' => array(
					'code'    => $code,
					'message' => get_status_header_desc( $code ),
				),
				'cookies'  => array(),
				'filename' => null,
			);
		}
	);
}

/**
 * Prints PASS or FAIL for one check and counts the passes.
 *
 * @param string $label What must be true.
 * @param bool   $ok    Whether it is.
 */
function pagesco_lab_check( string $label, bool $ok ): void {
	pagesco_lab_tally( 'passed', $ok ? 1 : 0 );
	printf( "%s %s\n", $ok ? 'PASS' : 'FAIL', $label );
}

// Check 1 (done for you): a good answer becomes an array keyed by ISBN.
pagesco_lab_fake( 200, '{"items":[{"isbn":"9780441172719","available":24,"next_delivery":""}],"unknown":[]}' );
$pagesco_result = $pagesco_client->availability( array( '9780441172719' ) );
pagesco_lab_check( 'a good answer is keyed by ISBN', is_array( $pagesco_result ) && 24 === $pagesco_result['9780441172719']['available'] );

// TODO check 2: the supplier answers 401 with the body {"message":"Send a valid API key in the X-Api-Key header."}.
//               The client must return a WP_Error with the code pagesco_supplier_http_error and 401 as its
//               data's status.
echo "TODO check 2: a 401 becomes pagesco_supplier_http_error with the status in its data\n";

// TODO check 3: the supplier answers 200 with an HTML maintenance page: <h1>Back soon</h1>
//               The client must return the WP_Error pagesco_supplier_bad_response (a 200 is not enough).
echo "TODO check 3: a 200 that is not JSON becomes pagesco_supplier_bad_response\n";

// TODO check 4: no answer at all: pass new WP_Error( 'http_request_failed', 'cURL error 28: Operation timed out' )
//               as the third argument of pagesco_lab_fake(). The client must return that error unchanged.
echo "TODO check 4: a network failure comes back unchanged\n";

remove_all_filters( 'pre_http_request' );
printf( "%d of 4 checks passed, %d requests answered by the fake, none by the network\n", pagesco_lab_tally( 'passed' ), pagesco_lab_tally( 'requests' ) );

// Expected when done (fake_supplier_solution.php, the course site after Lesson 7.3):
// PASS a good answer is keyed by ISBN
// PASS a 401 becomes pagesco_supplier_http_error with the status in its data
// PASS a 200 that is not JSON becomes pagesco_supplier_bad_response
// PASS a network failure comes back unchanged
// 4 of 4 checks passed, 4 requests answered by the fake, none by the network

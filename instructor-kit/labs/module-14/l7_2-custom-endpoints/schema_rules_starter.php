<?php
/**
 * schema_rules_starter.php: what a route's argument schema accepts, and what it turns the value into (Session 14, Lesson 7.2, lab B)
 * state: after:lesson_23
 * expect: price = "14.99"                   TODO
 *
 * Every argument of a route with a 'type' goes through two functions before your callback sees it:
 * rest_validate_value_from_schema() (true or a WP_Error) and rest_sanitize_value_from_schema() (the clean value).
 * Query strings only carry strings, so each value below arrives as a string. From your project folder:
 *     cp labs/module-14/l7_2-custom-endpoints/schema_rules_starter.php wordpress/
 *     wp eval-file --use-include schema_rules_starter.php
 * Predict yes or no for every case first (and what "yes" turns the string into), then fill in the TODOs.
 * When you are done: rm wordpress/schema_rules_starter.php
 */
$pagesco_cases = array(
	array( 'price', array( 'type' => 'number' ), '14.99' ),
	array( 'price', array( 'type' => 'number' ), 'free' ),
	array( 'in_stock', array( 'type' => 'boolean' ), 'true' ),
	array( 'in_stock', array( 'type' => 'boolean' ), 'maybe' ),
	array( 'per_page', array( 'type' => 'integer', 'minimum' => 1, 'maximum' => 100 ), '500' ),
	array( 'orderby', array( 'type' => 'string', 'enum' => array( 'title', 'newest', 'price' ) ), 'pages' ),
	array( 'genres', array( 'type' => 'array', 'items' => array( 'type' => 'string' ) ), 'fantasy,classic' ),
	array( 'title', array( 'type' => 'string', 'minLength' => 1 ), '' ),
	array( 'starts_at', array( 'type' => 'string', 'format' => 'date-time' ), '2027-12-16T19:00:00' ),
	array( 'starts_at', array( 'type' => 'string', 'format' => 'date-time' ), '16/12/2027 7pm' ),
);

foreach ( $pagesco_cases as $pagesco_case ) {
	list( $pagesco_name, $pagesco_schema, $pagesco_value ) = $pagesco_case;
	$pagesco_label = sprintf( '%-33s', $pagesco_name . ' = ' . wp_json_encode( $pagesco_value, JSON_UNESCAPED_SLASHES ) );

	// TODO 1: rest_validate_value_from_schema( value, schema, name ). A WP_Error: print " no: " and its message.
	// TODO 2: otherwise print " yes: " and wp_json_encode() of rest_sanitize_value_from_schema( value, schema, name ).
	echo $pagesco_label, " TODO\n";
}

// Expected when done (schema_rules_solution.php):
// price = "14.99"                   yes: 14.99
// price = "free"                    no: price is not of type number.
// in_stock = "true"                 yes: true
// in_stock = "maybe"                no: in_stock is not of type boolean.
// per_page = "500"                  no: per_page must be between 1 (inclusive) and 100 (inclusive)
// orderby = "pages"                 no: orderby is not one of title, newest, and price.
// genres = "fantasy,classic"        yes: ["fantasy","classic"]
// title = ""                        no: title must be at least 1 character long.
// starts_at = "2027-12-16T19:00:00" yes: "2027-12-16T19:00:00"
// starts_at = "16/12/2027 7pm"      no: Invalid date.

<?php
/**
 * schema_rules_solution.php: the instructor's reference for schema_rules_starter.php (Session 14, Lesson 7.2, lab B)
 * state: after:lesson_23
 * expect: no: per_page must be between 1 (inclusive) and 100 (inclusive)
 * expect: yes: ["fantasy","classic"]
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

	$pagesco_valid = rest_validate_value_from_schema( $pagesco_value, $pagesco_schema, $pagesco_name );
	$pagesco_label = sprintf( '%-33s', $pagesco_name . ' = ' . wp_json_encode( $pagesco_value, JSON_UNESCAPED_SLASHES ) );

	if ( is_wp_error( $pagesco_valid ) ) {
		echo $pagesco_label, ' no: ', $pagesco_valid->get_error_message(), "\n";
	} else {
		echo $pagesco_label, ' yes: ', wp_json_encode( rest_sanitize_value_from_schema( $pagesco_value, $pagesco_schema, $pagesco_name ) ), "\n";
	}
}

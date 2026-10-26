<?php
/**
 * ownership_sql_solution.php: ownership in the query, "not found" for everyone else (Session 17, Lesson 9.1, lab A)
 * state: after:lesson_29
 * expect: Devon closes wish 1          pagesco_wish_not_found (404)
 * expect: Maria closes wish 1          closed
 *
 * The reference for ownership_sql_starter.php. Wish lists, not holds: the same three habits as Milestones 2 to 4.
 * The user ID comes from the login, never from the request; the owner goes into the SQL WHERE; anyone else's
 * row is "not found", so nobody can test which IDs exist.
 */
global $wpdb;

/**
 * The lab's table name, with this site's prefix.
 */
function pagesco_lab_wish_table(): string {
	global $wpdb;

	return $wpdb->prefix . 'pagesco_lab_wishes';
}

// A TEMPORARY table: MySQL drops it when this script's connection closes, so nothing stays on your site.
$wpdb->query(
	$wpdb->prepare(
		'CREATE TEMPORARY TABLE %i (
			id bigint unsigned NOT NULL AUTO_INCREMENT,
			user_id bigint unsigned NOT NULL,
			book_id bigint unsigned NOT NULL,
			status varchar(20) NOT NULL DEFAULT %s,
			PRIMARY KEY  (id),
			KEY user_status (user_id,status)
		)',
		pagesco_lab_wish_table(),
		'open'
	)
);

/**
 * Adds an open wish and returns its ID (done for you, like HoldsTable::add()).
 *
 * @param int $user_id The customer.
 * @param int $book_id The book.
 */
function pagesco_lab_add_wish( int $user_id, int $book_id ): int {
	global $wpdb;

	$wpdb->insert( pagesco_lab_wish_table(), array( 'user_id' => $user_id, 'book_id' => $book_id ), array( '%d', '%d' ) );

	return (int) $wpdb->insert_id;
}

/**
 * One customer's wishes, newest first.
 *
 * @param int $user_id The customer.
 * @return object[]
 */
function pagesco_lab_wishes_of( int $user_id ): array {
	global $wpdb;

	return $wpdb->get_results(
		$wpdb->prepare( 'SELECT id, book_id, status FROM %i WHERE user_id = %d ORDER BY id DESC', pagesco_lab_wish_table(), $user_id )
	);
}

/**
 * Closes an open wish, only if it belongs to the user: the owner is part of the WHERE.
 *
 * @param int $wish_id The wish.
 * @param int $user_id The customer who asks.
 */
function pagesco_lab_close_wish( int $wish_id, int $user_id ): bool {
	global $wpdb;

	return 1 === $wpdb->update(
		pagesco_lab_wish_table(),
		array( 'status' => 'closed' ),
		array(
			'id'      => $wish_id,
			'user_id' => $user_id,
			'status'  => 'open',
		),
		array( '%s' ),
		array( '%d', '%d', '%s' )
	);
}

/**
 * The door: who is asking comes from the login. Every refusal is the same 404.
 *
 * @param int $wish_id The wish named in the request.
 * @return string|WP_Error
 */
function pagesco_lab_close_door( int $wish_id ) {
	$pagesco_user = get_current_user_id();

	if ( ! $pagesco_user || ! pagesco_lab_close_wish( $wish_id, $pagesco_user ) ) {
		return new WP_Error( 'pagesco_wish_not_found', 'You have no open wish with that ID.', array( 'status' => 404 ) );
	}

	return 'closed';
}

$pagesco_maria = get_user_by( 'login', 'maria' )->ID;
$pagesco_devon = get_user_by( 'login', 'devon' )->ID;
pagesco_lab_add_wish( $pagesco_maria, 30 );   // wish 1: Dune
pagesco_lab_add_wish( $pagesco_maria, 35 );   // wish 2: The Hobbit
pagesco_lab_add_wish( $pagesco_devon, 38 );   // wish 3: Lord of the Rings

$pagesco_show = function ( $label, $result ) {
	printf( "%-28s %s\n", $label, is_wp_error( $result ) ? $result->get_error_code() . ' (' . $result->get_error_data()['status'] . ')' : $result );
};

wp_set_current_user( $pagesco_devon );
$pagesco_show( 'Devon closes wish 1', pagesco_lab_close_door( 1 ) );
$pagesco_show( 'Devon closes wish 3', pagesco_lab_close_door( 3 ) );
wp_set_current_user( $pagesco_maria );
$pagesco_show( 'Maria closes wish 1', pagesco_lab_close_door( 1 ) );
$pagesco_show( 'Maria closes wish 1 again', pagesco_lab_close_door( 1 ) );
wp_set_current_user( 0 );
$pagesco_show( 'A visitor closes wish 2', pagesco_lab_close_door( 2 ) );

echo "Maria's wishes, newest first:\n";
foreach ( pagesco_lab_wishes_of( $pagesco_maria ) as $pagesco_wish ) {
	printf( "  wish %d: %s, %s\n", $pagesco_wish->id, get_the_title( (int) $pagesco_wish->book_id ), $pagesco_wish->status );
}

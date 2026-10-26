<?php
/**
 * staff_note_starter.php: four requests against one save handler (Session 10, Lesson 5.3, lab A)
 * state: after:lesson_15
 * expect: no token, as Maria
 * expect: saved
 *
 * The shop wants a private staff note on each book ("Signed copy, ask at the counter."). The handler below saves
 * it from a submitted form, and saves EVERYTHING it is given. The script then plays four requests against Dune
 * (book 30), as different users, and prints what happened. Make the handler apply Lesson 5.3's four habits.
 * From your project folder:
 *     cp labs/module-10/l5_3-security/staff_note_starter.php wordpress/
 *     wp eval-file --use-include staff_note_starter.php
 * The script removes the note again at the end. When you are done: rm wordpress/staff_note_starter.php
 */

/**
 * Saves the staff note of a book from a submitted form; returns what happened.
 *
 * @param int   $post_id The book.
 * @param array $fields  The submitted form fields (already unslashed).
 * @return string
 */
function pagesco_lab_save_note( $post_id, $fields ) {
	// TODO 1: no nonce field at all? return 'refused: no token'.
	// TODO 2: verify the nonce field pagesco_note_nonce for the action 'pagesco_lab_note_' . $post_id
	//         (sanitize_key() it first, as BookMetaBox does); a bad one: return 'refused: bad token'.
	// TODO 3: may the CURRENT user edit THIS book? If not: return 'refused: not allowed'.
	// TODO 4: sanitize the note before it is stored (one line of plain text: sanitize_text_field()).
	update_post_meta( $post_id, 'pagesco_staff_note', $fields['pagesco_note'] ?? '' );
	return 'saved';
}

// The four requests: who sends them, and which token they carry. Maria (2) is an editor, Devon (3) an author.
$pagesco_requests = array(
	'no token, as Maria'             => array( 2, null, 'Signed copy, ask at the counter.' ),
	'forged token, as Maria'         => array( 2, 'deadbeef', 'Signed copy, ask at the counter.' ),
	'real token, as Devon'           => array( 3, 'real', 'Signed copy, ask at the counter.' ),
	'real token, as Maria, with tag' => array( 2, 'real', 'Signed copy<script>alert(1)</script>, ask at the counter.' ),
);
foreach ( $pagesco_requests as $pagesco_label => list( $pagesco_user, $pagesco_token, $pagesco_note ) ) {
	delete_post_meta( 30, 'pagesco_staff_note' );
	wp_set_current_user( $pagesco_user );
	$pagesco_fields = array( 'pagesco_note' => $pagesco_note );
	if ( null !== $pagesco_token ) {
		// A real token is the one this site would print into the form for this user (wp_nonce_field()).
		$pagesco_fields['pagesco_note_nonce'] = 'real' === $pagesco_token ? wp_create_nonce( 'pagesco_lab_note_30' ) : $pagesco_token;
	}
	$pagesco_result = pagesco_lab_save_note( 30, $pagesco_fields );
	$pagesco_stored = get_post_meta( 30, 'pagesco_staff_note', true );
	printf( "%-31s %-20s stored: %s\n", $pagesco_label, $pagesco_result, '' === $pagesco_stored ? '(nothing)' : $pagesco_stored );
}
delete_post_meta( 30, 'pagesco_staff_note' );

// Expected when done (staff_note_solution.php):
// no token, as Maria              refused: no token    stored: (nothing)
// forged token, as Maria          refused: bad token   stored: (nothing)
// real token, as Devon            refused: not allowed stored: (nothing)
// real token, as Maria, with tag  saved                stored: Signed copy, ask at the counter.

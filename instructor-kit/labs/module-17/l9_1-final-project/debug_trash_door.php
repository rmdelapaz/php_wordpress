<?php
/**
 * debug_trash_door.php: a "move to trash" door for staff, typed in a hurry (Session 17, Lesson 9.1, find-the-bug handout)
 * state: after:lesson_29
 * expect-error: doing_it_wrong, Warning
 *
 * The door checks who is asking and prints its decision (it never trashes anything, so your site is safe). It is
 * tried as Devon, an author, on Maria's post 15, "Welcome to the new Pages & Co. website". The right answer is
 * "no": an author may trash his own posts, not an editor's. From your project folder:
 *     cp labs/module-17/l9_1-final-project/debug_trash_door.php wordpress/
 *     wp eval-file --use-include debug_trash_door.php
 * Two bugs announce themselves (read each message from the left). The third is SILENT and is the dangerous one:
 * it is Lesson 9.1's Common Mistake 2. Fix all three, run again after each fix.
 * When you are done: rm wordpress/debug_trash_door.php
 */
global $wpdb;

wp_set_current_user( get_user_by( 'login', 'devon' )->ID );

// What the form sent (in a real handler: $_POST, after its nonce was checked).
$pagesco_request = array(
	'post'   => '15',
	'reason' => 'duplicate',
);
$pagesco_post_id = absint( $pagesco_request['post'] );

// May this user trash this post?
$pagesco_allowed = current_user_can( 'delete_posts' );

// The title, for the confirmation message.
$pagesco_title = $wpdb->get_var(
	$wpdb->prepare( 'SELECT post_title FROM %i WHERE ID = %d AND post_type = %s', $wpdb->posts, $pagesco_post_id )
);

printf( "%s may trash \"%s\": %s\n", wp_get_current_user()->user_login, $pagesco_title, $pagesco_allowed ? 'yes' : 'no' );
echo 'Reason: ', $pagesco_request['why'], "\n";

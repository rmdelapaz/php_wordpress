<?php
/**
 * Plugin Name: Pages & Co. Checkpoint 1
 * Description: Checkpoint 1 (Modules 1 and 2): three small additions to the store notice and the footer.
 *
 * Copy this file into wordpress/wp-content/mu-plugins/ and run test_checkpoint.sh after each part.
 * Open site, closed notes (your course site, wp help, these comments); work alone; 23 minutes.
 *
 * (a) pagesco_checkpoint_latest_news(): on the filter pagesco_store_notice (Lesson 2.3's own hook), priority 30,
 *     add " Latest news: <title>." to the text, where <title> is the title of the NEWEST post in the category
 *     News (slug news). Use get_posts() with an array of arguments. Return the text: the notice escapes it.
 * (b) pagesco_checkpoint_ask_link(): on the action pagesco_store_notice_end, priority 20 (after the events
 *     link), print " · " and a link to the author archive of the user with the login maria, whose text is
 *     "Ask " and her display name. Escape the URL and the text.
 * (c) pagesco_checkpoint_page_count(): on wp_footer, print <p class="pagesco-pages">Published pages: N</p>, where
 *     N is counted with ONE prepared $wpdb query on the posts table (post_type page, post_status publish).
 */

/**
 * (a) Adds the newest News post to the store notice.
 *
 * @param string $text The notice text so far (plain text).
 * @return string
 */
function pagesco_checkpoint_latest_news( $text ) {
	// TODO (a): find the newest post in News with get_posts() and use its title instead of TODO.
	return $text . ' Latest news: TODO.';
}
// TODO (a): hook it to pagesco_store_notice at priority 30.

/**
 * (b) Prints a link to Maria's author archive inside the notice bar.
 */
function pagesco_checkpoint_ask_link() {
	// TODO (b): get the user with get_user_by(), build the link with get_author_posts_url(), escape both parts.
	echo ' · TODO';
}
add_action( 'pagesco_store_notice_end', 'pagesco_checkpoint_ask_link', 20 );

/**
 * (c) Prints the number of published pages in the footer.
 */
function pagesco_checkpoint_page_count() {
	global $wpdb;
	// TODO (c): one $wpdb->prepare() query with %s placeholders; $wpdb->get_var() returns the count.
	$pagesco_count = 'TODO';
	echo '<p class="pagesco-pages">Published pages: ' . esc_html( $pagesco_count ) . '</p>';
}
add_action( 'wp_footer', 'pagesco_checkpoint_page_count' );

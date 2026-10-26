<?php
/**
 * Plugin Name: Pages & Co. Checkpoint 1
 * Description: Checkpoint 1 (Modules 1 and 2), model answer: three small additions to the store notice and the footer.
 */

/**
 * (a) Adds the newest News post to the store notice.
 *
 * @param string $text The notice text so far (plain text).
 * @return string
 */
function pagesco_checkpoint_latest_news( $text ) {
	$posts = get_posts(
		array(
			'category_name' => 'news',
			'numberposts'   => 1,
		)
	);

	if ( ! $posts ) {
		return $text;
	}

	return $text . ' Latest news: ' . get_the_title( $posts[0] ) . '.';
}
add_filter( 'pagesco_store_notice', 'pagesco_checkpoint_latest_news', 30 );

/**
 * (b) Prints a link to Maria's author archive inside the notice bar.
 */
function pagesco_checkpoint_ask_link() {
	$user = get_user_by( 'login', 'maria' );

	if ( ! $user ) {
		return;
	}

	echo ' · <a href="' . esc_url( get_author_posts_url( $user->ID ) ) . '">' . esc_html( 'Ask ' . $user->display_name ) . '</a>';
}
add_action( 'pagesco_store_notice_end', 'pagesco_checkpoint_ask_link', 20 );

/**
 * (c) Prints the number of published pages in the footer.
 */
function pagesco_checkpoint_page_count() {
	global $wpdb;

	$count = (int) $wpdb->get_var(
		$wpdb->prepare(
			"SELECT COUNT(*) FROM {$wpdb->posts} WHERE post_type = %s AND post_status = %s",
			'page',
			'publish'
		)
	);

	echo '<p class="pagesco-pages">Published pages: ' . esc_html( $count ) . '</p>';
}
add_action( 'wp_footer', 'pagesco_checkpoint_page_count' );

<?php
/**
 * Plugin Name: Pages & Co. Archive Rules (Session 6 lab)
 * Description: Changes two archive lists of the main query with pre_get_posts, and nothing else.
 *
 * Session 6, Lesson 4.2, lab B: the reference solution.
 *
 * @param WP_Query $query The query WordPress is about to run.
 */
function pagesco_lab_archive_rules( $query ) {
	if ( is_admin() || ! $query->is_main_query() ) {
		return;
	}

	if ( $query->is_author() ) {
		$query->set( 'order', 'ASC' );
	}

	if ( $query->is_date() ) {
		$query->set( 'posts_per_page', 1 );
	}
}
add_action( 'pre_get_posts', 'pagesco_lab_archive_rules' );

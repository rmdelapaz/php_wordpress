<?php
/**
 * Plugin Name: Pages & Co. Archive Rules (Session 6 lab)
 * Description: Changes two archive lists of the main query with pre_get_posts, and nothing else.
 *
 * Session 6, Lesson 4.2, lab B: the starter. Copy this file into wordpress/wp-content/mu-plugins/ and run
 * test_archive_rules.sh after each TODO. The shop wants:
 *
 * TODO 1: guards first. Return early unless this is the front end (! is_admin()) AND the main query
 *         ($query->is_main_query()). Without them, rule 3 would also cut every secondary date query on the
 *         site, such as a "September" box (Lesson 4.2, Common Mistakes 3): the test's last line watches that.
 * TODO 2: author archives (/author/maria/) list the oldest post first: $query->is_author() → order ASC.
 * TODO 3: date archives (/2026/09/) show ONE post per page, so the archive gets a page 2:
 *         $query->is_date() → posts_per_page 1. (The theme's index.php prints whatever the main query holds.)
 *
 * @param WP_Query $query The query WordPress is about to run.
 */
function pagesco_lab_archive_rules( $query ) {
	// The callback runs for every WP_Query; it changes nothing yet.
}
add_action( 'pre_get_posts', 'pagesco_lab_archive_rules' );

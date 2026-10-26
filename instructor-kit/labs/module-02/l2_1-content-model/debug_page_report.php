<?php
/**
 * debug_page_report.php: a content report for the shop's weekly check (Session 2, Lesson 2.1, find-the-bug handout)
 * state: fresh
 * expect-error: Warning
 *
 * Someone wrote this report against an idea of WordPress's content model that is not quite Lesson 2.1's. Run it,
 * read every message from the left, and fix the code until it runs without one. Run it on the site as Session 1
 * left it (before the lesson project). From your project folder:
 *     cp labs/module-02/l2_1-content-model/debug_page_report.php wordpress/
 *     wp eval-file --use-include debug_page_report.php
 * Two loud bugs and one silent one: when the messages are gone, check every line against what Lesson 2.1 says
 * the site holds. The script only reads. Then delete the copy: rm wordpress/debug_page_report.php
 */

// The newest post and its category.
$pagesco_post = get_post( 1 );
echo 'Post: ', $pagesco_post->post_title, "\n";
echo 'Filed under: ', $pagesco_post->category, "\n";

// The categories of the two pages WordPress installs.
foreach ( array( 2, 3 ) as $pagesco_id ) {
	echo 'Page ', $pagesco_id, ' categories:';
	foreach ( get_the_terms( $pagesco_id, 'category' ) as $pagesco_term ) {
		echo ' ', $pagesco_term->name;
	}
	echo "\n";
}

// Who looks after the pages.
$pagesco_editor = get_user_by( 'login', 'maria' );
echo 'Pages are looked after by: ', $pagesco_editor->display_name, "\n";

<?php
/**
 * debug_related_box.php: a "More from the shop" box, tested from the terminal (Session 6, Lesson 4.2, find-the-bug handout)
 * state: after:lesson_11
 * expect-error: Warning
 *
 * wp( 'name=book-club-dune' ) runs the main query for the Book club post, exactly as a request for
 * http://localhost:8080/book-club-dune/ would, and the_post() makes it the current post. Then a secondary query
 * finds the two other News posts, and the script prints them as a box, with a summary line and a footer that names
 * the post the page is about. From your project folder:
 *     cp labs/module-06/l4_2-custom-queries/debug_related_box.php wordpress/
 *     wp eval-file --use-include debug_related_box.php
 * One bug announces itself with a Warning. Two are SILENT: an empty "Titles:" line, and a last line that names
 * the wrong post (it appears once the Warning is fixed). Fixed, it prints the two titles, "Titles: Staff picks for the season, Welcome to the new Pages &#038;
 * Co. website" and "This page is about: Book club: Dune". When you are done: rm wordpress/debug_related_box.php
 */
wp( 'name=book-club-dune' );
the_post();

$pagesco_related = new WP_Query(
	array(
		'category__in'        => wp_get_post_categories( get_the_ID() ),
		'post__not_in'        => array( get_the_ID() ),
		'posts_per_page'      => 2,
		'ignore_sticky_posts' => true,
		'no_found_rows'       => true,
	)
);

echo "More from the shop:\n";
for ( $pagesco_i = 0; $pagesco_i < 3; $pagesco_i++ ) {
	$pagesco_related->the_post();
	echo '- ', get_the_title(), "\n";
}

echo 'Titles: ', implode( ', ', wp_list_pluck( $pagesco_related, 'post_title' ) ), "\n";

echo 'This page is about: ', get_the_title(), "\n";

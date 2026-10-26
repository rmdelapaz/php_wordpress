<?php
/**
 * query_shelf_starter.php: five questions from the shop, five WP_Query argument arrays (Session 6, Lesson 4.2, lab A)
 * state: after:lesson_11
 * expect: news, page 2:      TODO
 *
 * Each question becomes one array of WP_Query arguments (Lesson 4.2's argument table). pagesco_show_query() is
 * done for you: it runs the query and prints the titles with post_count, found_posts and max_num_pages. An empty
 * array prints TODO. From your project folder:
 *     cp labs/module-06/l4_2-custom-queries/query_shelf_starter.php wordpress/
 *     wp eval-file --use-include query_shelf_starter.php
 * Fill in one array at a time, run again, and compare with "Expected when done" at the end. Then answer in your
 * workbook: why does the last query say found_posts 3 although it loaded one post?
 * When you are done: rm wordpress/query_shelf_starter.php
 */

/**
 * Runs one query and prints its titles and its three numbers.
 *
 * @param string $label The question.
 * @param array  $args  WP_Query arguments.
 */
function pagesco_show_query( $label, $args ) {
	if ( ! $args ) {
		printf( "%-18s TODO\n", $label );
		return;
	}
	$pagesco_query  = new WP_Query( $args );
	$pagesco_titles = array_map( 'get_the_title', $pagesco_query->posts );
	printf(
		"%-18s %s  (post_count %d, found_posts %d, max_num_pages %d)\n",
		$label,
		implode( ', ', $pagesco_titles ),
		$pagesco_query->post_count,
		$pagesco_query->found_posts,
		$pagesco_query->max_num_pages
	);
}

// TODO 1: Maria's posts (her login is maria; the argument takes the login slug, not the ID).
pagesco_show_query( "Maria's posts:", array() );

// TODO 2: the News category by slug, two posts per page, the SECOND page.
pagesco_show_query( 'news, page 2:', array() );

// TODO 3: every post published before 2026-10-01, oldest first (a date_query with 'before').
pagesco_show_query( 'before October:', array() );

// TODO 4: the About, Contact and Events pages by slug (post_name__in), sorted by title A to Z.
pagesco_show_query( 'pages, A to Z:', array() );

// TODO 5: how many News posts exist, loading as little as possible: only IDs, and only one of them.
pagesco_show_query( 'how many news?', array() );

// Expected when done (query_shelf_solution.php, the course site at the end of Lesson 4.1):
// Maria's posts:     Book club: Dune, Welcome to the new Pages &#038; Co. website  (post_count 2, found_posts 2, max_num_pages 1)
// news, page 2:      Welcome to the new Pages &#038; Co. website  (post_count 1, found_posts 3, max_num_pages 2)
// before October:    Welcome to the new Pages &#038; Co. website, Staff picks for the season  (post_count 2, found_posts 2, max_num_pages 1)
// pages, A to Z:     About Us, Contact, Events  (post_count 3, found_posts 3, max_num_pages 1)
// how many news?     Book club: Dune  (post_count 1, found_posts 3, max_num_pages 3)

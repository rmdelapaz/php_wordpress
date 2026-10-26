<?php
/**
 * query_shelf_solution.php: five questions from the shop, five WP_Query argument arrays (Session 6, Lesson 4.2, lab A)
 * state: after:lesson_11
 * expect: news, page 2:      Welcome to the new Pages &#038; Co. website  (post_count 1, found_posts 3, max_num_pages 2)
 *
 * The reference solution. See query_shelf_starter.php for the task.
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

pagesco_show_query( "Maria's posts:", array( 'author_name' => 'maria' ) );
pagesco_show_query(
	'news, page 2:',
	array(
		'category_name'  => 'news',
		'posts_per_page' => 2,
		'paged'          => 2,
	)
);
pagesco_show_query(
	'before October:',
	array(
		'date_query' => array( array( 'before' => '2026-10-01' ) ),
		'order'      => 'ASC',
	)
);
pagesco_show_query(
	'pages, A to Z:',
	array(
		'post_type'     => 'page',
		'post_name__in' => array( 'about', 'contact', 'events' ),
		'orderby'       => 'title',
		'order'         => 'ASC',
	)
);
pagesco_show_query(
	'how many news?',
	array(
		'category_name'  => 'news',
		'fields'         => 'ids',
		'posts_per_page' => 1,
	)
);

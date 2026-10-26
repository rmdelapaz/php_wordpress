<?php
/**
 * debug_query_review.php: a "latest news" list someone wrote for a theme. Four bugs (Session 8 review, Lesson 4.2).
 *
 * state: after:lesson_13
 * expect-error: Warning
 *
 * It should print the two newest posts of the News category, newest first, and the total number of News posts,
 * and leave the page on the screen (About Us) as the current post. One bug is loud; three are silent,
 * and the silent ones are the dangerous kind: read the output line by line against the site (wp post list).
 *     cp labs/module-08/p1-review/debug_query_review.php wordpress/
 *     wp eval-file --use-include debug_query_review.php
 *     rm wordpress/debug_query_review.php
 */

// The page on the screen, as a template's main query would hold it (this part is correct).
$GLOBALS['wp_query'] = new WP_Query( array( 'page_id' => 12 ) );
$GLOBALS['wp_query']->the_post();
echo 'On the screen: ', get_the_title(), "\n";

$pagesco_news = new WP_Query(
	array(
		'category'       => 'news',
		'posts_per_page' => 2,
	)
);

echo "Latest news:\n";
while ( $pagesco_news->have_posts() ) {
	$pagesco_news->the_post();
	echo '- ', get_the_title(), "\n";
}

echo 'News posts in all: ', $pagesco_news->found_post, "\n";
echo 'First title again: ', $pagesco_posts[0]->post_title, "\n";
echo 'On the screen after the list: ', get_the_title(), "\n";

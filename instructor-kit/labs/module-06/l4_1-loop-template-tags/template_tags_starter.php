<?php
/**
 * template_tags_starter.php: one post, every template tag pair, printed or returned (Session 6, Lesson 4.1, lab B)
 * state: after:lesson_10
 * expect: excerpt:           TODO
 *
 * Lesson 4.1's table of template tags, outside the Loop: WP-CLI runs no main query, but almost every get_
 * function also takes a post (an ID or a WP_Post). This script asks them all about one post, "Welcome to the new
 * Pages & Co. website". From your project folder:
 *     cp labs/module-06/l4_1-loop-template-tags/template_tags_starter.php wordpress/
 *     wp eval-file --use-include template_tags_starter.php
 * Replace each 'TODO' with the function its comment names, run again, compare with "Expected when done" at the
 * end, and answer the three questions in your workbook. When you are done: rm wordpress/template_tags_starter.php
 */
$pagesco_post = get_page_by_path( 'welcome', OBJECT, 'post' );

$pagesco_rows = array(
	'post_title:'       => $pagesco_post->post_title,                      // done: the title as stored
	'title:'            => get_the_title( $pagesco_post ),                 // done: with the display filters
	'title attribute:'  => 'TODO', // TODO 1: the_title_attribute() with array( 'echo' => false, 'post' => ... )
	'permalink:'        => 'TODO', // TODO 2: the post's URL
	'date (Y-m-d):'     => 'TODO', // TODO 3: get_the_date() with a format and the post
	'author:'           => 'TODO', // TODO 4: the display name: get_the_author_meta( 'display_name', <the author ID> )
	'categories:'       => 'TODO', // TODO 5: get_the_category_list( ', ', '', <the post ID> )
	'raw content:'      => 'TODO', // TODO 6: the FIRST line of get_the_content( null, false, $pagesco_post ) (strtok())
	'rendered content:' => 'TODO', // TODO 7: the first line of the same content run through the 'the_content' filters
	'excerpt:'          => 'TODO', // TODO 8: get_the_excerpt() for the post
	'classes:'          => 'TODO', // TODO 9: get_post_class( '', $pagesco_post ), joined with spaces
);
foreach ( $pagesco_rows as $pagesco_label => $pagesco_value ) {
	printf( "%-18s %s\n", $pagesco_label, $pagesco_value );
}

// Expected when done (template_tags_solution.php, the course site at the end of Lesson 3.4):
// post_title:        Welcome to the new Pages & Co. website
// title:             Welcome to the new Pages &#038; Co. website
// title attribute:   Welcome to the new Pages &#038; Co. website
// permalink:         http://localhost:8080/welcome/
// date (Y-m-d):      2026-09-01
// author:            Maria Lopez
// categories:        <a href="http://localhost:8080/category/news/" rel="category tag">News</a>
// raw content:       <!-- wp:paragraph -->
// rendered content:  <p class="wp-block-paragraph">Our new website is open! Browse our pages, read the shop news, and soon you will find our whole catalog here.</p>
// excerpt:           Our new website is open! Browse our pages, read the shop news, and soon you will find our whole catalog here.
// classes:           post-15 post type-post status-publish format-standard hentry category-news

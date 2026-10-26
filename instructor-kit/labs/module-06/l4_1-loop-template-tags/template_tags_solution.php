<?php
/**
 * template_tags_solution.php: one post, every template tag pair, printed or returned (Session 6, Lesson 4.1, lab B)
 * state: after:lesson_10
 * expect: excerpt:           Our new website is open!
 *
 * The reference solution. See template_tags_starter.php for the task.
 */
$pagesco_post = get_page_by_path( 'welcome', OBJECT, 'post' );

$pagesco_rows = array(
	'post_title:'       => $pagesco_post->post_title,
	'title:'            => get_the_title( $pagesco_post ),
	'title attribute:'  => the_title_attribute( array( 'echo' => false, 'post' => $pagesco_post ) ),
	'permalink:'        => get_permalink( $pagesco_post ),
	'date (Y-m-d):'     => get_the_date( 'Y-m-d', $pagesco_post ),
	'author:'           => get_the_author_meta( 'display_name', $pagesco_post->post_author ),
	'categories:'       => get_the_category_list( ', ', '', $pagesco_post->ID ),
	'raw content:'      => strtok( get_the_content( null, false, $pagesco_post ), "\n" ),
	'rendered content:' => strtok( trim( apply_filters( 'the_content', get_the_content( null, false, $pagesco_post ) ) ), "\n" ),
	'excerpt:'          => get_the_excerpt( $pagesco_post ),
	'classes:'          => implode( ' ', get_post_class( '', $pagesco_post ) ),
);
foreach ( $pagesco_rows as $pagesco_label => $pagesco_value ) {
	printf( "%-18s %s\n", $pagesco_label, $pagesco_value );
}

<?php
/**
 * post_report_starter.php: one row of wp_posts, seen through the content model (Session 2, Lesson 2.1, lab B)
 * state: fresh
 * expect: #4 TODO (publish) "Navigation"
 *
 * Everything Lesson 2.1 says about a post, asked of WordPress for five IDs: a post, two pages, the navigation menu
 * of Twenty Twenty-Five, and an ID that does not exist. From your project folder:
 *     cp labs/module-02/l2_1-content-model/post_report_starter.php wordpress/
 *     wp eval-file --use-include post_report_starter.php
 * Replace each TODO with the function its comment names (Code Reference: developer.wordpress.org/reference),
 * run again after each one, and compare with "Expected when done" at the end. The script only reads: it changes
 * nothing on your site. When you are done: rm wordpress/post_report_starter.php
 */

/**
 * Prints what the content model knows about one row of wp_posts.
 *
 * @param int $id A post ID.
 */
function pagesco_lab_describe( $id ) {
	$post = get_post( $id );
	if ( ! $post ) {
		echo "#{$id} not found\n";
		return;
	}
	// TODO 1: the post type's registration object: get_post_type_object( $post->post_type ). Use its
	//         labels->singular_name instead of 'TODO' below, and its ->hierarchical for the second line.
	$author = get_userdata( $post->post_author ); // false when post_author is 0 (WordPress made the post itself)

	printf( "#%d %s (%s) \"%s\"\n", $post->ID, 'TODO', $post->post_status, $post->post_title );
	printf( "   slug: %s · hierarchical type: %s\n", $post->post_name, 'TODO' );
	if ( $author ) {
		// TODO 2: yes or no: may this user edit other people's posts? Check the capability with user_can().
		printf( "   author: %s, may edit others' posts: %s\n", $author->display_name, 'TODO' );
	} else {
		echo "   author: none (post_author is 0)\n";
	}

	// TODO 3: every term of the post, as taxonomy:name. get_object_taxonomies( $post ) names the taxonomies;
	//         get_the_terms( $post, $taxonomy ) returns WP_Term objects, or false when there are none.
	echo "   terms: TODO\n";
	// TODO 4: how many revisions it has: count( wp_get_post_revisions( $post ) ).
	echo "   revisions: TODO\n";
	// TODO 5: parse_blocks( $post->post_content ): the number of top-level blocks with a name, then the
	//         distinct names in parentheses (skip the null "freeform" gaps; array_unique()).
	echo "   top-level blocks: TODO\n";
	// TODO 6: the address with get_permalink(), but only when is_post_type_viewable() says the type is public;
	//         otherwise print: none (not a public type)
	echo "   address: TODO\n";
}

foreach ( array( 1, 2, 3, 4, 999 ) as $pagesco_id ) {
	pagesco_lab_describe( $pagesco_id );
}

// Expected when done (post_report_solution.php, a fresh course site):
// #1 Post (publish) "Hello world!"
//    slug: hello-world · hierarchical type: no
//    author: admin, may edit others' posts: yes
//    terms: category:Uncategorized
//    revisions: 0
//    top-level blocks: 1 (core/paragraph)
//    address: http://localhost:8080/hello-world/
// #2 Page (publish) "Sample Page"
//    slug: sample-page · hierarchical type: yes
//    author: admin, may edit others' posts: yes
//    terms: none
//    revisions: 0
//    top-level blocks: 5 (core/paragraph, core/quote)
//    address: http://localhost:8080/sample-page/
// #3 Page (draft) "Privacy Policy"
//    slug: privacy-policy · hierarchical type: yes
//    author: admin, may edit others' posts: yes
//    terms: none
//    revisions: 0
//    top-level blocks: 24 (core/heading, core/paragraph)
//    address: http://localhost:8080/?page_id=3
// #4 Navigation Menu (publish) "Navigation"
//    slug: navigation · hierarchical type: no
//    author: none (post_author is 0)
//    terms: none
//    revisions: 0
//    top-level blocks: 1 (core/page-list)
//    address: none (not a public type)
// #999 not found

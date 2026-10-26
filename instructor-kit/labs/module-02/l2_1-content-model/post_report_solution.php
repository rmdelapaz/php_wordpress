<?php
/**
 * post_report_solution.php: the instructor's reference for post_report_starter.php (Session 2, Lesson 2.1, lab B)
 * state: fresh
 * expect: #4 Navigation Menu (publish) "Navigation"
 * expect: #999 not found
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
	$type   = get_post_type_object( $post->post_type );
	$author = get_userdata( $post->post_author );

	printf( "#%d %s (%s) \"%s\"\n", $post->ID, $type->labels->singular_name, $post->post_status, $post->post_title );
	printf( "   slug: %s · hierarchical type: %s\n", $post->post_name, $type->hierarchical ? 'yes' : 'no' );
	if ( $author ) {
		printf( "   author: %s, may edit others' posts: %s\n", $author->display_name, user_can( $author, 'edit_others_posts' ) ? 'yes' : 'no' );
	} else {
		echo "   author: none (post_author is 0)\n";
	}

	$terms = array();
	foreach ( get_object_taxonomies( $post ) as $taxonomy ) {
		foreach ( (array) get_the_terms( $post, $taxonomy ) as $term ) {
			if ( $term instanceof WP_Term ) {
				$terms[] = $taxonomy . ':' . $term->name;
			}
		}
	}
	echo '   terms: ', $terms ? implode( ', ', $terms ) : 'none', "\n";
	echo '   revisions: ', count( wp_get_post_revisions( $post ) ), "\n";

	$names = array();
	foreach ( parse_blocks( $post->post_content ) as $block ) {
		if ( null !== $block['blockName'] ) {
			$names[] = $block['blockName'];
		}
	}
	echo '   top-level blocks: ', count( $names ), $names ? ' (' . implode( ', ', array_unique( $names ) ) . ')' : '', "\n";
	echo '   address: ', is_post_type_viewable( $type ) ? get_permalink( $post ) : 'none (not a public type)', "\n";
}

foreach ( array( 1, 2, 3, 4, 999 ) as $pagesco_id ) {
	pagesco_lab_describe( $pagesco_id );
}

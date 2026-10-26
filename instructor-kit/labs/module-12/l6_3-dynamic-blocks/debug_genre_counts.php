<?php
/**
 * debug_genre_counts.php: a dynamic block with three bugs, rendered without a page (Session 12, Lesson 6.3, find-the-bug handout)
 * state: after:lesson_20
 * expect-error: Warning
 *
 * pagesco/lab-genres lists genres with their number of books, the biggest first: as many genres as its limit
 * attribute says, or 3 when no limit was chosen (limit has no default, like the Book List's count). The script
 * registers the block with a render_callback (the PHP twin of render.php) and renders two stored comments.
 * From your project folder:
 *     cp labs/module-12/l6_3-dynamic-blocks/debug_genre_counts.php wordpress/
 *     wp eval-file --use-include debug_genre_counts.php
 * Two bugs announce themselves with Warnings. The third is SILENT: the second block asks for 4 genres and gets
 * fewer. Find all three, fix them one at a time, run again after each fix. When you are done:
 *     rm wordpress/debug_genre_counts.php
 */
function pagesco_lab_render_genres( $attributes ) {
	$pagesco_limit = $attributes['limit'] ? absint( $attributes['limit'] ) : 3;
	$pagesco_limit = min( 1, max( 10, $pagesco_limit ) );

	$pagesco_terms = get_terms(
		array(
			'taxonomy'   => 'genre',
			'orderby'    => 'count',
			'order'      => 'DESC',
			'number'     => $pagesco_limit,
			'hide_empty' => true,
		)
	);

	foreach ( $pagesco_terms as $pagesco_term ) {
		$pagesco_items .= '<li>' . esc_html( $pagesco_term->name . ': ' . $pagesco_term->count ) . '</li>';
	}

	return '<ul class="wp-block-pagesco-lab-genres">' . $pagesco_items . '</ul>';
}

register_block_type(
	'pagesco/lab-genres',
	array(
		'attributes'      => array(
			'limit' => array( 'type' => 'integer' ),
		),
		'render_callback' => 'pagesco_lab_render_genres',
	)
);

echo do_blocks( '<!-- wp:pagesco/lab-genres /-->' ), "\n";
echo do_blocks( '<!-- wp:pagesco/lab-genres {"limit":4} /-->' ), "\n";

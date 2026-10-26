<?php
/**
 * core_sources_solution.php: the instructor's reference for core_sources_starter.php (Session 12, Lesson 6.3, lab B)
 * state: after:lesson_20
 * expect: Dune      pagesco_price      [14.99]
 * expect: Gatsby    pagesco_in_stock   []
 * expect: Dune      _edit_lock         [No data]
 */
/**
 * A paragraph whose content is bound to a source, as block markup (the fallback text is "No data").
 */
function pagesco_lab_bound_paragraph( string $source, array $args ): string {
	$attrs = array( 'metadata' => array( 'bindings' => array( 'content' => array( 'source' => $source, 'args' => $args ) ) ) );

	return '<!-- wp:paragraph ' . wp_json_encode( $attrs ) . ' --><p>No data</p><!-- /wp:paragraph -->';
}

$pagesco_books = array(
	'Dune'   => 30,
	'Gatsby' => 33,
);
$pagesco_tries = array(
	array( 'Dune', 'core/post-meta', array( 'key' => 'pagesco_author' ) ),
	array( 'Dune', 'core/post-meta', array( 'key' => 'pagesco_price' ) ),
	array( 'Gatsby', 'core/post-meta', array( 'key' => 'pagesco_in_stock' ) ),
	array( 'Dune', 'core/post-meta', array( 'key' => 'pagesco_in_stock' ) ),
	array( 'Dune', 'core/post-meta', array( 'key' => '_edit_lock' ) ),
	array( 'Dune', 'core/post-meta', array( 'key' => 'pagesco_writer' ) ),
	array( 'Dune', 'core/post-data', array( 'field' => 'link' ) ),
);

foreach ( $pagesco_tries as $pagesco_try ) {
	list( $pagesco_book, $pagesco_source, $pagesco_args ) = $pagesco_try;

	$pagesco_parsed = parse_blocks( pagesco_lab_bound_paragraph( $pagesco_source, $pagesco_args ) )[0];
	$pagesco_block  = new WP_Block(
		$pagesco_parsed,
		array(
			'postId'   => $pagesco_books[ $pagesco_book ],
			'postType' => 'book',
		)
	);
	$pagesco_text   = wp_strip_all_tags( $pagesco_block->render() );

	printf( "%-9s %-18s [%s]\n", $pagesco_book, $pagesco_args['key'] ?? $pagesco_args['field'], $pagesco_text );
}

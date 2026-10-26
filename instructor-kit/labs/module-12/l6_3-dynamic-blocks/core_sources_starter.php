<?php
/**
 * core_sources_starter.php: what core's binding sources return, block by block (Session 12, Lesson 6.3, lab B)
 * state: after:lesson_20
 * expect: Dune      pagesco_author     [TODO]
 *
 * Before the shop writes its own source (the lesson project), see what core/post-meta and core/post-data give a
 * bound paragraph: raw values, empty strings, or the fallback text. Rendering a block in PHP with a made-up
 * context needs no template and no browser. From your project folder:
 *     cp labs/module-12/l6_3-dynamic-blocks/core_sources_starter.php wordpress/
 *     wp eval-file --use-include core_sources_starter.php
 * Predict every line in the brackets first, then fill in the TODOs and compare with "Expected when done".
 * When you are done: rm wordpress/core_sources_starter.php
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

	// TODO 1: parse the markup of pagesco_lab_bound_paragraph( $pagesco_source, $pagesco_args ): parse_blocks()[0].
	// TODO 2: new WP_Block( $parsed, $context ): the context names the post, array( 'postId' => ..., 'postType' => 'book' ).
	// TODO 3: render() it and keep only the text: wp_strip_all_tags().
	$pagesco_text = 'TODO';

	printf( "%-9s %-18s [%s]\n", $pagesco_book, $pagesco_args['key'] ?? $pagesco_args['field'], $pagesco_text );
}

// Expected when done (core_sources_solution.php, the site after Lesson 6.2):
// Dune      pagesco_author     [Frank Herbert]
// Dune      pagesco_price      [14.99]
// Gatsby    pagesco_in_stock   []
// Dune      pagesco_in_stock   [1]
// Dune      _edit_lock         [No data]
// Dune      pagesco_writer     [No data]
// Dune      link               [http://localhost:8080/books/dune/]

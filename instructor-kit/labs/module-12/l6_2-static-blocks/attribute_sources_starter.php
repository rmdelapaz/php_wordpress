<?php
/**
 * attribute_sources_starter.php: where do core blocks keep their attributes? (Session 12, Lesson 6.2, lab A)
 * state: after:lesson_19
 * expect: core/heading content: TODO
 * expect: parse_blocks() sees: TODO
 *
 * Lesson 6.2's rule, asked of the blocks WordPress itself registers: an attribute with a "source" lives in the
 * saved HTML (found again through its selector); one without lives in the block comment, and only when it differs
 * from its default. The registry knows every attribute's definition. From your project folder:
 *     cp labs/module-12/l6_2-static-blocks/attribute_sources_starter.php wordpress/
 *     wp eval-file --use-include attribute_sources_starter.php
 * Fill in the TODOs, run again after each one, and compare with "Expected when done" at the end.
 * When you are done: rm wordpress/attribute_sources_starter.php
 */
// Attributes WordPress adds to many blocks (supports, editor helpers): not interesting here.
$pagesco_skip = array( 'lock', 'metadata', 'className', 'style', 'anchor', 'align', 'backgroundColor', 'textColor', 'gradient', 'fontSize', 'fontFamily', 'borderColor', 'fitText', 'textAlign', 'placeholder', 'levelOptions', 'layout' );

foreach ( array( 'core/heading', 'core/quote', 'core/button' ) as $pagesco_name ) {
	// TODO 1: the registered block type: WP_Block_Type_Registry::get_instance()->get_registered( ... ).
	$pagesco_type = null;
	if ( ! $pagesco_type ) {
		echo $pagesco_name, " content: TODO\n";
		continue;
	}

	foreach ( $pagesco_type->get_attributes() as $pagesco_key => $pagesco_attr ) {
		if ( in_array( $pagesco_key, $pagesco_skip, true ) ) {
			continue;
		}
		// TODO 2: when $pagesco_attr has a 'source', describe it as
		//         in the HTML (<source>, <selector>[ @<attribute>])   for example: in the HTML (attribute, a @href)
		// TODO 3: otherwise: in the comment, plus " (default <value as JSON>)" when the attribute has a default.
		//         (array_key_exists(), because a default can be false; wp_json_encode() prints "a" and false.)
		$pagesco_where = 'TODO';
		echo $pagesco_name, ' ', $pagesco_key, ': ', $pagesco_where, "\n";
	}
}

// What PHP sees of a stored heading and image.
$pagesco_markup = '<!-- wp:heading {"level":3} --><h3 class="wp-block-heading">New this week</h3><!-- /wp:heading -->'
	. '<!-- wp:image {"id":42,"sizeSlug":"large"} --><figure class="wp-block-image size-large"><img src="http://localhost:8080/wp-content/uploads/dune.jpg" alt="Dune, first edition" class="wp-image-42"/></figure><!-- /wp:image -->';
// TODO 4: print "parse_blocks() sees:", then for every block of parse_blocks( $pagesco_markup ) its blockName
//         and wp_json_encode() of its attrs. Before you run it: will the image's src be there? The heading's text?
echo "parse_blocks() sees: TODO\n";

// Expected when done (attribute_sources_solution.php, WordPress 7.1.3):
// core/heading content: in the HTML (rich-text, h1,h2,h3,h4,h5,h6)
// core/heading level: in the comment (default 2)
// core/quote value: in the HTML (html, blockquote)
// core/quote citation: in the HTML (rich-text, cite)
// core/button tagName: in the comment (default "a")
// core/button type: in the comment (default "button")
// core/button url: in the HTML (attribute, a @href)
// core/button title: in the HTML (attribute, a,button @title)
// core/button text: in the HTML (rich-text, a,button)
// core/button linkTarget: in the HTML (attribute, a @target)
// core/button rel: in the HTML (attribute, a @rel)
// parse_blocks() sees:
// core/heading {"level":3}
// core/image {"id":42,"sizeSlug":"large"}

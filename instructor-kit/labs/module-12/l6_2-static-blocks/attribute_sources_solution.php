<?php
/**
 * attribute_sources_solution.php: the instructor's reference for attribute_sources_starter.php (Session 12, Lesson 6.2, lab A)
 * state: after:lesson_19
 * expect: core/button url: in the HTML (attribute, a @href)
 * expect: core/heading level: in the comment (default 2)
 * expect: core/image {"id":42,"sizeSlug":"large"}
 */
$pagesco_skip = array( 'lock', 'metadata', 'className', 'style', 'anchor', 'align', 'backgroundColor', 'textColor', 'gradient', 'fontSize', 'fontFamily', 'borderColor', 'fitText', 'textAlign', 'placeholder', 'levelOptions', 'layout' );

foreach ( array( 'core/heading', 'core/quote', 'core/button' ) as $pagesco_name ) {
	$pagesco_type = WP_Block_Type_Registry::get_instance()->get_registered( $pagesco_name );

	foreach ( $pagesco_type->get_attributes() as $pagesco_key => $pagesco_attr ) {
		if ( in_array( $pagesco_key, $pagesco_skip, true ) ) {
			continue;
		}
		if ( isset( $pagesco_attr['source'] ) ) {
			$pagesco_where = sprintf(
				'in the HTML (%s, %s%s)',
				$pagesco_attr['source'],
				$pagesco_attr['selector'] ?? '',
				isset( $pagesco_attr['attribute'] ) ? ' @' . $pagesco_attr['attribute'] : ''
			);
		} else {
			$pagesco_where = 'in the comment' . ( array_key_exists( 'default', $pagesco_attr ) ? ' (default ' . wp_json_encode( $pagesco_attr['default'] ) . ')' : '' );
		}
		echo $pagesco_name, ' ', $pagesco_key, ': ', $pagesco_where, "\n";
	}
}

// What PHP sees of a stored heading and image: only the comment.
$pagesco_markup = '<!-- wp:heading {"level":3} --><h3 class="wp-block-heading">New this week</h3><!-- /wp:heading -->'
	. '<!-- wp:image {"id":42,"sizeSlug":"large"} --><figure class="wp-block-image size-large"><img src="http://localhost:8080/wp-content/uploads/dune.jpg" alt="Dune, first edition" class="wp-image-42"/></figure><!-- /wp:image -->';
echo "parse_blocks() sees:\n";
foreach ( parse_blocks( $pagesco_markup ) as $pagesco_block ) {
	echo $pagesco_block['blockName'], ' ', wp_json_encode( $pagesco_block['attrs'] ), "\n";
}

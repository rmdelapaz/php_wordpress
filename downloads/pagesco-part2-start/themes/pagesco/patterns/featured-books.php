<?php
/**
 * Title: Featured books: staff picks
 * Slug: pagesco/featured-books
 * Categories: pagesco, featured
 * Keywords: books, staff picks, featured
 * Description: Three featured books in a row, with title, author and price.
 * Viewport Width: 1200
 *
 * @package pagesco
 */

$pagesco_picks = array(
	array(
		'title'  => 'Dune',
		'author' => 'Frank Herbert',
		'price'  => 14.99,
	),
	array(
		'title'  => 'The Hobbit',
		'author' => 'J.R.R. Tolkien',
		'price'  => 10.99,
	),
	array(
		'title'  => 'Fahrenheit 451',
		'author' => 'Ray Bradbury',
		'price'  => 10.49,
	),
);
?>
<!-- wp:group {"align":"wide","style":{"spacing":{"padding":{"top":"var:preset|spacing|medium","bottom":"var:preset|spacing|medium"}}}} -->
<div class="wp-block-group alignwide" style="padding-top:var(--wp--preset--spacing--medium);padding-bottom:var(--wp--preset--spacing--medium)">
	<!-- wp:heading -->
	<h2 class="wp-block-heading"><?php esc_html_e( 'Staff picks', 'pagesco' ); ?></h2>
	<!-- /wp:heading -->

	<!-- wp:columns -->
	<div class="wp-block-columns">
		<?php foreach ( $pagesco_picks as $pagesco_book ) : ?>
		<!-- wp:column -->
		<div class="wp-block-column">
			<!-- wp:heading {"level":3} -->
			<h3 class="wp-block-heading"><?php echo esc_html( $pagesco_book['title'] ); ?></h3>
			<!-- /wp:heading -->

			<!-- wp:paragraph -->
			<p><?php /* translators: %s: author name. */ printf( esc_html__( 'by %s', 'pagesco' ), esc_html( $pagesco_book['author'] ) ); ?></p>
			<!-- /wp:paragraph -->

			<!-- wp:paragraph {"fontSize":"small"} -->
			<p class="has-small-font-size"><?php echo esc_html( '$' . number_format_i18n( $pagesco_book['price'], 2 ) ); ?></p>
			<!-- /wp:paragraph -->
		</div>
		<!-- /wp:column -->
		<?php endforeach; ?>
	</div>
	<!-- /wp:columns -->
</div>
<!-- /wp:group -->

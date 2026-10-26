<?php
/**
 * Title: Featured books: staff picks
 * Slug: pagesco/featured-books
 * Categories: pagesco, featured
 * Keywords: books, staff picks, featured
 * Description: Three featured books in a row, with title, author and their live price.
 * Viewport Width: 1200
 *
 * @package pagesco
 */

$pagesco_picks = array(
	array(
		'slug'   => 'dune',
		'title'  => 'Dune',
		'author' => 'Frank Herbert',
	),
	array(
		'slug'   => 'the-hobbit',
		'title'  => 'The Hobbit',
		'author' => 'J.R.R. Tolkien',
	),
	array(
		'slug'   => 'fahrenheit-451',
		'title'  => 'Fahrenheit 451',
		'author' => 'Ray Bradbury',
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
			<h3 class="wp-block-heading"><a href="<?php echo esc_url( home_url( '/books/' . $pagesco_book['slug'] . '/' ) ); ?>"><?php echo esc_html( $pagesco_book['title'] ); ?></a></h3>
			<!-- /wp:heading -->

			<!-- wp:paragraph -->
			<p><?php /* translators: %s: author name. */ printf( esc_html__( 'by %s', 'pagesco' ), esc_html( $pagesco_book['author'] ) ); ?></p>
			<!-- /wp:paragraph -->

			<?php
			// The price comes from the book itself, through the plugin's binding source, every time the page is shown.
			// Without the plugin, the binding does nothing and the paragraph keeps its own text.
			$pagesco_binding = array(
				'metadata' => array(
					'bindings' => array(
						'content' => array(
							'source' => 'pagesco/book',
							'args'   => array(
								'field' => 'price',
								'book'  => $pagesco_book['slug'],
							),
						),
					),
				),
				'fontSize' => 'small',
			);
			?>
			<!-- wp:paragraph <?php echo wp_json_encode( $pagesco_binding ); ?> -->
			<p class="has-small-font-size"><?php esc_html_e( 'Ask us for the price', 'pagesco' ); ?></p>
			<!-- /wp:paragraph -->
		</div>
		<!-- /wp:column -->
		<?php endforeach; ?>
	</div>
	<!-- /wp:columns -->
</div>
<!-- /wp:group -->

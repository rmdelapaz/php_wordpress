<?php
/**
 * Renders the Book List block on the server, every time a page with the block is viewed.
 *
 * WordPress includes this file inside a function and passes three variables:
 *     $attributes (array):    the block's attributes, with the defaults from block.json filled in.
 *     $content    (string):   the block's saved inner HTML (empty: this block saves nothing).
 *     $block      (WP_Block): the block instance (name, context, parsed block).
 *
 * @package PagesCo\Books
 */

defined( 'ABSPATH' ) || exit;

use PagesCo\Books\BookPostType;
use PagesCo\Books\GenreTaxonomy;
use PagesCo\Books\Settings;
use PagesCo\Books\Shortcodes\BookShortcode;

// No count in the block: use the Books per list setting (Lesson 5.4). Either way, 1 to 24.
$count = isset( $attributes['count'] ) ? absint( $attributes['count'] ) : (int) Settings::get( 'books_per_page' );
$count = min( 24, max( 1, $count ) );

$query_args = array(
	'post_type'      => BookPostType::NAME,
	'post_status'    => 'publish',
	'posts_per_page' => $count,
	'orderby'        => 'title',
	'order'          => 'ASC',
);

if ( 'newest' === $attributes['orderBy'] ) {
	$query_args['orderby'] = 'date';
	$query_args['order']   = 'DESC';
} elseif ( 'price' === $attributes['orderBy'] ) {
	$query_args['meta_key'] = 'pagesco_price';
	$query_args['orderby']  = 'meta_value_num';
}

if ( '' !== $attributes['genre'] ) {
	$query_args['tax_query'] = array(
		array(
			'taxonomy' => GenreTaxonomy::NAME,
			'field'    => 'slug',
			'terms'    => sanitize_key( $attributes['genre'] ),
		),
	);
}

$books = get_posts( $query_args );

if ( ! $books ) {
	printf(
		'<p %1$s>%2$s</p>',
		get_block_wrapper_attributes(),  // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- core escapes the attributes.
		esc_html__( 'No books match this list yet.', 'pagesco-books' )
	);
	return;
}

$card = new BookShortcode();
?>
<ul <?php echo get_block_wrapper_attributes(); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- core escapes the attributes. ?>>
	<?php foreach ( $books as $book ) : ?>
		<li class="wp-block-pagesco-book-list__item"><?php echo wp_kses_post( $card->render( array( 'id' => $book->ID ) ) ); ?></li>
	<?php endforeach; ?>
</ul>

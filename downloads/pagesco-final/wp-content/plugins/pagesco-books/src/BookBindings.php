<?php
/**
 * The pagesco/book block bindings source: book details, formatted for the shop.
 *
 * @package PagesCo\Books
 */

namespace PagesCo\Books;

/**
 * Lets core blocks show a book's price, stock, pages, year and genres, formatted.
 */
final class BookBindings implements Feature {

	/**
	 * The source's name, as blocks refer to it in metadata.bindings.
	 */
	public const SOURCE = 'pagesco/book';

	/**
	 * Registers the source on init, like core registers core/post-meta.
	 */
	public function register(): void {
		add_action( 'init', array( $this, 'register_source' ) );
	}

	/**
	 * Tells WordPress about the source: its label, its callback, and the context it needs.
	 */
	public function register_source(): void {
		register_block_bindings_source(
			self::SOURCE,
			array(
				'label'              => __( 'Book details', 'pagesco-books' ),
				'get_value_callback' => array( $this, 'get_value' ),
				'uses_context'       => array( 'postId', 'postType' ),
			)
		);
	}

	/**
	 * Returns the value for one bound attribute, or null to keep the block's own content.
	 *
	 * @param array     $source_args    The binding's args: array( 'field' => 'price' ), and optionally 'book' => a book's slug.
	 * @param \WP_Block $block_instance The block being rendered; its context names the post.
	 * @return string|null
	 */
	public function get_value( array $source_args, $block_instance ) {
		// A pattern can name the book by its slug, on any page; otherwise the book is the post being shown (Lesson 9.1).
		if ( isset( $source_args['book'] ) ) {
			$book    = get_page_by_path( sanitize_title( $source_args['book'] ), OBJECT, BookPostType::NAME );
			$book_id = $book ? $book->ID : 0;
		} else {
			$book_id = (int) ( $block_instance->context['postId'] ?? 0 );
		}

		if ( ! $book_id || BookPostType::NAME !== get_post_type( $book_id ) ) {
			return null;
		}
		// The same rule as core/post-meta: never reveal a book the visitor could not read.
		if ( ! is_post_publicly_viewable( $book_id ) && ! current_user_can( 'read_post', $book_id ) ) {
			return null;
		}

		switch ( $source_args['field'] ?? '' ) {
			case 'price':
				return esc_html( '$' . number_format_i18n( (float) get_post_meta( $book_id, 'pagesco_price', true ), 2 ) );

			case 'stock':
				return get_post_meta( $book_id, 'pagesco_in_stock', true )
					? esc_html__( 'In stock', 'pagesco-books' )
					: esc_html__( 'Sold out', 'pagesco-books' );

			case 'pages':
				$pages = (int) get_post_meta( $book_id, 'pagesco_pages', true );
				/* translators: %s: number of pages. */
				return esc_html( sprintf( _n( '%s page', '%s pages', $pages, 'pagesco-books' ), number_format_i18n( $pages ) ) );

			case 'year':
				$published = (string) get_post_meta( $book_id, 'pagesco_published', true );
				/* translators: %s: a year, such as 1965. */
				return '' === $published ? null : esc_html( sprintf( __( 'First published in %s', 'pagesco-books' ), substr( $published, 0, 4 ) ) );

			case 'genres':
				$genres = get_the_term_list( $book_id, GenreTaxonomy::NAME, '', ', ' );
				return is_string( $genres ) ? $genres : null;
		}

		return null;
	}
}

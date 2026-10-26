<?php
/**
 * Renders the Book Filter: genre links and the whole catalog, with Interactivity API directives.
 *
 * The server prints the finished HTML (filtered already if the URL says ?genre=…), and the
 * view.js store takes over in the browser. $attributes, $content and $block as in Lesson 6.3.
 *
 * @package PagesCo\Books
 */

defined( 'ABSPATH' ) || exit;

use PagesCo\Books\BookPostType;
use PagesCo\Books\GenreTaxonomy;
use PagesCo\Books\Shortcodes\BookShortcode;

$books  = get_posts(
	array(
		'post_type'      => BookPostType::NAME,
		'post_status'    => 'publish',
		'posts_per_page' => 100,
		'orderby'        => 'title',
		'order'          => 'ASC',
	)
);
$genres = get_terms(
	array(
		'taxonomy'   => GenreTaxonomy::NAME,
		'hide_empty' => true,
	)
);
$genres = is_array( $genres ) ? $genres : array();

// Each book's genre slugs, in the same order as $books.
$book_genres = array();
foreach ( $books as $book ) {
	$terms         = get_the_terms( $book, GenreTaxonomy::NAME );
	$book_genres[] = is_array( $terms ) ? wp_list_pluck( $terms, 'slug' ) : array();
}

// A genre in the address (?genre=fantasy) is the starting filter, so the links work without JavaScript.
$selected = isset( $_GET['genre'] ) ? sanitize_key( wp_unslash( $_GET['genre'] ) ) : '';  // phpcs:ignore WordPress.Security.NonceVerification.Recommended -- a read-only filter, checked against the genres below.
if ( ! in_array( $selected, wp_list_pluck( $genres, 'slug' ), true ) ) {
	$selected = '';
}

wp_interactivity_state(
	'pagesco/book-filter',
	array(
		'genre'        => $selected,
		'bookGenres'   => $book_genres,
		// Derived state: the server runs these closures while it processes the directives.
		'isVisible'    => function () {
			$state   = wp_interactivity_state();
			$context = wp_interactivity_get_context();
			return '' === $state['genre'] || in_array( $state['genre'], $context['genres'], true );
		},
		'isSelected'   => function () {
			$state   = wp_interactivity_state();
			$context = wp_interactivity_get_context();
			return $state['genre'] === $context['slug'];
		},
		'visibleCount' => function () {
			$state = wp_interactivity_state();
			$count = 0;
			foreach ( $state['bookGenres'] as $slugs ) {
				if ( '' === $state['genre'] || in_array( $state['genre'], $slugs, true ) ) {
					++$count;
				}
			}
			return $count;
		},
	)
);

$card  = new BookShortcode();
$links = array_merge(
	array( '' => __( 'All books', 'pagesco-books' ) ),
	wp_list_pluck( $genres, 'name', 'slug' )
);
?>
<div <?php echo get_block_wrapper_attributes(); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- core escapes the attributes. ?> data-wp-interactive="pagesco/book-filter">
	<nav class="wp-block-pagesco-book-filter__genres" aria-label="<?php esc_attr_e( 'Filter by genre', 'pagesco-books' ); ?>">
		<?php foreach ( $links as $slug => $name ) : ?>
			<a
				href="<?php echo esc_url( '' === $slug ? remove_query_arg( 'genre' ) : add_query_arg( 'genre', $slug ) ); ?>"
				<?php echo wp_interactivity_data_wp_context( array( 'slug' => (string) $slug ) ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- core escapes the JSON. ?>
				data-wp-on--click="actions.selectGenre"
				data-wp-bind--aria-current="state.isSelected"
				data-wp-class--is-selected="state.isSelected"
			><?php echo esc_html( $name ); ?></a>
		<?php endforeach; ?>
	</nav>

	<p class="wp-block-pagesco-book-filter__count" aria-live="polite">
		<?php
		printf(
			/* translators: 1: number of books shown, 2: number of books in the catalog. */
			esc_html__( 'Showing %1$s of %2$s books', 'pagesco-books' ),
			'<span data-wp-text="state.visibleCount"></span>',
			esc_html( number_format_i18n( count( $books ) ) )
		);
		?>
	</p>

	<ul class="wp-block-pagesco-book-filter__books">
		<?php foreach ( $books as $index => $book ) : ?>
			<li
				<?php echo wp_interactivity_data_wp_context( array( 'genres' => $book_genres[ $index ] ) ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- core escapes the JSON. ?>
				data-wp-bind--hidden="!state.isVisible"
			><?php echo wp_kses_post( $card->render( array( 'id' => $book->ID ) ) ); ?></li>
		<?php endforeach; ?>
	</ul>
</div>

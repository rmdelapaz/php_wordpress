<?php
/**
 * What the supplier has of each book, cached in a transient.
 *
 * @package PagesCo\Books
 */

namespace PagesCo\Books\Supplier;

use PagesCo\Books\BookPostType;
use PagesCo\Books\Feature;

/**
 * Keeps the supplier's availability for the whole catalog in one transient, and shows it on the Books screen.
 */
final class Availability implements Feature {

	/**
	 * The transient that holds the last answer (or the last error).
	 */
	public const TRANSIENT = 'pagesco_books_supplier_availability';

	/**
	 * Keep a good answer for 12 hours; the daily sync refreshes it anyway.
	 */
	private const LIFETIME = 12 * HOUR_IN_SECONDS;

	/**
	 * After a failure, wait 5 minutes before asking again.
	 */
	private const RETRY = 5 * MINUTE_IN_SECONDS;

	/**
	 * Adds a Supplier column to the Books screen.
	 */
	public function register(): void {
		add_filter( 'manage_' . BookPostType::NAME . '_posts_columns', array( $this, 'add_column' ), 20 );
		add_action( 'manage_' . BookPostType::NAME . '_posts_custom_column', array( $this, 'print_column' ), 10, 2 );
	}

	/**
	 * The cached availability; asks the supplier only when there is no cached answer.
	 *
	 * @return array{items: array, error: string}
	 */
	public function get(): array {
		$cached = get_transient( self::TRANSIENT );

		if ( is_array( $cached ) ) {
			return $cached;
		}

		return $this->refresh();
	}

	/**
	 * Asks the supplier now and caches the answer: for 12 hours, or for 5 minutes if it failed.
	 *
	 * @return array{items: array, error: string}
	 */
	public function refresh(): array {
		$result = ( new Client() )->availability( $this->catalog_isbns() );

		if ( is_wp_error( $result ) ) {
			$value = array(
				'items' => array(),
				'error' => $result->get_error_message(),
			);
			set_transient( self::TRANSIENT, $value, self::RETRY );

			return $value;
		}

		$value = array(
			'items' => $result,
			'error' => '',
		);
		set_transient( self::TRANSIENT, $value, self::LIFETIME );

		return $value;
	}

	/**
	 * The ISBNs of the published books that have one.
	 *
	 * @return string[]
	 */
	private function catalog_isbns(): array {
		$ids = get_posts(
			array(
				'post_type'      => BookPostType::NAME,
				'post_status'    => 'publish',
				'posts_per_page' => 100,
				'fields'         => 'ids',
			)
		);

		// One query for the meta of all books, not one per book (Lesson 8.2).
		update_postmeta_cache( $ids );

		$isbns = array_map( fn( $id ) => (string) get_post_meta( $id, 'pagesco_isbn', true ), $ids );

		return array_values( array_filter( $isbns ) );
	}

	/**
	 * Adds the Supplier column after the shop's own Stock column.
	 *
	 * @param string[] $columns Column keys and headings.
	 * @return string[]
	 */
	public function add_column( $columns ) {
		$columns['pagesco_supplier'] = __( 'Supplier', 'pagesco-books' );

		return $columns;
	}

	/**
	 * Prints a book's Supplier cell: copies there, or the next delivery date.
	 *
	 * @param string $column  The column key.
	 * @param int    $post_id The book in this row.
	 */
	public function print_column( $column, $post_id ): void {
		if ( 'pagesco_supplier' !== $column ) {
			return;
		}

		$isbn         = (string) get_post_meta( $post_id, 'pagesco_isbn', true );
		$availability = $this->get();
		$item         = $availability['items'][ $isbn ] ?? null;

		if ( '' !== $availability['error'] ) {
			esc_html_e( 'Supplier not reachable', 'pagesco-books' );
		} elseif ( null === $item ) {
			echo '&mdash;';
		} elseif ( $item['available'] > 0 ) {
			/* translators: %s: number of copies. */
			echo esc_html( sprintf( _n( '%s copy', '%s copies', $item['available'], 'pagesco-books' ), number_format_i18n( $item['available'] ) ) );
		} elseif ( '' !== $item['next_delivery'] ) {
			/* translators: %s: a date. */
			echo esc_html( sprintf( __( 'None; next delivery %s', 'pagesco-books' ), mysql2date( get_option( 'date_format' ), $item['next_delivery'] ) ) );
		} else {
			esc_html_e( 'None', 'pagesco-books' );
		}
	}
}

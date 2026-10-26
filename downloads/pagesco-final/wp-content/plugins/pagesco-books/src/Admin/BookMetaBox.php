<?php
/**
 * The "Book details" box on the book editing screen (hardened in Lesson 5.3).
 *
 * @package PagesCo\Books
 */

namespace PagesCo\Books\Admin;

use PagesCo\Books\BookPostType;
use PagesCo\Books\Feature;

/**
 * Shows the book meta as a form under the editor and saves it safely with the book.
 */
final class BookMetaBox implements Feature {

	/**
	 * The fields this box edits, so render and save stay in step.
	 */
	private const TEXT_FIELDS = array( 'pagesco_author', 'pagesco_isbn' );

	/**
	 * Hooks the box into the book screen and the save into save_post_book.
	 */
	public function register(): void {
		add_action( 'add_meta_boxes_' . BookPostType::NAME, array( $this, 'add' ) );
		add_action( 'save_post_' . BookPostType::NAME, array( $this, 'save' ), 10, 2 );
	}

	/**
	 * Adds the box to the book editing screen.
	 */
	public function add(): void {
		add_meta_box(
			'pagesco-book-details',
			__( 'Book details', 'pagesco-books' ),
			array( $this, 'render' ),
			BookPostType::NAME,
			'normal',
			'high'
		);
	}

	/**
	 * Prints the form fields, filled with the saved values and escaped for the attribute context.
	 *
	 * @param \WP_Post $post The book being edited.
	 */
	public function render( $post ): void {
		wp_nonce_field( 'pagesco_books_save_details', 'pagesco_books_details_nonce' );

		$author    = get_post_meta( $post->ID, 'pagesco_author', true );
		$price     = get_post_meta( $post->ID, 'pagesco_price', true );
		$pages     = get_post_meta( $post->ID, 'pagesco_pages', true );
		$published = get_post_meta( $post->ID, 'pagesco_published', true );
		$isbn      = get_post_meta( $post->ID, 'pagesco_isbn', true );
		$in_stock  = get_post_meta( $post->ID, 'pagesco_in_stock', true );
		?>
		<p>
			<label for="pagesco-author"><?php esc_html_e( 'Author', 'pagesco-books' ); ?></label><br>
			<input type="text" id="pagesco-author" name="pagesco_author" class="widefat" value="<?php echo esc_attr( $author ); ?>">
		</p>
		<p>
			<label for="pagesco-price"><?php esc_html_e( 'Price (USD)', 'pagesco-books' ); ?></label><br>
			<input type="number" id="pagesco-price" name="pagesco_price" min="0" step="0.01" value="<?php echo esc_attr( $price ); ?>">
		</p>
		<p>
			<label for="pagesco-pages"><?php esc_html_e( 'Pages', 'pagesco-books' ); ?></label><br>
			<input type="number" id="pagesco-pages" name="pagesco_pages" min="1" step="1" value="<?php echo esc_attr( $pages ); ?>">
		</p>
		<p>
			<label for="pagesco-published"><?php esc_html_e( 'First published', 'pagesco-books' ); ?></label><br>
			<input type="date" id="pagesco-published" name="pagesco_published" value="<?php echo esc_attr( $published ); ?>">
		</p>
		<p>
			<label for="pagesco-isbn"><?php esc_html_e( 'ISBN', 'pagesco-books' ); ?></label><br>
			<input type="text" id="pagesco-isbn" name="pagesco_isbn" value="<?php echo esc_attr( $isbn ); ?>">
		</p>
		<p>
			<label>
				<input type="checkbox" name="pagesco_in_stock" value="1" <?php checked( (bool) $in_stock ); ?>>
				<?php esc_html_e( 'In stock', 'pagesco-books' ); ?>
			</label>
		</p>
		<?php
	}

	/**
	 * Saves the fields when the book is saved from this form.
	 *
	 * @param int      $post_id The book's ID.
	 * @param \WP_Post $post    The book.
	 */
	public function save( $post_id, $post ): void {
		// 1. Is this a real submission of our form, not an autosave or a bulk edit?
		if ( ! isset( $_POST['pagesco_books_details_nonce'] ) ) {
			return;
		}
		if ( wp_is_post_autosave( $post_id ) || wp_is_post_revision( $post_id ) ) {
			return;
		}

		// 2. Did it carry our valid nonce?
		if ( ! wp_verify_nonce( sanitize_key( wp_unslash( $_POST['pagesco_books_details_nonce'] ) ), 'pagesco_books_save_details' ) ) {
			return;
		}

		// 3. May this user edit this book?
		if ( ! current_user_can( 'edit_post', $post_id ) ) {
			return;
		}

		// 4. Sanitize and validate every field before it is stored.
		$in = wp_unslash( $_POST );

		update_post_meta( $post_id, 'pagesco_author', sanitize_text_field( $in['pagesco_author'] ?? '' ) );
		update_post_meta( $post_id, 'pagesco_isbn', sanitize_text_field( $in['pagesco_isbn'] ?? '' ) );
		update_post_meta( $post_id, 'pagesco_price', max( 0, (float) ( $in['pagesco_price'] ?? 0 ) ) );
		update_post_meta( $post_id, 'pagesco_pages', absint( $in['pagesco_pages'] ?? 0 ) );
		update_post_meta( $post_id, 'pagesco_published', self::valid_date( $in['pagesco_published'] ?? '' ) );
		update_post_meta( $post_id, 'pagesco_in_stock', isset( $in['pagesco_in_stock'] ) );
	}

	/**
	 * Returns the value only if it is a real Y-m-d date, otherwise an empty string.
	 *
	 * @param string $value The submitted value.
	 * @return string
	 */
	private static function valid_date( $value ): string {
		$value = sanitize_text_field( $value );
		$date  = \DateTime::createFromFormat( 'Y-m-d', $value );

		return ( $date && $date->format( 'Y-m-d' ) === $value ) ? $value : '';
	}
}

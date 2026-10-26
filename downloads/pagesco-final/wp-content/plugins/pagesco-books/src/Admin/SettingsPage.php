<?php
/**
 * The Settings > Pages & Co. Books screen.
 *
 * @package PagesCo\Books
 */

namespace PagesCo\Books\Admin;

use PagesCo\Books\Feature;
use PagesCo\Books\Settings;

/**
 * Adds the settings page and builds its form with the Settings API.
 */
final class SettingsPage implements Feature {

	/**
	 * The page's slug: options-general.php?page=pagesco-books.
	 */
	public const SLUG = 'pagesco-books';

	/**
	 * Hooks the menu item, the sections and fields, and the Plugins screen link.
	 */
	public function register(): void {
		add_action( 'admin_menu', array( $this, 'add_page' ) );
		add_action( 'admin_init', array( $this, 'add_fields' ) );
		add_filter( 'plugin_action_links_' . plugin_basename( PAGESCO_BOOKS_FILE ), array( $this, 'add_settings_link' ) );
	}

	/**
	 * Adds the page under Settings, for users who can manage options.
	 */
	public function add_page(): void {
		add_options_page(
			__( 'Pages & Co. Books Settings', 'pagesco-books' ),
			__( 'Pages & Co. Books', 'pagesco-books' ),
			'manage_options',
			self::SLUG,
			array( $this, 'render' )
		);
	}

	/**
	 * Describes the form: four sections, seven fields.
	 */
	public function add_fields(): void {
		add_settings_section(
			'pagesco_books_notice',
			__( 'Store notice', 'pagesco-books' ),
			array( $this, 'render_notice_intro' ),
			self::SLUG
		);
		add_settings_field(
			'notice_extra',
			__( 'Notice addition', 'pagesco-books' ),
			array( $this, 'render_text_field' ),
			self::SLUG,
			'pagesco_books_notice',
			array(
				'key'         => 'notice_extra',
				'label_for'   => 'pagesco-notice-extra',
				'description' => __( 'Added after the free-shipping text. Leave empty to show only that text.', 'pagesco-books' ),
			)
		);
		add_settings_field(
			'show_events_link',
			__( 'Events link', 'pagesco-books' ),
			array( $this, 'render_checkbox_field' ),
			self::SLUG,
			'pagesco_books_notice',
			array(
				'key'       => 'show_events_link',
				'label_for' => 'pagesco-show-events-link',
				'label'     => __( 'Show a "See events" link in the notice', 'pagesco-books' ),
			)
		);

		add_settings_section(
			'pagesco_books_lists',
			__( 'Catalog and events', 'pagesco-books' ),
			'__return_false',
			self::SLUG
		);
		add_settings_field(
			'books_per_page',
			__( 'Books per list', 'pagesco-books' ),
			array( $this, 'render_number_field' ),
			self::SLUG,
			'pagesco_books_lists',
			array(
				'key'       => 'books_per_page',
				'label_for' => 'pagesco-books-per-page',
				'max'       => 24,
			)
		);
		add_settings_field(
			'events_limit',
			__( 'Events to show', 'pagesco-books' ),
			array( $this, 'render_number_field' ),
			self::SLUG,
			'pagesco_books_lists',
			array(
				'key'       => 'events_limit',
				'label_for' => 'pagesco-events-limit',
				'max'       => 20,
			)
		);

		add_settings_section(
			'pagesco_books_holds',
			__( 'Reserve & Pick Up', 'pagesco-books' ),
			'__return_false',
			self::SLUG
		);
		add_settings_field(
			'hold_days',
			__( 'Days to keep a hold', 'pagesco-books' ),
			array( $this, 'render_number_field' ),
			self::SLUG,
			'pagesco_books_holds',
			array(
				'key'       => 'hold_days',
				'label_for' => 'pagesco-hold-days',
				'max'       => 14,
			)
		);
		add_settings_field(
			'max_holds',
			__( 'Holds per customer', 'pagesco-books' ),
			array( $this, 'render_number_field' ),
			self::SLUG,
			'pagesco_books_holds',
			array(
				'key'       => 'max_holds',
				'label_for' => 'pagesco-max-holds',
				'max'       => 10,
			)
		);

		add_settings_section(
			'pagesco_books_uninstall',
			__( 'Uninstall', 'pagesco-books' ),
			'__return_false',
			self::SLUG
		);
		add_settings_field(
			'delete_data',
			__( 'Shop data', 'pagesco-books' ),
			array( $this, 'render_checkbox_field' ),
			self::SLUG,
			'pagesco_books_uninstall',
			array(
				'key'         => 'delete_data',
				'label_for'   => 'pagesco-delete-data',
				'label'       => __( 'Delete all books, genres and book details when the plugin is deleted', 'pagesco-books' ),
				'description' => __( 'Leave this off unless the shop is closing for good: deleted books cannot be restored. Settings, the events, the holds and the Bookseller role are always removed.', 'pagesco-books' ),
			)
		);
	}

	/**
	 * Prints the page: the form posts to options.php, which checks the nonce and saves the option.
	 */
	public function render(): void {
		if ( ! current_user_can( 'manage_options' ) ) {
			return;
		}
		?>
		<div class="wrap">
			<h1><?php echo esc_html( get_admin_page_title() ); ?></h1>
			<form action="options.php" method="post">
				<?php
				settings_fields( Settings::GROUP );
				do_settings_sections( self::SLUG );
				submit_button();
				?>
			</form>
		</div>
		<?php
	}

	/**
	 * Prints the text under the Store notice heading.
	 */
	public function render_notice_intro(): void {
		echo '<p>' . esc_html__( 'The bar at the top of every page of the shop.', 'pagesco-books' ) . '</p>';
	}

	/**
	 * Prints a text input for one setting.
	 *
	 * @param array $args The field's arguments from add_settings_field().
	 */
	public function render_text_field( $args ): void {
		printf(
			'<input type="text" id="%1$s" name="%2$s[%3$s]" value="%4$s" class="regular-text"><p class="description">%5$s</p>',
			esc_attr( $args['label_for'] ),
			esc_attr( Settings::OPTION ),
			esc_attr( $args['key'] ),
			esc_attr( Settings::get( $args['key'] ) ),
			esc_html( $args['description'] )
		);
	}

	/**
	 * Prints a checkbox for one setting.
	 *
	 * @param array $args The field's arguments from add_settings_field().
	 */
	public function render_checkbox_field( $args ): void {
		printf(
			'<label><input type="checkbox" id="%1$s" name="%2$s[%3$s]" value="1"%4$s> %5$s</label>',
			esc_attr( $args['label_for'] ),
			esc_attr( Settings::OPTION ),
			esc_attr( $args['key'] ),
			checked( Settings::get( $args['key'] ), true, false ),
			esc_html( $args['label'] )
		);

		if ( ! empty( $args['description'] ) ) {
			printf( '<p class="description">%s</p>', esc_html( $args['description'] ) );
		}
	}

	/**
	 * Prints a number input for one setting.
	 *
	 * @param array $args The field's arguments from add_settings_field().
	 */
	public function render_number_field( $args ): void {
		printf(
			'<input type="number" id="%1$s" name="%2$s[%3$s]" value="%4$s" min="1" max="%5$d" step="1" class="small-text">',
			esc_attr( $args['label_for'] ),
			esc_attr( Settings::OPTION ),
			esc_attr( $args['key'] ),
			esc_attr( Settings::get( $args['key'] ) ),
			absint( $args['max'] )
		);
	}

	/**
	 * Adds a Settings link next to Deactivate on the Plugins screen.
	 *
	 * @param string[] $links The plugin's action links.
	 * @return string[]
	 */
	public function add_settings_link( $links ) {
		$url = admin_url( 'options-general.php?page=' . self::SLUG );
		array_unshift( $links, sprintf( '<a href="%s">%s</a>', esc_url( $url ), esc_html__( 'Settings', 'pagesco-books' ) ) );

		return $links;
	}
}

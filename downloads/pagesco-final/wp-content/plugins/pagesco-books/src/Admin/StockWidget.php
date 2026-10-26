<?php
/**
 * The "Stock at a glance" dashboard widget.
 *
 * @package PagesCo\Books
 */

namespace PagesCo\Books\Admin;

use PagesCo\Books\Feature;

/**
 * Adds a dashboard widget that lists the books and switches their stock through the REST API.
 */
final class StockWidget implements Feature {

	/**
	 * The widget's ID, which is also its script's handle.
	 */
	public const HANDLE = 'pagesco-stock-widget';

	/**
	 * Hooks the widget and its script.
	 */
	public function register(): void {
		add_action( 'wp_dashboard_setup', array( $this, 'add_widget' ) );
		add_action( 'admin_enqueue_scripts', array( $this, 'enqueue' ) );
	}

	/**
	 * Who sees the widget: users who may edit everyone's books (editors and administrators).
	 */
	private function can_use(): bool {
		return current_user_can( 'edit_others_posts' );
	}

	/**
	 * Adds the widget to the Dashboard.
	 */
	public function add_widget(): void {
		if ( ! $this->can_use() ) {
			return;
		}

		wp_add_dashboard_widget( self::HANDLE, __( 'Stock at a glance', 'pagesco-books' ), array( $this, 'render' ) );
	}

	/**
	 * Prints the widget's frame; the script fills the list.
	 */
	public function render(): void {
		?>
		<p class="pagesco-stock-widget__status" aria-live="polite"><?php esc_html_e( 'Loading the catalog…', 'pagesco-books' ); ?></p>
		<ul class="pagesco-stock-widget__books"></ul>
		<?php
	}

	/**
	 * Loads the script on the Dashboard only.
	 *
	 * @param string $hook_suffix The current admin screen.
	 */
	public function enqueue( $hook_suffix ): void {
		if ( 'index.php' !== $hook_suffix || ! $this->can_use() ) {
			return;
		}

		wp_enqueue_script(
			self::HANDLE,
			plugins_url( 'assets/js/stock-widget.js', PAGESCO_BOOKS_FILE ),
			array( 'wp-api-fetch', 'wp-i18n' ),
			PAGESCO_BOOKS_VERSION,
			array( 'in_footer' => true )
		);
		wp_set_script_translations( self::HANDLE, 'pagesco-books' );
	}
}

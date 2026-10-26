<?php
/**
 * What happens when the plugin is activated or deactivated.
 *
 * @package PagesCo\Books
 */

namespace PagesCo\Books;

/**
 * Activation and deactivation callbacks (uninstall.php cleans up for good).
 */
final class Activator {

	/**
	 * Runs once, when an administrator activates the plugin.
	 */
	public static function activate(): void {
		$author = get_role( 'author' );

		add_role(
			'pagesco_bookseller',
			'Bookseller',
			$author ? $author->capabilities : array( 'read' => true )
		);

		// init has already run on this request: register the post type and taxonomy now, so their rules exist.
		( new BookPostType() )->register_post_type();
		( new GenreTaxonomy() )->register_taxonomy();
		flush_rewrite_rules();

		// Create the events table, or bring it up to date (Lesson 5.5).
		EventsTable::install();

		// Create the holds table (Lesson 9.1).
		Holds\HoldsTable::install();

		// Start the daily WP-Cron job (Lesson 7.3).
		DailySync::schedule();

		// The settings row, empty: it is autoloaded, so reading the settings costs no query on any
		// request, and empty, so every default still applies, in the site's language (Lesson 8.2).
		add_option( Settings::OPTION, array() );
	}

	/**
	 * Runs once, when the plugin is deactivated. Keeps all data.
	 */
	public static function deactivate(): void {
		// Remove the post type's and taxonomy's rules, so /books/ stops answering while the plugin is off.
		unregister_post_type( BookPostType::NAME );
		unregister_taxonomy( GenreTaxonomy::NAME );
		flush_rewrite_rules();

		// A deactivated plugin's cron job would still be due every day, with no callback to run.
		DailySync::unschedule();
	}
}

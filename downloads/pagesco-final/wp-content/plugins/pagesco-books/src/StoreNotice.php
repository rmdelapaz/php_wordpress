<?php
/**
 * The shop's additions to the store notice from the pagesco-site must-use plugin.
 *
 * @package PagesCo\Books
 */

namespace PagesCo\Books;

/**
 * Adds the shop's own sentence and an events link to the store notice, as the settings say.
 */
final class StoreNotice implements Feature {

	/**
	 * Hooks into the notice's own filter and action (Lesson 2.3).
	 */
	public function register(): void {
		add_filter( 'pagesco_store_notice', array( $this, 'add_late_opening' ), 20 );
		add_action( 'pagesco_store_notice_end', array( $this, 'print_events_link' ) );
	}

	/**
	 * Adds the "Notice addition" setting to the notice text.
	 *
	 * @param string $text The notice text so far.
	 * @return string
	 */
	public function add_late_opening( $text ) {
		$extra = Settings::get( 'notice_extra' );

		return '' === $extra ? $text : $text . ' ' . $extra;
	}

	/**
	 * Prints a link to the events page inside the notice bar, unless the settings turn it off.
	 */
	public function print_events_link(): void {
		if ( ! Settings::get( 'show_events_link' ) ) {
			return;
		}

		printf(
			' <a href="%s">%s</a>',
			esc_url( home_url( '/events/' ) ),
			esc_html__( 'See events', 'pagesco-books' )
		);
	}
}

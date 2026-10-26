<?php
/**
 * The [pagesco_events] shortcode.
 *
 * @package PagesCo\Books
 */

namespace PagesCo\Books\Shortcodes;

use PagesCo\Books\EventsTable;
use PagesCo\Books\Feature;
use PagesCo\Books\Settings;

/**
 * Lists the shop's events from the custom table.
 */
final class EventsShortcode implements Feature {

	/**
	 * The shortcode's tag.
	 */
	public const TAG = 'pagesco_events';

	/**
	 * Registers the shortcode on init.
	 */
	public function register(): void {
		add_action( 'init', array( $this, 'add_shortcode' ) );
	}

	/**
	 * Tells WordPress which callback renders [pagesco_events].
	 */
	public function add_shortcode(): void {
		add_shortcode( self::TAG, array( $this, 'render' ) );
	}

	/**
	 * Returns the list of events as HTML.
	 *
	 * @param array|string $atts limit (default: the Events to show setting) and location (default: all).
	 * @return string
	 */
	public function render( $atts ) {
		$atts = shortcode_atts(
			array(
				'limit'    => Settings::get( 'events_limit' ),
				'location' => '',
			),
			$atts,
			self::TAG
		);

		$limit  = min( 50, max( 1, absint( $atts['limit'] ) ) );
		$events = EventsTable::find( $limit, sanitize_text_field( $atts['location'] ) );

		if ( ! $events ) {
			return '<p class="pagesco-events-empty">' . esc_html__( 'No events are scheduled right now. Check back soon!', 'pagesco-books' ) . '</p>';
		}

		$items = '';
		foreach ( $events as $event ) {
			$seats = (int) $event->capacity
				/* translators: %d: number of seats. */
				? sprintf( _n( '%d seat', '%d seats', (int) $event->capacity, 'pagesco-books' ), (int) $event->capacity )
				: __( 'open to all', 'pagesco-books' );

			$items .= sprintf(
				'<li class="pagesco-event"><strong>%1$s</strong> <time datetime="%2$s">%3$s</time> <span class="pagesco-event__where">%4$s, %5$s</span></li>',
				esc_html( $event->title ),
				esc_attr( mysql2date( 'Y-m-d\TH:i', $event->starts_at, false ) ),
				esc_html( mysql2date( 'l, F j, g:i a', $event->starts_at ) ),
				esc_html( $event->location ),
				esc_html( $seats )
			);
		}

		return '<ul class="pagesco-events">' . $items . '</ul>';
	}
}

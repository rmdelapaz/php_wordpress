<?php
/**
 * The shop's settings: one option, an array of values with defaults.
 *
 * @package PagesCo\Books
 */

namespace PagesCo\Books;

/**
 * Registers the pagesco_books_settings option and reads it for the rest of the plugin.
 */
final class Settings implements Feature {

	/**
	 * The option's name in wp_options.
	 */
	public const OPTION = 'pagesco_books_settings';

	/**
	 * The option group the settings form posts (settings_fields() prints it).
	 */
	public const GROUP = 'pagesco_books';

	/**
	 * Registers the setting on init, so its sanitizing and default apply everywhere, not only in wp-admin.
	 */
	public function register(): void {
		add_action( 'init', array( $this, 'register_setting' ) );
	}

	/**
	 * Every setting with its default value.
	 *
	 * @return array{notice_extra: string, show_events_link: bool, books_per_page: int, events_limit: int, delete_data: bool, hold_days: int, max_holds: int}
	 */
	public static function defaults(): array {
		return array(
			'notice_extra'     => __( 'Open until 9 p.m. on Thursdays.', 'pagesco-books' ),
			'show_events_link' => true,
			'books_per_page'   => 6,
			'events_limit'     => 5,
			'delete_data'      => false,
			'hold_days'        => 3,
			'max_holds'        => 3,
		);
	}

	/**
	 * Returns one setting: the saved value, or its default when nothing is saved yet.
	 *
	 * @param string $key A key of defaults().
	 * @return mixed
	 */
	public static function get( string $key ) {
		$settings = wp_parse_args( get_option( self::OPTION, array() ), self::defaults() );

		return $settings[ $key ] ?? null;
	}

	/**
	 * Tells WordPress about the option: its group, type, sanitize callback and default.
	 */
	public function register_setting(): void {
		register_setting(
			self::GROUP,
			self::OPTION,
			array(
				'type'              => 'object',
				'sanitize_callback' => array( $this, 'sanitize' ),
				'default'           => self::defaults(),
			)
		);
	}

	/**
	 * Cleans the submitted values before WordPress stores them. Out-of-range numbers keep the saved value.
	 *
	 * @param mixed $input The submitted settings.
	 * @return array
	 */
	public function sanitize( $input ): array {
		$input = is_array( $input ) ? $input : array();
		$saved = wp_parse_args( get_option( self::OPTION, array() ), self::defaults() );

		$clean = array(
			'notice_extra'     => sanitize_text_field( $input['notice_extra'] ?? '' ),
			'show_events_link' => ! empty( $input['show_events_link'] ),
			'books_per_page'   => absint( $input['books_per_page'] ?? $saved['books_per_page'] ),
			'events_limit'     => absint( $input['events_limit'] ?? $saved['events_limit'] ),
			'delete_data'      => ! empty( $input['delete_data'] ),
			'hold_days'        => absint( $input['hold_days'] ?? $saved['hold_days'] ),
			'max_holds'        => absint( $input['max_holds'] ?? $saved['max_holds'] ),
		);

		if ( $clean['books_per_page'] < 1 || $clean['books_per_page'] > 24 ) {
			add_settings_error( self::OPTION, 'books_per_page', __( 'Books per list must be between 1 and 24.', 'pagesco-books' ) );
			$clean['books_per_page'] = $saved['books_per_page'];
		}
		if ( $clean['events_limit'] < 1 || $clean['events_limit'] > 20 ) {
			add_settings_error( self::OPTION, 'events_limit', __( 'Events to show must be between 1 and 20.', 'pagesco-books' ) );
			$clean['events_limit'] = $saved['events_limit'];
		}
		if ( $clean['hold_days'] < 1 || $clean['hold_days'] > 14 ) {
			add_settings_error( self::OPTION, 'hold_days', __( 'Days to keep a hold must be between 1 and 14.', 'pagesco-books' ) );
			$clean['hold_days'] = $saved['hold_days'];
		}
		if ( $clean['max_holds'] < 1 || $clean['max_holds'] > 10 ) {
			add_settings_error( self::OPTION, 'max_holds', __( 'Holds per customer must be between 1 and 10.', 'pagesco-books' ) );
			$clean['max_holds'] = $saved['max_holds'];
		}

		return $clean;
	}
}

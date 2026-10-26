<?php
/**
 * The shop's events, kept in a custom table.
 *
 * @package PagesCo\Books
 */

namespace PagesCo\Books;

/**
 * Creates and upgrades the {prefix}pagesco_events table, and reads and writes its rows.
 */
final class EventsTable implements Feature {

	/**
	 * The schema version this code expects. Raise it whenever schema() changes.
	 */
	public const DB_VERSION = 2;

	/**
	 * The option that records the schema version installed in this database.
	 */
	public const VERSION_OPTION = 'pagesco_books_db_version';

	/**
	 * The object cache group for the table's query results.
	 */
	public const CACHE_GROUP = 'pagesco_events';

	/**
	 * Checks the schema on every request, so a plugin update upgrades the table without a reactivation.
	 */
	public function register(): void {
		add_action( 'init', array( $this, 'maybe_upgrade' ) );
	}

	/**
	 * The table's full name, with this site's table prefix.
	 */
	public static function name(): string {
		global $wpdb;

		return $wpdb->prefix . 'pagesco_events';
	}

	/**
	 * Runs install() when the database is older than this code.
	 */
	public function maybe_upgrade(): void {
		if ( (int) get_option( self::VERSION_OPTION, 0 ) < self::DB_VERSION ) {
			self::install();
		}
	}

	/**
	 * Creates the table, or brings an existing one up to schema(), and records the version.
	 */
	public static function install(): void {
		require_once ABSPATH . 'wp-admin/includes/upgrade.php';

		dbDelta( self::schema() );
		update_option( self::VERSION_OPTION, self::DB_VERSION );
		self::flush_cache();
	}

	/**
	 * The CREATE TABLE statement in the exact shape dbDelta() expects.
	 */
	private static function schema(): string {
		global $wpdb;

		$table   = self::name();
		$collate = $wpdb->get_charset_collate();

		return "CREATE TABLE {$table} (
			id bigint unsigned NOT NULL AUTO_INCREMENT,
			title varchar(200) NOT NULL,
			starts_at datetime NOT NULL,
			location varchar(200) NOT NULL DEFAULT '',
			capacity smallint unsigned NOT NULL DEFAULT 0,
			created_at datetime NOT NULL,
			PRIMARY KEY  (id),
			KEY starts_at (starts_at)
		) {$collate};";
	}

	/**
	 * Adds one event and returns its ID (0 if the insert failed).
	 *
	 * @param string $title     The event's name.
	 * @param string $starts_at Local date and time, Y-m-d H:i:s.
	 * @param string $location  Where in the shop.
	 * @param int    $capacity  Seats, or 0 for an open event.
	 */
	public static function add( string $title, string $starts_at, string $location, int $capacity ): int {
		global $wpdb;

		$inserted = $wpdb->insert(
			self::name(),
			array(
				'title'      => $title,
				'starts_at'  => $starts_at,
				'location'   => $location,
				'capacity'   => $capacity,
				'created_at' => current_time( 'mysql', true ),
			),
			array( '%s', '%s', '%s', '%d', '%s' )
		);

		if ( ! $inserted ) {
			return 0;
		}

		self::flush_cache();
		return (int) $wpdb->insert_id;
	}

	/**
	 * Returns events in date order, optionally only those at one location.
	 *
	 * @param int    $limit    How many events at most.
	 * @param string $location Exact location, or '' for every location.
	 * @return object[] Rows with id, title, starts_at, location, capacity.
	 */
	public static function find( int $limit, string $location = '' ): array {
		global $wpdb;

		// The key names everything the result depends on: the arguments, and when the table last changed.
		$key    = 'find:' . md5( $limit . '|' . $location ) . ':' . wp_cache_get_last_changed( self::CACHE_GROUP );
		$events = wp_cache_get( $key, self::CACHE_GROUP );
		if ( is_array( $events ) ) {
			return $events;
		}

		if ( '' === $location ) {
			$sql = $wpdb->prepare(
				'SELECT id, title, starts_at, location, capacity FROM %i ORDER BY starts_at ASC LIMIT %d',
				self::name(),
				$limit
			);
		} else {
			$sql = $wpdb->prepare(
				'SELECT id, title, starts_at, location, capacity FROM %i WHERE location = %s ORDER BY starts_at ASC LIMIT %d',
				self::name(),
				$location,
				$limit
			);
		}

		$events = $wpdb->get_results( $sql ); // phpcs:ignore WordPress.DB.PreparedSQL.NotPrepared -- $sql comes from $wpdb->prepare() above.
		wp_cache_set( $key, $events, self::CACHE_GROUP );

		return $events;
	}

	/**
	 * Deletes the events that start before a date and time, and returns how many it deleted.
	 *
	 * @param string $datetime Local date and time, Y-m-d H:i:s.
	 */
	public static function delete_before( string $datetime ): int {
		global $wpdb;

		$deleted = (int) $wpdb->query(
			$wpdb->prepare( 'DELETE FROM %i WHERE starts_at < %s', self::name(), $datetime )
		);

		if ( $deleted ) {
			self::flush_cache();
		}
		return $deleted;
	}

	/**
	 * Marks every cached query result as outdated. Call it after each change to the table.
	 */
	private static function flush_cache(): void {
		wp_cache_set_last_changed( self::CACHE_GROUP );
	}
}

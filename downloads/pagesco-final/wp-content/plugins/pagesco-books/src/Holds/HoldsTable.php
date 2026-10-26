<?php
/**
 * The customers' holds, kept in a custom table.
 *
 * @package PagesCo\Books
 */

namespace PagesCo\Books\Holds;

use PagesCo\Books\Feature;

/**
 * Creates the {prefix}pagesco_holds table, and reads and writes its rows. No business rules here: see Holds.
 */
final class HoldsTable implements Feature {

	/**
	 * The schema version this code expects. Raise it whenever schema() changes.
	 */
	public const DB_VERSION = 1;

	/**
	 * The option that records the schema version installed in this database.
	 */
	public const VERSION_OPTION = 'pagesco_books_holds_db_version';

	/**
	 * Days after its pickup date that a hold is kept, whatever its status: holds are personal data.
	 */
	public const KEEP_DAYS = 30;

	/**
	 * Checks the schema on every request, so a plugin update creates the table without a reactivation.
	 */
	public function register(): void {
		add_action( 'init', array( $this, 'maybe_upgrade' ) );
	}

	/**
	 * The table's full name, with this site's table prefix.
	 */
	public static function name(): string {
		global $wpdb;

		return $wpdb->prefix . 'pagesco_holds';
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
			book_id bigint unsigned NOT NULL,
			user_id bigint unsigned NOT NULL,
			status varchar(20) NOT NULL DEFAULT 'waiting',
			pickup_by date NOT NULL,
			created_at datetime NOT NULL,
			PRIMARY KEY  (id),
			KEY user_status (user_id,status),
			KEY book_id (book_id)
		) {$collate};";
	}

	/**
	 * Adds a waiting hold and returns its ID (0 if the insert failed).
	 *
	 * @param int    $book_id   The book.
	 * @param int    $user_id   The customer.
	 * @param string $pickup_by The last day of pickup, Y-m-d in the site's time zone.
	 */
	public static function add( int $book_id, int $user_id, string $pickup_by ): int {
		global $wpdb;

		$inserted = $wpdb->insert(
			self::name(),
			array(
				'book_id'    => $book_id,
				'user_id'    => $user_id,
				'status'     => 'waiting',
				'pickup_by'  => $pickup_by,
				'created_at' => current_time( 'mysql', true ),
			),
			array( '%d', '%d', '%s', '%s', '%s' )
		);

		return $inserted ? (int) $wpdb->insert_id : 0;
	}

	/**
	 * One hold, or null.
	 *
	 * @param int $hold_id The hold's ID.
	 */
	public static function get( int $hold_id ): ?object {
		global $wpdb;

		return $wpdb->get_row(
			$wpdb->prepare( 'SELECT id, book_id, user_id, status, pickup_by, created_at FROM %i WHERE id = %d', self::name(), $hold_id )
		);
	}

	/**
	 * A customer's holds, newest first.
	 *
	 * @param int $user_id The customer.
	 * @return object[]
	 */
	public static function for_user( int $user_id ): array {
		global $wpdb;

		return $wpdb->get_results(
			$wpdb->prepare( 'SELECT id, book_id, user_id, status, pickup_by, created_at FROM %i WHERE user_id = %d ORDER BY id DESC', self::name(), $user_id )
		);
	}

	/**
	 * The holds still waiting at the counter, with their pickup date on or after a day, soonest first.
	 *
	 * @param string $from    Y-m-d: holds whose pickup date is before it are expired, and left out.
	 * @param int    $user_id Only this customer's holds, or 0 for everyone's.
	 * @param int    $book_id Only holds on this book, or 0 for every book.
	 * @return object[]
	 */
	public static function waiting( string $from, int $user_id = 0, int $book_id = 0 ): array {
		global $wpdb;

		// "%d = 0 OR ..." turns a filter off when its value is 0, so one prepared statement covers every case.
		return $wpdb->get_results(
			$wpdb->prepare(
				'SELECT id, book_id, user_id, status, pickup_by, created_at FROM %i
				WHERE status = %s AND pickup_by >= %s AND ( %d = 0 OR user_id = %d ) AND ( %d = 0 OR book_id = %d )
				ORDER BY pickup_by ASC, id ASC',
				self::name(),
				'waiting',
				$from,
				$user_id,
				$user_id,
				$book_id,
				$book_id
			)
		);
	}

	/**
	 * Changes a waiting hold's status, and returns whether a row changed.
	 *
	 * @param int    $hold_id The hold.
	 * @param string $status  The new status: collected or cancelled.
	 * @param int    $user_id Only if it belongs to this customer, or 0 for any customer (staff).
	 */
	public static function finish( int $hold_id, string $status, int $user_id = 0 ): bool {
		global $wpdb;

		$where = array(
			'id'     => $hold_id,
			'status' => 'waiting',
		);
		if ( $user_id ) {
			$where['user_id'] = $user_id;
		}

		return 1 === $wpdb->update( self::name(), array( 'status' => $status ), $where, array( '%s' ), array( '%d', '%s', '%d' ) );
	}

	/**
	 * Deletes the holds whose pickup date is before a day, and returns how many it deleted.
	 *
	 * @param string $date Y-m-d.
	 */
	public static function delete_before( string $date ): int {
		global $wpdb;

		return (int) $wpdb->query(
			$wpdb->prepare( 'DELETE FROM %i WHERE pickup_by < %s', self::name(), $date )
		);
	}
}

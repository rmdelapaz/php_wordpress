<?php
/**
 * The shop's daily WP-Cron job.
 *
 * @package PagesCo\Books
 */

namespace PagesCo\Books;

use PagesCo\Books\Holds\HoldsTable;
use PagesCo\Books\Supplier\Availability;

/**
 * Once a day: refresh the supplier's availability, remove events that are over, and forget old holds.
 */
final class DailySync implements Feature {

	/**
	 * The cron hook. WP-Cron fires it as an action, so the callback is added like any action.
	 */
	public const HOOK = 'pagesco_books_daily_sync';

	/**
	 * Connects the job to its hook, on every request: WP-Cron runs on whichever request finds it due.
	 */
	public function register(): void {
		add_action( self::HOOK, array( $this, 'run' ) );
	}

	/**
	 * Schedules the job once a day, from 3 a.m. tomorrow in the site's time zone. Called on activation.
	 */
	public static function schedule(): void {
		if ( wp_next_scheduled( self::HOOK ) ) {
			return;
		}

		$first = new \DateTimeImmutable( 'tomorrow 03:00', wp_timezone() );
		wp_schedule_event( $first->getTimestamp(), 'daily', self::HOOK );
	}

	/**
	 * Removes the job. Called on deactivation.
	 */
	public static function unschedule(): void {
		wp_clear_scheduled_hook( self::HOOK );
	}

	/**
	 * The job itself. It runs without a logged-in user, so it checks no capabilities and prints nothing.
	 */
	public function run(): void {
		$availability = Plugin::instance()->feature( Availability::class );
		if ( $availability instanceof Availability ) {
			$availability->refresh();
		}

		// Events that started before today are over (Lesson 5.5's promise).
		EventsTable::delete_before( wp_date( 'Y-m-d 00:00:00' ) );

		// Holds are personal data: keep them a month after their pickup date, no longer (Lesson 9.1).
		HoldsTable::delete_before( wp_date( 'Y-m-d', time() - HoldsTable::KEEP_DAYS * DAY_IN_SECONDS ) );
	}
}

<?php
/**
 * Tests of the daily WP-Cron job.
 *
 * @package PagesCo\Books
 */

namespace PagesCo\Books\Tests;

use PagesCo\Books\DailySync;
use PagesCo\Books\EventsTable;

/**
 * The job is scheduled once, at 3 a.m., and removes only events that are over.
 */
final class DailySyncTest extends \WP_UnitTestCase {

	/**
	 * Scheduling twice leaves one daily event, at 3:00 in the site's time zone.
	 */
	public function test_schedules_one_daily_event_at_three(): void {
		DailySync::unschedule();
		DailySync::schedule();
		DailySync::schedule();

		$events = 0;
		foreach ( _get_cron_array() as $hooks ) {
			$events += count( $hooks[ DailySync::HOOK ] ?? array() );
		}

		$this->assertSame( 1, $events );
		$this->assertSame( 'daily', wp_get_schedule( DailySync::HOOK ) );
		$this->assertSame( '03:00', wp_date( 'H:i', wp_next_scheduled( DailySync::HOOK ) ) );
	}

	/**
	 * The job deletes past events and keeps the ones still to come, even when the supplier is down.
	 */
	public function test_run_removes_only_past_events(): void {
		add_filter(
			'pre_http_request',
			function () {
				return new \WP_Error( 'http_request_failed', 'The supplier is down.' );
			}
		);
		EventsTable::add( 'Summer reading kickoff', '2025-06-12 18:00:00', 'Reading corner', 0 );
		EventsTable::add( 'Book club: Emma', '2099-01-14 19:00:00', 'Reading corner', 20 );

		( new DailySync() )->run();

		$titles = wp_list_pluck( EventsTable::find( 50 ), 'title' );
		$this->assertNotContains( 'Summer reading kickoff', $titles );
		$this->assertContains( 'Book club: Emma', $titles );
	}
}

<?php
/**
 * The Books > Holds screen: what is waiting behind the counter.
 *
 * @package PagesCo\Books
 */

namespace PagesCo\Books\Admin;

use PagesCo\Books\BookPostType;
use PagesCo\Books\Feature;
use PagesCo\Books\Holds\HoldActions;
use PagesCo\Books\Holds\Holds;
use PagesCo\Books\Holds\HoldsTable;

/**
 * Lists the waiting holds for staff, with a "Mark collected" button on each.
 */
final class HoldsPage implements Feature {

	/**
	 * The page's slug: edit.php?post_type=book&page=pagesco-holds.
	 */
	public const SLUG = 'pagesco-holds';

	/**
	 * Adds the page to the Books menu.
	 */
	public function register(): void {
		add_action( 'admin_menu', array( $this, 'add_page' ) );
	}

	/**
	 * Under Books, for staff only.
	 */
	public function add_page(): void {
		add_submenu_page(
			'edit.php?post_type=' . BookPostType::NAME,
			__( 'Holds waiting for pickup', 'pagesco-books' ),
			__( 'Holds', 'pagesco-books' ),
			HoldActions::STAFF_CAP,
			self::SLUG,
			array( $this, 'render' )
		);
	}

	/**
	 * Prints the table. Two queries for all the names, not two per row (Lesson 8.2).
	 */
	public function render(): void {
		if ( ! current_user_can( HoldActions::STAFF_CAP ) ) {
			return;
		}

		$holds = HoldsTable::waiting( Holds::today() );
		cache_users( wp_list_pluck( $holds, 'user_id' ) );
		_prime_post_caches( array_map( 'intval', wp_list_pluck( $holds, 'book_id' ) ), false, false );

		// The result of the last "Mark collected", from the address: only known codes have a message.
		$code    = isset( $_GET['pagesco_hold'] ) ? sanitize_key( wp_unslash( $_GET['pagesco_hold'] ) ) : ''; // phpcs:ignore WordPress.Security.NonceVerification.Recommended -- only chooses a message to show.
		$message = Holds::message( $code );
		?>
		<div class="wrap">
			<h1><?php echo esc_html( get_admin_page_title() ); ?></h1>
			<?php if ( $message ) : ?>
				<div class="notice notice-info"><p><?php echo esc_html( $message ); ?></p></div>
			<?php endif; ?>

			<?php if ( ! $holds ) : ?>
				<p><?php esc_html_e( 'No holds are waiting right now.', 'pagesco-books' ); ?></p>
			<?php else : ?>
				<table class="widefat striped">
					<thead>
						<tr>
							<th scope="col"><?php esc_html_e( 'Book', 'pagesco-books' ); ?></th>
							<th scope="col"><?php esc_html_e( 'Customer', 'pagesco-books' ); ?></th>
							<th scope="col"><?php esc_html_e( 'Pick up by', 'pagesco-books' ); ?></th>
							<th scope="col"><?php esc_html_e( 'Action', 'pagesco-books' ); ?></th>
						</tr>
					</thead>
					<tbody>
						<?php foreach ( $holds as $hold ) : ?>
							<?php $customer = get_userdata( (int) $hold->user_id ); ?>
							<tr>
								<td><?php echo esc_html( get_the_title( (int) $hold->book_id ) ); ?></td>
								<td><?php echo esc_html( $customer ? $customer->display_name . ' <' . $customer->user_email . '>' : '?' ); ?></td>
								<td><?php echo esc_html( wp_date( get_option( 'date_format' ), strtotime( $hold->pickup_by . ' 12:00:00' ) ) ); ?></td>
								<td>
									<form method="post" action="<?php echo esc_url( admin_url( 'admin-post.php' ) ); ?>">
										<?php HoldActions::print_fields( HoldActions::COLLECT, 'hold', (int) $hold->id ); ?>
										<button type="submit" class="button"><?php esc_html_e( 'Mark collected', 'pagesco-books' ); ?></button>
									</form>
								</td>
							</tr>
						<?php endforeach; ?>
					</tbody>
				</table>
			<?php endif; ?>
		</div>
		<?php
	}
}

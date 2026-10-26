<?php
/**
 * Renders the My Holds block: the logged-in customer's holds, each waiting one with a Cancel button.
 *
 * No JavaScript: the Cancel buttons are forms for admin-post.php. $attributes, $content and $block as in Lesson 6.3.
 *
 * @package PagesCo\Books
 */

defined( 'ABSPATH' ) || exit;

use PagesCo\Books\Holds\HoldActions;
use PagesCo\Books\Holds\Holds;
use PagesCo\Books\Holds\HoldsTable;

if ( ! is_user_logged_in() ) {
	printf(
		'<p %1$s><a href="%2$s">%3$s</a></p>',
		get_block_wrapper_attributes(), // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- core escapes the attributes.
		esc_url( wp_login_url( get_permalink() ) ),
		esc_html__( 'Log in to see your holds', 'pagesco-books' )
	);
	return;
}

// Only the current user's holds: the ID comes from the login, never from the address or a form.
$holds = HoldsTable::for_user( get_current_user_id() );
_prime_post_caches( array_map( 'intval', wp_list_pluck( $holds, 'book_id' ) ), false, false );

$code    = isset( $_GET['pagesco_hold'] ) ? sanitize_key( wp_unslash( $_GET['pagesco_hold'] ) ) : ''; // phpcs:ignore WordPress.Security.NonceVerification.Recommended -- only chooses a message to show.
$message = Holds::message( $code );
?>
<div <?php echo get_block_wrapper_attributes(); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- core escapes the attributes. ?>>
	<?php if ( $message ) : ?>
		<p class="wp-block-pagesco-my-holds__message" role="status"><?php echo esc_html( $message ); ?></p>
	<?php endif; ?>

	<?php if ( ! $holds ) : ?>
		<p>
			<?php esc_html_e( 'You have no holds yet.', 'pagesco-books' ); ?>
			<a href="<?php echo esc_url( home_url( '/find-a-book/' ) ); ?>"><?php esc_html_e( 'Find a book to reserve', 'pagesco-books' ); ?></a>
		</p>
	<?php else : ?>
		<ul class="wp-block-pagesco-my-holds__list">
			<?php foreach ( $holds as $hold ) : ?>
				<?php
				$book_title = get_the_title( (int) $hold->book_id );
				/* translators: %s: the book's title. */
				$cancel_label = sprintf( __( 'Cancel the hold on %s', 'pagesco-books' ), wp_strip_all_tags( $book_title ) );
				?>
				<li class="wp-block-pagesco-my-holds__hold is-<?php echo esc_attr( Holds::status( $hold ) ); ?>">
					<a href="<?php echo esc_url( get_permalink( (int) $hold->book_id ) ); ?>"><?php echo esc_html( $book_title ); ?></a>
					<span><?php echo esc_html( Holds::label( $hold ) ); ?></span>
					<?php if ( 'waiting' === Holds::status( $hold ) ) : ?>
						<form method="post" action="<?php echo esc_url( admin_url( 'admin-post.php' ) ); ?>">
							<?php HoldActions::print_fields( HoldActions::CANCEL, 'hold', (int) $hold->id ); ?>
							<button type="submit" class="wp-element-button" aria-label="<?php echo esc_attr( $cancel_label ); ?>"><?php esc_html_e( 'Cancel', 'pagesco-books' ); ?></button>
						</form>
					<?php endif; ?>
				</li>
			<?php endforeach; ?>
		</ul>
	<?php endif; ?>
</div>

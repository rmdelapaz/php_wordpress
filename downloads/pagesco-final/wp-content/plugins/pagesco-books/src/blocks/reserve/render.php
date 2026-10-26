<?php
/**
 * Renders the Reserve block on a book's page: a login link, the hold that is waiting, "sold out", or the form.
 *
 * It reads the book from the postId context, like the bindings of the single-book template (Lesson 6.3).
 * $attributes, $content and $block as in Lesson 6.3.
 *
 * @package PagesCo\Books
 */

defined( 'ABSPATH' ) || exit;

use PagesCo\Books\BookPostType;
use PagesCo\Books\Holds\HoldActions;
use PagesCo\Books\Holds\Holds;

$book_id = (int) ( $block->context['postId'] ?? 0 );
if ( ! $book_id || BookPostType::NAME !== get_post_type( $book_id ) ) {
	return;
}

// Visitors who are not logged in get a link, and cost no query: most page views are theirs (Lesson 8.2).
if ( ! is_user_logged_in() ) {
	printf(
		'<p %1$s><a href="%2$s">%3$s</a></p>',
		get_block_wrapper_attributes(), // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- core escapes the attributes.
		esc_url( wp_login_url( get_permalink( $book_id ) ) ),
		esc_html__( 'Log in to reserve this book for pickup', 'pagesco-books' )
	);
	return;
}

$hold     = ( new Holds() )->waiting_hold( $book_id, get_current_user_id() );
$in_stock = (bool) get_post_meta( $book_id, 'pagesco_in_stock', true );

if ( $hold ) {
	$message = Holds::label( $hold );
} elseif ( ! $in_stock ) {
	$message = __( 'This book is sold out, so it cannot be reserved right now.', 'pagesco-books' );
} else {
	// After the form was sent without JavaScript, the handler put its result in the address.
	$code    = isset( $_GET['pagesco_hold'] ) ? sanitize_key( wp_unslash( $_GET['pagesco_hold'] ) ) : ''; // phpcs:ignore WordPress.Security.NonceVerification.Recommended -- only chooses a message to show.
	$message = Holds::message( $code );
}

wp_interactivity_state(
	'pagesco/reserve',
	array(
		'url'   => rest_url( 'pagesco/v1/holds' ),
		'nonce' => wp_create_nonce( 'wp_rest' ),
	)
);

$context = array(
	'book'    => $book_id,
	'message' => $message,
	'busy'    => false,
	'done'    => false,
);
?>
<div
	<?php echo get_block_wrapper_attributes(); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- core escapes the attributes. ?>
	data-wp-interactive="pagesco/reserve"
	<?php echo wp_interactivity_data_wp_context( $context ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- core escapes the JSON. ?>
>
	<?php if ( ! $hold && $in_stock ) : ?>
		<form method="post" action="<?php echo esc_url( admin_url( 'admin-post.php' ) ); ?>" data-wp-on--submit="actions.reserve" data-wp-bind--hidden="context.done">
			<?php HoldActions::print_fields( HoldActions::PLACE, 'book', $book_id ); ?>
			<button type="submit" class="wp-element-button" data-wp-bind--disabled="context.busy"><?php esc_html_e( 'Reserve for pickup', 'pagesco-books' ); ?></button>
		</form>
	<?php endif; ?>
	<p class="wp-block-pagesco-reserve__message" role="status" data-wp-text="context.message"></p>
	<p><a href="<?php echo esc_url( home_url( '/my-holds/' ) ); ?>"><?php esc_html_e( 'See your holds', 'pagesco-books' ); ?></a></p>
</div>

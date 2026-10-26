<?php
/**
 * Title: Call to action: book club
 * Slug: pagesco/call-to-action
 * Categories: pagesco, call-to-action
 * Keywords: book club, events, join
 * Description: An ink-colored band inviting readers to the Thursday book club.
 * Viewport Width: 1200
 *
 * @package pagesco
 */

?>
<!-- wp:group {"align":"full","className":"is-style-section-ink","style":{"spacing":{"padding":{"top":"var:preset|spacing|medium","bottom":"var:preset|spacing|medium"}}},"layout":{"type":"constrained"}} -->
<div class="wp-block-group alignfull is-style-section-ink" style="padding-top:var(--wp--preset--spacing--medium);padding-bottom:var(--wp--preset--spacing--medium)">
	<!-- wp:heading -->
	<h2 class="wp-block-heading"><?php esc_html_e( 'Join the Thursday book club', 'pagesco' ); ?></h2>
	<!-- /wp:heading -->

	<!-- wp:paragraph -->
	<p><?php esc_html_e( 'We meet at 7 p.m. in the reading corner. Everyone is welcome, and the first coffee is on us.', 'pagesco' ); ?></p>
	<!-- /wp:paragraph -->

	<!-- wp:buttons -->
	<div class="wp-block-buttons">
		<!-- wp:button -->
		<div class="wp-block-button"><a class="wp-block-button__link wp-element-button" href="<?php echo esc_url( home_url( '/events/' ) ); ?>"><?php esc_html_e( 'See all events', 'pagesco' ); ?></a></div>
		<!-- /wp:button -->
	</div>
	<!-- /wp:buttons -->
</div>
<!-- /wp:group -->

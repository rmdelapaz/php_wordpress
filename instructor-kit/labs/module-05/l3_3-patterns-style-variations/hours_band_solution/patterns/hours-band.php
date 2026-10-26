<?php
/**
 * Title: Visit the shop: hours band
 * Slug: pagesco-lab-hours/hours-band
 * Categories: contact
 * Keywords: hours, address, visit
 * Description: A sage band with the shop's address and a button to the Contact page.
 *
 * Session 5 lab (Lesson 3.3), the reference solution.
 *
 * @package pagesco-lab-hours
 */

?>
<!-- wp:group {"align":"full","className":"is-style-section-sage","layout":{"type":"constrained"}} -->
<div class="wp-block-group alignfull is-style-section-sage">
	<!-- wp:heading -->
	<h2 class="wp-block-heading"><?php esc_html_e( 'Visit the shop', 'pagesco-lab-hours' ); ?></h2>
	<!-- /wp:heading -->

	<!-- wp:paragraph -->
	<p><?php esc_html_e( '12 Market Street, open late on Thursdays.', 'pagesco-lab-hours' ); ?></p>
	<!-- /wp:paragraph -->

	<!-- wp:buttons -->
	<div class="wp-block-buttons">
		<!-- wp:button -->
		<div class="wp-block-button"><a class="wp-block-button__link wp-element-button" href="<?php echo esc_url( home_url( '/contact/' ) ); ?>"><?php esc_html_e( 'Plan your visit', 'pagesco-lab-hours' ); ?></a></div>
		<!-- /wp:button -->
	</div>
	<!-- /wp:buttons -->
</div>
<!-- /wp:group -->

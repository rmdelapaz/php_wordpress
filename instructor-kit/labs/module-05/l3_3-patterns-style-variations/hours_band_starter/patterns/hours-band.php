<?php
/**
 * Title: Visit the shop: hours band
 * Slug: pagesco-lab-hours/hours-band
 *
 * Session 5 lab (Lesson 3.3): a sage band with the shop's address and a button to the Contact page.
 * It works, but it is not finished as a pattern. Fix it in five steps, running the test after each:
 *
 * TODO 1: add a Categories: line, so the inserter files it under the core "contact" category.
 * TODO 2: add a Keywords: line (hours, address, visit) and a Description: line (one sentence).
 * TODO 3: make the heading translatable: esc_html_e( '...', 'pagesco-lab-hours' ), the CHILD theme's text domain.
 * TODO 4: the same for the paragraph and the button text.
 * TODO 5: the button's link is hard-coded to this computer. Build it with home_url( '/contact/' ), escaped with
 *         esc_url(), so it works on the live site too.
 *
 * @package pagesco-lab-hours
 */

?>
<!-- wp:group {"align":"full","className":"is-style-section-sage","layout":{"type":"constrained"}} -->
<div class="wp-block-group alignfull is-style-section-sage">
	<!-- wp:heading -->
	<h2 class="wp-block-heading">Visit the shop</h2>
	<!-- /wp:heading -->

	<!-- wp:paragraph -->
	<p>12 Market Street, open late on Thursdays.</p>
	<!-- /wp:paragraph -->

	<!-- wp:buttons -->
	<div class="wp-block-buttons">
		<!-- wp:button -->
		<div class="wp-block-button"><a class="wp-block-button__link wp-element-button" href="http://localhost:8080/contact/">Plan your visit</a></div>
		<!-- /wp:button -->
	</div>
	<!-- /wp:buttons -->
</div>
<!-- /wp:group -->

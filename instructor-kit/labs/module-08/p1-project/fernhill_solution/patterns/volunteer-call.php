<?php
/**
 * Title: Call to action: volunteer
 * Slug: fernhill/volunteer-call
 * Categories: fernhill, call-to-action
 * Keywords: volunteer, workday, join
 * Description: A green band inviting neighbors to the Saturday workdays.
 * Viewport Width: 1200
 *
 * @package fernhill
 */

?>
<!-- wp:group {"align":"full","style":{"spacing":{"padding":{"top":"2.5rem","bottom":"2.5rem"}},"elements":{"link":{"color":{"text":"var:preset|color|base"}}}},"backgroundColor":"primary","textColor":"base","layout":{"type":"constrained"}} -->
<div class="wp-block-group alignfull has-base-color has-primary-background-color has-text-color has-background has-link-color" style="padding-top:2.5rem;padding-bottom:2.5rem">
	<!-- wp:heading -->
	<h2 class="wp-block-heading"><?php esc_html_e( 'Volunteer on Saturday mornings', 'fernhill' ); ?></h2>
	<!-- /wp:heading -->

	<!-- wp:paragraph -->
	<p><?php esc_html_e( 'Bring gloves and a friend. We start at 9 a.m. at the tool shed, and there is always tea.', 'fernhill' ); ?></p>
	<!-- /wp:paragraph -->

	<!-- wp:buttons -->
	<div class="wp-block-buttons">
		<!-- wp:button {"backgroundColor":"accent","textColor":"base"} -->
		<div class="wp-block-button"><a class="wp-block-button__link has-base-color has-accent-background-color has-text-color has-background wp-element-button" href="<?php echo esc_url( home_url( '/contact/' ) ); ?>"><?php esc_html_e( 'Sign up for a workday', 'fernhill' ); ?></a></div>
		<!-- /wp:button -->
	</div>
	<!-- /wp:buttons -->
</div>
<!-- /wp:group -->

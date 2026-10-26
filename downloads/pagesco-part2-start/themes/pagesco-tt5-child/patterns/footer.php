<?php
/**
 * Title: Footer
 * Slug: twentytwentyfive/footer
 * Categories: footer
 * Block Types: core/template-part/footer
 * Description: The Pages & Co. footer: address and contact.
 *
 * @package pagesco-tt5-child
 */

?>
<!-- wp:group {"align":"full","style":{"spacing":{"padding":{"top":"var:preset|spacing|50","bottom":"var:preset|spacing|50"}}},"backgroundColor":"accent-1","layout":{"type":"constrained"}} -->
<div class="wp-block-group alignfull has-accent-1-background-color has-background" style="padding-top:var(--wp--preset--spacing--50);padding-bottom:var(--wp--preset--spacing--50)">
	<!-- wp:site-title {"level":0} /-->

	<!-- wp:paragraph {"fontSize":"small"} -->
	<p class="has-small-font-size"><?php esc_html_e( '12 Market Street · 555-0142 · Open Monday to Saturday', 'pagesco-tt5-child' ); ?></p>
	<!-- /wp:paragraph -->
</div>
<!-- /wp:group -->

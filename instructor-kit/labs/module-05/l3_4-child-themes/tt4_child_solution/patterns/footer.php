<?php
/**
 * Title: Footer: the reading corner
 * Slug: twentytwentyfour/footer
 * Categories: footer
 * Block Types: core/template-part/footer
 * Description: The shop's address and opening line, on Twenty Twenty-Four's spacing presets.
 *
 * @package pagesco-lab-tt4-child
 */

?>
<!-- wp:group {"style":{"spacing":{"padding":{"top":"var:preset|spacing|50","bottom":"var:preset|spacing|50"}}},"layout":{"type":"constrained"}} -->
<div class="wp-block-group" style="padding-top:var(--wp--preset--spacing--50);padding-bottom:var(--wp--preset--spacing--50)">
	<!-- wp:paragraph {"fontSize":"small"} -->
	<p class="has-small-font-size"><?php esc_html_e( 'The reading corner at Pages & Co. · 12 Market Street', 'pagesco-lab-tt4-child' ); ?></p>
	<!-- /wp:paragraph -->
</div>
<!-- /wp:group -->

<?php
/**
 * Title: Hero: welcome to the shop
 * Slug: pagesco/hero
 * Categories: pagesco, banner, featured
 * Keywords: hero, welcome, intro
 * Description: A full-width welcome with the page heading, a short text, two buttons and a book image.
 * Viewport Width: 1200
 * Post Types: wp_template
 * Template Types: front-page
 *
 * @package pagesco
 */

?>
<!-- wp:group {"align":"full","className":"is-style-section-sage","style":{"spacing":{"padding":{"top":"var:preset|spacing|large","bottom":"var:preset|spacing|large"}}},"layout":{"type":"constrained"}} -->
<div class="wp-block-group alignfull is-style-section-sage" style="padding-top:var(--wp--preset--spacing--large);padding-bottom:var(--wp--preset--spacing--large)">
	<!-- wp:columns {"verticalAlignment":"center","align":"wide"} -->
	<div class="wp-block-columns alignwide are-vertically-aligned-center">
		<!-- wp:column {"verticalAlignment":"center","width":"60%"} -->
		<div class="wp-block-column is-vertically-aligned-center" style="flex-basis:60%">
			<!-- wp:heading {"level":1} -->
			<h1 class="wp-block-heading"><?php esc_html_e( 'Good books, good company', 'pagesco' ); ?></h1>
			<!-- /wp:heading -->

			<!-- wp:paragraph -->
			<p><?php esc_html_e( 'An independent bookstore with a big reading corner, a small café and staff who love to talk about books. Open late on Thursdays.', 'pagesco' ); ?></p>
			<!-- /wp:paragraph -->

			<!-- wp:buttons -->
			<div class="wp-block-buttons">
				<!-- wp:button -->
				<div class="wp-block-button"><a class="wp-block-button__link wp-element-button" href="<?php echo esc_url( home_url( '/events/' ) ); ?>"><?php esc_html_e( 'See what is on', 'pagesco' ); ?></a></div>
				<!-- /wp:button -->

				<!-- wp:button {"className":"is-style-outline"} -->
				<div class="wp-block-button is-style-outline"><a class="wp-block-button__link wp-element-button" href="<?php echo esc_url( home_url( '/about/' ) ); ?>"><?php esc_html_e( 'About the shop', 'pagesco' ); ?></a></div>
				<!-- /wp:button -->
			</div>
			<!-- /wp:buttons -->
		</div>
		<!-- /wp:column -->

		<!-- wp:column {"verticalAlignment":"center","width":"40%"} -->
		<div class="wp-block-column is-vertically-aligned-center" style="flex-basis:40%">
			<!-- wp:image {"width":"280px","sizeSlug":"full","linkDestination":"none","align":"center"} -->
			<figure class="wp-block-image aligncenter size-full is-resized"><img src="<?php echo esc_url( get_theme_file_uri( 'assets/images/book-image.webp' ) ); ?>" alt="<?php esc_attr_e( 'A hardcover book with a black-and-white photo on its cover', 'pagesco' ); ?>" style="width:280px"/></figure>
			<!-- /wp:image -->
		</div>
		<!-- /wp:column -->
	</div>
	<!-- /wp:columns -->
</div>
<!-- /wp:group -->

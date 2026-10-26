<?php
/**
 * Title: Hero: welcome to the garden
 * Slug: fernhill/hero
 * Categories: banner
 * Keywords: hero, welcome, garden
 * Description: A full-width welcome with the page heading, a short text, a button and a leaf drawing.
 * Viewport Width: 1200
 * Post Types: wp_template
 * Template Types: front-page
 *
 * TODO R3: add the theme's own category (fernhill) to Categories, then register it in functions.php (R5).
 * TODO R3: the paragraph and the button text are still plain English: make them translatable and escaped like the
 *          heading (esc_html_e with the fernhill text domain); the image's alt text needs esc_attr_e.
 *
 * @package fernhill
 */

?>
<!-- wp:group {"align":"full","style":{"spacing":{"padding":{"top":"3rem","bottom":"3rem"}}},"backgroundColor":"secondary","layout":{"type":"constrained"}} -->
<div class="wp-block-group alignfull has-secondary-background-color has-background" style="padding-top:3rem;padding-bottom:3rem">
	<!-- wp:columns {"verticalAlignment":"center","align":"wide"} -->
	<div class="wp-block-columns alignwide are-vertically-aligned-center">
		<!-- wp:column {"verticalAlignment":"center","width":"65%"} -->
		<div class="wp-block-column is-vertically-aligned-center" style="flex-basis:65%">
			<!-- wp:heading {"level":1} -->
			<h1 class="wp-block-heading"><?php esc_html_e( 'Grow food, grow friendships', 'fernhill' ); ?></h1>
			<!-- /wp:heading -->

			<!-- wp:paragraph -->
			<p>Forty raised beds, a tool shed and a compost corner, looked after by neighbors of every age. No experience needed.</p>
			<!-- /wp:paragraph -->

			<!-- wp:buttons -->
			<div class="wp-block-buttons">
				<!-- wp:button -->
				<div class="wp-block-button"><a class="wp-block-button__link wp-element-button" href="<?php echo esc_url( home_url( '/about/' ) ); ?>">About the garden</a></div>
				<!-- /wp:button -->
			</div>
			<!-- /wp:buttons -->
		</div>
		<!-- /wp:column -->

		<!-- wp:column {"verticalAlignment":"center","width":"35%"} -->
		<div class="wp-block-column is-vertically-aligned-center" style="flex-basis:35%">
			<!-- wp:image {"width":"200px","sizeSlug":"full","linkDestination":"none","align":"center"} -->
			<figure class="wp-block-image aligncenter size-full is-resized"><img src="<?php echo esc_url( get_theme_file_uri( 'assets/images/leaf.svg' ) ); ?>" alt="A green leaf drawn in a few lines" style="width:200px"/></figure>
			<!-- /wp:image -->
		</div>
		<!-- /wp:column -->
	</div>
	<!-- /wp:columns -->
</div>
<!-- /wp:group -->

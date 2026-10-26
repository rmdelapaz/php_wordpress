<?php
/**
 * A single post or page.
 *
 * @package brightwater
 */

get_header();
while ( have_posts() ) {
	the_post();
	?>
	<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
		<h1 class="entry-title"><?php the_title(); ?></h1>
		<?php the_content(); ?>
	</article>
	<?php
	if ( is_singular( 'post' ) ) {
		get_template_part( 'template-parts/related-news' );
		the_post_navigation();
	}
}
get_footer();

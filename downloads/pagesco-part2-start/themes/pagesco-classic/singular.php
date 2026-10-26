<?php
/**
 * A single post or page.
 *
 * @package pagesco-classic
 */

get_header();

while ( have_posts() ) {
	the_post();
	?>
	<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
		<?php the_title( '<h1 class="entry-title">', '</h1>' ); ?>
		<?php if ( is_singular( 'post' ) ) : ?>
			<p class="entry-meta">
				<?php
				printf(
					/* translators: 1: publish date, 2: author name. */
					esc_html__( '%1$s by %2$s', 'pagesco-classic' ),
					'<time datetime="' . esc_attr( get_the_date( 'c' ) ) . '">' . esc_html( get_the_date() ) . '</time>',
					esc_html( get_the_author() )
				);
				?>
			</p>
		<?php endif; ?>
		<div class="entry-content">
			<?php the_content(); ?>
		</div>
		<?php if ( is_singular( 'post' ) && has_category() ) : ?>
			<p class="entry-terms"><?php esc_html_e( 'Filed under:', 'pagesco-classic' ); ?> <?php the_category( ', ' ); ?></p>
		<?php endif; ?>
	</article>
	<?php
	if ( is_singular( 'post' ) ) {
		get_template_part( 'template-parts/related-posts' );
		the_post_navigation();
	}
}

get_footer();

<?php
/**
 * One post in a list: title, date and author, excerpt.
 *
 * @package pagesco-classic
 */

$pagesco_classic_level = isset( $args['heading_level'] ) ? absint( $args['heading_level'] ) : 2;
?>
<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
	<?php the_title( '<h' . $pagesco_classic_level . ' class="entry-title"><a href="' . esc_url( get_permalink() ) . '">', '</a></h' . $pagesco_classic_level . '>' ); ?>
	<?php if ( 'post' === get_post_type() ) : ?>
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
	<div class="entry-summary">
		<?php the_excerpt(); ?>
	</div>
</article>

<?php
/**
 * Up to two other posts from the current post's categories.
 *
 * @package pagesco-classic
 */

$pagesco_classic_related = new WP_Query(
	array(
		'category__in'        => wp_get_post_categories( get_the_ID() ),
		'post__not_in'        => array( get_the_ID() ),
		'posts_per_page'      => 2,
		'ignore_sticky_posts' => true,
		'no_found_rows'       => true,
	)
);

if ( $pagesco_classic_related->have_posts() ) :
	?>
	<aside class="related-posts">
		<h2><?php esc_html_e( 'More from the shop', 'pagesco-classic' ); ?></h2>
		<ul>
			<?php
			while ( $pagesco_classic_related->have_posts() ) {
				$pagesco_classic_related->the_post();
				the_title( '<li><a href="' . esc_url( get_permalink() ) . '">', '</a></li>' );
			}
			?>
		</ul>
	</aside>
	<?php
endif;

wp_reset_postdata();

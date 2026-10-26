<?php
/**
 * Two other posts from the News category, below a single post.
 *
 * @package brightwater
 */

$brightwater_related = new WP_Query(
	array(
		'category_name'       => 'news',
		'posts_per_page'      => 2,
		'post__not_in'        => array( get_the_ID() ),
		'ignore_sticky_posts' => true,
		'no_found_rows'       => true,
	)
);

if ( $brightwater_related->have_posts() ) {
	?>
	<aside class="related-news">
		<h2><?php esc_html_e( 'More news', 'brightwater' ); ?></h2>
		<ul>
			<?php
			while ( $brightwater_related->have_posts() ) {
				$brightwater_related->the_post();
				?>
				<li><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></li>
				<?php
			}
			?>
		</ul>
	</aside>
	<?php
	wp_reset_postdata();
}

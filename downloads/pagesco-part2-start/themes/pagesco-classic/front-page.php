<?php
/**
 * The front page: a welcome, the shop's pages, and the latest news.
 *
 * @package pagesco-classic
 */

get_header();

if ( ! is_paged() ) :
	?>
	<section class="hero">
		<h1><?php esc_html_e( 'Good books, good company', 'pagesco-classic' ); ?></h1>
		<p><?php esc_html_e( 'An independent bookstore with a big reading corner, a small café and staff who love to talk about books. Open late on Thursdays.', 'pagesco-classic' ); ?></p>
	</section>

	<?php
	$pagesco_classic_pages = new WP_Query(
		array(
			'post_type'     => 'page',
			'post_name__in' => array( 'about', 'events', 'contact' ),
			'orderby'       => 'post_name__in',
			'no_found_rows' => true,
		)
	);

	if ( $pagesco_classic_pages->have_posts() ) :
		?>
		<section class="visit-us">
			<h2><?php esc_html_e( 'Visit us', 'pagesco-classic' ); ?></h2>
			<ul>
				<?php
				while ( $pagesco_classic_pages->have_posts() ) {
					$pagesco_classic_pages->the_post();
					the_title( '<li><a href="' . esc_url( get_permalink() ) . '">', '</a></li>' );
				}
				?>
			</ul>
		</section>
		<?php
	endif;
	wp_reset_postdata();
endif;
?>

<section class="latest-news">
	<?php if ( is_paged() ) : ?>
		<h1><?php esc_html_e( 'News from the shop', 'pagesco-classic' ); ?></h1>
	<?php else : ?>
		<h2><?php esc_html_e( 'News from the shop', 'pagesco-classic' ); ?></h2>
	<?php endif; ?>

	<?php
	while ( have_posts() ) {
		the_post();
		get_template_part( 'template-parts/content', null, array( 'heading_level' => 3 ) );
	}

	the_posts_pagination();
	?>
</section>
<?php
get_footer();

<?php
/**
 * The main template: the blog home, archives and search results.
 *
 * @package pagesco-classic
 */

get_header();
?>
<header class="page-header">
	<?php if ( is_home() ) : ?>
		<h1><?php esc_html_e( 'News from the shop', 'pagesco-classic' ); ?></h1>
	<?php elseif ( is_search() ) : ?>
		<h1><?php /* translators: %s: the search terms. */ printf( esc_html__( 'Search results for: %s', 'pagesco-classic' ), esc_html( get_search_query( false ) ) ); ?></h1>
	<?php else : ?>
		<?php the_archive_title( '<h1>', '</h1>' ); ?>
		<?php the_archive_description( '<div class="archive-description">', '</div>' ); ?>
	<?php endif; ?>
</header>

<?php
if ( have_posts() ) {
	while ( have_posts() ) {
		the_post();
		get_template_part( 'template-parts/content' );
	}

	the_posts_pagination();
} else {
	get_template_part( 'template-parts/content', 'none' );
}

get_footer();

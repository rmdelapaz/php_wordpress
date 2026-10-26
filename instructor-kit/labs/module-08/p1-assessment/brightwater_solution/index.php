<?php
/**
 * The main template: the blog home and every list of posts.
 *
 * @package brightwater
 */

get_header();
?>
<h1><?php esc_html_e( 'News from the pool', 'brightwater' ); ?></h1>
<?php
if ( have_posts() ) {
	while ( have_posts() ) {
		the_post();
		?>
		<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
			<h2 class="entry-title"><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
			<p class="entry-meta"><?php echo esc_html( get_the_date() ); ?></p>
			<?php the_excerpt(); ?>
		</article>
		<?php
	}
	the_posts_pagination();
} else {
	?>
	<p><?php esc_html_e( 'No news yet.', 'brightwater' ); ?></p>
	<?php
}
get_footer();

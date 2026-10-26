<?php
/**
 * Search results.
 *
 * @package brightwater
 */

get_header();
?>
<h1 class="search-title">
	<?php
	/* translators: %s: the search term. */
	printf( esc_html__( 'Results for: %s', 'brightwater' ), esc_html( get_search_query( false ) ) );
	?>
</h1>
<?php
if ( have_posts() ) {
	while ( have_posts() ) {
		the_post();
		?>
		<h2 class="entry-title"><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
		<?php
	}
} else {
	?>
	<p><?php esc_html_e( 'Nothing matched. Try another word.', 'brightwater' ); ?></p>
	<?php
}
get_footer();

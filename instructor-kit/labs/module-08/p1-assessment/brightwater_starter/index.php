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
		// TODO T3: an <article> with the post's id and classes, an h2 "entry-title" whose link goes to the post,
		//         the date in a p "entry-meta", the excerpt. Then, after the loop, the pagination links.
		the_title( '<p>', '</p>' );
	}
} else {
	?>
	<p><?php esc_html_e( 'No news yet.', 'brightwater' ); ?></p>
	<?php
}
get_footer();

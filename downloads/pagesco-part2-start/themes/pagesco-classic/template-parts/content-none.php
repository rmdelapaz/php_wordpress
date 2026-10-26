<?php
/**
 * Shown when a list has no posts.
 *
 * @package pagesco-classic
 */

?>
<section class="no-results">
	<?php if ( is_search() ) : ?>
		<p><?php esc_html_e( 'No books or posts matched your search. Try another word.', 'pagesco-classic' ); ?></p>
		<?php get_search_form(); ?>
	<?php else : ?>
		<p><?php esc_html_e( 'Nothing here yet.', 'pagesco-classic' ); ?></p>
	<?php endif; ?>
</section>

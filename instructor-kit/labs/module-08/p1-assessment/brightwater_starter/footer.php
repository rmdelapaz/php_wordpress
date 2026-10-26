<?php
/**
 * The footer: the end of the main content and the bottom of every page.
 *
 * @package brightwater
 */

?>
</main>
<footer class="site-footer">
	<?php if ( is_active_sidebar( 'footer' ) ) : ?>
		<div class="footer-widgets">
			<?php dynamic_sidebar( 'footer' ); ?>
		</div>
	<?php endif; ?>
	<p><?php esc_html_e( 'Brightwater Swim School · 7 Pier Road · 555-0163', 'brightwater' ); ?></p>
</footer>
<?php wp_footer(); ?>
</body>
</html>

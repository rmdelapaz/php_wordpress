<?php
/**
 * The footer: the end of the main content and the bottom of every page.
 *
 * @package pagesco-classic
 */

?>
</main>
<footer class="site-footer">
	<?php if ( is_active_sidebar( 'footer' ) ) : ?>
		<div class="footer-widgets">
			<?php dynamic_sidebar( 'footer' ); ?>
		</div>
	<?php endif; ?>
	<p><?php esc_html_e( 'Pages & Co. · 12 Market Street · 555-0142', 'pagesco-classic' ); ?></p>
</footer>
<?php wp_footer(); ?>
</body>
</html>

<?php
/**
 * The footer (done for you).
 *
 * @package pagesco-lab-corner
 */

?>
</main>
<footer class="corner-footer">
	<?php if ( is_active_sidebar( 'corner-footer' ) ) : ?>
		<?php dynamic_sidebar( 'corner-footer' ); ?>
	<?php endif; ?>
	<p><?php esc_html_e( 'The reading corner at Pages & Co.', 'pagesco-lab-corner' ); ?></p>
</footer>
<?php wp_footer(); ?>
</body>
</html>

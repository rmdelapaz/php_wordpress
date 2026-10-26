<?php
/**
 * The "not found" page.
 *
 * @package pagesco-classic
 */

get_header();
?>
<h1><?php esc_html_e( 'This page is not on our shelves', 'pagesco-classic' ); ?></h1>
<p><?php esc_html_e( 'The page you asked for does not exist, or it has moved. Try a search:', 'pagesco-classic' ); ?></p>
<?php
get_search_form();

get_footer();

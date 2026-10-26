<?php
/**
 * Not found.
 *
 * @package brightwater
 */

get_header();
?>
<h1><?php esc_html_e( 'This lane is closed', 'brightwater' ); ?></h1>
<p><?php esc_html_e( 'The page you asked for is not here. Try a search:', 'brightwater' ); ?></p>
<?php
get_search_form();
get_footer();

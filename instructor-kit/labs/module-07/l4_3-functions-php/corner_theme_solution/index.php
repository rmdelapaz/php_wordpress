<?php
/**
 * The only template (done for you).
 *
 * @package pagesco-lab-corner
 */

get_header();
while ( have_posts() ) {
	the_post();
	the_title( '<h2><a href="' . esc_url( get_permalink() ) . '">', '</a></h2>' );
}
get_footer();

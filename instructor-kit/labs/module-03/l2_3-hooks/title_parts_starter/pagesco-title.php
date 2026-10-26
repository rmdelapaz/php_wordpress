<?php
/**
 * Plugin Name: Pages & Co. Page Titles (Session 3 lab)
 * Description: A tagline in the browser tab of the home page, and "News:" before the titles of news posts.
 *
 * Install it as a must-use plugin: copy this file into wordpress/wp-content/mu-plugins/. WordPress builds the
 * <title> from an array of parts (title, page, tagline, site) and passes that array through the filter
 * document_title_parts (wp-includes/general-template.php) before it joins the parts with the separator.
 */

function pagesco_lab_title_parts( $parts ) {
	if ( is_front_page() ) {
		// TODO 1: the front page's tagline part should say 'Independent bookstore since 1998'.
		$parts['tagline'] = 'TODO';
	}

	// TODO 2: on a single post filed in the News category (is_single() and in_category( 'news' )), put
	//         'News: ' in front of the title part ($parts['title']). Other posts and all pages stay as they are.

	// TODO 3: a filter must return the value it was given (changed or not). Check that EVERY path does.
	return $parts;
}
add_filter( 'document_title_parts', 'pagesco_lab_title_parts' );

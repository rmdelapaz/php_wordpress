<?php
/**
 * Plugin Name: Pages & Co. Page Titles (Session 3 lab, solution)
 * Description: A tagline in the browser tab of the home page, and "News:" before the titles of news posts.
 */

function pagesco_lab_title_parts( $parts ) {
	if ( is_front_page() ) {
		$parts['tagline'] = 'Independent bookstore since 1998';
	}

	if ( is_single() && in_category( 'news' ) ) {
		$parts['title'] = 'News: ' . $parts['title'];
	}

	return $parts;
}
add_filter( 'document_title_parts', 'pagesco_lab_title_parts' );

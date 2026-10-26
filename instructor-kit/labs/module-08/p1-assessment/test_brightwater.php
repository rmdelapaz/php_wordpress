<?php
/**
 * test_brightwater.php: the self-check of the Part 1 assessment, the Brightwater classic theme (Session 8).
 *
 * serve: brightwater
 * install: theme brightwater
 * state: after:lesson_13
 * expect-starter: Checks passed: 2 of 10
 * expect-solution: Checks passed: 10 of 10
 *
 * Run it as often as you like during the assessment: it requests your pages the way a browser does and prints OK
 * or TODO per task of BRIEF.md. It is a help, not the score. From your project folder, with the theme in
 * wordpress/wp-content/themes/brightwater/ and active (wp theme activate brightwater):
 *     cp labs/module-08/p1-assessment/test_brightwater.php wordpress/
 *     wp eval-file --use-include test_brightwater.php
 * It puts the course's "Main menu" into the theme's primary location for its own requests and takes it out again.
 * When you hand in: rm wordpress/test_brightwater.php and wp theme activate pagesco.
 */

$pagesco_results = array();
$pagesco_theme   = wp_get_theme();
$pagesco_get     = function ( $path ) {
	$response = wp_remote_get( home_url( $path ), array( 'timeout' => 30 ) );
	return array( (int) wp_remote_retrieve_response_code( $response ), (string) wp_remote_retrieve_body( $response ) );
};

// The menu: the course site's "Main menu" in the theme's primary location, for the test's requests only.
$pagesco_locations = get_theme_mod( 'nav_menu_locations', array() );
$pagesco_menu      = wp_get_nav_menu_object( 'Main menu' );
set_theme_mod( 'nav_menu_locations', array( 'primary' => $pagesco_menu ? $pagesco_menu->term_id : 0 ) );

list( , $pagesco_home )       = $pagesco_get( '/' );
list( $pagesco_code2, $pagesco_page2 ) = $pagesco_get( '/page/2/' );
list( , $pagesco_search )     = $pagesco_get( '/?s=' . rawurlencode( '<b>water</b>' ) );
list( , $pagesco_single )     = $pagesco_get( '/book-club-dune/' );

set_theme_mod( 'nav_menu_locations', $pagesco_locations );

// 1 The theme itself.
$pagesco_results[] = array(
	'Brightwater' === $pagesco_theme->get( 'Name' ) && 'brightwater' === $pagesco_theme->get( 'TextDomain' ) && ! wp_is_block_theme(),
	'A classic theme: Brightwater, text domain brightwater',
);

// 2 T1 The title: WordPress prints it (title-tag), the header no longer does.
$pagesco_results[] = array(
	current_theme_supports( 'title-tag' ) && 1 === substr_count( $pagesco_home, '<title' ),
	'T1 Title: title-tag support, exactly one <title> (now: ' . substr_count( $pagesco_home, '<title' ) . ')',
);

// 3 T1 wp_body_open(): the course's must-use plugin prints its notice band there.
$pagesco_results[] = array(
	str_contains( $pagesco_home, '<div class="pagesco-notice"' ),
	'T1 wp_body_open(): the store notice band from mu-plugins/pagesco-site.php appears',
);

// 4 T2 The stylesheet.
$pagesco_results[] = array(
	str_contains( $pagesco_home, "id='brightwater-style-css'" ) && str_contains( $pagesco_home, 'brightwater/style.css?ver=1.0.0' ),
	'T2 Stylesheet: brightwater-style, style.css?ver=1.0.0',
);

// 5 T1 The menu location.
$pagesco_results[] = array(
	1 === preg_match( '#<nav class="site-nav"[^>]*>.*?>About Us</a>.*?</nav>#s', $pagesco_home ),
	'T1 Menu: the primary location shows About Us, Events, Contact in the header nav',
);

// 6 T3 The Loop on the blog home: two posts, linked titles, pagination.
$pagesco_articles  = preg_match_all( '#<article id="post-\d+"#', $pagesco_home );
$pagesco_links     = preg_match_all( '#<h2 class="entry-title"><a href="' . preg_quote( home_url( '/' ), '#' ) . '[^"]+/">#', $pagesco_home );
$pagesco_results[] = array(
	2 === $pagesco_articles && 2 === $pagesco_links && str_contains( $pagesco_home, 'href="' . home_url( '/page/2/' ) . '"' ),
	"T3 Blog home: 2 posts with linked h2 titles, a link to page 2 (now: {$pagesco_articles} posts, {$pagesco_links} linked titles)",
);

// 7 T3 Page 2.
$pagesco_results[] = array(
	200 === $pagesco_code2 && 2 === preg_match_all( '#<article id="post-\d+"#', $pagesco_page2 ),
	'T3 /page/2/: status 200 and the other 2 posts',
);

// 8 T4 The search term, escaped.
$pagesco_results[] = array(
	str_contains( $pagesco_search, 'Results for: &lt;b&gt;water&lt;/b&gt;' ) && ! str_contains( $pagesco_search, '<b>water</b>' ),
	'T4 Search: the term is printed as text (&lt;b&gt;), never as HTML',
);

// 9 T5 Related news under a post.
$pagesco_results[] = array(
	1 === preg_match( '#<aside class="related-news">.*Staff picks for the season.*Welcome to the new Pages &(?:amp|\#038); Co\. website.*</aside>#s', $pagesco_single ),
	'T5 Related news on /book-club-dune/: Staff picks, then Welcome',
);

// 10 T5 Post navigation after the related loop: Dune's own neighbors.
$pagesco_results[] = array(
	1 === preg_match( '#<div class="nav-previous">.*?Staff picks for the season#s', $pagesco_single )
		&& 1 === preg_match( '#<div class="nav-next">.*?Hello world!#s', $pagesco_single ),
	'T5 Post navigation on /book-club-dune/: previous Staff picks, next Hello world!',
);

echo "Brightwater self-check (Part 1 assessment, BRIEF.md)\n";
$pagesco_passed = 0;
foreach ( $pagesco_results as $pagesco_i => $pagesco_r ) {
	$pagesco_passed += $pagesco_r[0] ? 1 : 0;
	printf( "%-4s %2d  %s\n", $pagesco_r[0] ? 'OK' : 'TODO', $pagesco_i + 1, $pagesco_r[1] );
}
printf( "Stretch: footer widget area %s\n", is_registered_sidebar( 'footer' ) ? 'registered' : 'not registered' );
echo "Checks passed: {$pagesco_passed} of " . count( $pagesco_results ) . "\n";

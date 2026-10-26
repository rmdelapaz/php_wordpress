<?php
/**
 * test_hours_band.php: asks WordPress about the hours-band pattern (Session 5, Lesson 3.3, lab A)
 * serve: hours_band
 * install: theme pagesco-lab-hours
 * state: after:lesson_08
 * expect-starter: Categories:  (none)
 * expect-starter: Button:      Plan your visit -> http://localhost:8080/contact/
 * expect-solution: Categories:  contact
 * expect-solution: Heading:     VISIT THE SHOP
 * expect-solution: Button:      PLAN YOUR VISIT -> https://pagesandco.example/contact/
 *
 * The lab folder is a tiny child theme of pagesco: copy it into your themes folder, activate it, run this test.
 * From your project folder (the starter; use hours_band_solution/ to see the reference):
 *     cp -r labs/module-05/l3_3-patterns-style-variations/hours_band_starter wordpress/wp-content/themes/pagesco-lab-hours
 *     wp theme activate pagesco-lab-hours
 *     cp labs/module-05/l3_3-patterns-style-variations/test_hours_band.php wordpress/
 *     wp eval-file --use-include test_hours_band.php
 * The test reads the pattern from WordPress's pattern registry, then renders it the way a SPANISH-speaking
 * visitor of the LIVE site would get it: a translation filter turns every string of the child's text domain into
 * capitals (a stand-in for a real translation), and home_url() pretends the site lives at pagesandco.example.
 * Text that stays lower case is not translatable; a link that still says localhost would break on the live site.
 * When you are done: wp theme activate pagesco && rm -r wordpress/wp-content/themes/pagesco-lab-hours wordpress/test_hours_band.php
 */
// The pattern file's PHP runs only when its content is first asked for (below), so these two filters are in
// place when it runs: a "translation" into capitals for the child's text domain, and a live-site address.
add_filter( 'gettext_pagesco-lab-hours', 'strtoupper' );
add_filter(
	'home_url',
	function ( $pagesco_url ) {
		return str_replace( 'http://localhost:8080', 'https://pagesandco.example', $pagesco_url );
	}
);

$pagesco_registry = WP_Block_Patterns_Registry::get_instance();
$pagesco_name     = 'pagesco-lab-hours/hours-band';
if ( ! $pagesco_registry->is_registered( $pagesco_name ) ) {
	echo "Not registered: is pagesco-lab-hours the active theme, and does the header say Slug: {$pagesco_name}?\n";
	return;
}

// What the header told WordPress (read once, when patterns are registered on init).
$pagesco_pattern = $pagesco_registry->get_registered( $pagesco_name );
printf( "%-12s %s\n", 'Title:', $pagesco_pattern['title'] );
foreach ( array( 'categories', 'keywords' ) as $pagesco_field ) {
	printf( "%-12s %s\n", ucfirst( $pagesco_field ) . ':', empty( $pagesco_pattern[ $pagesco_field ] ) ? '(none)' : implode( ', ', $pagesco_pattern[ $pagesco_field ] ) );
}
printf( "%-12s %s\n", 'Description:', empty( $pagesco_pattern['description'] ) ? '(none)' : $pagesco_pattern['description'] );


// The content: the pattern file's output, rendered with the two filters.
$pagesco_html = $pagesco_pattern['content'];
preg_match( '#<h2[^>]*>([^<]*)</h2>#', $pagesco_html, $pagesco_h2 );
preg_match( '#<p>([^<]*)</p>#', $pagesco_html, $pagesco_p );
preg_match( '#href="([^"]*)"[^>]*>([^<]*)</a>#', $pagesco_html, $pagesco_a );
printf( "%-12s %s\n", 'Heading:', $pagesco_h2[1] ?? '?' );
printf( "%-12s %s\n", 'Text:', $pagesco_p[1] ?? '?' );
printf( "%-12s %s -> %s\n", 'Button:', $pagesco_a[2] ?? '?', $pagesco_a[1] ?? '?' );

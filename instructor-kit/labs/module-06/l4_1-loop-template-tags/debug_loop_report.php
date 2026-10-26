<?php
/**
 * debug_loop_report.php: what does a search for "dune" find? (Session 6, Lesson 4.1, find-the-bug handout)
 * state: after:lesson_10
 * expect-error: Warning
 *
 * WP-CLI runs no main query, so this script runs one itself: wp( 's=dune' ) makes WordPress parse the query
 * string and run the main query exactly as it does for http://localhost:8080/?s=dune (the lesson's search). Then
 * a Loop prints one line per result. A colleague wrote it in a hurry. From your project folder:
 *     cp labs/module-06/l4_1-loop-template-tags/debug_loop_report.php wordpress/
 *     wp eval-file --use-include debug_loop_report.php
 * One bug announces itself with a Warning (read it from the left). Two are SILENT: the heading never prints
 * (in a browser request the same line would add a "called incorrectly" notice; here WP-CLI's own query object
 * answers false without one), and look at where each title lands. Fixed, it prints the heading, one "- <title> (<date>)" line per result,
 * and "2 result(s) for "dune"". When you are done: rm wordpress/debug_loop_report.php
 */
if ( is_search() ) {
	echo "Search results\n";
}

wp( 's=dune' );

$pagesco_found = 0;
while ( have_posts() ) {
	the_post();
	echo '- ' . the_title() . ' (' . esc_html( get_the_date( 'Y-m-d' ) ) . ")\n";
	++$pagesco_found;
}

printf( "%d result(s) for \"%s\"\n", $pagesco_foud, esc_html( get_search_query( false ) ) );

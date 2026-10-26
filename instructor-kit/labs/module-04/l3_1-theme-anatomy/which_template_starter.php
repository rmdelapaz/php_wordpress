<?php
/**
 * which_template_starter.php: predict which template draws a page, then let WordPress check you (Session 4, Lesson 3.1, lab A)
 * state: after:lesson_06
 * expect: tag-staff-picks
 * expect: => TODO
 *
 * Lesson 3.1's rule: WordPress builds a list of candidate templates, most specific first, and uses the FIRST one
 * the active theme has. This script does both halves for a few kinds of page on your site, with Twenty Twenty-Five
 * active. From your project folder:
 *     cp labs/module-04/l3_1-theme-anatomy/which_template_starter.php wordpress/
 *     wp eval-file --use-include which_template_starter.php
 * Before each TODO, write your prediction on paper. Then fill in the TODOs, run again and compare with "Expected
 * when done" at the end. When you are done: rm wordpress/which_template_starter.php
 */

// TODO 1: the slugs of every template the active theme offers. get_block_templates() returns objects with a
//         ->slug property; wp_list_pluck( $objects, 'slug' ) turns them into a plain array of strings.
$pagesco_have = array();

// The pages to check: the hierarchy name WordPress starts from (get_template_hierarchy() works from these).
$pagesco_pages = array(
	'/tag/staff-picks/'   => 'tag-staff-picks',
	'/author/devon/'      => 'author-devon',
	'/hello-world/'       => 'single-post-hello-world',
	'/?s=dune'            => 'search',
	// TODO 3: add two rows of your own: the front page ('front-page') and the Contact page ('page-contact').
);

foreach ( $pagesco_pages as $pagesco_url => $pagesco_slug ) {
	$pagesco_candidates = get_template_hierarchy( $pagesco_slug );   // done for you: the candidate list
	$pagesco_used       = 'TODO';
	// TODO 2: walk $pagesco_candidates in order and keep the FIRST one that is in $pagesco_have (in_array(),
	//         then break out of the loop).

	printf( "%-19s %s\n", $pagesco_url, implode( ' > ', $pagesco_candidates ) );
	printf( "%-19s => %s\n", '', $pagesco_used );
}

// Expected when done (which_template_solution.php, Twenty Twenty-Five active):
// /tag/staff-picks/   tag-staff-picks > tag > archive > index
//                     => archive
// /author/devon/      author-devon > author > archive > index
//                     => archive
// /hello-world/       single-post-hello-world > single-post > single > singular > index
//                     => single
// /?s=dune            search > index
//                     => search
// /                   front-page > home > index
//                     => home
// /contact/           page-contact > page > singular > index
//                     => page

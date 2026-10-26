<?php
/**
 * which_template_solution.php: the instructor's reference for which_template_starter.php (Session 4, Lesson 3.1, lab A)
 * state: after:lesson_06
 * expect: => home
 * expect: page-contact > page > singular > index
 */

$pagesco_have = wp_list_pluck( get_block_templates(), 'slug' );

$pagesco_pages = array(
	'/tag/staff-picks/'   => 'tag-staff-picks',
	'/author/devon/'      => 'author-devon',
	'/hello-world/'       => 'single-post-hello-world',
	'/?s=dune'            => 'search',
	'/'                   => 'front-page',
	'/contact/'           => 'page-contact',
);

foreach ( $pagesco_pages as $pagesco_url => $pagesco_slug ) {
	$pagesco_candidates = get_template_hierarchy( $pagesco_slug );
	$pagesco_used       = 'none';
	foreach ( $pagesco_candidates as $pagesco_candidate ) {
		if ( in_array( $pagesco_candidate, $pagesco_have, true ) ) {
			$pagesco_used = $pagesco_candidate;
			break;
		}
	}

	printf( "%-19s %s\n", $pagesco_url, implode( ' > ', $pagesco_candidates ) );
	printf( "%-19s => %s\n", '', $pagesco_used );
}

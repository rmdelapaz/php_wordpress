<?php
/**
 * variation_contrast_starter.php: do the shop's color pairs pass WCAG AA in every look? (Session 5, Lesson 3.3, lab B)
 * state: after:lesson_09
 * expect: Default   ink on paper      TODO
 *
 * Lesson 3.3 claims the Evening variation keeps the contrast rules of Lesson 3.2 ("about 13.5:1"). Prove it for
 * every look the theme offers, with WordPress's own data: the theme palette from the global settings and each
 * style variation from WP_Theme_JSON_Resolver. Needs the theme from the end of Lesson 3.3 (styles/evening.json).
 * From your project folder:
 *     cp labs/module-05/l3_3-patterns-style-variations/variation_contrast_starter.php wordpress/
 *     wp eval-file --use-include variation_contrast_starter.php
 * pagesco_luminance() is done for you (the WCAG formula). Do the three TODOs, run again after each, and compare
 * with "Expected when done" at the end. When you are done: rm wordpress/variation_contrast_starter.php
 */

/**
 * The relative luminance of a #rrggbb color (WCAG 2.2, the formula Lesson 3.2's contrast numbers use).
 *
 * @param string $hex A color such as #fbf8f1.
 * @return float 0 (black) to 1 (white).
 */
function pagesco_luminance( $hex ) {
	$pagesco_rgb = array_map( 'hexdec', str_split( ltrim( $hex, '#' ), 2 ) );
	$pagesco_lin = array();
	foreach ( $pagesco_rgb as $pagesco_c ) {
		$pagesco_c     = $pagesco_c / 255;
		$pagesco_lin[] = $pagesco_c <= 0.04045 ? $pagesco_c / 12.92 : ( ( $pagesco_c + 0.055 ) / 1.055 ) ** 2.4;
	}
	return 0.2126 * $pagesco_lin[0] + 0.7152 * $pagesco_lin[1] + 0.0722 * $pagesco_lin[2];
}

/**
 * The contrast ratio of two colors.
 *
 * TODO 1: return the lighter luminance plus 0.05, divided by the darker luminance plus 0.05 (max() and min()
 *         of the two pagesco_luminance() values). Until then it returns null, and the report prints TODO.
 *
 * @param string $a One color.
 * @param string $b The other.
 * @return float|null From 1 (no contrast) to 21 (black on white).
 */
function pagesco_contrast( $a, $b ) {
	return null;
}

// The theme's own palette, as slug => color: the "Default" look. (Done for you: wp_list_pluck() with a third
// argument makes an array keyed by slug.)
$pagesco_palette = wp_list_pluck( wp_get_global_settings( array( 'color', 'palette', 'theme' ) ), 'color', 'slug' );
$pagesco_looks   = array( 'Default' => $pagesco_palette );

// TODO 2: loop over WP_Theme_JSON_Resolver::get_style_variations(). For each variation that has a palette, add
//         $pagesco_looks[ <its title> ] = the theme palette with the variation's colors merged over it
//         (array_merge()). Careful: the resolver gives presets in theme.json's internal shape, keyed by origin, so
//         the list is in $variation['settings']['color']['palette']['theme']. var_dump() one variation first.

// The pairs the templates and section styles use: text color => background color.
// TODO 3: add two more pairs: ink on sage (the sage band of Lesson 3.3) and sage on paper.
$pagesco_pairs = array(
	array( 'ink', 'paper' ),
	array( 'oxblood', 'paper' ),
	array( 'slate', 'paper' ),
);
foreach ( $pagesco_looks as $pagesco_look => $pagesco_colors ) {
	foreach ( $pagesco_pairs as $pagesco_pair ) {
		$pagesco_ratio = pagesco_contrast( $pagesco_colors[ $pagesco_pair[0] ], $pagesco_colors[ $pagesco_pair[1] ] );
		if ( null === $pagesco_ratio ) {
			printf( "%-9s %-17s TODO\n", $pagesco_look, $pagesco_pair[0] . ' on ' . $pagesco_pair[1] );
			continue;
		}
		printf(
			"%-9s %-17s %4.1f:1  %s\n",
			$pagesco_look,
			$pagesco_pair[0] . ' on ' . $pagesco_pair[1],
			$pagesco_ratio,
			$pagesco_ratio >= 4.5 ? 'AA' : 'FAIL (needs 4.5)'
		);
	}
}

// Expected when done (variation_contrast_solution.php, the site at the end of Lesson 3.3):
// Default   ink on paper      13.9:1  AA
// Default   oxblood on paper   8.8:1  AA
// Default   slate on paper     5.8:1  AA
// Default   ink on sage       12.0:1  AA
// Default   sage on paper      1.2:1  FAIL (needs 4.5)
// Evening   ink on paper      13.5:1  AA
// Evening   oxblood on paper   8.3:1  AA
// Evening   slate on paper     8.4:1  AA
// Evening   ink on sage        9.7:1  AA
// Evening   sage on paper      1.4:1  FAIL (needs 4.5)

<?php
/**
 * variation_contrast_solution.php: do the shop's color pairs pass WCAG AA in every look? (Session 5, Lesson 3.3, lab B)
 * state: after:lesson_09
 * expect: Evening   ink on paper      13.5:1  AA
 *
 * The reference solution. See variation_contrast_starter.php for the task.
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
 * The contrast ratio of two colors: the lighter luminance plus 0.05, divided by the darker plus 0.05.
 *
 * @param string $a One color.
 * @param string $b The other.
 * @return float From 1 (no contrast) to 21 (black on white).
 */
function pagesco_contrast( $a, $b ) {
	$pagesco_l = array( pagesco_luminance( $a ), pagesco_luminance( $b ) );
	return ( max( $pagesco_l ) + 0.05 ) / ( min( $pagesco_l ) + 0.05 );
}

// The theme's own palette, as slug => color: the "Default" look.
$pagesco_palette = wp_list_pluck( wp_get_global_settings( array( 'color', 'palette', 'theme' ) ), 'color', 'slug' );
$pagesco_looks   = array( 'Default' => $pagesco_palette );

// Every site variation that changes the palette, merged over the theme's palette (a variation is a layer).
// The resolver hands each variation back in theme.json's internal shape: presets are keyed by their origin.
foreach ( WP_Theme_JSON_Resolver::get_style_variations() as $pagesco_variation ) {
	if ( ! empty( $pagesco_variation['settings']['color']['palette']['theme'] ) ) {
		$pagesco_own = wp_list_pluck( $pagesco_variation['settings']['color']['palette']['theme'], 'color', 'slug' );
		$pagesco_looks[ $pagesco_variation['title'] ] = array_merge( $pagesco_palette, $pagesco_own );
	}
}

// The pairs the templates and the section styles actually use: text color => background color.
$pagesco_pairs = array(
	array( 'ink', 'paper' ),
	array( 'oxblood', 'paper' ),
	array( 'slate', 'paper' ),
	array( 'ink', 'sage' ),
	array( 'sage', 'paper' ),
);
foreach ( $pagesco_looks as $pagesco_look => $pagesco_colors ) {
	foreach ( $pagesco_pairs as $pagesco_pair ) {
		$pagesco_ratio = pagesco_contrast( $pagesco_colors[ $pagesco_pair[0] ], $pagesco_colors[ $pagesco_pair[1] ] );
		printf(
			"%-9s %-17s %4.1f:1  %s\n",
			$pagesco_look,
			$pagesco_pair[0] . ' on ' . $pagesco_pair[1],
			$pagesco_ratio,
			$pagesco_ratio >= 4.5 ? 'AA' : 'FAIL (needs 4.5)'
		);
	}
}

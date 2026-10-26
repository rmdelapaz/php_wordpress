<?php
/**
 * merge_layers_solution.php: merge a parent's and a child's theme.json the way WordPress does (Session 5, Lesson 3.4, lab B)
 * state: after:lesson_10
 * expect: merged:  8 colors, accent-3 = #7a2e2e
 * expect: partial: 2 colors (base, contrast)
 *
 * The reference solution. See merge_layers_starter.php for the task.
 */
$pagesco_themes = get_theme_root();
$pagesco_parent = wp_json_file_decode( $pagesco_themes . '/twentytwentyfive/theme.json', array( 'associative' => true ) );
$pagesco_child  = wp_json_file_decode( $pagesco_themes . '/pagesco-tt5-child/theme.json', array( 'associative' => true ) );

/**
 * The slugs of a WP_Theme_JSON object's theme palette, and the color of one of them.
 *
 * @param WP_Theme_JSON $json The data.
 * @param string        $slug The color to look up.
 * @return string Such as "8 colors, accent-3 = #7a2e2e".
 */
function pagesco_palette_summary( $json, $slug ) {
	$pagesco_colors = wp_list_pluck( $json->get_raw_data()['settings']['color']['palette']['theme'] ?? array(), 'color', 'slug' );
	return count( $pagesco_colors ) . ' colors, ' . $slug . ' = ' . ( $pagesco_colors[ $slug ] ?? '(none)' );
}

$pagesco_merged = new WP_Theme_JSON( $pagesco_parent );
echo 'parent:  ', pagesco_palette_summary( $pagesco_merged, 'accent-3' ), "\n";
echo 'child:   ', pagesco_palette_summary( new WP_Theme_JSON( $pagesco_child ), 'accent-3' ), "\n";

// The child is a layer on top of the parent: merge() changes $pagesco_merged in place.
$pagesco_merged->merge( new WP_Theme_JSON( $pagesco_child ) );
$pagesco_styles = $pagesco_merged->get_raw_data()['styles'];
echo 'merged:  ', pagesco_palette_summary( $pagesco_merged, 'accent-3' ), "\n";
echo 'link:    ', $pagesco_styles['elements']['link']['color']['text'], "  (from the child)\n";
echo 'body:    ', $pagesco_styles['typography']['fontFamily'], "  (from the parent)\n";
echo 'h1 size: ', $pagesco_styles['elements']['h1']['typography']['fontSize'], "  (from the parent)\n";

// Lesson 3.4's Common Mistake 2: a child palette with only the two colors you meant to change.
$pagesco_partial = $pagesco_child;
$pagesco_partial['settings']['color']['palette'] = array_slice( $pagesco_child['settings']['color']['palette'], 0, 2 );
$pagesco_broken = new WP_Theme_JSON( $pagesco_parent );
$pagesco_broken->merge( new WP_Theme_JSON( $pagesco_partial ) );
$pagesco_left = wp_list_pluck( $pagesco_broken->get_raw_data()['settings']['color']['palette']['theme'], 'slug' );
echo 'partial: ', count( $pagesco_left ), ' colors (', implode( ', ', $pagesco_left ), ")\n";

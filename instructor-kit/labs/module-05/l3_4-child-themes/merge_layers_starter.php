<?php
/**
 * merge_layers_starter.php: merge a parent's and a child's theme.json the way WordPress does (Session 5, Lesson 3.4, lab B)
 * state: after:lesson_10
 * expect: merged:  TODO
 *
 * Lesson 3.4 says a child's theme.json is MERGED over the parent's, single values key by key, while preset lists
 * such as the palette are REPLACED whole. WordPress does the merging with one class, WP_Theme_JSON (the same
 * class that merges core, theme and user data, Lesson 3.3). Use it yourself on the two files of the lesson's
 * child theme, without activating anything. Needs pagesco-tt5-child from Lesson 3.4. From your project folder:
 *     cp labs/module-05/l3_4-child-themes/merge_layers_starter.php wordpress/
 *     wp eval-file --use-include merge_layers_starter.php
 * Do the three TODOs, run again after each, and compare with "Expected when done" at the end.
 * When you are done: rm wordpress/merge_layers_starter.php
 */
$pagesco_themes = get_theme_root();
$pagesco_parent = wp_json_file_decode( $pagesco_themes . '/twentytwentyfive/theme.json', array( 'associative' => true ) );
// TODO 1: decode the child's file, pagesco-tt5-child/theme.json, the same way.
$pagesco_child = null;

/**
 * The slugs of a WP_Theme_JSON object's theme palette, and the color of one of them. (Done for you: notice
 * where the palette is inside the object's data, keyed by its origin, 'theme'.)
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
echo 'child:   ', null === $pagesco_child ? 'TODO' : pagesco_palette_summary( new WP_Theme_JSON( $pagesco_child ), 'accent-3' ), "\n";

// TODO 2: merge the child into $pagesco_merged ($pagesco_merged->merge( new WP_Theme_JSON( ... ) ) changes it in
//         place), then replace each TODO below with a value from $pagesco_merged->get_raw_data()['styles']:
//         the link color (elements > link > color > text), the body font (typography > fontFamily) and the h1
//         size (elements > h1 > typography > fontSize). Which layer did each one come from?
echo "merged:  TODO\n";
echo "link:    TODO\n";
echo "body:    TODO\n";
echo "h1 size: TODO\n";

// TODO 3: Lesson 3.4's Common Mistake 2. Copy $pagesco_child into $pagesco_partial, keep only the first two
//         colors of its palette (array_slice()), merge it over a NEW WP_Theme_JSON of the parent, and print how
//         many theme colors are left, and their slugs.
echo "partial: TODO\n";

// Expected when done (merge_layers_solution.php, the site at the end of Lesson 3.4):
// parent:  8 colors, accent-3 = #503AA8
// child:   8 colors, accent-3 = #7a2e2e
// merged:  8 colors, accent-3 = #7a2e2e
// link:    var(--wp--preset--color--accent-3)  (from the child)
// body:    var(--wp--preset--font-family--manrope)  (from the parent)
// h1 size: var(--wp--preset--font-size--xx-large)  (from the parent)
// partial: 2 colors (base, contrast)

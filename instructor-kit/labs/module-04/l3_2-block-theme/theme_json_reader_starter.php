<?php
/**
 * theme_json_reader_starter.php: settings and styles, read from a theme's theme.json (Session 4, Lesson 3.2, lab B)
 * state: after:lesson_07
 * expect: version 3
 * expect: content width: TODO
 *
 * Lesson 3.2's key idea: settings say what is AVAILABLE (presets, widths), styles say what is APPLIED (usually by
 * pointing at a preset with "var:preset|color|slug"). This script reads Twenty Twenty-Five's file the way core
 * does, with wp_json_file_decode(), whichever theme is active. From your project folder:
 *     cp labs/module-04/l3_2-block-theme/theme_json_reader_starter.php wordpress/
 *     wp eval-file --use-include theme_json_reader_starter.php
 * Fill in the TODOs, run again, compare with "Expected when done" at the end.
 * When you are done: rm wordpress/theme_json_reader_starter.php
 */

$pagesco_slug = 'twentytwentyfive';
$pagesco_json = wp_json_file_decode( get_theme_root() . "/$pagesco_slug/theme.json", array( 'associative' => true ) );
$pagesco_set  = $pagesco_json['settings'];
$pagesco_sty  = $pagesco_json['styles'];

echo "$pagesco_slug: theme.json version ", $pagesco_json['version'], "\n";   // done for you

// TODO 1: the two layout widths from settings.layout (contentSize and wideSize).
echo "content width: TODO  wide width: TODO\n";

// TODO 2: the palette SLUGS, comma-separated (settings.color.palette is a list of arrays; wp_list_pluck()).
echo "palette: TODO\n";

// TODO 3: the font size slugs the same way (settings.typography.fontSizes).
echo "font sizes: TODO\n";

// TODO 4: what styles applies to the page: styles.color.background and styles.color.text, AS WRITTEN in the file.
echo "page background: TODO  text: TODO\n";

// TODO 5: turn the text value into the CSS WordPress prints: "var:preset|color|contrast" becomes
//         "var(--wp--preset--color--contrast)". str_replace() the "var:preset|" prefix with "var(--wp--preset--",
//         every remaining "|" with "--", and add the closing parenthesis.
echo "text as CSS: TODO\n";

// Expected when done (theme_json_reader_solution.php):
// twentytwentyfive: theme.json version 3
// content width: 645px  wide width: 1340px
// palette: base, contrast, accent-1, accent-2, accent-3, accent-4, accent-5, accent-6
// font sizes: small, medium, large, x-large, xx-large
// page background: var:preset|color|base  text: var:preset|color|contrast
// text as CSS: var(--wp--preset--color--contrast)

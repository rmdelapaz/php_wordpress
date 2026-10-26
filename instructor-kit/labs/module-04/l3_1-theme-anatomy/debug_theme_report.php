<?php
/**
 * debug_theme_report.php: a quick report on the active theme, with mistakes (Session 4, Lesson 3.1, find-the-bug handout)
 * state: after:lesson_06
 * expect-error: Warning
 *
 * Meant to print the active theme's name, the WordPress version it needs, its kind, and its palette with a count.
 * Run it as shipped and read every message from the left (level, message, file, line), from your project folder:
 *     cp labs/module-04/l3_1-theme-anatomy/debug_theme_report.php wordpress/
 *     wp eval-file --use-include debug_theme_report.php
 * There are two loud bugs (PHP warnings) and one silent one: a line that prints a wrong or empty answer without
 * any message. Fix all three until the report is complete and clean. Then: rm wordpress/debug_theme_report.php
 */

$pagesco_theme = wp_get_theme();
echo 'Theme: ', $pagesco_theme->get( 'Name' ), "\n";
echo 'Needs WordPress: ', $pagesco_theme->get( 'Requires at least' ), "\n";
echo 'Block theme: ', wp_is_block_theme() ? 'yes' : 'no', "\n";

$pagesco_json = wp_json_file_decode( get_theme_file_path( 'theme.json' ), array( 'associative' => true ) );
foreach ( $pagesco_json['settings']['colors']['palette'] as $pagesco_color ) {
	printf( "  %-9s %s\n", $pagesco_color['slug'], $pagesco_color['color'] );
	$pagesco_count++;
}
echo 'Colors in the palette: ', $pagesco_count, "\n";

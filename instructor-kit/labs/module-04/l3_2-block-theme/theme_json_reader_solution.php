<?php
/**
 * theme_json_reader_solution.php: the instructor's reference for theme_json_reader_starter.php (Session 4, Lesson 3.2, lab B)
 * state: after:lesson_07
 * expect: text as CSS: var(--wp--preset--color--contrast)
 */

$pagesco_slug = 'twentytwentyfive';
$pagesco_json = wp_json_file_decode( get_theme_root() . "/$pagesco_slug/theme.json", array( 'associative' => true ) );
$pagesco_set  = $pagesco_json['settings'];
$pagesco_sty  = $pagesco_json['styles'];

echo "$pagesco_slug: theme.json version ", $pagesco_json['version'], "\n";
echo 'content width: ', $pagesco_set['layout']['contentSize'], '  wide width: ', $pagesco_set['layout']['wideSize'], "\n";
echo 'palette: ', implode( ', ', wp_list_pluck( $pagesco_set['color']['palette'], 'slug' ) ), "\n";
echo 'font sizes: ', implode( ', ', wp_list_pluck( $pagesco_set['typography']['fontSizes'], 'slug' ) ), "\n";
echo 'page background: ', $pagesco_sty['color']['background'], '  text: ', $pagesco_sty['color']['text'], "\n";

$pagesco_css = str_replace( array( 'var:preset|', '|' ), array( 'var(--wp--preset--', '--' ), $pagesco_sty['color']['text'] ) . ')';
echo 'text as CSS: ', $pagesco_css, "\n";

<?php
/**
 * test_fernhill.php: the self-check of the Part 1 project, the Fernhill block theme (Session 8).
 *
 * serve: fernhill
 * install: theme fernhill
 * state: after:lesson_13
 * expect-starter: Checks passed: 1 of 12
 * expect-solution: Checks passed: 12 of 12
 *
 * Run it as often as you like: it reads your theme the way WordPress does and requests your pages the way a
 * browser does, then prints OK or TODO per requirement of BRIEF.md (R1 to R7; R8, quality, is the whole output:
 * no PHP message anywhere). It is a help, not the score. From your project folder, with your theme in
 * wordpress/wp-content/themes/fernhill/ and active (wp theme activate fernhill):
 *     cp labs/module-08/p1-project/test_fernhill.php wordpress/
 *     wp eval-file --use-include test_fernhill.php
 * When you stop for the day: rm wordpress/test_fernhill.php and wp theme activate pagesco (Lesson 5.1 expects it).
 */

$pagesco_results = array();
$pagesco_theme   = wp_get_theme();

// R1 The theme header (style.css).
$pagesco_results[] = array(
	'Fernhill' === $pagesco_theme->get( 'Name' ) && 'fernhill' === $pagesco_theme->get( 'TextDomain' )
		&& '1.0.0' === $pagesco_theme->get( 'Version' ) && '7.1' === $pagesco_theme->get( 'RequiresWP' )
		&& '' !== $pagesco_theme->get( 'RequiresPHP' ),
	'Theme header: Fernhill 1.0.0, text domain fernhill, requires WordPress 7.1 and a PHP version',
);

// R1 A block theme with a valid theme.json, version 3.
$pagesco_json_file = get_stylesheet_directory() . '/theme.json';
$pagesco_json      = is_readable( $pagesco_json_file ) ? json_decode( (string) file_get_contents( $pagesco_json_file ), true ) : null;
$pagesco_results[] = array(
	wp_is_block_theme() && is_array( $pagesco_json ) && 3 === ( $pagesco_json['version'] ?? 0 ),
	'A block theme with a valid theme.json, version 3',
);

// R1 The palette: five colors named by role, no core palette.
$pagesco_palette   = array_column( array_filter( (array) wp_get_global_settings( array( 'color', 'palette', 'theme' ) ), 'is_array' ), 'slug' );
$pagesco_results[] = array(
	array( 'base', 'contrast', 'primary', 'secondary', 'accent' ) === $pagesco_palette
		&& false === wp_get_global_settings( array( 'color', 'defaultPalette' ) ),
	'Palette: base, contrast, primary, secondary, accent (in that order); the default palette off',
);

// R1 The layout widths.
$pagesco_layout    = (array) wp_get_global_settings( array( 'layout' ) );
$pagesco_results[] = array(
	'680px' === ( $pagesco_layout['contentSize'] ?? '' ) && '1100px' === ( $pagesco_layout['wideSize'] ?? '' ),
	'Layout: content 680px, wide 1100px',
);

// R2 + R7 The templates, from the theme's own files.
$pagesco_have      = wp_list_pluck( get_block_templates( array(), 'wp_template' ), 'slug' );
$pagesco_missing   = array_diff( array( 'index', 'front-page', 'single', 'page', '404' ), $pagesco_have );
$pagesco_results[] = array(
	array() === $pagesco_missing,
	'Templates: index, front-page, single, page, 404' . ( $pagesco_missing ? ' (missing: ' . implode( ', ', $pagesco_missing ) . ')' : '' ),
);

// R2 The template parts and their areas.
$pagesco_areas = array();
foreach ( get_block_templates( array(), 'wp_template_part' ) as $pagesco_part ) {
	$pagesco_areas[ $pagesco_part->slug ] = $pagesco_part->area;
}
$pagesco_results[] = array(
	'header' === ( $pagesco_areas['header'] ?? '' ) && 'footer' === ( $pagesco_areas['footer'] ?? '' ),
	'Template parts: header (area header) and footer (area footer)',
);

// R3 + R5 The patterns, their category and their text domain.
$pagesco_patterns = WP_Block_Patterns_Registry::get_instance();
$pagesco_domains  = array();
foreach ( glob( get_stylesheet_directory() . '/patterns/*.php' ) as $pagesco_file ) {
	preg_match_all( "/\\b(?:__|_e|esc_html__|esc_html_e|esc_attr__|esc_attr_e)\\(\\s*'(?:[^'\\\\]|\\\\.)*'\\s*,\\s*'([^']*)'/", (string) file_get_contents( $pagesco_file ), $pagesco_m );
	$pagesco_domains = array_merge( $pagesco_domains, $pagesco_m[1] );
}
$pagesco_cats      = $pagesco_patterns->is_registered( 'fernhill/hero' ) ? (array) $pagesco_patterns->get_registered( 'fernhill/hero' )['categories'] : array();
$pagesco_results[] = array(
	$pagesco_patterns->is_registered( 'fernhill/hero' ) && $pagesco_patterns->is_registered( 'fernhill/volunteer-call' )
		&& in_array( 'fernhill', $pagesco_cats, true ) && WP_Block_Pattern_Categories_Registry::get_instance()->is_registered( 'fernhill' )
		&& count( $pagesco_domains ) >= 6 && array( 'fernhill' ) === array_values( array_unique( $pagesco_domains ) ),
	'Patterns: fernhill/hero and fernhill/volunteer-call in the fernhill category; every string translatable with fernhill',
);

// R4 The style variation.
$pagesco_titles    = wp_list_pluck( WP_Theme_JSON_Resolver::get_style_variations(), 'title' );
$pagesco_results[] = array( in_array( 'Autumn', $pagesco_titles, true ), 'Style variation: Autumn' );

// R3 The front page, as a browser gets it.
$pagesco_front     = wp_remote_retrieve_body( wp_remote_get( home_url( '/' ), array( 'timeout' => 30 ) ) );
$pagesco_results[] = array(
	str_contains( $pagesco_front, '>Grow food, grow friendships</h1>' ) && str_contains( $pagesco_front, '>Volunteer on Saturday mornings</h2>' )
		&& str_contains( $pagesco_front, '<header class="wp-block-template-part"' ) && 1 === preg_match( '/<main [^>]*class="wp-block-group/', $pagesco_front )
		&& str_contains( $pagesco_front, '<footer class="wp-block-template-part"' ),
	'Front page: header, main, the hero heading, the volunteer heading, footer',
);

// R5 The stylesheet, enqueued with the theme's version.
$pagesco_results[] = array(
	str_contains( $pagesco_front, "id='fernhill-style-css'" ) && str_contains( $pagesco_front, 'assets/css/fernhill.css?ver=1.0.0' ),
	'Stylesheet: fernhill-style, assets/css/fernhill.css?ver=1.0.0',
);

// R6 The main query: three posts per page on the blog home, the fourth on page 2.
$pagesco_page2     = wp_remote_retrieve_body( wp_remote_get( home_url( '/page/2/' ), array( 'timeout' => 30 ) ) );
$pagesco_on_front  = substr_count( $pagesco_front, '<li class="wp-block-post ' );
$pagesco_on_page2  = substr_count( $pagesco_page2, '<li class="wp-block-post ' );
$pagesco_results[] = array(
	3 === $pagesco_on_front && 1 === $pagesco_on_page2,
	"Main query: 3 posts on the front page, 1 on /page/2/ (now: {$pagesco_on_front} and {$pagesco_on_page2})",
);

// R7 The 404 page.
$pagesco_missing_page = wp_remote_get( home_url( '/no-such-path/' ), array( 'timeout' => 30 ) );
$pagesco_results[]    = array(
	404 === wp_remote_retrieve_response_code( $pagesco_missing_page )
		&& str_contains( wp_remote_retrieve_body( $pagesco_missing_page ), '>This path is overgrown</h1>' ),
	'404: status 404 and the heading "This path is overgrown"',
);

echo "Fernhill self-check (Part 1 project, BRIEF.md)\n";
$pagesco_passed = 0;
foreach ( $pagesco_results as $pagesco_i => $pagesco_r ) {
	$pagesco_passed += $pagesco_r[0] ? 1 : 0;
	printf( "%-4s %2d  %s\n", $pagesco_r[0] ? 'OK' : 'TODO', $pagesco_i + 1, $pagesco_r[1] );
}
echo "Checks passed: {$pagesco_passed} of " . count( $pagesco_results ) . "\n";

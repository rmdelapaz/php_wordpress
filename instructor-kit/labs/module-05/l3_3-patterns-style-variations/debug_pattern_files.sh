# debug_pattern_files.sh: a gift-card pattern and a sepia look that never show up (Session 5, Lesson 3.3, find-the-bug handout)
# state: after:lesson_09
# expect-error: doing_it_wrong, Notice
#
# A colleague added two files to pagesco and says "neither of them appears in the editor". The script writes
# both files into the theme, asks WordPress what it registered, and deletes them again, so your theme is left as
# it was. The two files are the heredocs below (between the EOF lines): fix them THERE, in this script.
# Needs the theme from the end of Lesson 3.3 (WP_DEVELOPMENT_MODE theme, so pattern files are read at once).
# From your project folder:
#     cp labs/module-05/l3_3-patterns-style-variations/debug_pattern_files.sh wordpress/
#     docker compose run --rm wpcli sh debug_pattern_files.sh
# Two bugs announce themselves with a Notice (read each from the left). The third is SILENT: once the loud ones
# are fixed the sepia look is registered, but not as what your colleague wanted. When it works, the last lines
# list pagesco/gift-cards among the patterns and Sepia next to Evening as a SITE variation.
# When you are done: rm wordpress/debug_pattern_files.sh

theme=wp-content/themes/pagesco

cat > "$theme/patterns/gift-cards.php" <<'PHP'
<?php
/**
 * Title: Gift cards
 * Categories: call-to-action
 * Description: A short paragraph about the shop's gift cards.
 *
 * @package pagesco
 */

?>
<!-- wp:paragraph -->
<p><?php esc_html_e( 'Gift cards from $10, in the shop and by email.', 'pagesco' ); ?></p>
<!-- /wp:paragraph -->
PHP

cat > "$theme/styles/sepia.json" <<'JSON'
{
	"$schema": "https://schemas.wp.org/wp/7.1/theme.json",
	"version": 3,
	"title": "Sepia",
	"blockTypes": [ "core/group" ],
	"settings": {
		"color": {
			"palette": [
				{ "slug": "paper", "name": "Paper", "color": "#f4ecd8" },
				{ "slug": "ink", "name": "Ink", "color": "#3b2f25" },
			]
		}
	}
}
JSON

echo "== what WordPress registered =="
wp eval '
foreach ( WP_Block_Patterns_Registry::get_instance()->get_all_registered() as $p ) {
	if ( str_starts_with( $p["name"], "pagesco/" ) ) {
		echo "pattern: ", $p["name"], "\n";
	}
}
foreach ( WP_Theme_JSON_Resolver::get_style_variations() as $v ) {
	echo "site variation: ", $v["title"], "\n";
}
foreach ( WP_Theme_JSON_Resolver::get_style_variations( "block" ) as $v ) {
	echo "section style: ", $v["title"], "\n";
}'

rm "$theme/patterns/gift-cards.php" "$theme/styles/sepia.json"

# debug_child_theme.sh: a child theme written in a hurry (Session 5, Lesson 3.4, find-the-bug handout)
# state: after:lesson_10
# expect-error: doing_it_wrong, Notice
#
# A colleague's child of Twenty Twenty-Five should: give links the shop's oxblood, load its own style.css after
# the parent's, and drop the parent's "Checkmark" list style. The script writes the child into themes/,
# activates it, checks the three wishes, switches back to the theme that was active, and deletes the child, so
# your site is left as it was (apart from one harmless theme_mods_ option, Lesson 3.4). The child's files are
# the heredocs below: fix them THERE, in this script. From your project folder:
#     cp labs/module-05/l3_4-child-themes/debug_child_theme.sh wordpress/
#     docker compose run --rm wpcli sh debug_child_theme.sh
# Two bugs announce themselves with notices (the first one comes with two companions: read the first). The
# third is SILENT. Fixed, the checks say: link #7a2e2e, child CSS 1 (after the parent's), checkmark: no.
# When you are done: rm wordpress/debug_child_theme.sh

child=wp-content/themes/pagesco-lab-broken
previous=$(wp option get stylesheet)
log=wp-content/debug.log
before=$(wc -c < "$log" 2>/dev/null || echo 0)
mkdir -p "$child"

cat > "$child/style.css" <<'CSS'
/*
Theme Name: Pages & Co. Lab: Broken Child
Template: twentytwentyfive
Version: 1.0.0
Text Domain: pagesco-lab-broken
*/
.pagesco-notice { background: var(--wp--preset--color--contrast); color: var(--wp--preset--color--base); }
CSS

cat > "$child/theme.json" <<'JSON'
{
	"$schema": "https://schemas.wp.org/wp/7.1/theme.json",
	"version": 3,
	"styles": {
		"elements": {
			"link": {
				"color": { "text": "#7a2e2e" },
			}
		}
	}
}
JSON

cat > "$child/functions.php" <<'PHP'
<?php
/**
 * Broken Child functions.
 *
 * @package pagesco-lab-broken
 */

wp_enqueue_style( 'pagesco-lab-broken-style', get_stylesheet_uri(), array( 'twentytwentyfive-style' ), '1.0.0' );

remove_action( 'init', 'twentytwentyfive_block_styles' );
PHP

wp theme activate pagesco-lab-broken
home=$(curl -s http://localhost:8080/)
echo "link:      $(printf '%s' "$home" | grep -o 'a:where(:not(.wp-element-button)){color: [^;]*' | sed 's/.*color: //')"
echo "child CSS: $(printf '%s' "$home" | grep -c "pagesco-lab-broken-style-css")"
printf 'checkmark: '
wp eval 'echo WP_Block_Styles_Registry::get_instance()->is_registered( "core/list", "checkmark-list" ) ? "yes" : "no", "\n";'

echo "== what the page request added to debug.log (time stamps and HTML removed) =="
tail -c +$((before + 1)) "$log" | sed 's/^\[[^]]*\] //; s/<[^>]*>//g' | sort | uniq -c

wp theme activate "$previous"
rm -r "$child"

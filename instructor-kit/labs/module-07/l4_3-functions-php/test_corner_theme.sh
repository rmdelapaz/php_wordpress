# test_corner_theme.sh: what the Reading Corner theme's functions.php hands to WordPress (Session 7, Lesson 4.3, lab A)
# serve: corner_theme
# install: theme pagesco-lab-corner
# state: after:lesson_12
# expect-starter: <title>:      0
# expect-starter: search form:  xhtml (id="searchform")
# expect-solution: <title>:      1
# expect-solution: search form:  html5 (type="search")
# expect-solution: style:        style.css?ver=2.0.0
# expect-solution: script:       corner.js?ver=2.0.0, defer
# expect-solution: menu places:  corner (Reading corner menu)
# expect-solution: widget areas: corner-footer
#
# Asks the home page and WP-CLI about each TODO; nothing is changed. From your project folder (the starter;
# the solution likewise):
#     cp -r labs/module-07/l4_3-functions-php/corner_theme_starter wordpress/wp-content/themes/pagesco-lab-corner
#     wp theme activate pagesco-lab-corner
#     cp labs/module-07/l4_3-functions-php/test_corner_theme.sh wordpress/
#     docker compose run --rm wpcli sh test_corner_theme.sh
# When you are done: wp theme activate pagesco-classic && rm -r wordpress/wp-content/themes/pagesco-lab-corner wordpress/test_corner_theme.sh

home=$(curl -s http://localhost:8080/)
echo "<title>:      $(printf '%s' "$home" | grep -c '<title>')"
if printf '%s' "$home" | grep -q 'id="searchform"'; then echo 'search form:  xhtml (id="searchform")'; else echo 'search form:  html5 (type="search")'; fi
style=$(printf '%s' "$home" | grep -o "pagesco-lab-corner/style.css?ver=[^']*" | head -n 1 | sed 's#.*/##')
echo "style:        ${style:-(not enqueued)}"
script=$(printf '%s' "$home" | grep -o '<script[^>]*pagesco-lab-corner-script-js[^>]*>' | head -n 1)
if [ -n "$script" ]; then
	echo "script:       $(printf '%s' "$script" | grep -o 'corner.js?ver=[^"]*'), $(printf '%s' "$script" | grep -o ' defer' | sed 's/ //')"
else
	echo "script:       (not enqueued)"
fi
places=$(wp menu location list --format=csv | tail -n +2 | tr -d '"' | sed 's/,/ (/; s/$/)/')
echo "menu places:  ${places:-(none)}"
areas=$(wp sidebar list --fields=id --format=csv | tail -n +2 | grep -v wp_inactive_widgets | tr '\n' ' ' | sed 's/ $//')
echo "widget areas: ${areas:-(none)}"

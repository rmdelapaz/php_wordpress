# test_debug_cafe_theme.sh: a café theme with three mistakes, and a test that shows them (Session 4, Lesson 3.2, debug handout)
# serve: debug_cafe_theme
# install: theme pagesco-cafe
# state: after:lesson_07
# expect-error: Notice, Deprecated
# expect: header parts: 0
#
# debug_cafe_theme/ is a small block theme for the café's pages. It activates without complaint, but the page is
# wrong in three ways: two of them print messages at the top of the page (and in debug.log), one is silent.
# Note your theme first (wp theme list --status=active --field=name). From your project folder:
#     cp -r labs/module-04/l3_2-block-theme/debug_cafe_theme wordpress/wp-content/themes/pagesco-cafe
#     wp theme activate pagesco-cafe
#     cp labs/module-04/l3_2-block-theme/test_debug_cafe_theme.sh wordpress/
#     docker compose run --rm wpcli sh test_debug_cafe_theme.sh
# Fix the theme's files in wordpress/wp-content/themes/pagesco-cafe/ until the test prints no message, the
# espresso and foam colors, "header parts: 1" and the titles with their cup.
# When you are done: wp theme activate <your theme>, wp theme delete pagesco-cafe, rm wordpress/test_debug_cafe_theme.sh

page=$(curl -s http://localhost:8080/)
echo "messages in the page (how many of each):"
echo "$page" | grep '^\(Notice\|Deprecated\|Warning\): ' | sort | uniq -c || echo "(none)"
echo "palette: $(echo "$page" | grep -o -- '--wp--preset--color--\(espresso\|foam\): #[0-9a-f]*' | tr '\n' ' ')"
echo "header parts: $(echo "$page" | grep -c '<header class="wp-block-template-part"')"
echo "titles:"
echo "$page" | grep -o '<h2 class="wp-block-post-title"><a [^>]*>[^<]*' | sed 's/<[^>]*>//g'

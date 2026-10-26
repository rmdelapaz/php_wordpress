# test_tt4_child.sh: checks the reading-corner child theme of Twenty Twenty-Four (Session 5, Lesson 3.4, lab A)
# serve: tt4_child
# install: theme pagesco-lab-tt4-child
# state: after:lesson_09
# expect-starter: accent-3:    #d8613c
# expect-starter: child CSS:   0
# expect-starter: footer:      (not the shop's: still the parent's footer pattern)
# expect-solution: accent-3:    #7a2e2e
# expect-solution: palette:     10 theme colors
# expect-solution: child CSS:   1
# expect-solution: footer:      The reading corner at Pages &amp; Co. · 12 Market Street
# expect-solution: styles:      core/list checkmark-list
#
# One line per inheritance rule of Lesson 3.4. From your project folder (the starter; the solution likewise):
#     cp -r labs/module-05/l3_4-child-themes/tt4_child_starter wordpress/wp-content/themes/pagesco-lab-tt4-child
#     wp theme activate pagesco-lab-tt4-child
#     cp labs/module-05/l3_4-child-themes/test_tt4_child.sh wordpress/
#     docker compose run --rm wpcli sh test_tt4_child.sh
# When you are done: wp theme activate pagesco && rm -r wordpress/wp-content/themes/pagesco-lab-tt4-child wordpress/test_tt4_child.sh

home=$(curl -s http://localhost:8080/)
echo "template:    $(wp option get template)"
echo "stylesheet:  $(wp option get stylesheet)"
echo "accent-3:    $(printf '%s' "$home" | grep -o -- '--wp--preset--color--accent-3: [^;]*' | head -n 1 | sed 's/.*: //')"
echo "palette:     $(printf '%s' "$home" | grep -o -- '--wp--preset--color--\(base\|contrast\|accent\)[a-z0-9-]*: ' | sort -u | wc -l) theme colors"
echo "child CSS:   $(printf '%s' "$home" | grep -c 'pagesco-lab-tt4-child/style.css')"
footer=$(printf '%s' "$home" | grep -o 'The reading corner[^<]*' | head -n 1)
echo "footer:      ${footer:-(not the shop's: still the parent's footer pattern)}"
printf 'styles:      '
wp eval '$pagesco_found = array(); foreach ( WP_Block_Styles_Registry::get_instance()->get_all_registered() as $pagesco_block => $pagesco_styles ) { foreach ( $pagesco_styles as $pagesco_style ) { $pagesco_found[] = $pagesco_block . " " . $pagesco_style["name"]; } } echo implode( ", ", $pagesco_found ), "\n";'

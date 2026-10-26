# test_book_fair.sh: what the home page got from the book-fair theme (Session 4, Lesson 3.2, lab A)
# serve: book_fair
# install: theme pagesco-fair
# state: after:lesson_07
# expect-starter: lantern: (missing)
# expect-starter: footer parts: 0
# expect-solution: --wp--preset--color--lantern: #f2b134
# expect-solution: posts listed: 4
# expect-solution: footer parts: 1
#
# Install the theme as wp-content/themes/pagesco-fair/ and switch to it, then run this test in the WP-CLI
# container. First note which theme you have now (wp theme list --status=active --field=name), to switch back.
# From your project folder:
#     cp -r labs/module-04/l3_2-block-theme/book_fair_starter wordpress/wp-content/themes/pagesco-fair
#     wp theme activate pagesco-fair
#     cp labs/module-04/l3_2-block-theme/test_book_fair.sh wordpress/
#     docker compose run --rm wpcli sh test_book_fair.sh
# When you are done: wp theme activate <your theme>, then wp theme delete pagesco-fair and rm wordpress/test_book_fair.sh

page=$(curl -s http://localhost:8080/)
echo "active theme: $(wp theme list --status=active --field=name)"
echo "palette:"
for slug in night cream lantern; do
	echo "$page" | grep -o -- "--wp--preset--color--$slug: #[0-9a-f]*" || echo "$slug: (missing)"
done
echo "page colors: $(echo "$page" | grep -o 'body{background-color: [^;]*;color: [^;]*;' || echo '(none: theme.json has no styles.color)')"
echo "posts listed: $(echo "$page" | grep -o '<h2 class="wp-block-post-title">' | wc -l)"
echo "header parts: $(echo "$page" | grep -c '<header class="wp-block-template-part"')"
echo "footer parts: $(echo "$page" | grep -c '<footer class="wp-block-template-part"')"
echo "footer text: $(echo "$page" | grep -o 'Book fair weekend · [^<]*' || echo '(none)')"

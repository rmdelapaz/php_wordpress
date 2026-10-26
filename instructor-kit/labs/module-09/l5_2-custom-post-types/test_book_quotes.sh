# test_book_quotes.sh: one quote, asked for as a visitor and as the REST API (Session 9, Lesson 5.2, lab A)
# serve: book_quotes
# install: plugin pagesco-quotes
# state: after:lesson_14
# expect-starter: archive /quotes/: 404
# expect-starter: rest_no_route
# expect-solution: archive /quotes/: 200
# expect-solution: "pagesco_quote_source":"Pride and Prejudice"
#
# Install the folder as a plugin and activate it (the activation hook runs then), then run the test. From your
# project folder:
#     cp -r labs/module-09/l5_2-custom-post-types/book_quotes_starter wordpress/wp-content/plugins/pagesco-quotes
#     wp plugin activate pagesco-quotes
#     cp labs/module-09/l5_2-custom-post-types/test_book_quotes.sh wordpress/
#     docker compose run --rm wpcli sh test_book_quotes.sh
# The test creates one quote and deletes it again. When you are done:
#     wp plugin deactivate pagesco-quotes
#     rm -r wordpress/wp-content/plugins/pagesco-quotes wordpress/test_book_quotes.sh

QUOTE=$(wp post create --post_type=pagesco_quote --post_title="A truth universally acknowledged" --post_status=publish --porcelain)
wp post meta update "$QUOTE" pagesco_quote_source "Pride and Prejudice" > /dev/null
echo "archive /quotes/: $(curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/quotes/)"
echo "REST /wp/v2/quotes:"
curl -s 'http://localhost:8080/wp-json/wp/v2/quotes?_fields=title,meta'
echo
wp post delete "$QUOTE" --force > /dev/null
echo "quotes left: $(wp post list --post_type=pagesco_quote --post_status=any --format=count)"

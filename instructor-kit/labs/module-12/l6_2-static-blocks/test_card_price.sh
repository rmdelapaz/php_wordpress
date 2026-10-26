# test_card_price.sh: two Book Cards on a test post, with and without a link, and what the page prints (Session 12, Lesson 6.2, lab B)
# serve: card_price
# install: mu-plugin
# state: after:lesson_19
# expect-starter: price lines: 0
# expect-solution: <p class="pagesco-card-price">Today: $10.99</p>
# expect-solution: price lines: 1
#
# The cards are stored as finished HTML (written the way Lesson 6.2's save() writes them), so the test can create
# them without the editor. From your project folder, with pagesco-card-price.php in wordpress/wp-content/mu-plugins/:
#     cp labs/module-12/l6_2-static-blocks/test_card_price.sh wordpress/
#     docker compose run --rm wpcli sh test_card_price.sh
# The test deletes its post again. When you are done:
#     rm wordpress/test_card_price.sh wordpress/wp-content/mu-plugins/pagesco-card-price.php

ID=$(wp post create --post_type=post --post_status=publish --post_title='Card price lab' --post_name=card-price-lab --porcelain --post_content='<!-- wp:pagesco/book-card -->
<div class="wp-block-pagesco-book-card"><a class="wp-block-pagesco-book-card__link" href="http://localhost:8080/books/the-hobbit/"><h3 class="wp-block-pagesco-book-card__title">The Hobbit</h3></a><p class="wp-block-pagesco-book-card__author">J.R.R. Tolkien</p></div>
<!-- /wp:pagesco/book-card -->

<!-- wp:pagesco/book-card -->
<div class="wp-block-pagesco-book-card"><h3 class="wp-block-pagesco-book-card__title">A book without a link</h3></div>
<!-- /wp:pagesco/book-card -->')

echo "The cards and what follows them:"
curl -s http://localhost:8080/card-price-lab/ | grep -o '<h3 class="wp-block-pagesco-book-card__title">[^<]*</h3>\|<p class="pagesco-card-price">[^<]*</p>'
printf 'price lines: '
curl -s http://localhost:8080/card-price-lab/ | grep -c '<p class="pagesco-card-price">'

wp post delete "$ID" --force > /dev/null

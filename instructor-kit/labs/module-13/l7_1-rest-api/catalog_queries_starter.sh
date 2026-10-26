# catalog_queries_starter.sh: questions for the catalog, answered by the REST API (Session 13, Lesson 7.1, lab A)
# state: after:lesson_22
# expect: Books in the catalog: 11
# expect: Its books, by title: TODO
#
# Every answer is one curl request to a core route, shaped with the parameters of Lesson 7.1 (_fields, per_page,
# orderby, order, search, genres) or read from a header. The script runs in the WP-CLI container, where
# http://localhost:8080 is the site. From your project folder:
#     cp labs/module-13/l7_1-rest-api/catalog_queries_starter.sh wordpress/
#     docker compose run --rm wpcli sh catalog_queries_starter.sh
# Try each request alone first (paste it into a shell in the container: docker compose run --rm wpcli sh), then
# replace its echo "... TODO" line, run the script again and compare with "Expected when done".
# When you are done: rm wordpress/catalog_queries_starter.sh

API=http://localhost:8080/wp-json/wp/v2

printf 'Books in the catalog: '                 # done for you: the total is a header, so ask for the headers only
curl -s -I "$API/books?per_page=1" | grep -i '^X-WP-Total:' | tr -dc '0-9'
echo

# TODO 1: the genre whose slug is dystopian, with only its id and name (/genres, ?slug=..., _fields).
echo "The Dystopian genre: TODO"

# TODO 2: the slugs of its books, by title A to Z. The genres filter takes the ID from TODO 1, not the slug.
echo "Its books, by title: TODO"

# TODO 3: the id and the rendered title of every book whose text contains "farm" (search=...).
echo "Search for farm: TODO"

# TODO 4: the slugs of all pages, oldest ID first (the route is /pages).
echo "The site's pages, oldest first: TODO"

# TODO 5: only the HTTP status code of a request for book 99: curl -s -o /dev/null -w '%{http_code}\n' ...
echo "Book 99: TODO"

# TODO 6: the two genres with the most books, their name and count (orderby=count, order=desc, per_page=2).
echo "The two biggest genres: TODO"

# Expected when done (catalog_queries_solution.sh, the site after Lesson 6.4):
# Books in the catalog: 11
# The Dystopian genre:
# [{"id":9,"name":"Dystopian"}]
# Its books, by title:
# [{"slug":"1984"},{"slug":"brave-new-world"},{"slug":"fahrenheit-451"}]
# Search for farm:
# [{"id":40,"title":{"rendered":"Animal Farm"}}]
# The site's pages, oldest first:
# [{"slug":"sample-page"},{"slug":"about"},{"slug":"contact"},{"slug":"events"},{"slug":"find-a-book"}]
# Book 99: 404
# The two biggest genres:
# [{"count":11,"name":"Fiction"},{"count":6,"name":"Classic"}]

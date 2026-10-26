# catalog_queries_solution.sh: the instructor's reference for catalog_queries_starter.sh (Session 13, Lesson 7.1, lab A)
# state: after:lesson_22
# expect: [{"slug":"1984"},{"slug":"brave-new-world"},{"slug":"fahrenheit-451"}]
# expect: Book 99: 404

API=http://localhost:8080/wp-json/wp/v2

printf 'Books in the catalog: '
curl -s -I "$API/books?per_page=1" | grep -i '^X-WP-Total:' | tr -dc '0-9'
echo

echo "The Dystopian genre:"
curl -s "$API/genres?slug=dystopian&_fields=id,name"
echo

echo "Its books, by title:"
curl -s "$API/books?genres=9&orderby=title&order=asc&_fields=slug"
echo

echo "Search for farm:"
curl -s "$API/books?search=farm&_fields=id,title.rendered"
echo

echo "The site's pages, oldest first:"
curl -s "$API/pages?orderby=id&order=asc&_fields=slug"
echo

printf 'Book 99: '
curl -s -o /dev/null -w '%{http_code}\n' "$API/books/99"

echo "The two biggest genres:"
curl -s "$API/genres?orderby=count&order=desc&per_page=2&_fields=name,count"
echo

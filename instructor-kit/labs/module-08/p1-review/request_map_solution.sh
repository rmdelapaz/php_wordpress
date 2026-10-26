# request_map_solution.sh: what WordPress thinks each address is (Session 8 review, Lessons 3.1 and 4.1)
# state: after:lesson_13
# expect: /  200  home blog
# expect: /no-such-path/  404  error404
#
# For each address: the HTTP status and the body classes that name the request type (body_class(), which every
# theme prints on <body>). That is the template hierarchy's input: the classes say which question WordPress
# asked, the theme's file list says which template answered. Run it with ANY theme active.
#     cp labs/module-08/p1-review/request_map_solution.sh wordpress/
#     docker compose run --rm wpcli sh request_map_solution.sh

for pagesco_url in / /page/2/ /book-club-dune/ /about/ /category/news/ "/?s=dune" /no-such-path/; do
	pagesco_page=$(curl -s -w '\n%{http_code}' "http://localhost:8080$pagesco_url")
	pagesco_code=$(echo "$pagesco_page" | tail -n 1)
	pagesco_classes=$(echo "$pagesco_page" | grep -o '<body class="[^"]*"' | sed 's/<body class="//; s/"$//' | tr ' ' '\n' \
		| grep -x 'home\|blog\|paged\|single\|single-post\|page\|page-template-default\|archive\|category\|category-news\|search\|search-results\|error404' | tr '\n' ' ')
	echo "$pagesco_url  $pagesco_code  $pagesco_classes"
done

# request_map_starter.sh: what WordPress thinks each address is (Session 8 review, Lessons 3.1 and 4.1)
# state: after:lesson_13
# expect: /  200  TODO
#
# For each address: the HTTP status and the body classes that name the request type (body_class(), which every
# theme prints on <body>). That is the template hierarchy's input: the classes say which question WordPress
# asked, the theme's file list says which template answered. Run it with ANY theme active.
#     cp labs/module-08/p1-review/request_map_starter.sh wordpress/
#     docker compose run --rm wpcli sh request_map_starter.sh
# TODO 1: add /page/2/, /about/, /category/news/, "/?s=dune" and /no-such-path/ to the list.
# TODO 2: replace TODO with the body classes: grep -o the <body class="..."> attribute, strip it to the class
#         list, then keep only these words, one per line with tr and grep -x: home blog paged single single-post
#         page page-template-default archive category category-news search search-results error404.

for pagesco_url in / /book-club-dune/; do
	pagesco_page=$(curl -s -w '\n%{http_code}' "http://localhost:8080$pagesco_url")
	pagesco_code=$(echo "$pagesco_page" | tail -n 1)
	echo "$pagesco_url  $pagesco_code  TODO"
done

# The classes are the same with any theme; the statuses are pagesco's (ten posts per page: no page 2).
# Expected when done:
# /  200  home blog
# /page/2/  404  error404
# /book-club-dune/  200  single single-post
# /about/  200  page-template-default page
# /category/news/  200  archive category category-news
# /?s=dune  200  search search-results
# /no-such-path/  404  error404

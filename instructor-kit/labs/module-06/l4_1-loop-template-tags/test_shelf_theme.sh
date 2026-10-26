# test_shelf_theme.sh: one template, five addresses (Session 6, Lesson 4.1, lab A)
# serve: shelf_theme
# install: theme pagesco-lab-shelf
# state: after:lesson_10
# expect-starter: TODO: the Loop
# expect-solution: /category/news/   Shelf: News
# expect-solution: Book club: Dune · 2026-10-01 · Maria Lopez
# expect-solution: /?s=zzz           Found for: zzz
# expect-solution: /book-club-dune/  Book club: Dune
# expect-solution: Nothing on this shelf.
#
# The Shelf theme has ONE template. The test asks for five different addresses and prints, for each, the h1 and
# the text of the list (tags removed). From your project folder (the starter; the solution likewise):
#     cp -r labs/module-06/l4_1-loop-template-tags/shelf_theme_starter wordpress/wp-content/themes/pagesco-lab-shelf
#     wp theme activate pagesco-lab-shelf
#     cp labs/module-06/l4_1-loop-template-tags/test_shelf_theme.sh wordpress/
#     docker compose run --rm wpcli sh test_shelf_theme.sh
# When you are done: wp theme activate pagesco && rm -r wordpress/wp-content/themes/pagesco-lab-shelf wordpress/test_shelf_theme.sh

for url in /category/news/ /author/devon/ "/?s=dune" "/?s=zzz" /book-club-dune/; do
	page=$(curl -s "http://localhost:8080$url" | tr '\n\t' '  ' | tr -s ' ')
	printf '%-17s %s\n' "$url" "$(printf '%s' "$page" | grep -o '<h1>[^<]*' | sed 's/<h1>//')"
	printf '%s' "$page" | sed 's#</li>#</li>\n#g; s#</p>#</p>\n#g' | grep -o '<li class="shelf-item">.*</li>\|<p class="shelf-empty">.*</p>\|<p class="todo">.*</p>' \
		| sed 's/<[^>]*>//g; s/^ */    /; s/ *$//'
done
echo "the first link: $(curl -s http://localhost:8080/category/news/ | tr -d '\n\t' | grep -o '<li class="shelf-item"><a [^>]*>' | head -n 1)"

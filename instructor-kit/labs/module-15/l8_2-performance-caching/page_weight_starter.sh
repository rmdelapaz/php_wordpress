# page_weight_starter.sh: what four pages make the browser download, counted with curl and grep (Session 15, Lesson 8.2, lab C)
# state: after:lesson_26
# expect: hero image reserves its space: TODO
#
# Lesson 8.2's "What the Browser Downloads" and "Images", as one report you can rerun after every change. The
# script runs in the WP-CLI container. From your project folder:
#     cp labs/module-15/l8_2-performance-caching/page_weight_starter.sh wordpress/
#     docker compose run --rm wpcli sh page_weight_starter.sh
# The page size is done for you. Each TODO is one grep -o '...' | wc -l on the saved page (grep -c counts LINES,
# and WordPress prints several tags on one line). Run again after each one; compare with "Expected when done".
# When you are done: rm wordpress/page_weight_starter.sh

printf '%-14s %8s %7s %9s %8s %7s\n' page 'KB html' styles 'css files' modules images
for page in / /books/dune/ /find-a-book/ /events/; do
	curl -s "http://localhost:8080$page" > /tmp/pagesco-page.html
	# TODO 1 to 4, one column each: inline <style elements; <link rel='stylesheet' tags (WordPress writes them with
	#           single quotes); script modules (type="module"); <img  tags.
	printf '%-14s %8s %7s %9s %8s %7s\n' "$page" \
		"$(( $(wc -c < /tmp/pagesco-page.html) / 1024 ))" \
		TODO TODO TODO TODO
done

curl -s http://localhost:8080/ > /tmp/pagesco-page.html
# TODO 5: find the hero image's <img> tag (its src contains book-image) and print "yes" when it has width="..." or
#         aspect-ratio in it, else "no (no width, height or aspect-ratio)".
echo "hero image reserves its space: TODO"
# TODO 6: is there a <link rel='preload' ...> for book-image in the page? yes or no.
echo "hero image preloaded: TODO"
# TODO 7: how many <img> tags have loading="lazy"?
echo "lazy images on the front page: TODO"
rm /tmp/pagesco-page.html

# Expected when done (page_weight_solution.sh, the course site after Lesson 8.1; your KB may differ by one):
# page            KB html  styles css files  modules  images
# /                    82      20         1        2       1
# /books/dune/         78      16         0        2       0
# /find-a-book/        81      15         0        3       0
# /events/             75      14         0        2       0
# hero image reserves its space: no (no width, height or aspect-ratio)
# hero image preloaded: no
# lazy images on the front page: 0

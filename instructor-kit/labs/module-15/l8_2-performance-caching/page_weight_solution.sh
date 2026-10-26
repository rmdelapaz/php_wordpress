# page_weight_solution.sh: what four pages make the browser download, counted with curl and grep (Session 15, Lesson 8.2, lab C)
# state: after:lesson_26
# expect: hero image reserves its space: no (no width, height or aspect-ratio)
#
# Lesson 8.2's "What the Browser Downloads" and "Images", as one report you can rerun after every change. The
# script runs in the WP-CLI container. From your project folder:
#     cp labs/module-15/l8_2-performance-caching/page_weight_solution.sh wordpress/
#     docker compose run --rm wpcli sh page_weight_solution.sh
#     rm wordpress/page_weight_solution.sh

printf '%-14s %8s %7s %9s %8s %7s\n' page 'KB html' styles 'css files' modules images
for page in / /books/dune/ /find-a-book/ /events/; do
	curl -s "http://localhost:8080$page" > /tmp/pagesco-page.html
	printf '%-14s %8s %7s %9s %8s %7s\n' "$page" \
		"$(( $(wc -c < /tmp/pagesco-page.html) / 1024 ))" \
		"$(grep -o '<style' /tmp/pagesco-page.html | wc -l)" \
		"$(grep -o "<link rel='stylesheet'" /tmp/pagesco-page.html | wc -l)" \
		"$(grep -o 'type="module"' /tmp/pagesco-page.html | wc -l)" \
		"$(grep -o '<img ' /tmp/pagesco-page.html | wc -l)"
done

curl -s http://localhost:8080/ > /tmp/pagesco-page.html
hero=$(grep -o '<img[^>]*book-image[^>]*>' /tmp/pagesco-page.html | head -1)
if echo "$hero" | grep -q -e 'width="' -e 'aspect-ratio'; then
	echo "hero image reserves its space: yes"
else
	echo "hero image reserves its space: no (no width, height or aspect-ratio)"
fi
if grep -q "<link rel='preload'[^>]*book-image" /tmp/pagesco-page.html; then
	echo "hero image preloaded: yes"
else
	echo "hero image preloaded: no"
fi
echo "lazy images on the front page: $(grep -o '<img[^>]*loading="lazy"' /tmp/pagesco-page.html | wc -l)"
rm /tmp/pagesco-page.html

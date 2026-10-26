# a11y_scan_solution.sh: seven markup checks an automated audit makes, with curl and grep (Session 16, Lesson 8.3, lab B)
# state: after:lesson_27
# expect: /find-a-book/  lang=en-US  main=1  h1=1  img-no-alt=0  skip-link=yes  notice-landmark=no  nested-list=yes
#
# axe and Lighthouse check hundreds of rules in a browser; a few of the most useful need nothing but the HTML.
# This report checks four pages: the page language, one main landmark, exactly one h1, images without an alt
# attribute, the skip link, whether the store notice is a landmark, and a <ul> directly inside a <ul> (Lesson 8.3's
# "list" finding). From your project folder:
#     cp labs/module-16/l8_3-i18n-a11y-distribution/a11y_scan_solution.sh wordpress/
#     docker compose run --rm wpcli sh a11y_scan_solution.sh
#     rm wordpress/a11y_scan_solution.sh

for page in / /books/dune/ /find-a-book/ /events/; do
	# One line per page: WordPress breaks some tags over several lines, and grep reads line by line.
	curl -s "http://localhost:8080$page" | tr '\n' ' ' > /tmp/pagesco-a11y.html
	lang=$(grep -o '<html lang="[^"]*"' /tmp/pagesco-a11y.html | cut -d'"' -f2)
	h1=$(grep -o '<h1[ >]' /tmp/pagesco-a11y.html | wc -l)
	noalt=$(grep -o '<img [^>]*>' /tmp/pagesco-a11y.html | grep -v -c ' alt=')
	if grep -q 'id="wp-skip-link"' /tmp/pagesco-a11y.html; then skip=yes; else skip=no; fi
	main=$(grep -o '<main[ >]' /tmp/pagesco-a11y.html | wc -l)
	if grep -q '<div class="pagesco-notice"[^>]*role="region"' /tmp/pagesco-a11y.html; then notice=yes; else notice=no; fi
	if grep -q '<ul class="wp-block-navigation__container[^>]*><ul' /tmp/pagesco-a11y.html; then nested=yes; else nested=no; fi
	printf '%-14s lang=%s  main=%s  h1=%s  img-no-alt=%s  skip-link=%s  notice-landmark=%s  nested-list=%s\n' \
		"$page" "$lang" "$main" "$h1" "$noalt" "$skip" "$notice" "$nested"
done
rm /tmp/pagesco-a11y.html
echo "Not checked here, and never by a machine alone: alt texts that describe, focus you can see, a screen reader."

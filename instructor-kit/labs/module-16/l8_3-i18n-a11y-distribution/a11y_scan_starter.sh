# a11y_scan_starter.sh: seven markup checks an automated audit makes, with curl and grep (Session 16, Lesson 8.3, lab B)
# state: after:lesson_27
# expect: /find-a-book/  lang=en-US  main=1  h1=TODO
#
# axe and Lighthouse check hundreds of rules in a browser; a few of the most useful need nothing but the HTML.
# This report checks four pages: the page language, one main landmark, exactly one h1, images without an alt
# attribute, the skip link, whether the store notice is a landmark, and a <ul> directly inside a <ul> (Lesson 8.3's
# "list" finding). From your project folder:
#     cp labs/module-16/l8_3-i18n-a11y-distribution/a11y_scan_starter.sh wordpress/
#     docker compose run --rm wpcli sh a11y_scan_starter.sh
# The language and the main landmark are done for you. Replace each TODO value with a grep on the saved page
# (grep -o '...' | wc -l counts matches; grep -q '...' answers yes or no in an if). Run again after each one, and
# compare with "Expected when done" at the end. Then predict: which columns change after Lesson 8.3's project?
# When you are done: rm wordpress/a11y_scan_starter.sh

for page in / /books/dune/ /find-a-book/ /events/; do
	# One line per page: WordPress breaks some tags over several lines, and grep reads line by line.
	curl -s "http://localhost:8080$page" | tr '\n' ' ' > /tmp/pagesco-a11y.html
	lang=$(grep -o '<html lang="[^"]*"' /tmp/pagesco-a11y.html | cut -d'"' -f2)
	main=$(grep -o '<main[ >]' /tmp/pagesco-a11y.html | wc -l)
	# TODO 1: how many <h1 tags (followed by a space or >)?
	h1=TODO
	# TODO 2: how many <img tags have no alt= attribute? (grep -o the tags, then grep -v -c ' alt=')
	noalt=TODO
	# TODO 3: yes when the page has the skip link (id="wp-skip-link"), else no
	skip=TODO
	# TODO 4: yes when the store notice <div class="pagesco-notice" ...> has role="region", else no
	notice=TODO
	# TODO 5: yes when the Navigation's list (<ul class="wp-block-navigation__container ...>) starts with another <ul
	nested=TODO
	printf '%-14s lang=%s  main=%s  h1=%s  img-no-alt=%s  skip-link=%s  notice-landmark=%s  nested-list=%s\n' \
		"$page" "$lang" "$main" "$h1" "$noalt" "$skip" "$notice" "$nested"
done
rm /tmp/pagesco-a11y.html
echo "Not checked here, and never by a machine alone: alt texts that describe, focus you can see, a screen reader."

# Expected when done (a11y_scan_solution.sh, the course site after Lesson 8.2):
# /              lang=en-US  main=1  h1=1  img-no-alt=0  skip-link=yes  notice-landmark=no  nested-list=yes
# /books/dune/   lang=en-US  main=1  h1=1  img-no-alt=0  skip-link=yes  notice-landmark=no  nested-list=yes
# /find-a-book/  lang=en-US  main=1  h1=1  img-no-alt=0  skip-link=yes  notice-landmark=no  nested-list=yes
# /events/       lang=en-US  main=1  h1=1  img-no-alt=0  skip-link=yes  notice-landmark=no  nested-list=yes
# Not checked here, and never by a machine alone: alt texts that describe, focus you can see, a screen reader.

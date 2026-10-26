# test_title_parts.sh: asks the site for three pages and prints their <title> (Session 3, Lesson 2.3, lab C)
# serve: title_parts
# install: mu-plugin
# state: after:lesson_04
# expect-starter: <title>Pages &amp; Co. &#8211; TODO</title>
# expect-solution: <title>Pages &amp; Co. &#8211; Independent bookstore since 1998</title>
# expect-solution: <title>News: Book club: Dune &#8211; Pages &amp; Co.</title>
#
# From your project folder, with pagesco-title.php copied into wordpress/wp-content/mu-plugins/:
#     cp labs/module-03/l2_3-hooks/test_title_parts.sh wordpress/
#     docker compose run --rm wpcli sh test_title_parts.sh
# When you are done: rm wordpress/test_title_parts.sh wordpress/wp-content/mu-plugins/pagesco-title.php

for pagesco_path in / /book-club-dune/ /hello-world/ /about/; do
	printf '%-17s ' "$pagesco_path"
	curl -s "http://localhost:8080$pagesco_path" | grep -o '<title>.*</title>'
done

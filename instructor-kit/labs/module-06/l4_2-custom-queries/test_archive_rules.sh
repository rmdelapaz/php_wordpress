# test_archive_rules.sh: the main query's lists, and the queries that must stay untouched (Session 6, Lesson 4.2, lab B)
# serve: archive_rules
# install: mu-plugin
# state: after:lesson_11
# expect-starter: /author/maria/      200  Book club: Dune | Welcome to the new Pages &#038; Co. website
# expect-starter: /2026/09/page/2/    404  (no list)
# expect-solution: /author/maria/      200  Welcome to the new Pages &#038; Co. website | Book club: Dune
# expect-solution: /2026/09/page/2/    200  Welcome to the new Pages &#038; Co. website
# expect-solution: WP-CLI post list:   4 posts
# expect-solution: a September box:    2 posts
#
# Requests three archive pages with curl and prints the titles each list shows, then runs two queries that are NOT the
# main query: WP-CLI's post list and a secondary WP_Query for September (it is a date query too, so an unguarded
# rule 3 would cut it to one post). From your project
# folder, with the must-use plugin installed:
#     cp labs/module-06/l4_2-custom-queries/archive_rules_starter/pagesco-archive-rules.php wordpress/wp-content/mu-plugins/
#     cp labs/module-06/l4_2-custom-queries/test_archive_rules.sh wordpress/
#     docker compose run --rm wpcli sh test_archive_rules.sh
# When you are done: rm wordpress/test_archive_rules.sh wordpress/wp-content/mu-plugins/pagesco-archive-rules.php

for url in /author/maria/ /2026/09/ /2026/09/page/2/; do
	code=$(curl -s -o /dev/null -w '%{http_code}' "http://localhost:8080$url")
	titles=$(curl -s "http://localhost:8080$url" | grep -o 'class="entry-title"><a [^>]*>[^<]*' | sed 's/.*>//' | sed ':a;N;$!ba;s/\n/ | /g')
	printf '%-19s %s  %s\n' "$url" "$code" "${titles:-(no list)}"
done
echo "WP-CLI post list:   $(wp post list --post_type=post --format=count) posts"
echo "a September box:    $(wp eval '$pagesco_q = new WP_Query( array( "year" => 2026, "monthnum" => 9 ) ); echo $pagesco_q->post_count;') posts (a secondary query: must stay 2)"

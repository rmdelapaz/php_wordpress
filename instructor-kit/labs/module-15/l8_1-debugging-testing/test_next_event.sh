# test_next_event.sh: lints the must-use plugin with the plugin's own ruleset, then asks for the page (Session 15, Lesson 8.1, lab B)
# serve: next_event
# install: mu-plugin
# state: after:lesson_26
# expect-starter: Next event: Book club: Dune
# expect-solution: PHPCS: no findings
# expect-solution: <p class="pagesco-next-event">Next event: Book club: Dune</p>
#
# Lesson 8.1's ruleset (phpcs.xml.dist in the plugin's folder) on one file outside the plugin: PHPCS runs in the
# WP-CLI container, which has PHP. From your project folder, after Lesson 8.1's Step 2 (composer update):
#     cp labs/module-15/l8_1-debugging-testing/next_event_starter/pagesco-books-next-event.php wordpress/wp-content/mu-plugins/
#     cp labs/module-15/l8_1-debugging-testing/test_next_event.sh wordpress/
#     docker compose run --rm wpcli sh test_next_event.sh
# Edit wordpress/wp-content/mu-plugins/pagesco-books-next-event.php until PHPCS has no findings.
# When you are done: rm wordpress/test_next_event.sh wordpress/wp-content/mu-plugins/pagesco-books-next-event.php

echo "PHPCS with the plugin's ruleset:"
cd wp-content/plugins/pagesco-books
php vendor/bin/phpcs -q --report-width=110 --basepath=/var/www/html/wp-content ../../mu-plugins/pagesco-books-next-event.php > /tmp/pagesco-phpcs.txt && echo "PHPCS: no findings"
grep -v -e '^Time:' -e '^$' /tmp/pagesco-phpcs.txt
rm /tmp/pagesco-phpcs.txt
cd ../../..
echo "The footer line, as a visitor gets it:"
curl -s http://localhost:8080/ | grep -o '<p class="pagesco-next-event">[^<]*</p>' || echo "(none: is the file in wp-content/mu-plugins/?)"

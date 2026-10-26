# test_store_hours.sh: asks the site for its home page and reads the debug log (Session 1, Lesson 1.2, lab B)
# serve: store_hours
# install: mu-plugin
# state: fresh
# expect-starter: Open Saturday: TODO
# expect-solution: Open Saturday: 10:00-16:00
# expect-solution: pagesco-hours: footer printed
#
# The test plays the browser: curl requests the page from inside the containers, as Lesson 1.1 did. From your
# project folder, with pagesco-hours.php copied into wordpress/wp-content/mu-plugins/:
#     cp labs/module-01/l1_2-local-environment/test_store_hours.sh wordpress/
#     docker compose run --rm wpcli sh test_store_hours.sh
# When you are done: rm wordpress/test_store_hours.sh wordpress/wp-content/mu-plugins/pagesco-hours.php

echo "Home page, the plugin's paragraph:"
curl -s http://localhost:8080/ | grep -o '<p class="pagesco-hours">[^<]*</p>' || echo "(none: is pagesco-hours.php in wp-content/mu-plugins/?)"
echo "debug.log, the plugin's lines (without the time stamps):"
if [ -f wp-content/debug.log ] && grep -q 'pagesco-hours:' wp-content/debug.log; then
	grep 'pagesco-hours:' wp-content/debug.log | sed 's/^\[[^]]*\] //' | sort | uniq -c
else
	echo "(none yet)"
fi

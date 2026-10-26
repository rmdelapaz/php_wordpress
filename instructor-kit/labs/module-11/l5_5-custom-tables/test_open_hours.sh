# test_open_hours.sh: four ways to write the shortcode, run through do_shortcode() (Session 11, Lesson 5.5, lab B)
# serve: open_hours
# install: mu-plugin
# state: after:lesson_17
# expect-starter: <ul class="pagesco-hours">
# expect-solution: [pagesco_open_hours day="SATURDAY"] => '<span class="pagesco-hours">Saturday: 10:00-16:00</span>'
# expect-solution: [pagesco_open_hours day="holiday"] => ''
#
# Each line prints the shortcode as an editor would type it, then exactly what do_shortcode() returned, in quotes.
# Anything printed BEFORE "=>" did not come back from the callback: it was echoed. From your project folder, with
# the plugin file copied into wordpress/wp-content/mu-plugins/:
#     cp labs/module-11/l5_5-custom-tables/open_hours_starter/pagesco-lab-hours-shortcode.php wordpress/wp-content/mu-plugins/
#     cp labs/module-11/l5_5-custom-tables/test_open_hours.sh wordpress/
#     docker compose run --rm wpcli sh test_open_hours.sh
# When you are done: rm wordpress/test_open_hours.sh wordpress/wp-content/mu-plugins/pagesco-lab-hours-shortcode.php

wp eval 'foreach ( array( "[pagesco_open_hours day=\"saturday\"]", "[pagesco_open_hours day=\"SATURDAY\"]", "[pagesco_open_hours day=\"holiday\"]", "[pagesco_open_hours]" ) as $pagesco_case ) {
	echo $pagesco_case, " => ";
	$pagesco_html = do_shortcode( $pagesco_case );
	echo "\x27", $pagesco_html, "\x27\n";
}'

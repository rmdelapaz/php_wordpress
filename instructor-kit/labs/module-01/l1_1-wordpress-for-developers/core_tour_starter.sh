# core_tour_starter.sh: read the front door of WordPress yourself (Session 1, Lesson 1.1, lab A)
# state: fresh
# expect: TODO 2
#
# Lesson 1.1 followed one request: index.php, wp-blog-header.php, wp-load.php, wp-config.php, wp-settings.php,
# wp(), template-loader.php. This script finds the lines in core that do each step, with grep -n (line numbers).
# It runs in the WP-CLI container, in the WordPress root. From your project folder:
#     cp labs/module-01/l1_1-wordpress-for-developers/core_tour_starter.sh wordpress/
#     docker compose run --rm wpcli sh core_tour_starter.sh
# Step 1 is done for you. For each TODO, replace the echo line with a grep that prints the line the comment
# describes (edit wordpress/core_tour_starter.sh, save, run again). Reading is all it does: never edit core.
# When you are done: rm wordpress/core_tour_starter.sh

echo "1. wp-load.php loads your settings file:"
grep -n "require_once ABSPATH . 'wp-config.php'" wp-load.php

echo "2. wp-settings.php runs every must-use plugin:"
# TODO 2: in wp-settings.php, find the foreach line that loops over wp_get_mu_plugins().
echo "TODO 2"

echo "3. wp-settings.php fires plugins_loaded, then init:"
# TODO 3: ONE grep with two patterns joined by \| finds both do_action lines (search for "do_action( 'init' )").
echo "TODO 3"

echo "4. template-loader.php: the last chance to redirect, then the filter that can swap the template:"
# TODO 4: in wp-includes/template-loader.php, find the do_action() of template_redirect and the apply_filters()
#         of template_include (a plain grep for template_include also finds a comment: make the pattern exact).
echo "TODO 4"

echo "5. PHP files in wp-includes, the core library:"
# TODO 5: count them: find lists files by name, wc -l counts lines.
echo "TODO 5"

# Expected when done (core_tour_solution.sh, WordPress 7.1.3):
# 1. wp-load.php loads your settings file:
# 50:	require_once ABSPATH . 'wp-config.php';
# 2. wp-settings.php runs every must-use plugin:
# 506:foreach ( wp_get_mu_plugins() as $mu_plugin ) {
# 3. wp-settings.php fires plugins_loaded, then init:
# 630:do_action( 'plugins_loaded' );
# 779:do_action( 'init' );
# 4. template-loader.php: the last chance to redirect, then the filter that can swap the template:
# 23:	do_action( 'template_redirect' );
# 114:	$template   = apply_filters( 'template_include', $template );
# 5. PHP files in wp-includes, the core library:
# 1059

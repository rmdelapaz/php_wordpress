# core_tour_solution.sh: the instructor's reference for core_tour_starter.sh (Session 1, Lesson 1.1, lab A)
# state: fresh
# expect: 506:foreach ( wp_get_mu_plugins() as $mu_plugin ) {
# expect: 779:do_action( 'init' );

echo "1. wp-load.php loads your settings file:"
grep -n "require_once ABSPATH . 'wp-config.php'" wp-load.php

echo "2. wp-settings.php runs every must-use plugin:"
grep -n "foreach ( wp_get_mu_plugins()" wp-settings.php

echo "3. wp-settings.php fires plugins_loaded, then init:"
grep -n "do_action( 'plugins_loaded' )\|do_action( 'init' )" wp-settings.php

echo "4. template-loader.php: the last chance to redirect, then the filter that can swap the template:"
grep -n "do_action( 'template_redirect' )\|apply_filters( 'template_include'" wp-includes/template-loader.php

echo "5. PHP files in wp-includes, the core library:"
find wp-includes -name '*.php' | wc -l

# test_gift_wrap.sh: the gift-wrap plugin's whole life cycle, from the outside (Session 9, Lesson 5.1, lab A)
# serve: gift_wrap
# install: plugin pagesco-gift-wrap
# state: after:lesson_13
# expect-starter: requires WordPress TODO, PHP TODO
# expect-starter: direct request: 500
# expect-solution: requires WordPress 6.8, PHP 8.2
# expect-solution: direct request: 200
# expect-solution: Gift wrapping: $2.50.
# expect-solution: after uninstall: (not stored)
#
# Install the folder as a plugin, activate it (that runs the activation hook), then run this test. From your
# project folder:
#     cp -r labs/module-09/l5_1-first-plugin/gift_wrap_starter wordpress/wp-content/plugins/pagesco-gift-wrap
#     wp plugin activate pagesco-gift-wrap
#     cp labs/module-09/l5_1-first-plugin/test_gift_wrap.sh wordpress/
#     docker compose run --rm wpcli sh test_gift_wrap.sh
# The test ends with the uninstall procedure (deactivate + uninstall.php, files kept). Then remove both:
#     rm -r wordpress/wp-content/plugins/pagesco-gift-wrap wordpress/test_gift_wrap.sh

wp eval 'require_once ABSPATH . "wp-admin/includes/plugin.php";
$pagesco_d = get_plugin_data( WP_PLUGIN_DIR . "/pagesco-gift-wrap/pagesco-gift-wrap.php", false, false );
printf( "header: requires WordPress %s, PHP %s\n", $pagesco_d["RequiresWP"] ? $pagesco_d["RequiresWP"] : "TODO", $pagesco_d["RequiresPHP"] ? $pagesco_d["RequiresPHP"] : "TODO" );'
echo "direct request: $(curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/wp-content/plugins/pagesco-gift-wrap/pagesco-gift-wrap.php)"
echo "stored price: $(wp eval 'echo get_option( "pagesco_gift_wrap_price", "(not stored)" );')"
echo "notice:"
curl -s http://localhost:8080/ | grep -o '<div class="pagesco-notice">.*</div>'
wp plugin uninstall pagesco-gift-wrap --deactivate --skip-delete
echo "after uninstall: $(wp eval 'echo get_option( "pagesco_gift_wrap_price", "(not stored)" );')"

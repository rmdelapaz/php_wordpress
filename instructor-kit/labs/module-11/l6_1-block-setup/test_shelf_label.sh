# test_shelf_label.sh: what WordPress knows about the Shelf Label block, and what a visitor gets (Session 11,
# Lesson 6.1, lab A)
# serve: shelf_label
# install: plugin pagesco-shelf-label
# state: after:lesson_18
# expect-starter: pagesco/shelf-label: not registered
# expect-starter: front end: 0 stylesheet(s)
# expect-solution: Shelf Label (text, icon tag)
# expect-solution: keywords: shelf, sign
# expect-solution: front end: 1 stylesheet(s)
#
# Install the folder as a plugin (its build/ is prebuilt), activate it, then run the test. From your project folder:
#     cp -r labs/module-11/l6_1-block-setup/shelf_label_starter wordpress/wp-content/plugins/pagesco-shelf-label
#     wp plugin activate pagesco-shelf-label
#     cp labs/module-11/l6_1-block-setup/test_shelf_label.sh wordpress/
#     docker compose run --rm wpcli sh test_shelf_label.sh
# The test creates one post that uses the block and deletes it again. When you are done:
#     wp plugin deactivate pagesco-shelf-label
#     rm -r wordpress/wp-content/plugins/pagesco-shelf-label wordpress/test_shelf_label.sh

wp eval '$pagesco_type = WP_Block_Type_Registry::get_instance()->get_registered( "pagesco/shelf-label" );
if ( ! $pagesco_type ) {
	echo "pagesco/shelf-label: not registered\n";
} else {
	echo $pagesco_type->title, " (", $pagesco_type->category, ", icon ", $pagesco_type->icon, ")\n";
	echo "keywords: ", $pagesco_type->keywords ? implode( ", ", $pagesco_type->keywords ) : "(none)", "\n";
	echo "handles: ", implode( ", ", array_merge( $pagesco_type->editor_script_handles, $pagesco_type->style_handles ) ), "\n";
}'
POST=$(wp post create --post_title="Shelf test" --post_status=publish --porcelain --post_content='<!-- wp:pagesco/shelf-label -->
<p class="wp-block-pagesco-shelf-label">Staff picks</p>
<!-- /wp:pagesco/shelf-label -->')
echo "front end: $(curl -sL "http://localhost:8080/?p=$POST" | grep -c 'id="pagesco-shelf-label-style-inline-css"') stylesheet(s)"
curl -sL "http://localhost:8080/?p=$POST" | grep -o '<p class="wp-block-pagesco-shelf-label">[^<]*</p>'
wp post delete "$POST" --force > /dev/null

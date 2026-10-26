<?php
/**
 * test_next_events.php: renders four Next Events blocks the way a page view does (Session 12, Lesson 6.3, lab A)
 * serve: next_events
 * install: plugin pagesco-next-events
 * state: after:lesson_20
 * expect-starter: <p class="wp-block-pagesco-next-events">TODO: the next events</p>
 * expect-solution: <li><time datetime="2027-11-04T19:00">Nov 4</time> Book club: Dune</li>
 * expect-solution: <p class="wp-block-pagesco-next-events">No events at this location yet.</p>
 * expect-solution: count 99: 6 events
 *
 * A dynamic block stores only its comment; do_blocks() runs render.php with the comment's attributes, exactly as
 * a page view does. From your project folder, with the plugin folder copied and activated:
 *     cp -r labs/module-12/l6_3-dynamic-blocks/next_events_starter wordpress/wp-content/plugins/pagesco-next-events
 *     wp plugin activate pagesco-next-events
 *     cp labs/module-12/l6_3-dynamic-blocks/test_next_events.php wordpress/
 *     wp eval-file --use-include test_next_events.php
 * When you are done: wp plugin deactivate pagesco-next-events, then
 *     rm -r wordpress/wp-content/plugins/pagesco-next-events wordpress/test_next_events.php
 */
$pagesco_comments = array(
	'no attributes' => '<!-- wp:pagesco/next-events /-->',
	'2 at the Café' => '<!-- wp:pagesco/next-events {"count":2,"location":"Café"} /-->',
	'rooftop'       => '<!-- wp:pagesco/next-events {"location":"Rooftop"} /-->',
);
foreach ( $pagesco_comments as $pagesco_label => $pagesco_comment ) {
	echo "== {$pagesco_label}\n", trim( do_blocks( $pagesco_comment ) ), "\n";
}
echo 'count 99: ', substr_count( do_blocks( '<!-- wp:pagesco/next-events {"count":99} /-->' ), '<li>' ), " events\n";

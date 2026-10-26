<?php
/**
 * debug_block_registration.php: three block types registered with three bugs (Session 11, Lesson 6.1,
 * find-the-bug handout)
 * state: after:lesson_18
 * expect-error: doing_it_wrong
 *
 * A quick test of three block names before they get a block.json each: a sale badge, a gift card and a reading
 * list, registered in PHP for this one run (nothing is stored), then a report of what the registry holds.
 * From your project folder:
 *     cp labs/module-11/l6_1-block-setup/debug_block_registration.php wordpress/
 *     wp eval-file --use-include debug_block_registration.php
 * WordPress reports two of the bugs ("called incorrectly"). The third is SILENT: read the report against
 * Lesson 6.1's table of block.json fields. Fix all three; when you are done: rm wordpress/debug_block_registration.php
 */
$pagesco_registry = WP_Block_Type_Registry::get_instance();
register_block_type(
	'pagesco/Sale-Badge',
	array(
		'title'       => 'Sale badge',
		'category'    => 'widgets',
		'api_version' => 3,
	)
);
register_block_type(
	'pagesco-gift-card',
	array(
		'title'       => 'Gift card',
		'category'    => 'widgets',
		'api_version' => 3,
	)
);
register_block_type(
	'pagesco/reading-list',
	array(
		'title'       => 'Reading list',
		'category'    => 'widgets',
		'api_version' => 2,
	)
);
foreach ( array( 'pagesco/sale-badge', 'pagesco/gift-card', 'pagesco/reading-list' ) as $pagesco_name ) {
	$pagesco_type = $pagesco_registry->get_registered( $pagesco_name );
	echo $pagesco_name, ': ', $pagesco_type ? "registered, apiVersion {$pagesco_type->api_version}" : 'NOT registered', "\n";
}

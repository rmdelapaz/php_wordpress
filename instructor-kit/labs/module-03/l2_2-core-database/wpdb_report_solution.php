<?php
/**
 * wpdb_report_solution.php: the instructor's reference for wpdb_report_starter.php (Session 3, Lesson 2.2, lab B)
 * state: after:lesson_04
 * expect: Comments (SQL): 1
 * expect: Maria's pages: about, contact, events
 */
global $wpdb;

echo 'Prefix: ', $wpdb->prefix, "\n";

echo 'Comments (SQL): ', $wpdb->get_var( "SELECT COUNT(*) FROM {$wpdb->comments}" ), "\n";
echo 'Comments (API): ', wp_count_comments()->total_comments, "\n";

$pagesco_slugs = $wpdb->get_col(
	$wpdb->prepare(
		"SELECT post_name FROM {$wpdb->posts} WHERE post_type = 'page' AND post_status = 'publish' AND post_author = %d ORDER BY ID",
		2
	)
);
echo "Maria's pages: ", implode( ', ', $pagesco_slugs ), "\n";

$pagesco_row = $wpdb->get_row(
	$wpdb->prepare( "SELECT option_value, autoload FROM {$wpdb->options} WHERE option_name = %s", 'permalink_structure' )
);
echo 'permalink_structure: ', $pagesco_row->option_value, ' (autoload ', $pagesco_row->autoload, ")\n";

echo 'Autoload values WordPress loads: ', implode( ', ', wp_autoload_values_to_autoload() ), "\n";

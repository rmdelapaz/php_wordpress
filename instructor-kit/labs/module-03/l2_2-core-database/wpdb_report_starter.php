<?php
/**
 * wpdb_report_starter.php: four questions for $wpdb, each checked against the WordPress API (Session 3, Lesson 2.2, lab B)
 * state: after:lesson_04
 * expect: Comments (SQL): TODO
 *
 * Lesson 2.2's project asked $wpdb for a report with get_results(). $wpdb has a method for every shape of answer:
 * get_var() one value, get_col() one column, get_row() one row, get_results() many rows. From your project folder:
 *     cp labs/module-03/l2_2-core-database/wpdb_report_starter.php wordpress/
 *     wp eval-file --use-include wpdb_report_starter.php
 * Rules from the lesson: table names come from $wpdb ({$wpdb->posts}, never wp_posts), and every value goes in
 * through $wpdb->prepare() (%d for a number, %s for a string). Replace each TODO, run again, compare with
 * "Expected when done" at the end. When you are done: rm wordpress/wpdb_report_starter.php
 */
global $wpdb;

echo 'Prefix: ', $wpdb->prefix, "\n";   // done for you

// TODO 1: the number of rows in the comments table, with $wpdb->get_var() and {$wpdb->comments}.
echo "Comments (SQL): TODO\n";
// TODO 2: the same number from the API: wp_count_comments() returns an object; read its total_comments.
echo "Comments (API): TODO\n";

// TODO 3: with $wpdb->get_col() and $wpdb->prepare(): the slugs (post_name) of the PUBLISHED pages whose
//         post_author is 2 (Maria; pass the 2 through %d), oldest ID first. Print them joined with ', '.
echo "Maria's pages: TODO\n";

// TODO 4: with $wpdb->get_row() and prepare(): the option_value and autoload columns of the option named
//         permalink_structure (%s). Print: permalink_structure: <value> (autoload <autoload>)
echo "permalink_structure: TODO\n";

// TODO 5: the list of autoload values WordPress treats as "load it": wp_autoload_values_to_autoload() (an array).
echo "Autoload values WordPress loads: TODO\n";

// Expected when done (wpdb_report_solution.php, the site after Lesson 2.1):
// Prefix: wp_
// Comments (SQL): 1
// Comments (API): 1
// Maria's pages: about, contact, events
// permalink_structure: /%postname%/ (autoload on)
// Autoload values WordPress loads: yes, on, auto-on, auto

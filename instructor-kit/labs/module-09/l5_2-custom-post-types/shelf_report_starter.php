<?php
/**
 * shelf_report_starter.php: four questions about the catalog, asked in PHP (Session 9, Lesson 5.2, lab B)
 * state: after:lesson_15
 * expect: Cheapest in stock: TODO
 *
 * Run it on your site after the lesson project (eleven books, five genres). It reads only: nothing is changed.
 * From your project folder:
 *     cp labs/module-09/l5_2-custom-post-types/shelf_report_starter.php wordpress/
 *     wp eval-file --use-include shelf_report_starter.php
 * Replace each TODO with the query its comment describes (Lesson 4.2's WP_Query arguments work in get_posts()),
 * run again, and compare with "Expected when done" at the end. When you are done: rm wordpress/shelf_report_starter.php
 */

// 1. Done for you: every genre with the number of books filed under it (the term's count column).
foreach ( get_terms( array( 'taxonomy' => 'genre', 'hide_empty' => false, 'orderby' => 'term_id' ) ) as $pagesco_term ) {
	printf( "%-16s %d\n", $pagesco_term->name . ':', $pagesco_term->count );
}

// TODO 2: the cheapest book that is IN STOCK: get_posts() with a meta_query on pagesco_in_stock = '1' and
// 'meta_key' => 'pagesco_price', 'orderby' => 'meta_value_num', 'order' => 'ASC', 'numberposts' => 1.
// Print its title and price: "Cheapest in stock: Pride and Prejudice ($7.99)".
echo "Cheapest in stock: TODO\n";

// TODO 3: the average price of all eleven books, two decimals (array_map() over get_post_meta(), then
// array_sum() / count(); number_format()).
echo "Average price: TODO\n";

// TODO 4: how many books were first published before 1950? A meta_query on pagesco_published with
// 'compare' => '<' and 'type' => 'DATE' (the values are Y-m-d strings). Count them with 'fields' => 'ids'.
echo "Published before 1950: TODO\n";

// Expected when done (shelf_report_solution.php, the catalog after Lesson 5.2):
// Fiction:         11
// Science Fiction: 3
// Classic:         6
// Fantasy:         2
// Dystopian:       3
// Cheapest in stock: Pride and Prejudice ($7.99)
// Average price: $10.76
// Published before 1950: 6

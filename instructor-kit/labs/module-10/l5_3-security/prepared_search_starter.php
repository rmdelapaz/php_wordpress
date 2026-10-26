<?php
/**
 * prepared_search_starter.php: three hand-written queries, every value through a placeholder (Session 10,
 * Lesson 5.3, lab B)
 * state: after:lesson_15
 * expect: TODO
 *
 * Lesson 5.3's rule: no variable ever goes directly into a query string. Each search below receives its value as a
 * visitor would type it. Build each query with $wpdb->prepare(), print the SQL prepare() produced, then the
 * result. It only reads. From your project folder:
 *     cp labs/module-10/l5_3-security/prepared_search_starter.php wordpress/
 *     wp eval-file --use-include prepared_search_starter.php
 * When you are done: rm wordpress/prepared_search_starter.php
 */
global $wpdb;

// 1. Books cheaper than a price typed as text. Done for you: %f turns '9.99' into a number.
$pagesco_max = '9.99';
$pagesco_sql = $wpdb->prepare(
	"SELECT COUNT(*) FROM {$wpdb->postmeta} WHERE meta_key = %s AND meta_value + 0 < %f",
	'pagesco_price',
	$pagesco_max
);
echo $pagesco_sql, "\n=> ", $wpdb->get_var( $pagesco_sql ), " books under \${$pagesco_max}\n";

// TODO 2: the titles of the books whose author CONTAINS a typed word: join wp_posts and wp_postmeta on
// pagesco_author, compare with LIKE %s, and pass '%' . $wpdb->esc_like( $pagesco_word ) . '%' as the value
// (esc_like() escapes % and _ inside the word; prepare() then quotes it). Order by the title. Print the SQL with
// $wpdb->remove_placeholder_escape( $sql ): prepare() hides every literal % behind a long random string until the
// query runs, and that function shows the SQL as MySQL receives it.
$pagesco_word = 'Tolkien';
echo "TODO\n";

// TODO 3: the same query with a hostile word. Print the SQL and the number of rows: the quote is escaped,
// so the OR never becomes SQL.
$pagesco_word = "x' OR '1'='1";
echo "TODO\n";

// Expected when done (prepared_search_solution.php):
// SELECT COUNT(*) FROM wp_postmeta WHERE meta_key = 'pagesco_price' AND meta_value + 0 < 9.990000
// => 5 books under $9.99
// SELECT p.post_title FROM wp_posts p INNER JOIN wp_postmeta m ON m.post_id = p.ID WHERE p.post_type = 'book' AND m.meta_key = 'pagesco_author' AND m.meta_value LIKE '%Tolkien%' ORDER BY p.post_title
// => Lord of the Rings, The Hobbit
// SELECT p.post_title FROM wp_posts p INNER JOIN wp_postmeta m ON m.post_id = p.ID WHERE p.post_type = 'book' AND m.meta_key = 'pagesco_author' AND m.meta_value LIKE '%x\' OR \'1\'=\'1%' ORDER BY p.post_title
// => 0 rows

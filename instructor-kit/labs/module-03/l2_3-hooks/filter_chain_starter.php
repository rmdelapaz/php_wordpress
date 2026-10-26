<?php
/**
 * filter_chain_starter.php: three callbacks on one filter, in the right order (Session 3, Lesson 2.3, lab A)
 * state: after:lesson_04
 * expect: Line: fahrenheit 451 [SALE]
 *
 * The bookstore prints a "book line" through its own filter, pagesco_lab_book_line, which passes two values:
 * the title and the author. Lesson 2.3's priorities, accepted arguments and removal rules, on one hook.
 * From your project folder:
 *     cp labs/module-03/l2_3-hooks/filter_chain_starter.php wordpress/
 *     wp eval-file --use-include filter_chain_starter.php
 * Do the TODOs in order and run the file after each one. Compare with "Expected when done" at the end.
 * When you are done: rm wordpress/filter_chain_starter.php
 */

// Already in the site: a "plugin" that marks every book line as on sale. Do not edit these three lines.
function pagesco_lab_sale_badge( $line ) {
	return $line . ' [SALE]';
}
add_filter( 'pagesco_lab_book_line', 'pagesco_lab_sale_badge', 30 );

// TODO 1: a function pagesco_lab_capitalize( $line ) that returns ucwords( $line ), added at priority 5.

// TODO 2: a function pagesco_lab_add_author( $line, $author ) that returns the line plus ' by ' and the author,
//         added at the default priority. It needs BOTH values of the hook: what does add_filter() need to know?

// TODO 3: the sale is over. Remove pagesco_lab_sale_badge and print what remove_filter() returned
//         (var_export( ..., true ) prints true or false).
echo "Removed the sale badge: TODO\n";

// TODO 4: ask the hook which priority each of the three callbacks has now: has_filter( hook, callback ),
//         printed with var_export() like TODO 3, one line each, in the order of the expected output.
echo "pagesco_lab_capitalize: TODO\n";

echo 'Line: ', apply_filters( 'pagesco_lab_book_line', 'fahrenheit 451', 'Ray Bradbury' ), "\n";

// Expected when done (filter_chain_solution.php):
// Removed the sale badge: true
// pagesco_lab_capitalize: 5
// pagesco_lab_add_author: 10
// pagesco_lab_sale_badge: false
// Line: Fahrenheit 451 by Ray Bradbury

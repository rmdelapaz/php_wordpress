<?php
/**
 * diagnostic_starter.php: three of the Start Here questions, answered by PHP (Session 1, practice at home)
 * state: fresh
 * expect: D1  PHP says: 3 Emma
 *
 * The workbook's diagnostic asked six questions on what this course builds on. D1, D2 and D6 are PHP, so PHP
 * can answer them. Run this file like every PHP lab, from your project folder:
 *     cp labs/module-01/l1_0-orientation/diagnostic_starter.php wordpress/
 *     wp eval-file --use-include diagnostic_starter.php
 * As shipped, each answer has one small gap (a TODO). Fix the three gaps one at a time, run again after each,
 * and compare with your workbook answers. Then delete the copy: rm wordpress/diagnostic_starter.php
 */

// D1: an associative array, counted, and its FIRST key.
$pagesco_books = array(
	'Dune' => 14.99,
	'1984' => 9.99,
	'Emma' => 7.99,
);
// TODO 1: the question asks for the first key. Which function gives the first key, not the last?
echo 'D1  PHP says: ', count( $pagesco_books ), ' ', array_key_last( $pagesco_books ), "\n";

// D2: a visitor typed this into a form. What must reach the browser so it shows as text, not as bold HTML?
$pagesco_name = '<b>Maya</b>';
// TODO 2: escape the value for HTML before printing it (PHP Foundations, Lesson 4.2).
echo 'D2  PHP says: Hello, ', $pagesco_name, "\n";

// D6: a function passed BY NAME to another function (a callback). WordPress hooks work exactly like this.
function pagesco_shout( $text ) {
	return strtoupper( $text ) . '!';
}
// TODO 3: array_map() should call pagesco_shout on every title, not strtolower.
echo 'D6  PHP says: ', implode( ' ', array_map( 'strtolower', array( 'Dune', 'Emma' ) ) ), "\n";

// Expected when done (diagnostic_solution.php):
// D1  PHP says: 3 Dune
// D2  PHP says: Hello, &lt;b&gt;Maya&lt;/b&gt;
// D6  PHP says: DUNE! EMMA!

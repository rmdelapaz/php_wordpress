<?php
/**
 * diagnostic_solution.php: the instructor's reference for diagnostic_starter.php (Session 1)
 * state: fresh
 * expect: D1  PHP says: 3 Dune
 * expect: D2  PHP says: Hello, &lt;b&gt;Maya&lt;/b&gt;
 * expect: D6  PHP says: DUNE! EMMA!
 */

// D1: count() counts the entries; array_key_first() is the first key (PHP 7.3+).
$pagesco_books = array(
	'Dune' => 14.99,
	'1984' => 9.99,
	'Emma' => 7.99,
);
echo 'D1  PHP says: ', count( $pagesco_books ), ' ', array_key_first( $pagesco_books ), "\n";

// D2: htmlspecialchars() turns < and > into entities; the browser shows them as text. (WordPress: esc_html().)
$pagesco_name = '<b>Maya</b>';
echo 'D2  PHP says: Hello, ', htmlspecialchars( $pagesco_name ), "\n";

// D6: the callback is passed by its name as a string; array_map() calls it once per item.
function pagesco_shout( $text ) {
	return strtoupper( $text ) . '!';
}
echo 'D6  PHP says: ', implode( ' ', array_map( 'pagesco_shout', array( 'Dune', 'Emma' ) ) ), "\n";

<?php
/**
 * prepared_search_solution.php: three hand-written queries, every value through a placeholder (Session 10,
 * Lesson 5.3, lab B, reference)
 * state: after:lesson_15
 * expect: => Lord of the Rings, The Hobbit
 * expect: => 0 rows
 */
global $wpdb;

// 1. Books cheaper than a price typed as text: %f turns '9.99' into a number.
$pagesco_max = '9.99';
$pagesco_sql = $wpdb->prepare(
	"SELECT COUNT(*) FROM {$wpdb->postmeta} WHERE meta_key = %s AND meta_value + 0 < %f",
	'pagesco_price',
	$pagesco_max
);
echo $pagesco_sql, "\n=> ", $wpdb->get_var( $pagesco_sql ), " books under \${$pagesco_max}\n";

// prepare() hides every literal % behind a long random placeholder until the query runs (so a value cannot
// smuggle in a new placeholder); remove_placeholder_escape() shows the SQL as MySQL will receive it.

/**
 * The prepared query for "books whose author contains $word" (the word is escaped for LIKE, then quoted).
 *
 * @param string $word What the visitor typed.
 * @return string
 */
function pagesco_lab_author_search( $word ) {
	global $wpdb;
	return $wpdb->prepare(
		"SELECT p.post_title FROM {$wpdb->posts} p INNER JOIN {$wpdb->postmeta} m ON m.post_id = p.ID WHERE p.post_type = %s AND m.meta_key = %s AND m.meta_value LIKE %s ORDER BY p.post_title",
		'book',
		'pagesco_author',
		'%' . $wpdb->esc_like( $word ) . '%'
	);
}

// 2. A typed word.
$pagesco_sql = pagesco_lab_author_search( 'Tolkien' );
echo $wpdb->remove_placeholder_escape( $pagesco_sql ), "\n=> ", implode( ', ', $wpdb->get_col( $pagesco_sql ) ), "\n";

// 3. A hostile word: the quotes are escaped, so the OR stays inside the string.
$pagesco_sql = pagesco_lab_author_search( "x' OR '1'='1" );
echo $wpdb->remove_placeholder_escape( $pagesco_sql ), "\n=> ", count( $wpdb->get_col( $pagesco_sql ) ), " rows\n";

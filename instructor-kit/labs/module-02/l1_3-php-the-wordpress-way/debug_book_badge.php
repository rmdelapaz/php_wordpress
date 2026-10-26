<?php
/**
 * debug_book_badge.php: a badge helper for the shop's book lists (Session 2, Lesson 1.3, find-the-bug handout)
 * state: fresh
 * expect-error: Warning, Deprecated
 *
 * A colleague wrote this helper the WordPress way (a prefix, an array of arguments, escaping) and says it is
 * finished. Run it, read every message from the left, and fix the code until it runs without one. From your
 * project folder:
 *     cp labs/module-02/l1_3-php-the-wordpress-way/debug_book_badge.php wordpress/
 *     wp eval-file --use-include debug_book_badge.php
 * There are two loud bugs and one silent one: when the messages are gone, check the output against what the
 * calls at the bottom ASK for. Then delete the copy: rm wordpress/debug_book_badge.php
 */

/**
 * Returns a book's badge line, escaped for HTML.
 *
 * @param array $book { @type string $title  @type string $author  @type float $price (optional) }
 * @param array $args { @type string $label Badge text. Default 'Staff pick'.  @type bool $show_price Default true. }
 * @return string
 */
function pagesco_lab_badge( $book, $args = array() ) {
	$args = wp_parse_args(
		array(
			'label'      => 'Staff pick',
			'show_price' => true,
		),
		$args
	);

	$html  = '<span class="pagesco-badge">' . esc_html( $args['label'] ) . '</span> ';
	$html .= '<b>' . esc_html( $book['title'] ) . '</b> by ' . esc_html( $book['autor'] );
	if ( $args['show_price'] ) {
		$html .= ' $' . number_format_i18n( $book['price'], 2 );
	}
	return $html;
}

echo pagesco_lab_badge( array( 'title' => 'The Left Hand of Darkness', 'author' => 'Ursula K. Le Guin' ) ), "\n";
echo pagesco_lab_badge(
	array(
		'title'  => 'Emma',
		'author' => 'Jane Austen',
		'price'  => 7.99,
	),
	array( 'label' => 'New in paperback' )
), "\n";

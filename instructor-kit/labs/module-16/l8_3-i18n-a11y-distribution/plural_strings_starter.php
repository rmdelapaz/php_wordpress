<?php
/**
 * plural_strings_starter.php: four strings a translator can translate, shown in English and Spanish (Session 16, Lesson 8.3, lab A)
 * state: after:lesson_27
 * expect: TODO 1 to 4: every es line should be Spanish
 *
 * A translator sent the Spanish translation for a small "catalog summary" (below, as the .l10n.php file
 * wp i18n make-php would build from her PO file). The script writes it to /tmp, loads it for the text domain
 * pagesco-lab, and prints every string twice: before loading (English) and after (Spanish). From your project folder:
 *     cp labs/module-16/l8_3-i18n-a11y-distribution/plural_strings_starter.php wordpress/
 *     wp eval-file --use-include plural_strings_starter.php
 * As shipped the es lines are still English: the code's strings are not the ones the translator translated, and
 * two of them could never be. Rewrite pagesco_lab_summary() (TODO 1 to 4) with _n(), numbered placeholders, _x()
 * and whole sentences, each with a translators comment, until every es line is Spanish. Do not change the
 * translator's file: change your code. Compare with "Expected when done" at the end.
 * When you are done: rm wordpress/plural_strings_starter.php
 */

$pagesco_file = get_temp_dir() . 'pagesco-lab-es_ES.l10n.php';
$pagesco_po   = array(
	'domain'       => 'pagesco-lab',
	'language'     => 'es_ES',
	'plural-forms' => 'nplurals=2; plural=(n != 1);',
	'messages'     => array(
		'%d book in stock'           => "%d libro disponible\0%d libros disponibles",
		'Showing %1$s of %2$s books' => 'De %2$s libros, se muestran %1$s',
		"sort order\4Order"          => 'Orden',
		"purchase order\4Order"      => 'Pedido',
		'Books in %s'                => 'Libros de %s',
	),
);
file_put_contents( $pagesco_file, '<?php return ' . var_export( $pagesco_po, true ) . ';' );

/**
 * The catalog summary: every string through a translation function, in a form a translator can work with.
 */
function pagesco_lab_summary(): string {
	$lines = array(
		// TODO 1: one string for every count, with _n( singular, plural, count, domain ) inside sprintf().
		1 . __( ' book in stock', 'pagesco-lab' ) . ' | ' . 9 . __( ' books in stock', 'pagesco-lab' ),
		// TODO 2: numbered placeholders, so a language can put the numbers in another order.
		sprintf( __( 'Showing %s of %s books', 'pagesco-lab' ), 3, 11 ),
		// TODO 3: the same English word with two meanings needs a context each (_x()).
		__( 'Order', 'pagesco-lab' ) . ' | ' . __( 'Order', 'pagesco-lab' ),
		// TODO 4: a whole sentence with a placeholder, not a fragment and the genre glued on.
		__( 'Books in ', 'pagesco-lab' ) . 'Fantasy',
	);
	return implode( "\n", $lines );
}

echo preg_replace( '/^/m', 'en  ', pagesco_lab_summary() ), "\n";
load_textdomain( 'pagesco-lab', get_temp_dir() . 'pagesco-lab-es_ES.mo' );
echo preg_replace( '/^/m', 'es  ', pagesco_lab_summary() ), "\n";

unload_textdomain( 'pagesco-lab' );
wp_delete_file( $pagesco_file );
echo "TODO 1 to 4: every es line should be Spanish\n";

// Expected when done (plural_strings_solution.php):
// en  1 book in stock | 9 books in stock
// en  Showing 3 of 11 books
// en  Order | Order
// en  Books in Fantasy
// es  1 libro disponible | 9 libros disponibles
// es  De 11 libros, se muestran 3
// es  Orden | Pedido
// es  Libros de Fantasy

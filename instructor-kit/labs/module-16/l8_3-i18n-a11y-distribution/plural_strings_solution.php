<?php
/**
 * plural_strings_solution.php: four strings a translator can translate, shown in English and Spanish (Session 16, Lesson 8.3, lab A)
 * state: after:lesson_27
 * expect: es  1 libro disponible | 9 libros disponibles
 * expect: es  De 11 libros, se muestran 3
 *
 * A translator sent the Spanish translation for a small "catalog summary" (below, as the .l10n.php file
 * wp i18n make-php would build from her PO file). The script writes it to /tmp, loads it for the text domain
 * pagesco-lab, and prints every string twice: before loading (English) and after (Spanish). From your project folder:
 *     cp labs/module-16/l8_3-i18n-a11y-distribution/plural_strings_solution.php wordpress/
 *     wp eval-file --use-include plural_strings_solution.php
 *     rm wordpress/plural_strings_solution.php
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
		sprintf(
			/* translators: %d: number of books. */
			_n( '%d book in stock', '%d books in stock', 1, 'pagesco-lab' ),
			1
		) . ' | ' . sprintf(
			/* translators: %d: number of books. */
			_n( '%d book in stock', '%d books in stock', 9, 'pagesco-lab' ),
			9
		),
		/* translators: 1: books shown, 2: books in the catalog. */
		sprintf( __( 'Showing %1$s of %2$s books', 'pagesco-lab' ), 3, 11 ),
		_x( 'Order', 'sort order', 'pagesco-lab' ) . ' | ' . _x( 'Order', 'purchase order', 'pagesco-lab' ),
		/* translators: %s: genre name, such as Fantasy. */
		sprintf( __( 'Books in %s', 'pagesco-lab' ), 'Fantasy' ),
	);
	return implode( "\n", $lines );
}

echo preg_replace( '/^/m', 'en  ', pagesco_lab_summary() ), "\n";
load_textdomain( 'pagesco-lab', get_temp_dir() . 'pagesco-lab-es_ES.mo' );
echo preg_replace( '/^/m', 'es  ', pagesco_lab_summary() ), "\n";

unload_textdomain( 'pagesco-lab' );
wp_delete_file( $pagesco_file );

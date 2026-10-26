<?php
/**
 * debug_seats_spanish.php: the next events with their seats, in Spanish (Session 16, Lesson 8.3, find-the-bug handout)
 * state: after:lesson_27
 * expect-error: Warning
 *
 * A translator sent three Spanish strings for an events summary (written to /tmp as the .l10n.php file that
 * wp i18n make-php builds). On a working course site the script prints the next three events in Spanish, each with
 * "20 plazas" or "entrada libre", and a Spanish total line. From your project folder:
 *     cp labs/module-16/l8_3-i18n-a11y-distribution/debug_seats_spanish.php wordpress/
 *     wp eval-file --use-include debug_seats_spanish.php
 * Two bugs announce themselves with Warnings (read each from the left: level, message, file, line); one of them
 * also makes every event look "open to all". The third is SILENT: one line stays English, with no message at all.
 * Fix them one at a time and run again after each fix. Then delete the copy: rm wordpress/debug_seats_spanish.php
 */

$pagesco_file = get_temp_dir() . 'pagesco-lab-es_ES.l10n.php';
$pagesco_po   = array(
	'domain'       => 'pagesco-lab',
	'language'     => 'es_ES',
	'plural-forms' => 'nplurals=2; plural=(n != 1);',
	'messages'     => array(
		'%s seat'                            => "%s plaza\0%s plazas",
		'open to all'                        => 'entrada libre',
		'%1$s seats in the next %2$d events' => '%1$s plazas en los próximos %2$d eventos',
	),
);
file_put_contents( $pagesco_file, '<?php return ' . var_export( $pagesco_po, true ) . ';' );
load_textdomain( 'pagesco-lab', get_temp_dir() . 'pagesco-lab-es_ES.mo' );

foreach ( PagesCo\Books\EventsTable::find( 3 ) as $pagesco_event ) {
	$pagesco_seats = $pagesco_event->seats
		/* translators: %s: number of seats. */
		? sprintf( _n( '%s seat', '%s seats', $pagesco_event->capacity, 'pagesco-lab' ), number_format_i18n( $pagesco_event->seats ) )
		: __( 'open to all', 'pagesco-lab' );
	printf( "%-44s %s\n", $pagesco_event->title, $pagesco_seats );
	$pagesco_total += (int) $pagesco_event->capacity;
}

/* translators: 1: number of seats, 2: number of events. */
printf( __( '%1$s seats in the next %2$d events', 'pagesco-books' ) . "\n", number_format_i18n( $pagesco_total ), 3 );

unload_textdomain( 'pagesco-lab' );
wp_delete_file( $pagesco_file );

<?php
/**
 * Renders pagesco/next-events on the server, on every view. WordPress passes $attributes, $content and $block.
 *
 * @package PagesCo\Books
 */

use PagesCo\Books\EventsTable;
use PagesCo\Books\Settings;

// No count chosen: the Events to show setting (Lesson 5.4). Either way 1 to 10.
$count = isset( $attributes['count'] ) ? absint( $attributes['count'] ) : (int) Settings::get( 'events_limit' );
$count = min( 10, max( 1, $count ) );

$events = EventsTable::find( $count, sanitize_text_field( $attributes['location'] ) );

if ( ! $events ) {
	printf(
		'<p %1$s>%2$s</p>',
		get_block_wrapper_attributes(),
		esc_html__( 'No events at this location yet.', 'pagesco-next-events' )
	);
	return;
}
?>
<ul <?php echo get_block_wrapper_attributes(); ?>>
	<?php foreach ( $events as $event ) : ?>
		<li><time datetime="<?php echo esc_attr( mysql2date( 'Y-m-d\TH:i', $event->starts_at, false ) ); ?>"><?php echo esc_html( mysql2date( 'M j', $event->starts_at ) ); ?></time> <?php echo esc_html( $event->title ); ?></li>
	<?php endforeach; ?>
</ul>

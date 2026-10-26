<?php
/**
 * open_today_solution.php: the instructor's reference for open_today_starter.php (Session 13, Lesson 6.4, lab A)
 * state: after:lesson_21
 * expect: <p data-wp-text="state.todayText">Today (Saturday): 10:00-16:00</p>
 * expect: <button aria-expanded="false" data-wp-on--click="actions.toggleWeek" data-wp-bind--aria-expanded="state.showWeek">
 */
$pagesco_hours = array(
	'Friday'   => '9:00-18:00',
	'Saturday' => '10:00-16:00',
	'Sunday'   => 'closed',
);
$pagesco_today = 'Saturday';

wp_interactivity_state(
	'pagesco/hours',
	array(
		'today'     => $pagesco_today,
		'showWeek'  => false,
		'todayText' => sprintf( 'Today (%s): %s', $pagesco_today, $pagesco_hours[ $pagesco_today ] ),
		// Derived state: the server calls these while it processes the directives.
		'isToday'   => function () {
			$pagesco_state = wp_interactivity_state();
			return $pagesco_state['today'] === wp_interactivity_get_context()['day'];
		},
		'isHidden'  => function () {
			$pagesco_state = wp_interactivity_state();
			return ! $pagesco_state['showWeek'] && $pagesco_state['today'] !== wp_interactivity_get_context()['day'];
		},
	)
);

$pagesco_html = '<div data-wp-interactive="pagesco/hours">'
	. '<p data-wp-text="state.todayText"></p>'
	. '<button data-wp-on--click="actions.toggleWeek" data-wp-bind--aria-expanded="state.showWeek">The whole week</button><ul>';
foreach ( $pagesco_hours as $pagesco_day => $pagesco_time ) {
	$pagesco_html .= '<li ' . wp_interactivity_data_wp_context( array( 'day' => $pagesco_day ) )
		. ' data-wp-bind--hidden="state.isHidden" data-wp-bind--aria-current="state.isToday" data-wp-class--is-today="state.isToday">'
		. esc_html( $pagesco_day . ': ' . $pagesco_time ) . '</li>';
}
$pagesco_html .= '</ul></div>';

// The server runs the directives, as WordPress does for a block with "interactivity": true.
echo str_replace( array( '<button', '<li', '</ul>' ), array( "\n<button", "\n<li", "\n</ul>" ), wp_interactivity_process_directives( $pagesco_html ) ), "\n";

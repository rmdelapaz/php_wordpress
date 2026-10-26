<?php
/**
 * open_today_starter.php: an opening-hours box the SERVER renders with Interactivity API directives (Session 13, Lesson 6.4, lab A)
 * state: after:lesson_21
 * expect: <p>TODO: today's hours</p>
 *
 * Lesson 6.4's first consequence, without a browser: WordPress evaluates the directives on the server, so the
 * HTML is right before any JavaScript runs. State: today and showWeek (the week is folded away). Derived state:
 * isToday and isHidden, closures that read each day's context. The script builds the HTML a render.php would
 * print and lets wp_interactivity_process_directives() do what WordPress does for an interactive block.
 * From your project folder:
 *     cp labs/module-13/l6_4-interactivity-api/open_today_starter.php wordpress/
 *     wp eval-file --use-include open_today_starter.php
 * Fill in the TODOs; before each run, predict which <li> gets hidden, aria-current and the class.
 * When you are done: rm wordpress/open_today_starter.php
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
		// TODO 1: 'isToday' => a closure: true when the state's today equals the context's day
		//         (wp_interactivity_state() and wp_interactivity_get_context(), no arguments, inside the closure).
		// TODO 2: 'isHidden' => a closure: true when showWeek is false AND this day is not today.
	)
);

// TODO 3: give the <p> the directive data-wp-text="state.todayText" (and drop its TODO text: the server fills it).
$pagesco_html = '<div data-wp-interactive="pagesco/hours">'
	. '<p>TODO: today\'s hours</p>'
	. '<button data-wp-on--click="actions.toggleWeek" data-wp-bind--aria-expanded="state.showWeek">The whole week</button><ul>';
foreach ( $pagesco_hours as $pagesco_day => $pagesco_time ) {
	// TODO 4: after the context, three directives: data-wp-bind--hidden="state.isHidden",
	//         data-wp-bind--aria-current="state.isToday" and data-wp-class--is-today="state.isToday".
	$pagesco_html .= '<li ' . wp_interactivity_data_wp_context( array( 'day' => $pagesco_day ) ) . '>'
		. esc_html( $pagesco_day . ': ' . $pagesco_time ) . '</li>';
}
$pagesco_html .= '</ul></div>';

// The server runs the directives, as WordPress does for a block with "interactivity": true.
echo str_replace( array( '<button', '<li', '</ul>' ), array( "\n<button", "\n<li", "\n</ul>" ), wp_interactivity_process_directives( $pagesco_html ) ), "\n";

// Expected when done (open_today_solution.php):
// <div data-wp-interactive="pagesco/hours"><p data-wp-text="state.todayText">Today (Saturday): 10:00-16:00</p>
// <button aria-expanded="false" data-wp-on--click="actions.toggleWeek" data-wp-bind--aria-expanded="state.showWeek">The whole week</button><ul>
// <li aria-current="false" hidden data-wp-context='{"day":"Friday"}' data-wp-bind--hidden="state.isHidden" data-wp-bind--aria-current="state.isToday" data-wp-class--is-today="state.isToday">Friday: 9:00-18:00</li>
// <li aria-current="true" class="is-today" data-wp-context='{"day":"Saturday"}' data-wp-bind--hidden="state.isHidden" data-wp-bind--aria-current="state.isToday" data-wp-class--is-today="state.isToday">Saturday: 10:00-16:00</li>
// <li aria-current="false" hidden data-wp-context='{"day":"Sunday"}' data-wp-bind--hidden="state.isHidden" data-wp-bind--aria-current="state.isToday" data-wp-class--is-today="state.isToday">Sunday: closed</li>
// </ul></div>

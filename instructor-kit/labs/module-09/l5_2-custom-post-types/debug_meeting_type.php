<?php
/**
 * debug_meeting_type.php: a post type, a taxonomy and a meta key, registered with three bugs (Session 9,
 * Lesson 5.2, find-the-bug handout)
 * state: after:lesson_14
 * expect-error: doing_it_wrong, Warning
 *
 * A quick test before the code goes into a feature class: register a "meeting" type for the book club, a "room"
 * taxonomy on it and a list of reading assignments as meta, then report what WordPress knows. It registers for
 * this one run only (nothing is stored). From your project folder:
 *     cp labs/module-09/l5_2-custom-post-types/debug_meeting_type.php wordpress/
 *     wp eval-file --use-include debug_meeting_type.php
 * WordPress reports two of the bugs ("called incorrectly" notices, and a Warning that follows from the first).
 * The third is SILENT: look at the "taxonomies on meetings" line. Fix all three; when you are done:
 *     rm wordpress/debug_meeting_type.php
 */
register_post_type(
	'pagesco_bookclub_meeting',
	array(
		'label'        => 'Meetings',
		'public'       => true,
		'show_in_rest' => true,
	)
);
register_taxonomy(
	'pagesco_room',
	'pagesco_meetings',
	array(
		'label'        => 'Rooms',
		'hierarchical' => false,
		'show_in_rest' => true,
	)
);
register_post_meta(
	'pagesco_bookclub_meeting',
	'pagesco_reading',
	array(
		'type'         => 'array',
		'single'       => true,
		'show_in_rest' => true,
	)
);
echo 'type: ', get_post_type_object( 'pagesco_bookclub_meeting' )->label, "\n";
echo 'taxonomies on meetings: ', implode( ', ', get_object_taxonomies( 'pagesco_bookclub_meeting' ) ) ?: '(none)', "\n";
echo 'meta keys: ', implode( ', ', array_keys( get_registered_meta_keys( 'post', 'pagesco_bookclub_meeting' ) ) ) ?: '(none)', "\n";

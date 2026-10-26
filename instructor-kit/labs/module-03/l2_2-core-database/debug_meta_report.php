<?php
/**
 * debug_meta_report.php: a three-line site report with three bugs (Session 3, Lesson 2.2, find-the-bug handout)
 * state: after:lesson_04
 * expect-error: Warning
 *
 * Each section asks the metadata API or a counting function one question about the Pages & Co. site after
 * Lesson 2.1. Two bugs are loud (PHP Warnings), one is silent (a wrong answer with no message). From your
 * project folder:
 *     cp labs/module-03/l2_2-core-database/debug_meta_report.php wordpress/
 *     wp eval-file --use-include debug_meta_report.php
 * Read every message from the left (level, message, file, line), fix the lines one at a time, and check each
 * answer against the database (wp db query "SELECT ... FROM wp_postmeta ..."). Done: no message, and
 *     Post 15 waiting for pings: yes
 *     Maria's role: editor
 *     Published pages: 4
 * Then delete the copy: rm wordpress/debug_meta_report.php
 */

// 1. Post 15 (a News post) has the meta key _pingme with the value '1' (Lesson 2.2, the wp_postmeta table).
$pagesco_ping = get_post_meta( 15, '_pingme' );
echo 'Post 15 waiting for pings: ', ( '1' === $pagesco_ping ? 'yes' : 'no' ), "\n";

// 2. Maria (user 2) and her role, read from the capabilities meta (a serialized array in the database).
$pagesco_caps = get_user_meta( 2, 'capabilities', true );
foreach ( $pagesco_caps as $pagesco_role => $pagesco_has ) {
	echo "Maria's role: ", $pagesco_role, "\n";
}

// 3. How many pages are published (wp_count_posts() returns one property per status).
$pagesco_counts = wp_count_posts( 'page' );
echo 'Published pages: ', $pagesco_counts->published, "\n";

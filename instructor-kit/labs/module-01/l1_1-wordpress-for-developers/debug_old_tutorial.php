<?php
/**
 * debug_old_tutorial.php: code copied from an old tutorial (Session 1, Lesson 1.1, find-the-problem handout)
 * state: fresh
 * expect-error: Deprecated
 *
 * It "works": every line prints a result. Run it and read what WordPress says about it, from your project folder:
 *     cp labs/module-01/l1_1-wordpress-for-developers/debug_old_tutorial.php wordpress/
 *     wp eval-file --use-include debug_old_tutorial.php
 * Each message names the version that deprecated the function and what to use instead (Lesson 1.1, Common
 * Mistakes 2). Fix the lines one at a time until the file runs without a single message, and note for each one
 * how old the tutorial must have been. Then delete the copy: rm wordpress/debug_old_tutorial.php
 */

// The Sample Page's ID.
$pagesco_page = get_page_by_title( 'Sample Page' );
echo 'Sample Page ID: ', $pagesco_page->ID, "\n";

// The administrator's email address.
$pagesco_admin = get_userdatabylogin( 'admin' );
echo 'Admin email: ', $pagesco_admin->user_email, "\n";

// A book title printed safely in HTML.
echo 'Escaped: ', wp_specialchars( 'Pride & Prejudice <new edition>' ), "\n";

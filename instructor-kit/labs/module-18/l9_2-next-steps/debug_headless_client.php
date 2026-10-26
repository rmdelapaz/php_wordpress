<?php
/**
 * debug_headless_client.php: a headless front end's first draft, in PHP (Session 18, Lesson 9.2, find-the-bug handout)
 * state: after:lesson_30
 * expect-error: Warning, Deprecated
 *
 * It reads the site's name and the catalog from the REST API, as a separate front end would (this one happens to
 * run with WordPress loaded, so it can use wp_remote_get()). On the course site the last line should read
 * "Pages & Co.: 11 books on 2 pages". From your project folder:
 *     cp labs/module-18/l9_2-next-steps/debug_headless_client.php wordpress/
 *     wp eval-file --use-include debug_headless_client.php
 * One mistyped key produces two messages. The third bug is SILENT: Lesson 9.2's Common Mistake 3, in PHP. Fix
 * all three, run again after each fix. When you are done: rm wordpress/debug_headless_client.php
 */
$pagesco_api = home_url( '/wp-json/' );

// The site's name: the REST index gives it HTML-escaped ("Pages &amp; Co."), so decode it once for plain text.
$pagesco_index = json_decode( wp_remote_retrieve_body( wp_remote_get( $pagesco_api . '?_fields=name' ) ), true );
$pagesco_name  = html_entity_decode( $pagesco_index['title'] );

// The catalog.
$pagesco_response = wp_remote_get( $pagesco_api . 'pagesco/v1/books' );
$pagesco_books    = json_decode( wp_remote_retrieve_body( $pagesco_response ), true );
$pagesco_pages    = (int) wp_remote_retrieve_header( $pagesco_response, 'X-WP-TotalPages' );

printf( "%s: %d books on %d pages\n", $pagesco_name, count( $pagesco_books ), $pagesco_pages );
echo 'Last in the list: ', end( $pagesco_books )['title'], "\n";

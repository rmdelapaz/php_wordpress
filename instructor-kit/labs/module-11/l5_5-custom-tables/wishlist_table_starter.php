<?php
/**
 * wishlist_table_starter.php: a custom table's whole life in one script (Session 11, Lesson 5.5, lab A)
 * state: after:lesson_17
 * expect: 1. TODO
 *
 * A throwaway {prefix}pagesco_lab_wishlist table: which reader wants which book. Create it with dbDelta(), fill it
 * with $wpdb->insert() and its formats, read it with prepare() and %i, change a row, then drop it again, so your
 * site ends as it started. From your project folder:
 *     cp labs/module-11/l5_5-custom-tables/wishlist_table_starter.php wordpress/
 *     wp eval-file --use-include wishlist_table_starter.php
 * Do the TODOs in order and run the script after each one. If a run stops half-way, drop the table by hand:
 *     wp db query "DROP TABLE IF EXISTS wp_pagesco_lab_wishlist"
 * When you are done: rm wordpress/wishlist_table_starter.php
 */
require_once ABSPATH . 'wp-admin/includes/upgrade.php';
global $wpdb;
$pagesco_table = $wpdb->prefix . 'pagesco_lab_wishlist';

// TODO 1: create the table with dbDelta() and print what it returns (implode the array with "\n"). Columns:
// id (bigint unsigned, auto-increment), book_id (bigint unsigned), reader (varchar(100)), added_at (datetime),
// all NOT NULL; PRIMARY KEY  (id) with TWO spaces; KEY book_id (book_id); then $wpdb->get_charset_collate().
// One column or index per line (Lesson 5.5, "Creating the Table with dbDelta()").
echo "1. TODO\n";

// TODO 2: insert four wishes with $wpdb->insert() and a format array ( '%d', '%s', '%s' ), added_at from
// current_time( 'mysql', true ): book 30 Priya Shah, 35 Tomas Berg, 30 Lena Ortiz, 39 Priya Shah. Then print
// "rows: N, last ID N" (COUNT(*) with prepare() and %i; $wpdb->insert_id).
echo "2. TODO\n";

// TODO 3: the most wished-for books with their titles: join wp_posts ($wpdb->posts, also through %i), GROUP BY
// the book, ORDER BY readers DESC, then the title. Print "Dune: 2 reader(s)" lines.
echo "3. TODO\n";

// TODO 4: Priya changes her mind: her wish for book 39 becomes book 36. $wpdb->update() with a data format and a
// where format; print "updated: N row(s)".
echo "4. TODO\n";

// TODO 5: drop the table through prepare() ('DROP TABLE IF EXISTS %i') and prove it is gone: count it in
// information_schema.TABLES (TABLE_SCHEMA = DATABASE(), TABLE_NAME = %s). Print "tables left: 0".
echo "5. TODO\n";

// Expected when done (wishlist_table_solution.php):
// Created table wp_pagesco_lab_wishlist
// rows: 4, last ID 4
// Dune: 2 reader(s)
// Fahrenheit 451: 1 reader(s)
// The Hobbit: 1 reader(s)
// updated: 1 row(s)
// tables left: 0

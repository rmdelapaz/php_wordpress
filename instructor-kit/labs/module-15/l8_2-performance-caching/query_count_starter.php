<?php
/**
 * query_count_starter.php: what five everyday calls cost the database, asked twice (Session 15, Lesson 8.2, lab A)
 * state: after:lesson_26
 * expect: TODO row 2: an option that has no row
 *
 * $wpdb->num_queries counts every query of this request, so the difference before and after a call is what the
 * call cost. Each row runs its call twice: the second time shows what the object cache (Lesson 8.2) remembered
 * within the same request. From your project folder:
 *     cp labs/module-15/l8_2-performance-caching/query_count_starter.php wordpress/
 *     wp eval-file --use-include query_count_starter.php
 * Row 1 is done for you. For each TODO, PREDICT the two numbers first (write them in the comment), then replace
 * the echo line with a pagesco_lab_row() call and run again. Compare with "Expected when done" at the end.
 * When you are done: rm wordpress/query_count_starter.php
 */

/**
 * Runs $work and returns how many database queries it made.
 *
 * @param callable $work The code to measure.
 */
function pagesco_lab_queries( callable $work ): int {
	global $wpdb;

	$before = $wpdb->num_queries;
	$work();
	return $wpdb->num_queries - $before;
}

/**
 * Prints one row: the call, its queries the first time and the second time.
 *
 * @param string   $label What is measured.
 * @param callable $work  The code to measure.
 */
function pagesco_lab_row( string $label, callable $work ): void {
	printf( "%-72s %5d %9d\n", $label, pagesco_lab_queries( $work ), pagesco_lab_queries( $work ) );
}

/**
 * Makes the object cache forget these posts' meta, so the next read goes to the database again.
 *
 * @param int[] $ids Post IDs.
 */
function pagesco_lab_forget_meta( array $ids ): void {
	foreach ( $ids as $id ) {
		wp_cache_delete( $id, 'post_meta' );
	}
}

printf( "%-72s %5s %9s\n", 'call', 'first', 'again' );

// 1. An autoloaded option: loaded with all the others before WordPress even started this script.
pagesco_lab_row( "get_option( 'blogname' )", fn() => get_option( 'blogname' ) );

// TODO row 2: get_option() for an option that has no row, such as 'pagesco_lab_missing'. My prediction: __ __
echo "TODO row 2: an option that has no row\n";

// TODO row 3: two meta values of book 33 (The Great Gatsby), 'pagesco_price' and 'pagesco_author', in one
//             function () { ... } that calls get_post_meta() twice. My prediction: __ __
echo "TODO row 3: two meta values of one book\n";

// TODO row 4: new WP_Query() for the three cheapest books (post_type book, posts_per_page 3, meta_key
//             pagesco_price, orderby meta_value_num, order ASC). My prediction: __ __
echo "TODO row 4: the same WP_Query twice\n";

// TODO row 5: the N+1 shape. Get the IDs of all books with get_posts( array( ..., 'fields' => 'ids' ) ), call
//             pagesco_lab_forget_meta( $pagesco_ids ), then measure a foreach that calls
//             get_post_meta( $pagesco_id, 'pagesco_isbn', true ) for each ID. My prediction: __ __
echo "TODO row 5: one meta read per book\n";

// TODO row 6: the same loop with update_postmeta_cache( $pagesco_ids ) before the foreach (forget the meta
//             first, as in row 5). My prediction: __ __
echo "TODO row 6: one meta query for all books\n";

// Expected when done (query_count_solution.php, the course site after Lesson 8.1):
// call                                                                     first     again
// get_option( 'blogname' )                                                     0         0
// get_option( 'pagesco_lab_missing' )                                          1         0
// get_post_meta( 33, 'pagesco_price' ) and 'pagesco_author'                    1         0
// WP_Query: the three cheapest books                                           6         0
// get_post_meta() over 11 books, one by one                                   11         0
// get_post_meta() over 11 books, after update_postmeta_cache()                 1         0

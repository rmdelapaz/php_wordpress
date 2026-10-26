<?php
/**
 * query_count_solution.php: what five everyday calls cost the database, asked twice (Session 15, Lesson 8.2, lab A)
 * state: after:lesson_26
 * expect: get_post_meta() over 11 books, one by one                                   11         0
 *
 * $wpdb->num_queries counts every query of this request, so the difference before and after a call is what the
 * call cost. Each row runs its call twice: the second time shows what the object cache (Lesson 8.2) remembered
 * within the same request. From your project folder:
 *     cp labs/module-15/l8_2-performance-caching/query_count_solution.php wordpress/
 *     wp eval-file --use-include query_count_solution.php
 *     rm wordpress/query_count_solution.php
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

// 2. An option that has no row: one query to learn that, then the notoptions cache remembers.
pagesco_lab_row( "get_option( 'pagesco_lab_missing' )", fn() => get_option( 'pagesco_lab_missing' ) );

// 3. Two meta values of one book: the first read loads all of the book's meta.
pagesco_lab_row(
	"get_post_meta( 33, 'pagesco_price' ) and 'pagesco_author'",
	function () {
		get_post_meta( 33, 'pagesco_price', true );
		get_post_meta( 33, 'pagesco_author', true );
	}
);

// 4. The same WP_Query twice: WP_Query caches its own results since WordPress 6.1.
pagesco_lab_row(
	'WP_Query: the three cheapest books',
	fn() => new WP_Query(
		array(
			'post_type'      => 'book',
			'posts_per_page' => 3,
			'meta_key'       => 'pagesco_price',
			'orderby'        => 'meta_value_num',
			'order'          => 'ASC',
		)
	)
);

// 5. The N+1 shape: IDs only (get_posts() with 'fields' => 'ids' loads no meta), then one meta read per book ...
$pagesco_ids = get_posts(
	array(
		'post_type'      => 'book',
		'posts_per_page' => 100,
		'fields'         => 'ids',
	)
);
pagesco_lab_forget_meta( $pagesco_ids );
pagesco_lab_row(
	'get_post_meta() over ' . count( $pagesco_ids ) . ' books, one by one',
	function () use ( $pagesco_ids ) {
		foreach ( $pagesco_ids as $pagesco_id ) {
			get_post_meta( $pagesco_id, 'pagesco_isbn', true );
		}
	}
);

// ... and the fix: all their meta in one query, before the loop.
pagesco_lab_forget_meta( $pagesco_ids );
pagesco_lab_row(
	'get_post_meta() over ' . count( $pagesco_ids ) . ' books, after update_postmeta_cache()',
	function () use ( $pagesco_ids ) {
		update_postmeta_cache( $pagesco_ids );
		foreach ( $pagesco_ids as $pagesco_id ) {
			get_post_meta( $pagesco_id, 'pagesco_isbn', true );
		}
	}
);

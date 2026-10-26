<?php
/**
 * Variations of the Book List: "New Arrivals", and one list per genre.
 *
 * WordPress requires this file only when someone asks for the block's variations
 * (the editor does, through the REST API), not on every page view.
 *
 * @package PagesCo\Books
 */

defined( 'ABSPATH' ) || exit;

use PagesCo\Books\GenreTaxonomy;

$variations = array(
	array(
		'name'        => 'new-arrivals',
		'title'       => __( 'New Arrivals', 'pagesco-books' ),
		'description' => __( 'The three books most recently added to the catalog.', 'pagesco-books' ),
		'icon'        => 'star-filled',
		'attributes'  => array(
			'count'   => 3,
			'orderBy' => 'newest',
		),
		'scope'       => array( 'inserter' ),
	),
);

$genres = get_terms(
	array(
		'taxonomy'   => GenreTaxonomy::NAME,
		'hide_empty' => false,
	)
);

foreach ( is_array( $genres ) ? $genres : array() as $genre ) {
	$variations[] = array(
		'name'        => 'genre-' . $genre->slug,
		/* translators: %s: genre name, such as Fantasy. */
		'title'       => sprintf( __( '%s Books', 'pagesco-books' ), $genre->name ),
		/* translators: %s: genre name, such as Fantasy. */
		'description' => sprintf( __( 'Books in the %s genre.', 'pagesco-books' ), $genre->name ),
		'attributes'  => array( 'genre' => $genre->slug ),
		'isActive'    => array( 'genre' ),
		'scope'       => array( 'inserter', 'transform' ),
	);
}

return $variations;

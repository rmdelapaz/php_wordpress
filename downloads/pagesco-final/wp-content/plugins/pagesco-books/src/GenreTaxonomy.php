<?php
/**
 * The genre taxonomy for books.
 *
 * @package PagesCo\Books
 */

namespace PagesCo\Books;

/**
 * Registers the genre taxonomy on init.
 */
final class GenreTaxonomy implements Feature {

	/**
	 * The taxonomy's name, stored in wp_term_taxonomy.taxonomy.
	 */
	public const NAME = 'genre';

	/**
	 * Hooks the registration into init.
	 */
	public function register(): void {
		add_action( 'init', array( $this, 'register_taxonomy' ) );
	}

	/**
	 * Registers the taxonomy for books. Also called by Activator::activate().
	 */
	public function register_taxonomy(): void {
		register_taxonomy(
			self::NAME,
			array( BookPostType::NAME ),
			array(
				'labels'            => array(
					'name'          => __( 'Genres', 'pagesco-books' ),
					'singular_name' => __( 'Genre', 'pagesco-books' ),
					'search_items'  => __( 'Search Genres', 'pagesco-books' ),
					'all_items'     => __( 'All Genres', 'pagesco-books' ),
					'edit_item'     => __( 'Edit Genre', 'pagesco-books' ),
					'add_new_item'  => __( 'Add Genre', 'pagesco-books' ),
					'not_found'     => __( 'No genres found.', 'pagesco-books' ),
				),
				'hierarchical'      => true,
				'show_admin_column' => true,
				'show_in_rest'      => true,
				'rest_base'         => 'genres',
				'rewrite'           => array( 'slug' => 'genre' ),
			)
		);
	}
}

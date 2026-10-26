<?php
/**
 * The book post type: the shop's catalog.
 *
 * @package PagesCo\Books
 */

namespace PagesCo\Books;

/**
 * Registers the book post type on init.
 */
final class BookPostType implements Feature {

	/**
	 * The post type's name, stored in wp_posts.post_type.
	 */
	public const NAME = 'book';

	/**
	 * Hooks the registration into init.
	 */
	public function register(): void {
		add_action( 'init', array( $this, 'register_post_type' ) );
	}

	/**
	 * Registers the post type. Also called by Activator::activate().
	 */
	public function register_post_type(): void {
		register_post_type(
			self::NAME,
			array(
				'labels'        => array(
					'name'          => __( 'Books', 'pagesco-books' ),
					'singular_name' => __( 'Book', 'pagesco-books' ),
					'add_new_item'  => __( 'Add Book', 'pagesco-books' ),
					'edit_item'     => __( 'Edit Book', 'pagesco-books' ),
					'new_item'      => __( 'New Book', 'pagesco-books' ),
					'view_item'     => __( 'View Book', 'pagesco-books' ),
					'view_items'    => __( 'View Books', 'pagesco-books' ),
					'search_items'  => __( 'Search Books', 'pagesco-books' ),
					'not_found'     => __( 'No books found.', 'pagesco-books' ),
					'all_items'     => __( 'All Books', 'pagesco-books' ),
					'archives'      => __( 'Book Archives', 'pagesco-books' ),
					'item_updated'  => __( 'Book updated.', 'pagesco-books' ),
				),
				'public'        => true,
				'has_archive'   => 'books',
				'rewrite'       => array( 'slug' => 'books' ),
				'show_in_rest'  => true,
				'rest_base'     => 'books',
				'menu_position' => 5,
				'menu_icon'     => 'dashicons-book',
				'supports'      => array( 'title', 'editor', 'excerpt', 'thumbnail', 'custom-fields' ),
			)
		);
	}
}

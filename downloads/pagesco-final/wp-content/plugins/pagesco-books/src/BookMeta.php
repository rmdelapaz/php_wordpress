<?php
/**
 * The book's details, stored as post meta.
 *
 * @package PagesCo\Books
 */

namespace PagesCo\Books;

/**
 * Registers the book meta keys on init.
 */
final class BookMeta implements Feature {

	/**
	 * Hooks the registration into init.
	 */
	public function register(): void {
		add_action( 'init', array( $this, 'register_meta' ) );
	}

	/**
	 * The book's meta keys with their types and labels.
	 *
	 * @return array<string, array{type: string, label: string}>
	 */
	public static function fields(): array {
		return array(
			'pagesco_author'    => array(
				'type'  => 'string',
				'label' => __( 'Author', 'pagesco-books' ),
			),
			'pagesco_price'     => array(
				'type'  => 'number',
				'label' => __( 'Price', 'pagesco-books' ),
			),
			'pagesco_pages'     => array(
				'type'  => 'integer',
				'label' => __( 'Pages', 'pagesco-books' ),
			),
			'pagesco_published' => array(
				'type'  => 'string',
				'label' => __( 'First published', 'pagesco-books' ),
			),
			'pagesco_in_stock'  => array(
				'type'  => 'boolean',
				'label' => __( 'In stock', 'pagesco-books' ),
			),
			'pagesco_isbn'      => array(
				'type'  => 'string',
				'label' => __( 'ISBN', 'pagesco-books' ),
			),
		);
	}

	/**
	 * Registers every key for the book post type: one value per book, visible in the REST API.
	 */
	public function register_meta(): void {
		foreach ( self::fields() as $key => $field ) {
			register_post_meta(
				BookPostType::NAME,
				$key,
				array(
					'type'         => $field['type'],
					'label'        => $field['label'],
					'single'       => true,
					'show_in_rest' => true,
				)
			);
		}
	}
}

<?php
/**
 * The shop's abilities: what other programs (and AI assistants) may ask the site to do.
 *
 * @package PagesCo\Books
 */

namespace PagesCo\Books;

use PagesCo\Books\Supplier\Availability;
use WP_Error;

/**
 * Registers the pagesco ability category and the pagesco/check-stock ability (Abilities API, WordPress 6.9+).
 */
final class Abilities implements Feature {

	/**
	 * Hooks into the Abilities API's two registration actions. On WordPress 6.8 they never fire.
	 */
	public function register(): void {
		add_action( 'wp_abilities_api_categories_init', array( $this, 'register_category' ) );
		add_action( 'wp_abilities_api_init', array( $this, 'register_abilities' ) );
	}

	/**
	 * The category that groups the shop's abilities.
	 */
	public function register_category(): void {
		wp_register_ability_category(
			'pagesco',
			array(
				'label'       => __( 'Pages & Co.', 'pagesco-books' ),
				'description' => __( 'What the Pages & Co. bookstore can do.', 'pagesco-books' ),
			)
		);
	}

	/**
	 * One ability: check a book's stock, at the shop and at the supplier.
	 */
	public function register_abilities(): void {
		wp_register_ability(
			'pagesco/check-stock',
			array(
				'label'               => __( 'Check a book\'s stock', 'pagesco-books' ),
				'description'         => __( 'Says whether the shop has a book in stock, how many copies the supplier has, and when the supplier\'s next delivery is.', 'pagesco-books' ),
				'category'            => 'pagesco',
				'input_schema'        => array(
					'type'                 => 'object',
					'properties'           => array(
						'slug' => array(
							'type'        => 'string',
							'description' => __( 'The book\'s slug, such as the-great-gatsby.', 'pagesco-books' ),
							'minLength'   => 1,
						),
					),
					'required'             => array( 'slug' ),
					'additionalProperties' => false,
				),
				'output_schema'       => array(
					'type'       => 'object',
					'properties' => array(
						'title'              => array( 'type' => 'string' ),
						'in_stock'           => array( 'type' => 'boolean' ),
						'supplier_available' => array( 'type' => array( 'integer', 'null' ) ),
						'next_delivery'      => array( 'type' => 'string' ),
					),
				),
				'execute_callback'    => array( $this, 'check_stock' ),
				'permission_callback' => array( $this, 'can_check_stock' ),
				'meta'                => array(
					'annotations'  => array(
						'readonly'    => true,
						'destructive' => false,
						'idempotent'  => true,
					),
					'show_in_rest' => true,
				),
			)
		);
	}

	/**
	 * Staff only: the supplier's numbers are not for the public.
	 */
	public function can_check_stock(): bool {
		return current_user_can( 'edit_others_posts' );
	}

	/**
	 * The ability's work: the shop's stock from the book's meta, the supplier's from the cached availability.
	 *
	 * @param array $input Validated against input_schema: array( 'slug' => '…' ).
	 * @return array|WP_Error
	 */
	public function check_stock( $input ) {
		$book = get_page_by_path( sanitize_title( $input['slug'] ), OBJECT, BookPostType::NAME );

		if ( ! $book || 'publish' !== $book->post_status ) {
			return new WP_Error( 'pagesco_book_not_found', __( 'No book was found with that slug.', 'pagesco-books' ), array( 'status' => 404 ) );
		}

		$isbn         = (string) get_post_meta( $book->ID, 'pagesco_isbn', true );
		$availability = Plugin::instance()->feature( Availability::class );
		$item         = $availability instanceof Availability ? ( $availability->get()['items'][ $isbn ] ?? null ) : null;

		return array(
			'title'              => $book->post_title,
			'in_stock'           => (bool) get_post_meta( $book->ID, 'pagesco_in_stock', true ),
			'supplier_available' => $item ? $item['available'] : null,
			'next_delivery'      => $item ? $item['next_delivery'] : '',
		);
	}
}

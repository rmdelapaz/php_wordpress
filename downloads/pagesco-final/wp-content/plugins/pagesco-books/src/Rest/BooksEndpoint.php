<?php
/**
 * The shop's own books routes: GET /pagesco/v1/books and /pagesco/v1/books/<id>.
 *
 * @package PagesCo\Books
 */

namespace PagesCo\Books\Rest;

use PagesCo\Books\BookPostType;
use PagesCo\Books\Feature;
use PagesCo\Books\GenreTaxonomy;
use PagesCo\Books\Settings;
use WP_Error;
use WP_Post;
use WP_Query;
use WP_REST_Request;
use WP_REST_Response;
use WP_REST_Server;

/**
 * A compact, filterable catalog for the shop's JavaScript and partners: one book = ten plain fields.
 */
final class BooksEndpoint implements Feature {

	/**
	 * The namespace of every route the plugin adds: vendor/version.
	 */
	public const NAMESPACE = 'pagesco/v1';

	/**
	 * The schema, built once per request.
	 *
	 * @var array|null
	 */
	private ?array $schema = null;

	/**
	 * Registers the routes when the REST API starts, not on every request.
	 */
	public function register(): void {
		add_action( 'rest_api_init', array( $this, 'register_routes' ) );
	}

	/**
	 * Tells the REST server about the two routes: their methods, callbacks, permissions and arguments.
	 */
	public function register_routes(): void {
		register_rest_route(
			self::NAMESPACE,
			'/books',
			array(
				array(
					'methods'             => WP_REST_Server::READABLE,
					'callback'            => array( $this, 'get_books' ),
					'permission_callback' => '__return_true',
					'args'                => $this->collection_args(),
				),
				'schema' => array( $this, 'get_schema' ),
			)
		);

		register_rest_route(
			self::NAMESPACE,
			'/books/(?P<id>\d+)',
			array(
				array(
					'methods'             => WP_REST_Server::READABLE,
					'callback'            => array( $this, 'get_book' ),
					'permission_callback' => '__return_true',
					'args'                => array(
						'id' => array(
							'description' => __( 'The book ID.', 'pagesco-books' ),
							'type'        => 'integer',
							'minimum'     => 1,
						),
					),
				),
				'schema' => array( $this, 'get_schema' ),
			)
		);
	}

	/**
	 * The query arguments GET /books accepts. With a type and no sanitize_callback, WordPress
	 * validates and sanitizes each one against its schema (rest_parse_request_arg).
	 */
	private function collection_args(): array {
		return array(
			'page'     => array(
				'description' => __( 'The page of results.', 'pagesco-books' ),
				'type'        => 'integer',
				'default'     => 1,
				'minimum'     => 1,
			),
			'per_page' => array(
				'description' => __( 'Books per page. Default: the Books per list setting.', 'pagesco-books' ),
				'type'        => 'integer',
				'default'     => (int) Settings::get( 'books_per_page' ),
				'minimum'     => 1,
				'maximum'     => 100,
			),
			'genre'    => array(
				'description'       => __( 'Only books in this genre (a genre slug).', 'pagesco-books' ),
				'type'              => 'string',
				'default'           => '',
				'sanitize_callback' => 'sanitize_key',
				'validate_callback' => array( $this, 'validate_genre' ),
			),
			'in_stock' => array(
				'description' => __( 'true: only books in stock; false: only sold-out books.', 'pagesco-books' ),
				'type'        => 'boolean',
			),
			'orderby'  => array(
				'description' => __( 'The order of the books.', 'pagesco-books' ),
				'type'        => 'string',
				'enum'        => array( 'title', 'newest', 'price' ),
				'default'     => 'title',
			),
		);
	}

	/**
	 * Accepts '' (all genres) or the slug of an existing genre.
	 *
	 * @param mixed $value The genre argument as sent.
	 * @return true|WP_Error
	 */
	public function validate_genre( $value ) {
		if ( ! is_string( $value ) ) {
			return new WP_Error( 'rest_invalid_type', __( 'genre must be a genre slug.', 'pagesco-books' ) );
		}
		if ( '' === $value || term_exists( sanitize_key( $value ), GenreTaxonomy::NAME ) ) {
			return true;
		}

		return new WP_Error( 'pagesco_unknown_genre', __( 'genre must be the slug of an existing genre.', 'pagesco-books' ) );
	}

	/**
	 * GET /pagesco/v1/books: one page of books, with the totals in the X-WP-Total headers.
	 *
	 * @param WP_REST_Request $request The request, its arguments already validated and sanitized.
	 * @return WP_REST_Response|WP_Error
	 */
	public function get_books( WP_REST_Request $request ) {
		$query_args = array(
			'post_type'      => BookPostType::NAME,
			'post_status'    => 'publish',
			'posts_per_page' => $request['per_page'],
			'paged'          => $request['page'],
			'orderby'        => 'title',
			'order'          => 'ASC',
		);

		if ( 'newest' === $request['orderby'] ) {
			$query_args['orderby'] = 'date';
			$query_args['order']   = 'DESC';
		} elseif ( 'price' === $request['orderby'] ) {
			$query_args['meta_key'] = 'pagesco_price';
			$query_args['orderby']  = 'meta_value_num';
		}

		if ( '' !== $request['genre'] ) {
			$query_args['tax_query'] = array(
				array(
					'taxonomy' => GenreTaxonomy::NAME,
					'field'    => 'slug',
					'terms'    => $request['genre'],
				),
			);
		}

		if ( isset( $request['in_stock'] ) ) {
			$query_args['meta_query'] = array(
				array(
					'key'   => 'pagesco_in_stock',
					'value' => $request['in_stock'] ? '1' : '',
				),
			);
		}

		$query = new WP_Query( $query_args );

		if ( $request['page'] > 1 && $request['page'] > $query->max_num_pages ) {
			return new WP_Error(
				'pagesco_invalid_page',
				__( 'The page number is larger than the number of pages.', 'pagesco-books' ),
				array( 'status' => 400 )
			);
		}

		$response = rest_ensure_response( array_map( array( $this, 'prepare_book' ), $query->posts ) );
		$response->header( 'X-WP-Total', (string) $query->found_posts );
		$response->header( 'X-WP-TotalPages', (string) $query->max_num_pages );

		return $response;
	}

	/**
	 * GET /pagesco/v1/books/<id>: one published book, or a 404 error.
	 *
	 * @param WP_REST_Request $request The request; $request['id'] comes from the route's pattern.
	 * @return WP_REST_Response|WP_Error
	 */
	public function get_book( WP_REST_Request $request ) {
		$book = get_post( $request['id'] );

		if ( ! $book || BookPostType::NAME !== $book->post_type || 'publish' !== $book->post_status ) {
			return new WP_Error(
				'pagesco_book_not_found',
				__( 'No book was found with that ID.', 'pagesco-books' ),
				array( 'status' => 404 )
			);
		}

		return rest_ensure_response( $this->prepare_book( $book ) );
	}

	/**
	 * One book as the API shows it: plain values, in the types the schema promises.
	 *
	 * @param WP_Post $book A published book.
	 */
	public function prepare_book( WP_Post $book ): array {
		$genres = get_the_terms( $book, GenreTaxonomy::NAME );

		return array(
			'id'        => $book->ID,
			'title'     => $book->post_title,
			'slug'      => $book->post_name,
			'link'      => get_permalink( $book ),
			'author'    => (string) get_post_meta( $book->ID, 'pagesco_author', true ),
			'price'     => (float) get_post_meta( $book->ID, 'pagesco_price', true ),
			'in_stock'  => (bool) get_post_meta( $book->ID, 'pagesco_in_stock', true ),
			'pages'     => (int) get_post_meta( $book->ID, 'pagesco_pages', true ),
			'published' => (string) get_post_meta( $book->ID, 'pagesco_published', true ),
			'genres'    => is_array( $genres ) ? wp_list_pluck( $genres, 'slug' ) : array(),
		);
	}

	/**
	 * The JSON Schema of one book: what clients may rely on. OPTIONS requests return it.
	 */
	public function get_schema(): array {
		if ( null === $this->schema ) {
			$this->schema = array(
				'$schema'    => 'http://json-schema.org/draft-04/schema#',
				'title'      => 'pagesco-book',
				'type'       => 'object',
				'properties' => array(
					'id'        => array(
						'type'     => 'integer',
						'readonly' => true,
					),
					'title'     => array( 'type' => 'string' ),
					'slug'      => array( 'type' => 'string' ),
					'link'      => array(
						'type'   => 'string',
						'format' => 'uri',
					),
					'author'    => array( 'type' => 'string' ),
					'price'     => array( 'type' => 'number' ),
					'in_stock'  => array( 'type' => 'boolean' ),
					'pages'     => array( 'type' => 'integer' ),
					'published' => array(
						'type'   => 'string',
						'format' => 'date',
					),
					'genres'    => array(
						'type'  => 'array',
						'items' => array( 'type' => 'string' ),
					),
				),
			);
		}

		return $this->schema;
	}
}

<?php
/**
 * The holds routes: GET and POST /pagesco/v1/holds, DELETE /pagesco/v1/holds/<id>.
 *
 * @package PagesCo\Books
 */

namespace PagesCo\Books\Rest;

use PagesCo\Books\Feature;
use PagesCo\Books\Holds\HoldActions;
use PagesCo\Books\Holds\Holds;
use PagesCo\Books\Holds\HoldsTable;
use WP_Error;
use WP_REST_Request;
use WP_REST_Response;
use WP_REST_Server;

/**
 * A customer's own holds over the REST API: the Reserve block's JavaScript uses POST.
 */
final class HoldsEndpoint implements Feature {

	/**
	 * Registers the routes when the REST API starts.
	 */
	public function register(): void {
		add_action( 'rest_api_init', array( $this, 'register_routes' ) );
	}

	/**
	 * Two routes. Every endpoint needs a logged-in customer; which holds they reach is decided in Holds.
	 */
	public function register_routes(): void {
		register_rest_route(
			BooksEndpoint::NAMESPACE,
			'/holds',
			array(
				array(
					'methods'             => WP_REST_Server::READABLE,
					'callback'            => array( $this, 'get_holds' ),
					'permission_callback' => array( $this, 'can_hold' ),
				),
				array(
					'methods'             => WP_REST_Server::CREATABLE,
					'callback'            => array( $this, 'create_hold' ),
					'permission_callback' => array( $this, 'can_hold' ),
					'args'                => array(
						'book' => array(
							'description' => __( 'The ID of the book to reserve.', 'pagesco-books' ),
							'type'        => 'integer',
							'required'    => true,
							'minimum'     => 1,
						),
					),
				),
				'schema' => array( $this, 'get_schema' ),
			)
		);

		register_rest_route(
			BooksEndpoint::NAMESPACE,
			'/holds/(?P<id>\d+)',
			array(
				array(
					'methods'             => WP_REST_Server::DELETABLE,
					'callback'            => array( $this, 'cancel_hold' ),
					'permission_callback' => array( $this, 'can_hold' ),
					'args'                => array(
						'id' => array(
							'type'    => 'integer',
							'minimum' => 1,
						),
					),
				),
				'schema' => array( $this, 'get_schema' ),
			)
		);
	}

	/**
	 * Who may use the routes: logged-in users who may read (every role). Visitors get a 401.
	 *
	 * @return true|WP_Error
	 */
	public function can_hold() {
		if ( is_user_logged_in() && current_user_can( HoldActions::CUSTOMER_CAP ) ) {
			return true;
		}

		return new WP_Error(
			'rest_forbidden',
			__( 'Log in to reserve books.', 'pagesco-books' ),
			array( 'status' => rest_authorization_required_code() )
		);
	}

	/**
	 * GET /pagesco/v1/holds: the current user's holds, newest first. Only ever their own.
	 */
	public function get_holds(): WP_REST_Response {
		return rest_ensure_response( array_map( array( $this, 'prepare_hold' ), HoldsTable::for_user( get_current_user_id() ) ) );
	}

	/**
	 * POST /pagesco/v1/holds: places a hold and answers 201 Created, or the rule it broke.
	 *
	 * @param WP_REST_Request $request The request, its arguments validated.
	 * @return WP_REST_Response|WP_Error
	 */
	public function create_hold( WP_REST_Request $request ) {
		$hold = ( new Holds() )->place( $request['book'], get_current_user_id() );
		if ( is_wp_error( $hold ) ) {
			return $hold;
		}

		$response = rest_ensure_response( $this->prepare_hold( $hold ) );
		$response->set_status( 201 );

		return $response;
	}

	/**
	 * DELETE /pagesco/v1/holds/<id>: cancels one of the user's own waiting holds.
	 *
	 * @param WP_REST_Request $request The request.
	 * @return WP_REST_Response|WP_Error
	 */
	public function cancel_hold( WP_REST_Request $request ) {
		$hold = ( new Holds() )->cancel( $request['id'], get_current_user_id() );

		return is_wp_error( $hold ) ? $hold : rest_ensure_response( $this->prepare_hold( $hold ) );
	}

	/**
	 * One hold as the API shows it: real types, the computed status, and a label to show as it is.
	 *
	 * @param object $hold A row from HoldsTable.
	 */
	public function prepare_hold( object $hold ): array {
		return array(
			'id'        => (int) $hold->id,
			'book'      => (int) $hold->book_id,
			'title'     => get_post_field( 'post_title', (int) $hold->book_id ),
			'status'    => Holds::status( $hold ),
			'pickup_by' => $hold->pickup_by,
			'label'     => Holds::label( $hold ),
		);
	}

	/**
	 * The JSON Schema of one hold.
	 */
	public function get_schema(): array {
		return array(
			'$schema'    => 'http://json-schema.org/draft-04/schema#',
			'title'      => 'pagesco-hold',
			'type'       => 'object',
			'properties' => array(
				'id'        => array(
					'type'     => 'integer',
					'readonly' => true,
				),
				'book'      => array( 'type' => 'integer' ),
				'title'     => array( 'type' => 'string' ),
				'status'    => array(
					'type' => 'string',
					'enum' => array( 'waiting', 'expired', 'collected', 'cancelled' ),
				),
				'pickup_by' => array(
					'description' => 'Y-m-d',
					'type'        => 'string',
				),
				'label'     => array( 'type' => 'string' ),
			),
		);
	}
}

<?php
/**
 * The shop's events route: GET and POST /pagesco/v1/events.
 *
 * @package PagesCo\Books
 */

namespace PagesCo\Books\Rest;

use PagesCo\Books\EventsTable;
use PagesCo\Books\Feature;
use PagesCo\Books\Settings;
use WP_Error;
use WP_REST_Request;
use WP_REST_Response;
use WP_REST_Server;

/**
 * Lists the events from the custom table, and lets staff add one, through EventsTable (Lesson 5.5).
 */
final class EventsEndpoint implements Feature {

	/**
	 * Registers the route when the REST API starts.
	 */
	public function register(): void {
		add_action( 'rest_api_init', array( $this, 'register_routes' ) );
	}

	/**
	 * One route, two endpoints: anyone may read, staff may write.
	 */
	public function register_routes(): void {
		register_rest_route(
			BooksEndpoint::NAMESPACE,
			'/events',
			array(
				array(
					'methods'             => WP_REST_Server::READABLE,
					'callback'            => array( $this, 'get_events' ),
					'permission_callback' => '__return_true',
					'args'                => array(
						'limit'    => array(
							'description' => __( 'How many events at most. Default: the Events to show setting.', 'pagesco-books' ),
							'type'        => 'integer',
							'default'     => (int) Settings::get( 'events_limit' ),
							'minimum'     => 1,
							'maximum'     => 50,
						),
						'location' => array(
							'description' => __( 'Only events at this location (exact match).', 'pagesco-books' ),
							'type'        => 'string',
							'default'     => '',
						),
					),
				),
				array(
					'methods'             => WP_REST_Server::CREATABLE,
					'callback'            => array( $this, 'create_event' ),
					'permission_callback' => array( $this, 'can_manage_events' ),
					'args'                => array(
						'title'     => array(
							'description'       => __( 'The event\'s name.', 'pagesco-books' ),
							'type'              => 'string',
							'required'          => true,
							'minLength'         => 1,
							'maxLength'         => 200,
							'sanitize_callback' => 'sanitize_text_field',
							'validate_callback' => 'rest_validate_request_arg',
						),
						'starts_at' => array(
							'description'       => __( 'Local date and time, such as 2027-12-16 19:00.', 'pagesco-books' ),
							'type'              => 'string',
							'required'          => true,
							'validate_callback' => array( $this, 'validate_starts_at' ),
							'sanitize_callback' => array( $this, 'sanitize_starts_at' ),
						),
						'location'  => array(
							'description'       => __( 'Where in the shop.', 'pagesco-books' ),
							'type'              => 'string',
							'default'           => '',
							'maxLength'         => 200,
							'sanitize_callback' => 'sanitize_text_field',
							'validate_callback' => 'rest_validate_request_arg',
						),
						'capacity'  => array(
							'description' => __( 'Seats, or 0 for an event open to all.', 'pagesco-books' ),
							'type'        => 'integer',
							'default'     => 0,
							'minimum'     => 0,
							'maximum'     => 65535,
						),
					),
				),
				'schema' => array( $this, 'get_schema' ),
			)
		);
	}

	/**
	 * Who may add or change events: staff who may edit everyone's posts (editors and administrators).
	 *
	 * @return true|WP_Error
	 */
	public function can_manage_events() {
		if ( current_user_can( 'edit_others_posts' ) ) {
			return true;
		}

		return new WP_Error(
			'rest_forbidden',
			__( 'Sorry, you are not allowed to manage events.', 'pagesco-books' ),
			array( 'status' => rest_authorization_required_code() )
		);
	}

	/**
	 * Accepts a local date and time written Y-m-d H:i, such as 2027-12-16 19:00.
	 *
	 * @param mixed $value The starts_at argument as sent.
	 * @return true|WP_Error
	 */
	public function validate_starts_at( $value ) {
		$date = is_string( $value ) ? \DateTime::createFromFormat( '!Y-m-d H:i', $value ) : false;

		if ( $date && $date->format( 'Y-m-d H:i' ) === $value ) {
			return true;
		}

		return new WP_Error( 'pagesco_invalid_date', __( 'starts_at must be a date and time such as 2027-12-16 19:00.', 'pagesco-books' ) );
	}

	/**
	 * Turns a valid starts_at into the table's DATETIME format.
	 *
	 * @param string $value A value validate_starts_at() accepted.
	 */
	public function sanitize_starts_at( $value ): string {
		return $value . ':00';
	}

	/**
	 * GET /pagesco/v1/events: events in date order, from the custom table.
	 *
	 * @param WP_REST_Request $request The request.
	 */
	public function get_events( WP_REST_Request $request ): WP_REST_Response {
		$events = EventsTable::find( $request['limit'], $request['location'] );

		return rest_ensure_response( array_map( array( $this, 'prepare_event' ), $events ) );
	}

	/**
	 * POST /pagesco/v1/events: adds an event and answers 201 Created with it.
	 *
	 * @param WP_REST_Request $request The request, its arguments validated and sanitized.
	 * @return WP_REST_Response|WP_Error
	 */
	public function create_event( WP_REST_Request $request ) {
		$id = EventsTable::add( $request['title'], $request['starts_at'], $request['location'], $request['capacity'] );

		if ( ! $id ) {
			return new WP_Error( 'pagesco_event_not_saved', __( 'The event could not be saved.', 'pagesco-books' ), array( 'status' => 500 ) );
		}

		$response = rest_ensure_response(
			$this->prepare_event(
				(object) array(
					'id'        => $id,
					'title'     => $request['title'],
					'starts_at' => $request['starts_at'],
					'location'  => $request['location'],
					'capacity'  => $request['capacity'],
				)
			)
		);
		$response->set_status( 201 );

		return $response;
	}

	/**
	 * One event as the API shows it. Table rows arrive as strings; the API promises real types.
	 *
	 * @param object $event A row from EventsTable::find(), or the same shape.
	 */
	public function prepare_event( object $event ): array {
		return array(
			'id'        => (int) $event->id,
			'title'     => $event->title,
			'starts_at' => mysql2date( 'Y-m-d\TH:i:s', $event->starts_at, false ),
			'location'  => $event->location,
			'capacity'  => (int) $event->capacity,
		);
	}

	/**
	 * The JSON Schema of one event.
	 */
	public function get_schema(): array {
		return array(
			'$schema'    => 'http://json-schema.org/draft-04/schema#',
			'title'      => 'pagesco-event',
			'type'       => 'object',
			'properties' => array(
				'id'        => array(
					'type'     => 'integer',
					'readonly' => true,
				),
				'title'     => array( 'type' => 'string' ),
				'starts_at' => array(
					'type'   => 'string',
					'format' => 'date-time',
				),
				'location'  => array( 'type' => 'string' ),
				'capacity'  => array( 'type' => 'integer' ),
			),
		);
	}
}

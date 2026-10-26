import { store, getContext, withSyncEvent } from '@wordpress/interactivity';

const { state } = store( 'pagesco/reserve', {
	actions: {
		// The form works without JavaScript (admin-post.php). With JavaScript, the REST API answers and the page stays.
		// A generator action: each yield waits for a promise, and the store keeps the block's context for us.
		reserve: withSyncEvent( function* ( event ) {
			event.preventDefault();
			const context = getContext();
			context.busy = true;

			try {
				const response = yield fetch( state.url, {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						'X-WP-Nonce': state.nonce,
					},
					body: JSON.stringify( { book: context.book } ),
				} );
				const answer = yield response.json();

				// The hold's label, or the error message of the rule it broke: both translated by the server.
				context.message = response.ok ? answer.label : answer.message;
				context.done = response.ok;
			} catch ( error ) {
				// No answer at all (the network, a timeout): send the form the old way.
				event.target.submit();
			} finally {
				context.busy = false;
			}
		} ),
	},
} );

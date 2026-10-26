import { store, getContext, withSyncEvent } from '@wordpress/interactivity';

const { state } = store( 'pagesco/book-filter', {
	state: {
		// The same derived state as the closures in render.php, for the browser.
		get isVisible() {
			const { genres } = getContext();
			return state.genre === '' || genres.includes( state.genre );
		},
		get isSelected() {
			return getContext().slug === state.genre;
		},
		get visibleCount() {
			return state.bookGenres.filter(
				( genres ) => state.genre === '' || genres.includes( state.genre )
			).length;
		},
	},
	actions: {
		// withSyncEvent: this action needs the event right away, to stop the link.
		selectGenre: withSyncEvent( ( event ) => {
			event.preventDefault();
			state.genre = getContext().slug;

			// Keep the address in step, so a reload or a shared link shows the same list.
			const url = new URL( window.location.href );
			if ( state.genre ) {
				url.searchParams.set( 'genre', state.genre );
			} else {
				url.searchParams.delete( 'genre' );
			}
			window.history.replaceState( null, '', url );
		} ),
	},
} );

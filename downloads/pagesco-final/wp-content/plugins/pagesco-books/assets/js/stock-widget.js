/**
 * Stock at a glance: lists the books and switches their stock, through the REST API.
 *
 * Plain JavaScript, no build step: wp.apiFetch and wp.i18n come from WordPress
 * (the script's dependencies), and apiFetch sends the REST nonce for the logged-in user.
 */
( function () {
	const { __, sprintf } = wp.i18n;
	const widget = document.getElementById( 'pagesco-stock-widget' );

	if ( ! widget ) {
		return;
	}

	const status = widget.querySelector( '.pagesco-stock-widget__status' );
	const list = widget.querySelector( '.pagesco-stock-widget__books' );

	// One line per book: its title and stock, and a button that switches the stock.
	function bookItem( book ) {
		const item = document.createElement( 'li' );
		const label = document.createElement( 'span' );
		const button = document.createElement( 'button' );

		label.textContent = book.meta.pagesco_in_stock
			? /* translators: %s: book title. */ sprintf( __( '%s: in stock', 'pagesco-books' ), book.title.raw )
			: /* translators: %s: book title. */ sprintf( __( '%s: sold out', 'pagesco-books' ), book.title.raw );

		button.type = 'button';
		button.className = 'button button-small';
		button.textContent = book.meta.pagesco_in_stock
			? __( 'Mark sold out', 'pagesco-books' )
			: __( 'Mark in stock', 'pagesco-books' );
		button.addEventListener( 'click', () => switchStock( book, item, button ) );

		item.append( label, ' ', button );
		return item;
	}

	// POST /wp/v2/books/<id> with the opposite stock; the answer is the updated book.
	async function switchStock( book, item, button ) {
		button.disabled = true;
		try {
			const updated = await wp.apiFetch( {
				path: `/wp/v2/books/${ book.id }?context=edit&_fields=id,title,meta`,
				method: 'POST',
				data: { meta: { pagesco_in_stock: ! book.meta.pagesco_in_stock } },
			} );
			item.replaceWith( bookItem( updated ) );
			/* translators: %s: book title. */
			status.textContent = sprintf( __( 'Saved: %s', 'pagesco-books' ), updated.title.raw );
		} catch ( error ) {
			status.textContent = error.message;
			button.disabled = false;
		}
	}

	// GET the catalog, sorted by title, with only the fields the widget needs.
	wp.apiFetch( {
		path: '/wp/v2/books?per_page=100&orderby=title&order=asc&context=edit&_fields=id,title,meta',
	} )
		.then( ( books ) => {
			list.replaceChildren( ...books.map( bookItem ) );
			/* translators: %d: number of books. */
			status.textContent = sprintf( __( '%d books in the catalog.', 'pagesco-books' ), books.length );
		} )
		.catch( ( error ) => {
			status.textContent = error.message;
		} );
} )();

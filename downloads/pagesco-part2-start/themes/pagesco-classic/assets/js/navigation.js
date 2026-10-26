/**
 * Pages & Co. Classic: opens and closes the primary menu on small screens.
 */
( function () {
	const nav = document.querySelector( '.site-nav' );
	const button = nav ? nav.querySelector( '.menu-toggle' ) : null;

	if ( ! button ) {
		return;
	}

	// Only now, with JavaScript running, may the menu start closed.
	nav.classList.add( 'is-collapsible' );

	button.addEventListener( 'click', function () {
		const open = 'true' !== button.getAttribute( 'aria-expanded' );
		button.setAttribute( 'aria-expanded', String( open ) );
		nav.classList.toggle( 'is-open', open );
	} );
}() );

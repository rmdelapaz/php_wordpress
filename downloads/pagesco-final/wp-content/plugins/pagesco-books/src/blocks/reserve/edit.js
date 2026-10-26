import { __ } from '@wordpress/i18n';
import { useBlockProps } from '@wordpress/block-editor';

export default function Edit() {
	// What a customer sees depends on who is logged in, so the editor shows the button as an example.
	return (
		<div { ...useBlockProps() }>
			<button type="button" className="wp-element-button" disabled>
				{ __( 'Reserve for pickup', 'pagesco-books' ) }
			</button>
		</div>
	);
}

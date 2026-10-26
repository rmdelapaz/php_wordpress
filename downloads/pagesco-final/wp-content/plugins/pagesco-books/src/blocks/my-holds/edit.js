import { __ } from '@wordpress/i18n';
import { useBlockProps } from '@wordpress/block-editor';

export default function Edit() {
	// Every customer sees their own list, so the editor shows a description instead of a preview.
	return (
		<p { ...useBlockProps() }>
			{ __(
				'My Holds: each logged-in customer sees their holds here, and can cancel the ones still waiting.',
				'pagesco-books'
			) }
		</p>
	);
}

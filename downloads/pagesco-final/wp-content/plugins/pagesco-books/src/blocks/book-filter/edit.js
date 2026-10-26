import { useBlockProps } from '@wordpress/block-editor';
import ServerSideRender from '@wordpress/server-side-render';

export default function Edit() {
	// A preview from render.php; the filter itself works on the front end.
	return (
		<div { ...useBlockProps() }>
			<ServerSideRender
				block="pagesco/book-filter"
				skipBlockSupportAttributes
			/>
		</div>
	);
}

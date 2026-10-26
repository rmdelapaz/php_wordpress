/**
 * The Shelf Label's saved HTML.
 */
import { useBlockProps } from '@wordpress/block-editor';

export default function save() {
	return <p { ...useBlockProps.save() }>{ 'Staff picks' }</p>;
}

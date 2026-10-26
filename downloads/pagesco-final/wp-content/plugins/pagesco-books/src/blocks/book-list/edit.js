import { __ } from '@wordpress/i18n';
import { InspectorControls, useBlockProps } from '@wordpress/block-editor';
import { PanelBody, RangeControl, SelectControl } from '@wordpress/components';
import { useSelect } from '@wordpress/data';
import { store as coreStore } from '@wordpress/core-data';
import ServerSideRender from '@wordpress/server-side-render';

export default function Edit( { attributes, setAttributes } ) {
	const { count, genre, orderBy } = attributes;

	// The genre terms, from the REST API (/wp/v2/genres), cached by the editor.
	const genres = useSelect(
		( select ) =>
			select( coreStore ).getEntityRecords( 'taxonomy', 'genre', {
				per_page: -1,
			} ),
		[]
	);

	const genreOptions = [
		{ label: __( 'All genres', 'pagesco-books' ), value: '' },
		...( genres || [] ).map( ( term ) => ( {
			label: term.name,
			value: term.slug,
		} ) ),
	];

	return (
		<>
			<InspectorControls>
				<PanelBody title={ __( 'List settings', 'pagesco-books' ) }>
					<RangeControl
						__next40pxDefaultSize
						label={ __( 'Number of books', 'pagesco-books' ) }
						help={ __(
							'Reset to use the Books per list setting.',
							'pagesco-books'
						) }
						value={ count }
						onChange={ ( value ) => setAttributes( { count: value } ) }
						min={ 1 }
						max={ 24 }
						allowReset
					/>
					<SelectControl
						__next40pxDefaultSize
						label={ __( 'Genre', 'pagesco-books' ) }
						value={ genre }
						options={ genreOptions }
						onChange={ ( value ) => setAttributes( { genre: value } ) }
					/>
					<SelectControl
						__next40pxDefaultSize
						label={ __( 'Order', 'pagesco-books' ) }
						value={ orderBy }
						options={ [
							{ label: __( 'Title, A to Z', 'pagesco-books' ), value: 'title' },
							{ label: __( 'Newest first', 'pagesco-books' ), value: 'newest' },
							{ label: __( 'Price, low to high', 'pagesco-books' ), value: 'price' },
						] }
						onChange={ ( value ) => setAttributes( { orderBy: value } ) }
					/>
				</PanelBody>
			</InspectorControls>
			<div { ...useBlockProps() }>
				<ServerSideRender
					block="pagesco/book-list"
					attributes={ attributes }
					skipBlockSupportAttributes
				/>
			</div>
		</>
	);
}

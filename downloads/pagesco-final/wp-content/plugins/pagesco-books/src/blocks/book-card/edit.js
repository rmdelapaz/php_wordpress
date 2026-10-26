import { __ } from '@wordpress/i18n';
import {
	InspectorControls,
	RichText,
	useBlockProps,
} from '@wordpress/block-editor';
import {
	PanelBody,
	SelectControl,
	TextControl,
	ToggleControl,
} from '@wordpress/components';
import './editor.scss';

export default function Edit( { attributes, setAttributes } ) {
	const { title, author, pick, url, headingLevel, showBadge } = attributes;

	return (
		<>
			<InspectorControls>
				<PanelBody title={ __( 'Card settings', 'pagesco-books' ) }>
					<TextControl
						__next40pxDefaultSize
						label={ __( 'Link to the book', 'pagesco-books' ) }
						type="url"
						value={ url || '' }
						onChange={ ( value ) => setAttributes( { url: value } ) }
					/>
					<SelectControl
						__next40pxDefaultSize
						label={ __( 'Heading level', 'pagesco-books' ) }
						value={ headingLevel }
						options={ [ 2, 3, 4, 5, 6 ].map( ( level ) => ( {
							label: 'H' + level,
							value: level,
						} ) ) }
						onChange={ ( value ) =>
							setAttributes( { headingLevel: Number( value ) } )
						}
					/>
					<ToggleControl
						label={ __( 'Show the "Staff pick" badge', 'pagesco-books' ) }
						checked={ showBadge }
						onChange={ ( value ) => setAttributes( { showBadge: value } ) }
					/>
				</PanelBody>
			</InspectorControls>
			<div { ...useBlockProps() }>
				{ showBadge && (
					<p className="wp-block-pagesco-book-card__badge">Staff pick</p>
				) }
				<RichText
					tagName={ 'h' + headingLevel }
					className="wp-block-pagesco-book-card__title"
					value={ title }
					onChange={ ( value ) => setAttributes( { title: value } ) }
					placeholder={ __( 'Book title', 'pagesco-books' ) }
					allowedFormats={ [] }
				/>
				<RichText
					tagName="p"
					className="wp-block-pagesco-book-card__author"
					value={ author }
					onChange={ ( value ) => setAttributes( { author: value } ) }
					placeholder={ __( 'Author', 'pagesco-books' ) }
					allowedFormats={ [] }
				/>
				<RichText
					tagName="p"
					className="wp-block-pagesco-book-card__pick"
					value={ pick }
					onChange={ ( value ) => setAttributes( { pick: value } ) }
					placeholder={ __( 'Why do you recommend it?', 'pagesco-books' ) }
					allowedFormats={ [ 'core/bold', 'core/italic' ] }
				/>
			</div>
		</>
	);
}

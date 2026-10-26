import { RichText, useBlockProps } from '@wordpress/block-editor';

/**
 * Earlier versions of the block, newest first. Each one describes the
 * attributes and the save() output that cards saved back then still have.
 */
const v1 = {
	attributes: {
		title: {
			type: 'string',
			source: 'html',
			selector: '.wp-block-pagesco-book-card__title',
		},
		author: {
			type: 'string',
			source: 'html',
			selector: '.wp-block-pagesco-book-card__author',
		},
		pick: {
			type: 'string',
			source: 'html',
			selector: '.wp-block-pagesco-book-card__pick',
		},
		url: {
			type: 'string',
			source: 'attribute',
			selector: '.wp-block-pagesco-book-card__link',
			attribute: 'href',
		},
		headingLevel: {
			type: 'integer',
			default: 3,
		},
	},
	supports: {
		html: false,
		color: { background: true, text: true, link: true },
		spacing: { margin: true, padding: true },
		typography: { fontSize: true, lineHeight: true },
	},
	// Cards saved before the badge existed keep looking as they did.
	migrate( attributes ) {
		return { ...attributes, showBadge: false };
	},
	save( { attributes } ) {
		const { title, author, pick, url, headingLevel } = attributes;

		const heading = (
			<RichText.Content
				tagName={ 'h' + headingLevel }
				className="wp-block-pagesco-book-card__title"
				value={ title }
			/>
		);

		return (
			<div { ...useBlockProps.save() }>
				{ url ? (
					<a className="wp-block-pagesco-book-card__link" href={ url }>
						{ heading }
					</a>
				) : (
					heading
				) }
				<RichText.Content
					tagName="p"
					className="wp-block-pagesco-book-card__author"
					value={ author }
				/>
				<RichText.Content
					tagName="p"
					className="wp-block-pagesco-book-card__pick"
					value={ pick }
				/>
			</div>
		);
	},
};

export default [ v1 ];

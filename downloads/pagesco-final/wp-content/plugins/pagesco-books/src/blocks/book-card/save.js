import { RichText, useBlockProps } from '@wordpress/block-editor';

export default function save( { attributes } ) {
	const { title, author, pick, url, headingLevel, showBadge } = attributes;

	const heading = (
		<RichText.Content
			tagName={ 'h' + headingLevel }
			className="wp-block-pagesco-book-card__title"
			value={ title }
		/>
	);

	return (
		<div { ...useBlockProps.save() }>
			{ showBadge && (
				<p className="wp-block-pagesco-book-card__badge">Staff pick</p>
			) }
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
}

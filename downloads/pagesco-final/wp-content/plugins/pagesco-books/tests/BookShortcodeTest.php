<?php
/**
 * Tests of the [pagesco_book] shortcode.
 *
 * @package PagesCo\Books
 */

namespace PagesCo\Books\Tests;

use PagesCo\Books\Shortcodes\BookShortcode;

/**
 * The shortcode prints a published book's card, escaped, and nothing for anything else.
 */
final class BookShortcodeTest extends \WP_UnitTestCase {

	/**
	 * A published book shows its title, author, price and stock.
	 */
	public function test_renders_a_published_book(): void {
		$book_id = self::factory()->post->create(
			array(
				'post_type'  => 'book',
				'post_title' => 'Emma',
				'meta_input' => array(
					'pagesco_author'   => 'Jane Austen',
					'pagesco_price'    => 9.49,
					'pagesco_in_stock' => true,
				),
			)
		);

		$html = ( new BookShortcode() )->render( array( 'id' => $book_id ) );

		$this->assertStringContainsString( '>Emma</a> by Jane Austen,', $html );
		$this->assertStringContainsString( '<span class="pagesco-book__price">$9.49</span>', $html );
		$this->assertStringContainsString( '<span class="pagesco-book__stock">In stock</span>', $html );
	}

	/**
	 * Drafts and posts of other types print nothing.
	 */
	public function test_prints_nothing_for_drafts_and_pages(): void {
		$draft = self::factory()->post->create(
			array(
				'post_type'   => 'book',
				'post_status' => 'draft',
			)
		);
		$page  = self::factory()->post->create( array( 'post_type' => 'page' ) );

		$this->assertSame( '', ( new BookShortcode() )->render( array( 'id' => $draft ) ) );
		$this->assertSame( '', ( new BookShortcode() )->render( array( 'id' => $page ) ) );
	}

	/**
	 * Meta is escaped: markup in an author's name is shown as text.
	 */
	public function test_escapes_the_author(): void {
		$book_id = self::factory()->post->create(
			array(
				'post_type'  => 'book',
				'meta_input' => array( 'pagesco_author' => '<script>alert(1)</script>' ),
			)
		);

		$html = ( new BookShortcode() )->render( array( 'id' => $book_id ) );

		$this->assertStringNotContainsString( '<script>', $html );
		$this->assertStringContainsString( '&lt;script&gt;', $html );
	}
}

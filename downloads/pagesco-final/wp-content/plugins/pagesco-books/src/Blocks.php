<?php
/**
 * The plugin's blocks, built from src/blocks/ into build/blocks/.
 *
 * @package PagesCo\Books
 */

namespace PagesCo\Books;

/**
 * Registers every block in build/blocks/ from the manifest that npm run build writes.
 */
final class Blocks implements Feature {

	/**
	 * Registers the blocks on init, like core registers its own.
	 */
	public function register(): void {
		add_action( 'init', array( $this, 'register_blocks' ) );
	}

	/**
	 * Registers the block types listed in build/blocks/blocks-manifest.php.
	 */
	public function register_blocks(): void {
		wp_register_block_types_from_metadata_collection(
			PAGESCO_BOOKS_DIR . 'build/blocks',
			PAGESCO_BOOKS_DIR . 'build/blocks/blocks-manifest.php'
		);
	}
}

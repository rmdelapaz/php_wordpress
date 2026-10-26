<?php
/**
 * The contract every feature of the plugin follows.
 *
 * @package PagesCo\Books
 */

namespace PagesCo\Books;

/**
 * A feature adds its hooks in register(), and does nothing before that.
 */
interface Feature {

	/**
	 * Adds the feature's actions and filters.
	 */
	public function register(): void;
}

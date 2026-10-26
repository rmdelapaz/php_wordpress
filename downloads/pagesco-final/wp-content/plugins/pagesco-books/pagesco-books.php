<?php
/**
 * Plugin Name:       Pages & Co. Books
 * Description:       The bookstore features of the Pages & Co. website: books, genres, events, holds and the shop's blocks.
 * Version:           1.2.0
 * Requires at least: 6.9
 * Requires PHP:      8.2
 * Author:            Pages & Co.
 * License:           GPL-2.0-or-later
 * License URI:       https://www.gnu.org/licenses/gpl-2.0.html
 * Text Domain:       pagesco-books
 * Domain Path:       /languages
 * Update URI:        false
 *
 * @package PagesCo\Books
 */

defined( 'ABSPATH' ) || exit;

define( 'PAGESCO_BOOKS_VERSION', '1.2.0' );
define( 'PAGESCO_BOOKS_FILE', __FILE__ );
define( 'PAGESCO_BOOKS_DIR', plugin_dir_path( __FILE__ ) );

require PAGESCO_BOOKS_DIR . 'vendor/autoload.php';

add_action( 'plugins_loaded', array( PagesCo\Books\Plugin::instance(), 'boot' ) );

register_activation_hook( __FILE__, array( PagesCo\Books\Activator::class, 'activate' ) );
register_deactivation_hook( __FILE__, array( PagesCo\Books\Activator::class, 'deactivate' ) );

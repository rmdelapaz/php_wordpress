<?php
/**
 * Runs when an administrator deletes the plugin (or: wp plugin uninstall pagesco-gift-wrap --skip-delete).
 */
defined( 'WP_UNINSTALL_PLUGIN' ) || exit;
delete_option( 'pagesco_gift_wrap_price' );

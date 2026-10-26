<?php
// Hide PHP 8.5 deprecation notices raised by WP-CLI's own code (files inside the wp-cli phar).
// Every other notice is shown as usual: your themes and plugins, and code you run with wp eval.
set_error_handler(
	static fn ( int $errno, string $message, string $file = '' ): bool
		=> str_starts_with( $file, 'phar://' ) && ! str_contains( $file, "eval()'d code" ),
	E_DEPRECATED | E_USER_DEPRECATED
);

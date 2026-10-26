<?php
/**
 * psr4_paths_solution.php: the PSR-4 rule, done by hand (Session 9, Lesson 5.1, lab B, reference)
 * state: after:lesson_13
 * expect: PagesCo\Books\Admin\SettingsPage     src/Admin/SettingsPage.php
 * expect: pagesco\books\plugin                 (no rule matches: not autoloaded)
 */
$pagesco_rules = array(
	'PagesCo\\Books\\' => 'src/',
	'PagesCo\\Shop\\'  => 'shop/src/',
);

/**
 * Returns the file PSR-4 would load for $class, or null when no rule matches.
 *
 * @param string $class The fully qualified class name.
 * @param array  $rules Namespace prefix => folder.
 * @return string|null
 */
function pagesco_psr4_file( $class, $rules ) {
	foreach ( $rules as $prefix => $folder ) {
		if ( str_starts_with( $class, $prefix ) ) {
			return $folder . str_replace( '\\', '/', substr( $class, strlen( $prefix ) ) ) . '.php';
		}
	}
	return null;
}

$pagesco_classes = array(
	'PagesCo\Books\Plugin',
	'PagesCo\Books\Admin\SettingsPage',
	'PagesCo\Books\Rest\BooksController',
	'PagesCo\Shop\Cart',
	'pagesco\books\plugin',
);
foreach ( $pagesco_classes as $pagesco_class ) {
	printf( "%-36s %s\n", $pagesco_class, pagesco_psr4_file( $pagesco_class, $pagesco_rules ) ?? '(no rule matches: not autoloaded)' );
}

// TODO 3's answer: PHP compares class names without case, but the autoloader compares STRINGS and builds a
// file name from them; on Linux, src/plugin.php and src/Plugin.php are different files. Write every class
// name exactly as declared (Lesson 5.1, Project Step 3).

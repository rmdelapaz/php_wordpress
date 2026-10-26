<?php
/**
 * psr4_paths_starter.php: the PSR-4 rule, done by hand (Session 9, Lesson 5.1, lab B)
 * state: after:lesson_13
 * expect: PagesCo\Books\Plugin                 TODO
 *
 * Composer's autoloader turns a class name into a file name with one rule per namespace prefix (Lesson 5.1,
 * "A Structure That Grows"). Write that rule yourself, then ask it about five class names. From your project folder:
 *     cp labs/module-09/l5_1-first-plugin/psr4_paths_starter.php wordpress/
 *     wp eval-file --use-include psr4_paths_starter.php
 * When you are done: rm wordpress/psr4_paths_starter.php
 */
$pagesco_rules = array(
	'PagesCo\\Books\\' => 'src/',
	// TODO 2: a second rule: classes in PagesCo\Shop\ live in shop/src/.
);

/**
 * Returns the file PSR-4 would load for $class, or null when no rule matches.
 *
 * @param string $class The fully qualified class name.
 * @param array  $rules Namespace prefix => folder.
 * @return string|null
 */
function pagesco_psr4_file( $class, $rules ) {
	// TODO 1: for each rule whose prefix starts the class name (str_starts_with(), letter for letter), return the
	// folder, then the rest of the name (substr()) with every \ turned into / (str_replace()), then '.php'.
	return 'TODO';
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

// TODO 3: the last line printed. Why does a class written in lowercase find no file, although PHP itself treats
// class names as case-insensitive? Write your answer here as a comment.

// Expected when done (psr4_paths_solution.php):
// PagesCo\Books\Plugin                 src/Plugin.php
// PagesCo\Books\Admin\SettingsPage     src/Admin/SettingsPage.php
// PagesCo\Books\Rest\BooksController   src/Rest/BooksController.php
// PagesCo\Shop\Cart                    shop/src/Cart.php
// pagesco\books\plugin                 (no rule matches: not autoloaded)

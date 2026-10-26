<?php
/**
 * files_list_starter.php: which src/ folders would a release ZIP leave out? (Session 18, Lesson 9.1, lab B)
 * state: after:lesson_29
 * expect: src/Holds (planned)        TODO
 *
 * npm run plugin-zip packs only the paths in package.json's "files" (Lesson 8.3), and nothing warns about a folder
 * that is not listed (Lesson 9.1, Common Mistake 1). This check needs no Node: it compares the folders in src/
 * with the list, and also a folder you plan to add. From your project folder:
 *     cp labs/module-18/l9_1-final-project/files_list_starter.php wordpress/
 *     wp eval-file --use-include files_list_starter.php
 * Do TODOs 1 to 3, run again, compare with "Expected when done".
 * When you are done: rm wordpress/files_list_starter.php
 */
$pagesco_dir   = WP_PLUGIN_DIR . '/pagesco-books';
$pagesco_files = json_decode( (string) file_get_contents( $pagesco_dir . '/package.json' ), true )['files'];

// TODO 1: the folders in src/, each as 'src/<name>': glob( $pagesco_dir . '/src/*', GLOB_ONLYDIR ) gives full
// paths; array_map() with basename() makes the names.
$pagesco_folders = array();
$pagesco_folders[] = 'src/Holds (planned)';

foreach ( $pagesco_folders as $pagesco_folder ) {
	$pagesco_path = strtok( $pagesco_folder, ' ' );   // 'src/Holds (planned)' -> 'src/Holds'
	// TODO 2: three verdicts. In $pagesco_files (strict in_array()): 'shipped'. The block sources, src/blocks,
	// while "build" is listed: 'not shipped, on purpose: build/ ships the blocks'. Anything else:
	// 'MISSING from "files": add it in the same commit'.
	$pagesco_verdict = 'TODO';
	printf( "%-26s %s\n", $pagesco_folder, $pagesco_verdict );
}

// TODO 3: count the PHP files directly in src/ (glob() with '/src/*.php') and print
// "src/*.php: <n> files, shipped by the pattern "src/*.php"".
echo "src/*.php: TODO\n";

// Expected when done (files_list_solution.php, the course site after Lesson 8.4):
// src/Admin                  shipped
// src/Rest                   shipped
// src/Shortcodes             shipped
// src/Supplier               shipped
// src/blocks                 not shipped, on purpose: build/ ships the blocks
// src/Holds (planned)        MISSING from "files": add it in the same commit
// src/*.php: 13 files, shipped by the pattern "src/*.php"

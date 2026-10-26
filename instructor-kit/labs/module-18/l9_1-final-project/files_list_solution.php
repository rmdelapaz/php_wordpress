<?php
/**
 * files_list_solution.php: which src/ folders would a release ZIP leave out? (Session 18, Lesson 9.1, lab B)
 * state: after:lesson_29
 * expect: src/Holds (planned)        MISSING from "files": add it in the same commit
 *
 * The reference for files_list_starter.php. npm run plugin-zip packs only the paths in package.json's "files"
 * (Lesson 8.3), and nothing warns about a folder that is not listed (Lesson 9.1, Common Mistake 1). This check
 * needs no Node: it compares the folders in src/ with the list, and also a folder you plan to add.
 */
$pagesco_dir   = WP_PLUGIN_DIR . '/pagesco-books';
$pagesco_files = json_decode( (string) file_get_contents( $pagesco_dir . '/package.json' ), true )['files'];

$pagesco_folders = array_map(
	fn( $path ) => 'src/' . basename( $path ),
	glob( $pagesco_dir . '/src/*', GLOB_ONLYDIR )
);
$pagesco_folders[] = 'src/Holds (planned)';

foreach ( $pagesco_folders as $pagesco_folder ) {
	$pagesco_path = strtok( $pagesco_folder, ' ' );
	if ( in_array( $pagesco_path, $pagesco_files, true ) ) {
		$pagesco_verdict = 'shipped';
	} elseif ( 'src/blocks' === $pagesco_path && in_array( 'build', $pagesco_files, true ) ) {
		$pagesco_verdict = 'not shipped, on purpose: build/ ships the blocks';
	} else {
		$pagesco_verdict = 'MISSING from "files": add it in the same commit';
	}
	printf( "%-26s %s\n", $pagesco_folder, $pagesco_verdict );
}

printf( "src/*.php: %d files, shipped by the pattern \"src/*.php\"\n", count( glob( $pagesco_dir . '/src/*.php' ) ) );

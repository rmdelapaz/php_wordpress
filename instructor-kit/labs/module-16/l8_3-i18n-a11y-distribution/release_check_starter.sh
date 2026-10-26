# release_check_starter.sh: before you ship a release ZIP, check what it promises (Session 16, Lesson 8.3, lab C)
# state: after:lesson_28
# expect: requires WordPress: TODO
#
# A version lives in four places (Lesson 8.3, "Versions"), the requirements in two, and the ZIP must hold what the
# plugin needs and nothing a developer uses. This script checks all of it in the plugin's folder, after Lesson
# 8.3's project built pagesco-books.zip. From your project folder:
#     cp labs/module-16/l8_3-i18n-a11y-distribution/release_check_starter.sh wordpress/
#     docker compose run --rm wpcli sh release_check_starter.sh
# The version check is done for you: read how it finds each value (grep -m1, awk '{print $NF}', cut). TODO 1 to 3
# work the same way. Every failed check adds 1 to problems. Compare with "Expected when done" at the end, then
# break something on purpose (a Stable tag of 1.0.9 in readme.txt) and run again; put it back afterwards.
# When you are done: rm wordpress/release_check_starter.sh

cd wp-content/plugins/pagesco-books
problems=0

header=$(grep -m1 '^ \* Version:' pagesco-books.php | awk '{print $NF}')
constant=$(grep -o "define( 'PAGESCO_BOOKS_VERSION', '[^']*'" pagesco-books.php | cut -d"'" -f4)
stable=$(grep -m1 '^Stable tag:' readme.txt | awk '{print $NF}')
npm=$(grep -m1 '"version":' package.json | cut -d'"' -f4)
if [ "$header" = "$constant" ] && [ "$header" = "$stable" ] && [ "$header" = "$npm" ]; then
	echo "versions agree: $header $constant $stable $npm"
else
	echo "VERSIONS DIFFER: header $header, constant $constant, readme $stable, package.json $npm"
	problems=$((problems + 1))
fi

# TODO 1: compare "Requires at least:" in pagesco-books.php with the same header in readme.txt.
echo "requires WordPress: TODO"

# TODO 2: read the Domain Path header (/languages) and check that pagesco-books.pot is in that folder.
echo "translations: TODO"

# TODO 3: list the ZIP's files (unzip -l pagesco-books.zip, the 4th column from line 4 on) into a file in /tmp,
#         print how many there are, add a problem for each file the plugin needs that is MISSING
#         (pagesco-books/pagesco-books.php, .../readme.txt, .../vendor/autoload.php,
#         .../build/blocks/blocks-manifest.php) and for each that SHOULD NOT SHIP (tests/, phpcs.xml.dist,
#         phpunit.xml.dist, .wp-env.json, node_modules/, src/blocks/, autoload_files.php). Delete the /tmp file.
echo "the ZIP: TODO"
echo "release check: $problems problems"

# Expected when done (release_check_solution.sh, the course site after Lesson 8.3):
# versions agree: 1.1.0 1.1.0 1.1.0 1.1.0
# requires WordPress 6.9 in both
# translations: ./languages/pagesco-books.pot
# the ZIP: 72 entries
# release check: 0 problems

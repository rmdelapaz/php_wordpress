# release_check_solution.sh: before you ship a release ZIP, check what it promises (Session 16, Lesson 8.3, lab C)
# state: after:lesson_28
# expect: versions agree: 1.1.0 1.1.0 1.1.0 1.1.0
# expect: release check: 0 problems
#
# A version lives in four places (Lesson 8.3, "Versions"), the requirements in two, and the ZIP must hold what the
# plugin needs and nothing a developer uses. This script checks all of it in the plugin's folder, after Lesson
# 8.3's project built pagesco-books.zip. From your project folder:
#     cp labs/module-16/l8_3-i18n-a11y-distribution/release_check_solution.sh wordpress/
#     docker compose run --rm wpcli sh release_check_solution.sh
#     rm wordpress/release_check_solution.sh

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

wp_header=$(grep -m1 'Requires at least:' pagesco-books.php | awk '{print $NF}')
wp_readme=$(grep -m1 '^Requires at least:' readme.txt | awk '{print $NF}')
if [ "$wp_header" = "$wp_readme" ]; then echo "requires WordPress $wp_header in both"; else echo "REQUIRES DIFFER: $wp_header and $wp_readme"; problems=$((problems + 1)); fi

domain_path=$(grep -m1 'Domain Path:' pagesco-books.php | awk '{print $NF}')
if [ -f ".$domain_path/pagesco-books.pot" ]; then echo "translations: .$domain_path/pagesco-books.pot"; else echo "NO POT in .$domain_path"; problems=$((problems + 1)); fi

unzip -l pagesco-books.zip | awk 'NR > 3 {print $4}' | grep . > /tmp/pagesco-zip.txt
echo "the ZIP: $(grep -c . /tmp/pagesco-zip.txt) entries"
for needed in pagesco-books/pagesco-books.php pagesco-books/readme.txt pagesco-books/vendor/autoload.php pagesco-books/build/blocks/blocks-manifest.php; do
	grep -q -x "$needed" /tmp/pagesco-zip.txt || { echo "MISSING from the ZIP: $needed"; problems=$((problems + 1)); }
done
for unwanted in tests/ phpcs.xml.dist phpunit.xml.dist .wp-env.json node_modules/ src/blocks/ autoload_files.php; do
	if grep -q -F "$unwanted" /tmp/pagesco-zip.txt; then echo "SHOULD NOT SHIP: $unwanted"; problems=$((problems + 1)); fi
done
rm /tmp/pagesco-zip.txt
echo "release check: $problems problems"

# publish_scan_solution.sh: is the shop's code safe to publish? (Session 18, Lesson 9.2, lab C)
# state: after:lesson_30
# expect: sk-ant-          0 file(s)
# expect: Never-publish files in the shop's folders: 0
#
# The reference for publish_scan_starter.sh. Lesson 9.2's step 4 searches the Git HISTORY; this scan looks at the
# files on disk, in the three places the repository tracks (the theme, the plugin without what tools generate,
# the site plugin), so it also catches a secret you are about to commit.
places="wp-content/themes/pagesco wp-content/plugins/pagesco-books wp-content/mu-plugins/pagesco-site.php"

# Every file of the shop's own code, leaving out what Composer, npm and the build make (not published either).
files=$(find $places -type f | grep -v -e '/vendor/' -e '/node_modules/' -e '/build/')
echo "Files scanned: $(printf '%s\n' "$files" | wc -l)"

echo "== Secrets =="
for secret in sandbox-7f3a9c maria-pass devon-pass jordan-pass sk-ant-; do
	printf '%-16s %s file(s)\n' "$secret" "$(printf '%s\n' "$files" | xargs grep -l -F -- "$secret" | wc -l)"
done

echo "== Never-publish files =="
echo "Never-publish files in the shop's folders: $(find $places -name '.env' -o -name '*.sql' -o -name 'wp-config.php' -o -name 'debug.log' | wc -l)"

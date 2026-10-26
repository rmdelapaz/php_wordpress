# publish_scan_starter.sh: is the shop's code safe to publish? (Session 18, Lesson 9.2, lab C)
# state: after:lesson_30
# expect: Files scanned: 109
# expect: sk-ant-          TODO
#
# Lesson 9.2's step 4 searches the Git HISTORY; this scan looks at the files on disk, in the three places the
# repository tracks (the theme, the plugin without what tools generate, the site plugin), so it also catches a
# secret you are about to commit. It runs in the WP-CLI container. From your project folder:
#     cp labs/module-18/l9_2-next-steps/publish_scan_starter.sh wordpress/
#     docker compose run --rm wpcli sh publish_scan_starter.sh
# Do TODOs 1 and 2, run again, compare with "Expected when done". When you are done: rm wordpress/publish_scan_starter.sh
places="wp-content/themes/pagesco wp-content/plugins/pagesco-books wp-content/mu-plugins/pagesco-site.php"

# Every file of the shop's own code, leaving out what Composer, npm and the build make (not published either).
files=$(find $places -type f | grep -v -e '/vendor/' -e '/node_modules/' -e '/build/')
echo "Files scanned: $(printf '%s\n' "$files" | wc -l)"

echo "== Secrets =="
for secret in sandbox-7f3a9c maria-pass devon-pass jordan-pass sk-ant-; do
	# TODO 1: how many of $files contain $secret? printf the list into xargs grep -l -F -- "$secret", count with
	# wc -l, and print it in the same shape: printf '%-16s %s file(s)\n' "$secret" "<the count>"
	printf '%-16s %s\n' "$secret" "TODO"
done

echo "== Never-publish files =="
# TODO 2: count the files in $places named .env, *.sql, wp-config.php or debug.log (find with -name ... -o -name
# ...) and print "Never-publish files in the shop's folders: <count>".
echo "Never-publish files in the shop's folders: TODO"

# Expected when done (publish_scan_solution.sh, the course site after Lesson 9.1):
# Files scanned: 109
# == Secrets ==
# sandbox-7f3a9c   0 file(s)
# maria-pass       0 file(s)
# devon-pass       0 file(s)
# jordan-pass      0 file(s)
# sk-ant-          0 file(s)
# == Never-publish files ==
# Never-publish files in the shop's folders: 0

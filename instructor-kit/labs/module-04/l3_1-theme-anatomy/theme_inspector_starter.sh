# theme_inspector_starter.sh: one line per installed theme, read from its files (Session 4, Lesson 3.1, lab B)
# state: after:lesson_06
# expect: twentytwentyfive
# expect: kind: TODO
#
# Lesson 3.1 took Twenty Twenty-Five apart. This script asks the same questions of EVERY theme in
# wp-content/themes/, so you can compare the three default themes at a glance. It runs in the WP-CLI container.
# From your project folder:
#     cp labs/module-04/l3_1-theme-anatomy/theme_inspector_starter.sh wordpress/
#     docker compose run --rm wpcli sh theme_inspector_starter.sh
# Replace each TODO with the command its comment describes, run again, compare with "Expected when done".
# When you are done: rm wordpress/theme_inspector_starter.sh

for t in $(wp theme list --field=name); do
	d="wp-content/themes/$t"
	echo "== $t $(wp theme get "$t" --field=version)"            # done for you: the folder name and the version

	# TODO 1: the "Requires at least:" line of the theme header in $d/style.css (grep -m 1 stops at the first match).
	echo "  TODO"

	# TODO 2: block or classic? A block theme has $d/templates/index.html. Use: if [ -f ... ]; then ...; else ...; fi
	echo "  kind: TODO"

	# TODO 3: how many files are in templates/, parts/ and patterns/ (ls "$d/templates" | wc -l, and so on).
	echo "  templates: TODO  parts: TODO  patterns: TODO"

	# TODO 4: does the theme have a functions.php? Print "functions.php: yes" or "functions.php: no".
	echo "  functions.php: TODO"
done

# Expected when done (theme_inspector_solution.sh, the course site after Lesson 2.3):
# == twentytwentyfive 1.5
#   Requires at least: 6.7
#   kind: block
#   templates: 8  parts: 7  patterns: 98
#   functions.php: yes
# == twentytwentyfour 1.6
#   Requires at least: 6.4
#   kind: block
#   templates: 11  parts: 4  patterns: 57
#   functions.php: yes
# == twentytwentythree 1.7
#   Requires at least: 6.1
#   kind: block
#   templates: 9  parts: 4  patterns: 7
#   functions.php: no

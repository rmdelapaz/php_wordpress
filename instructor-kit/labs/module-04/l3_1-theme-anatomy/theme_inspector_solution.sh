# theme_inspector_solution.sh: the instructor's reference for theme_inspector_starter.sh (Session 4, Lesson 3.1, lab B)
# state: after:lesson_06
# expect: == twentytwentythree 1.7
# expect: functions.php: no

for t in $(wp theme list --field=name); do
	d="wp-content/themes/$t"
	echo "== $t $(wp theme get "$t" --field=version)"
	echo "  $(grep -m 1 'Requires at least:' "$d/style.css")"
	if [ -f "$d/templates/index.html" ]; then
		echo "  kind: block"
	else
		echo "  kind: classic"
	fi
	echo "  templates: $(ls "$d/templates" | wc -l)  parts: $(ls "$d/parts" | wc -l)  patterns: $(ls "$d/patterns" | wc -l)"
	if [ -f "$d/functions.php" ]; then
		echo "  functions.php: yes"
	else
		echo "  functions.php: no"
	fi
done

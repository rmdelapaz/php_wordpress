# site_report_solution.sh: the instructor's reference for site_report_starter.sh (Session 1, Lesson 1.2, lab A)
# state: fresh
# expect: Title: Pages &amp; Co.
# expect: Active theme: twentytwentyfive

echo "== Pages & Co. site report =="
printf 'WordPress: '
wp core version

printf 'Title: '
wp option get blogname

printf 'Admin email: '
wp option get admin_email

printf 'Active theme: '
wp theme list --status=active --field=name

echo "Inactive plugins:"
wp plugin list --status=inactive --field=name

echo "Pages:"
wp post list --post_type=page --orderby=ID --order=asc --fields=ID,post_title,post_status

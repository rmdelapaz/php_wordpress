# site_report_starter.sh: a one-screen report of your development site, with WP-CLI (Session 1, Lesson 1.2, lab A)
# state: fresh
# expect: Title: TODO
#
# Every line of the report is one wp command (Lesson 1.2, "WP-CLI and the wp Shortcut"). The script runs in the
# WP-CLI container, where wp needs no shortcut. From your project folder:
#     cp labs/module-01/l1_2-local-environment/site_report_starter.sh wordpress/
#     docker compose run --rm wpcli sh site_report_starter.sh
# Replace each echo "...TODO" line with the wp command its comment describes (try the command alone first:
# wp help option, wp help theme list ...), run the script again, compare with "Expected when done".
# When you are done: rm wordpress/site_report_starter.sh

echo "== Pages & Co. site report =="
printf 'WordPress: '
wp core version                      # done for you

# TODO 1: the site title, which WordPress stores in the option blogname (printf first, as above).
echo "Title: TODO"

# TODO 2: the administrator email address, stored in the option admin_email.
echo "Admin email: TODO"

# TODO 3: ONLY the name of the active theme: wp theme list with --status=... and --field=...
echo "Active theme: TODO"

# TODO 4: the installed plugins that are NOT active, one name per line (wp plugin list, the same two options).
echo "Inactive plugins: TODO"

# TODO 5: the site's pages, oldest ID first, as a table with three columns:
#         wp post list --post_type=page --orderby=ID --order=asc --fields=...
#         (the columns are called ID, post_title and post_status)
echo "Pages: TODO"

# Expected when done (site_report_solution.sh, a fresh course site):
# == Pages & Co. site report ==
# WordPress: 7.1.3
# Title: Pages &amp; Co.
# Admin email: wordpress@example.com
# Active theme: twentytwentyfive
# Inactive plugins:
# akismet
# hello
# Pages:
# +----+----------------+-------------+
# | ID | post_title     | post_status |
# +----+----------------+-------------+
# | 2  | Sample Page    | publish     |
# | 3  | Privacy Policy | draft       |
# +----+----------------+-------------+

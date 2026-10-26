#!/bin/sh
# Pages & Co. Part 2 starting site (PHP and WordPress Development): the site as Lesson 4.3 leaves it.
# Run it INSIDE the course's WP-CLI container, from your project folder (pagesco-dev, Lesson 1.2):
#     docker compose run --rm wpcli sh pagesco-part2-start/install.sh
# It saves your current database first, copies the three course themes and the two must-use plugins into
# wp-content, imports the Part 2 database (it REPLACES your posts, pages, users and settings) and keeps your
# site address.
set -e
SRC=pagesco-part2-start
if [ ! -f wp-load.php ] || [ ! -f "$SRC/database.sql" ]; then
	echo "Error: copy the pagesco-part2-start folder into wordpress/ and run, from your project folder:"
	echo "    docker compose run --rm wpcli sh pagesco-part2-start/install.sh"
	exit 1
fi
if ! wp core is-installed 2>/dev/null; then
	echo "Error: WordPress is not installed yet: install it as Lesson 1.2 shows, then run this again."
	exit 1
fi
URL=$(wp option get siteurl)
wp db export "$SRC/backup-before-part2.sql" --quiet
echo "Saved your current database as wordpress/$SRC/backup-before-part2.sql"
for t in pagesco pagesco-classic pagesco-tt5-child; do
	rm -rf "wp-content/themes/$t"
	cp -R "$SRC/themes/$t" wp-content/themes/
done
mkdir -p wp-content/mu-plugins
cp "$SRC/mu-plugins/mailpit-smtp.php" "$SRC/mu-plugins/pagesco-site.php" wp-content/mu-plugins/
echo "Copied themes pagesco, pagesco-classic, pagesco-tt5-child and mu-plugins mailpit-smtp.php, pagesco-site.php"
wp db import "$SRC/database.sql"
if [ "$URL" != "http://localhost:8080" ]; then
	wp search-replace "http://localhost:8080" "$URL" --all-tables --quiet
	echo "Changed the site address to $URL"
fi
wp rewrite flush
echo "Active theme: $(wp theme list --status=active --field=name)"
echo "Done: log in at $URL/wp-admin/ as admin / password, then run the Part 2 check (Session 9)."

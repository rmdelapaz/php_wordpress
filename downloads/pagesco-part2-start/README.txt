Pages & Co. Part 2 starting site (PHP and WordPress Development, Part 2 "Plugins to Launch")

The site exactly as Lesson 4.3 leaves it: the end of Part 1. Use it when you start the course at
Part 2 (Session 9, Lesson 5.1), or when your own Part 1 site is broken and you want a clean start.

What is inside
  themes/pagesco              the Pages & Co. block theme (Lessons 3.2 to 4.3), ACTIVE after the import
  themes/pagesco-classic      the classic theme of Module 4 (installed, inactive)
  themes/pagesco-tt5-child    the Twenty Twenty-Five child theme of Lesson 3.4 (installed, inactive)
  mu-plugins/pagesco-site.php the store notice of Lesson 2.3
  mu-plugins/mailpit-smtp.php the Mailpit mail fix of Lesson 1.2
  database.sql                users (admin, maria, devon), pages About Us, Contact, Events, the News posts,
                              the classic menu and footer widget, the theme settings; next new post ID = 30
  install.sh                  the installer (runs inside the WP-CLI container)

What you need first
  The Lesson 1.2 project (pagesco-dev) started with "docker compose up -d" and WordPress installed
  (Lesson 1.2's "wp core install" and permalinks). Linux and Windows (WSL 2): the Lesson 1.2 user setup
  (.env + compose.override.yaml) must be in place, so the files are yours and WordPress can read them.
  Without it, copying into wordpress/ fails with "Permission denied": do the Lesson 1.2 setup first.

Install (about one minute)
  1. Download and unzip it (or use the copy your instructor gives you):
         curl -LO https://rays-php-wordpress.netlify.app/downloads/pagesco-part2-start.zip
         unzip pagesco-part2-start.zip
  2. Copy the pagesco-part2-start folder into your project's wordpress/ folder:
         cp -R pagesco-part2-start ~/pagesco-dev/wordpress/
  3. From the project folder, run the installer in the WP-CLI container:
         cd ~/pagesco-dev
         docker compose run --rm wpcli sh pagesco-part2-start/install.sh
     It saves your current database as wordpress/pagesco-part2-start/backup-before-part2.sql, copies the
     themes and must-use plugins into wp-content (replacing those three theme folders), imports
     database.sql and keeps your site address (it runs wp search-replace when yours is not
     http://localhost:8080).
  4. Log in at http://localhost:8080/wp-admin/ as admin / password (maria / maria-pass and
     devon / devon-pass are the course's editor and author).
  5. Check it: bash labs/module-01/l1_0-orientation/check_environment.sh --part2
     The line "OK the site as Lesson 4.3 left it" must be there; the verdict is READY or READY WITH NOTES.

Undo
  docker compose run --rm wpcli wp db import pagesco-part2-start/backup-before-part2.sql
  (the three theme folders stay; delete them in Appearance > Themes if you do not want them)

When you are done you may delete wordpress/pagesco-part2-start/ (keep the backup somewhere else if you
want it). The database contains only the course's fictional data and the development passwords above:
never import it on a public site.

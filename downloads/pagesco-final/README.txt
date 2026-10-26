Pages & Co. final project: the reference solution (PHP and WordPress Development, Lesson 9.1)

Reserve & Pick Up, as committed at the tag release-3: Pages & Co. Books 1.2.0,
the pagesco theme 1.2.0 and the site plugin, exactly the files the lesson's
reference solution writes and runs (WordPress 7.1.3, PHP 8.5).

  wp-content/                 the shop's code at release-3, the same files Git tracks
    .gitignore                (Lesson 8.4)
    mu-plugins/pagesco-site.php
    themes/pagesco/           theme 1.2.0
    plugins/pagesco-books/    plugin 1.2.0: sources, tests, languages, lock files
  holds-smoke.sh              the smoke test of Milestone 5 (sh, curl, grep)

What is NOT here, on purpose (Lesson 8.4): vendor/, node_modules/ and build/.
A release build makes them: composer install --no-dev --optimize-autoloader,
npm ci, npm run build, npm run plugin-zip.

Compare it with your own work. Unzip it in your home folder (next to
pagesco-dev), take your own release-3 the same way, and let diff show the
differences:

    mkdir -p /tmp/mine
    git -C pagesco-dev/wordpress/wp-content archive release-3 | tar -x -C /tmp/mine
    diff -ru /tmp/mine pagesco-final/wp-content | less

Different names and a different design can be just as good: what matters is
the brief, the security and privacy checklist, and the checks of each milestone.

Do not copy these files over a site you care about without reading them: the
plugin's activation creates tables, and its uninstall.php deletes data.

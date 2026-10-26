Pages & Co. catalog seeder (PHP and WordPress Development, Lesson 5.2)

Place this pagesco-seed/ folder at the root of your WordPress install
(next to wp-load.php), then from your project folder run:

    wp eval-file pagesco-seed/seed-books.php

It creates the five genres and the eleven books of the Pages & Co. catalog.
Activate the pagesco-books plugin first (the book post type and genre
taxonomy must exist). Safe to run more than once: it skips anything that
already exists.

Files:
  seed-books.php  the WP-CLI seeding script (read it before you run it)
  books.json      the eleven books: title, author, price, pages, date, stock, genres

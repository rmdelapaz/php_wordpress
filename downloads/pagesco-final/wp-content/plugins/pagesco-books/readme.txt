=== Pages & Co. Books ===
Contributors: pagesco
Tags: books, bookstore, catalog, events, blocks
Requires at least: 6.9
Tested up to: 7.1
Requires PHP: 8.2
Stable tag: 1.2.0
License: GPL-2.0-or-later
License URI: https://www.gnu.org/licenses/gpl-2.0.html

The catalog, events, holds and blocks of the Pages & Co. bookstore: books with prices and stock, genres, a book filter, Reserve & Pick Up and a REST API.

== Description ==

Pages & Co. Books runs the bookstore features of the Pages & Co. website:

* A Book post type with author, price, pages, publication date, stock and ISBN, and a Genre taxonomy.
* Blocks: Book Card, Book List (always up to date), Book Filter (filters the catalog instantly, and works without JavaScript), Reserve for Pickup and My Holds.
* Reserve & Pick Up: logged-in customers put a book aside to collect in the shop, get a confirmation email, and see or cancel their holds; staff see what is waiting under Books > Holds.
* Events in their own table, shown with the `[pagesco_events]` shortcode and in the REST API.
* A REST API under `pagesco/v1`, and the `pagesco/check-stock` ability for assistants and automation tools.
* A Stock at a glance widget on the Dashboard, and a Supplier column on the Books screen.

The plugin is translation-ready and ships with a partial Spanish translation.

= External services =

To show how many copies the book distributor has, the plugin connects to the distributor's API (Riverside Books). It sends the ISBNs of the shop's published books, and the API key you configure, once a day and when the Books screen needs fresh numbers. Nothing about visitors or customers is sent: holds stay on your site. The service is only used when `PAGESCO_BOOKS_SUPPLIER_URL` and `PAGESCO_BOOKS_SUPPLIER_KEY` are defined in `wp-config.php`.
Terms of service: https://riverside.example/terms
Privacy policy: https://riverside.example/privacy

== Installation ==

1. Upload the `pagesco-books` folder to `/wp-content/plugins/`, or install the ZIP file under Plugins > Add Plugin > Upload Plugin.
2. Activate the plugin on the Plugins screen.
3. To show the distributor's stock, add `PAGESCO_BOOKS_SUPPLIER_URL` and `PAGESCO_BOOKS_SUPPLIER_KEY` to `wp-config.php`.
4. Adjust the store notice and list sizes under Settings > Pages & Co. Books.

== Frequently Asked Questions ==

= What happens to my books when I delete the plugin? =

They stay. Deleting the plugin removes its settings, its events and holds tables and the Bookseller role, and keeps your books, genres and book details. To remove those too, turn on "Delete all books, genres and book details when the plugin is deleted" under Settings > Pages & Co. Books before you delete the plugin.

= Which blocks does the plugin add? =

Book Card, Book List, Book Filter, Reserve for Pickup (for the single book template) and My Holds (for a page), in the Widgets category of the block inserter.

== Changelog ==

= 1.2.0 =
* New: Reserve & Pick Up. Customers reserve books for pickup, with a limit and a pickup date from the settings, a confirmation email, a My Holds block and the REST routes /pagesco/v1/holds; staff mark holds as collected under Books > Holds.
* New: the pagesco/book binding source accepts a book's slug, so patterns can show live prices.
* Changed: holds are deleted 30 days after their pickup date by the daily job.

= 1.1.1 =
* Security: the supplier's API key is sent only over HTTPS, except on a local development site.
* Changed: an Update URI header, so that WordPress.org never offers an update for this private plugin.

= 1.1.0 =
* New: an option to delete all books, genres and book details when the plugin is deleted (off by default).
* New: Spanish translation, including the blocks and the Stock at a glance widget.
* Improved: fewer database queries (cached events, autoloaded settings, one query for the supplier's ISBN list).
* Fixed: the keyboard focus on the selected genre in the Book Filter is visible again.
* Changed: requires WordPress 6.9 or later (the Abilities API).

= 1.0.0 =
* First release.

== Upgrade Notice ==

= 1.2.0 =
Adds Reserve & Pick Up. The holds table is created by itself after the update; add a page with the My Holds block at /my-holds/.

= 1.1.0 =
Requires WordPress 6.9. Adds a Spanish translation and an opt-in to delete all shop data on uninstall.

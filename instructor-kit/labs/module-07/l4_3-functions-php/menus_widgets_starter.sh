# menus_widgets_starter.sh: fill pagesco-classic's menu and widget area from WP-CLI, then clean up (Session 7, Lesson 4.3, lab B)
# state: after:lesson_13
# expect: Second menu: TODO
#
# At the end of Lesson 4.3 pagesco-classic has a "primary" location with the Main menu and a "footer" widget area
# with one block widget. This script switches to it for a moment, adds a second menu and a second widget with
# WP-CLI (the lesson's commands, plus two new ones), shows them, removes them again and switches back to pagesco.
# From your project folder:
#     cp labs/module-07/l4_3-functions-php/menus_widgets_starter.sh wordpress/
#     docker compose run --rm wpcli sh menus_widgets_starter.sh
# Replace each echo "...TODO" with the commands its comment names (wp help menu item, wp help widget add), run
# again, compare with "Expected when done". When you are done: rm wordpress/menus_widgets_starter.sh

wp theme activate pagesco-classic

echo "== locations =="
wp menu location list                 # done for you

# TODO 1: create a menu called "Shop links" (its slug becomes shop-links), add the Events page (ID 14) with
#         wp menu item add-post, add a custom link "Gift cards" to http://localhost:8080/contact/ with
#         wp menu item add-custom, then list its items with the fields title and link.
echo "Second menu: TODO"

# TODO 2: add a block widget to the footer area at position 1 with the content
#         '<!-- wp:search {"label":"Search the shop","buttonText":"Search"} /-->', then list the footer's widgets
#         (fields name, id, position).
echo "Second widget: TODO"

# TODO 3: clean up. Delete the widget you added (the first id of wp widget list footer --fields=id --format=csv)
#         and the menu shop-links. Then the line below prints only the lesson's widget.
echo "footer widgets after cleanup: $(wp widget list footer --fields=id --format=csv | tail -n +2 | tr '\n' ' ' | sed 's/ $//')"
wp theme activate pagesco

# Expected when done (menus_widgets_solution.sh, the site at the end of Lesson 4.3; menu and widget IDs may differ):
# Success: Switched to 'Pages &amp; Co. Classic' theme.
# == locations ==
# +----------+--------------+
# | location | description  |
# +----------+--------------+
# | primary  | Primary menu |
# +----------+--------------+
# == a second menu ==
# Success: Created menu 5.
# Success: Menu item added.
# Success: Menu item added.
# +------------+--------------------------------+
# | title      | link                           |
# +------------+--------------------------------+
# | Events     | http://localhost:8080/events/  |
# | Gift cards | http://localhost:8080/contact/ |
# +------------+--------------------------------+
# == one more widget ==
# Success: Added widget to sidebar.
# +-------+---------+----------+
# | name  | id      | position |
# +-------+---------+----------+
# | block | block-8 | 1        |
# | block | block-7 | 2        |
# +-------+---------+----------+
# == cleanup ==
# Success: Deleted 1 of 1 widgets.
# Deleted menu 'shop-links'.
# Success: Deleted 1 of 1 menus.
# footer widgets after cleanup: block-7
# Success: Switched to 'Pages &amp; Co.' theme.

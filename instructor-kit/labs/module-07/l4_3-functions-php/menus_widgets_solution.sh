# menus_widgets_solution.sh: fill pagesco-classic's menu and widget area from WP-CLI, then clean up (Session 7, Lesson 4.3, lab B)
# state: after:lesson_13
# expect: Gift cards
# expect: footer widgets after cleanup: block-7
#
# The reference solution. See menus_widgets_starter.sh for the task.

wp theme activate pagesco-classic

echo "== locations =="
wp menu location list

echo "== a second menu =="
wp menu create "Shop links"
wp menu item add-post shop-links 14
wp menu item add-custom shop-links "Gift cards" http://localhost:8080/contact/
wp menu item list shop-links --fields=title,link

echo "== one more widget =="
wp widget add block footer 1 --content='<!-- wp:search {"label":"Search the shop","buttonText":"Search"} /-->'
wp widget list footer --fields=name,id,position

echo "== cleanup =="
wp widget delete $(wp widget list footer --fields=id --format=csv | tail -n +2 | head -n 1)
wp menu delete shop-links
echo "footer widgets after cleanup: $(wp widget list footer --fields=id --format=csv | tail -n +2 | tr '\n' ' ' | sed 's/ $//')"
wp theme activate pagesco

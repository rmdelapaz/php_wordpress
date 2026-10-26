# test_checkpoint.sh: Checkpoint 1's test: the notice bar and the footer line of the home page (Session 4)
# serve: checkpoint
# install: mu-plugin
# state: after:lesson_06
# expect-starter: See events</a> · TODO</div>
# expect-starter: Published pages: TODO
# expect-solution: Latest news: Book club: Dune.
# expect-solution: Ask Maria Lopez</a></div>
# expect-solution: Published pages: 4
#
# With pagesco-checkpoint.php in wordpress/wp-content/mu-plugins/, from your project folder:
#     cp labs/module-04/checkpoint-1/test_checkpoint.sh wordpress/
#     docker compose run --rm wpcli sh test_checkpoint.sh
# Any PHP message also shows in the page and in wordpress/wp-content/debug.log: read it from the left.
# When you are done: rm wordpress/test_checkpoint.sh wordpress/wp-content/mu-plugins/pagesco-checkpoint.php

page=$(curl -s http://localhost:8080/)
echo "notice bar:"
echo "$page" | grep -o '<div class="pagesco-notice">.*</div>' | head -n 1 || echo "(no notice bar: is pagesco-site.php still in mu-plugins/?)"
echo "footer line:"
echo "$page" | grep -o '<p class="pagesco-pages">[^<]*</p>' || echo "(none)"

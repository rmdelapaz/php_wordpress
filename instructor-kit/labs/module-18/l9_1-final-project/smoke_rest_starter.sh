# smoke_rest_starter.sh: a smoke test from outside, for pages and the REST API (Session 18, Lesson 9.1, lab C)
# state: after:lesson_29
# expect: TODO    the REST API lists 11 books
#
# Like holds-smoke.sh (Milestone 5) it asks through the same doors a browser uses, prints one line per check and
# exits with 1 when any check failed, so a deploy script can stop. It runs in the WP-CLI container (sh, curl,
# grep), against your development site or, with an address, any copy. From your project folder:
#     cp labs/module-18/l9_1-final-project/smoke_rest_starter.sh wordpress/
#     docker compose run --rm wpcli sh smoke_rest_starter.sh
# Check 1 is done for you. Replace each echo "TODO ..." with a check in the same shape, run again, and compare
# with "Expected when done". When you are done: rm wordpress/smoke_rest_starter.sh
base="${1:-http://localhost:8080}"
failed=0

check() {   # check LABEL RESULT (0 = ok)
	if [ "$2" = 0 ]; then echo "ok      $1"; else echo "FAILED  $1"; failed=1; fi
}

status=$(curl -s -o /dev/null -w '%{http_code}' "$base/books/dune/")
[ "$status" = 200 ]
check "Dune's page answers (status $status)" $?

# TODO 1: the REST API's X-WP-Total header for /wp-json/pagesco/v1/books is 11 (curl -s -I, then tr -d '\r',
#         grep -i '^x-wp-total:' and cut -d' ' -f2). Label: "the REST API lists $total books".
echo "TODO    the REST API lists 11 books"
# TODO 2: ?genre=no-such-genre is refused with status 400. Label: "an unknown genre is refused (status $status)".
echo "TODO    an unknown genre is refused"
# TODO 3: /books/no-such-book/ answers 404. Label: "a book that does not exist is a 404 (status $status)".
echo "TODO    a book that does not exist is a 404"
# TODO 4: a visitor asking for /wp-admin/options-general.php?page=pagesco-books is redirected to wp-login.php
#         (curl -w '%{redirect_url}', then case ... in *wp-login.php*). Label: "the settings screen sends
#         visitors to the login".
echo "TODO    the settings screen sends visitors to the login"

exit $failed

# Expected when done (smoke_rest_solution.sh, the course site after Lesson 8.4):
# ok      Dune's page answers (status 200)
# ok      the REST API lists 11 books
# ok      an unknown genre is refused (status 400)
# ok      a book that does not exist is a 404 (status 404)
# ok      the settings screen sends visitors to the login

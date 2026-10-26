# smoke_rest_solution.sh: a smoke test from outside, for pages and the REST API (Session 18, Lesson 9.1, lab C)
# state: after:lesson_29
# expect: ok      the REST API lists 11 books
# expect: ok      an unknown genre is refused (status 400)
#
# The reference for smoke_rest_starter.sh. Like holds-smoke.sh (Milestone 5) it asks through the same doors a
# browser uses, prints one line per check and exits with 1 when any check failed, so a deploy script can stop.
base="${1:-http://localhost:8080}"
failed=0

check() {   # check LABEL RESULT (0 = ok)
	if [ "$2" = 0 ]; then echo "ok      $1"; else echo "FAILED  $1"; failed=1; fi
}

status=$(curl -s -o /dev/null -w '%{http_code}' "$base/books/dune/")
[ "$status" = 200 ]
check "Dune's page answers (status $status)" $?

total=$(curl -s -I "$base/wp-json/pagesco/v1/books" | tr -d '\r' | grep -i '^x-wp-total:' | cut -d' ' -f2)
[ "$total" = 11 ]
check "the REST API lists $total books" $?

status=$(curl -s -o /dev/null -w '%{http_code}' "$base/wp-json/pagesco/v1/books?genre=no-such-genre")
[ "$status" = 400 ]
check "an unknown genre is refused (status $status)" $?

status=$(curl -s -o /dev/null -w '%{http_code}' "$base/books/no-such-book/")
[ "$status" = 404 ]
check "a book that does not exist is a 404 (status $status)" $?

location=$(curl -s -o /dev/null -w '%{redirect_url}' "$base/wp-admin/options-general.php?page=pagesco-books")
case "$location" in *wp-login.php*) true ;; *) false ;; esac
check "the settings screen sends visitors to the login" $?

exit $failed

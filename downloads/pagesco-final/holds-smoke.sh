#!/bin/sh
# A smoke test of Reserve & Pick Up, from the outside, like a customer and an attacker.
# Usage: sh holds-smoke.sh BASE-URL LOGIN PASSWORD BOOK-SLUG
# The customer reserves the book, sees it on My holds and cancels it again: it leaves one cancelled hold.
base="${1:?usage: holds-smoke.sh BASE-URL LOGIN PASSWORD BOOK-SLUG}"
login="$2"; password="$3"; book="$4"
jar=$(mktemp)
failed=0

check() {   # check LABEL CONDITION-RESULT(0 = ok)
	if [ "$2" = 0 ]; then echo "ok      $1"; else echo "FAILED  $1"; failed=1; fi
}

# 1. Visitors: a login link on the book's page, and the REST API turns them away.
curl -s "$base/books/$book/" | grep -q 'Log in to reserve this book'
check "visitor sees the login link" $?
status=$(curl -s -o /dev/null -w '%{http_code}' -H 'Content-Type: application/json' -d '{"book":1}' "$base/wp-json/pagesco/v1/holds")
[ "$status" = 401 ]
check "REST refuses a visitor (status $status)" $?

# 2. Log in, the way a browser does.
curl -s -o /dev/null -c "$jar" -b "$jar" "$base/wp-login.php"
curl -s -o /dev/null -c "$jar" -b "$jar" --data-urlencode "log=$login" --data-urlencode "pwd=$password" -d testcookie=1 "$base/wp-login.php"
grep -q wordpress_logged_in "$jar"
check "$login can log in" $?

# 3. The form without its nonce is refused; with the page's nonce, the book is reserved.
page=$(curl -s -b "$jar" "$base/books/$book/")
book_id=$(printf '%s' "$page" | grep -o 'name="book" value="[0-9]*"' | grep -o '[0-9]*')
nonce=$(printf '%s' "$page" | grep -o 'name="_wpnonce" value="[^"]*"' | head -n 1 | cut -d'"' -f4)
status=$(curl -s -o /dev/null -w '%{http_code}' -b "$jar" -d action=pagesco_books_place_hold -d "book=$book_id" "$base/wp-admin/admin-post.php")
[ "$status" = 403 ]
check "a form without a nonce is refused (status $status)" $?
location=$(curl -s -o /dev/null -w '%{redirect_url}' -b "$jar" -d action=pagesco_books_place_hold -d "book=$book_id" -d "_wpnonce=$nonce" "$base/wp-admin/admin-post.php")
case "$location" in *pagesco_hold=placed) true ;; *) false ;; esac
check "the form reserves the book" $?

# 4. My holds lists it, waiting; the customer cancels it.
holds=$(curl -s -b "$jar" "$base/my-holds/")
printf '%s' "$holds" | grep -q 'is-waiting'
check "My holds shows the waiting hold" $?
hold_id=$(printf '%s' "$holds" | grep -o 'name="hold" value="[0-9]*"' | head -n 1 | grep -o '[0-9]*')
nonce=$(printf '%s' "$holds" | grep -A 1 "name=\"hold\" value=\"$hold_id\"" | grep -o 'name="_wpnonce" value="[^"]*"' | head -n 1 | cut -d'"' -f4)
location=$(curl -s -o /dev/null -w '%{redirect_url}' -b "$jar" -d action=pagesco_books_cancel_hold -d "hold=$hold_id" -d "_wpnonce=$nonce" "$base/wp-admin/admin-post.php")
case "$location" in *pagesco_hold=cancelled) true ;; *) false ;; esac
check "the customer cancels the hold" $?

# 5. A customer is not staff: the collect action refuses even a valid-looking request.
status=$(curl -s -o /dev/null -w '%{http_code}' -b "$jar" -d action=pagesco_books_collect_hold -d "hold=$hold_id" -d "_wpnonce=$nonce" "$base/wp-admin/admin-post.php")
[ "$status" = 403 ]
check "a customer cannot mark holds collected (status $status)" $?

rm -f "$jar"
exit $failed

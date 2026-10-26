# cors_headers_starter.sh: what a front end on another origin may read (Session 18, Lesson 9.2, lab A)
# state: after:lesson_30
# expect: Allow-Credentials: TODO
#
# A browser on http://localhost:3000 sends an Origin header with every request to the shop's API; it lets the
# page read the answer only if the server's CORS headers say so (Lesson 9.2, "Your API, from another origin").
# This script asks the way that browser would, from the WP-CLI container. From your project folder:
#     cp labs/module-18/l9_2-next-steps/cors_headers_starter.sh wordpress/
#     docker compose run --rm wpcli sh cors_headers_starter.sh
# Line 1 is done for you; each TODO is the same grep and cut on another header. Compare with "Expected when done".
# When you are done: rm wordpress/cors_headers_starter.sh
origin="http://localhost:3000"
api="http://localhost:8080/wp-json/pagesco/v1"

# One request's headers, without the carriage returns HTTP puts at the end of each line.
headers=$(curl -s -I -H "Origin: $origin" "$api/books" | tr -d '\r')

echo "== GET /pagesco/v1/books, from $origin =="
echo "Allow-Origin: $(printf '%s\n' "$headers" | grep -i '^access-control-allow-origin:' | cut -d' ' -f2)"
# TODO 1: Access-Control-Allow-Credentials (does the browser send cookies along?).
echo "Allow-Credentials: TODO"
# TODO 2: Access-Control-Expose-Headers, the whole value (cut -d' ' -f2- keeps everything after the name).
echo "Expose-Headers: TODO"
# TODO 3: "Books: <X-WP-Total> on <X-WP-TotalPages> pages".
echo "Books: TODO"

# TODO 4: the same Origin on "$api/holds" as a visitor (curl -s -i: the status line and the headers). Print
# "holds as a visitor: <status>, Allow-Origin: <value>": the first line's second field is the status.
echo "holds as a visitor: TODO"

# Expected when done (cors_headers_solution.sh, the course site after Lesson 9.1):
# == GET /pagesco/v1/books, from http://localhost:3000 ==
# Allow-Origin: http://localhost:3000
# Allow-Credentials: true
# Expose-Headers: X-WP-Total, X-WP-TotalPages, Link
# Books: 11 on 2 pages
# holds as a visitor: 401, Allow-Origin: http://localhost:3000

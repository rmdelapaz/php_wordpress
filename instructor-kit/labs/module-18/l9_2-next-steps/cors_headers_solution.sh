# cors_headers_solution.sh: what a front end on another origin may read (Session 18, Lesson 9.2, lab A)
# state: after:lesson_30
# expect: Allow-Origin: http://localhost:3000
# expect: holds as a visitor: 401, Allow-Origin: http://localhost:3000
#
# The reference for cors_headers_starter.sh. A browser on http://localhost:3000 sends an Origin header with every
# request to the shop's API; it lets the page read the answer only if the server's CORS headers say so.
origin="http://localhost:3000"
api="http://localhost:8080/wp-json/pagesco/v1"

# One request's headers, without the carriage returns HTTP puts at the end of each line.
headers=$(curl -s -I -H "Origin: $origin" "$api/books" | tr -d '\r')

echo "== GET /pagesco/v1/books, from $origin =="
echo "Allow-Origin: $(printf '%s\n' "$headers" | grep -i '^access-control-allow-origin:' | cut -d' ' -f2)"
echo "Allow-Credentials: $(printf '%s\n' "$headers" | grep -i '^access-control-allow-credentials:' | cut -d' ' -f2)"
echo "Expose-Headers: $(printf '%s\n' "$headers" | grep -i '^access-control-expose-headers:' | cut -d' ' -f2-)"
echo "Books: $(printf '%s\n' "$headers" | grep -i '^x-wp-total:' | cut -d' ' -f2) on $(printf '%s\n' "$headers" | grep -i '^x-wp-totalpages:' | cut -d' ' -f2) pages"

# A route with a permission callback: CORS lets the page READ the refusal, it does not let it in.
holds=$(curl -s -i -H "Origin: $origin" "$api/holds" | tr -d '\r')
echo "holds as a visitor: $(printf '%s\n' "$holds" | head -n 1 | cut -d' ' -f2), Allow-Origin: $(printf '%s\n' "$holds" | grep -i '^access-control-allow-origin:' | cut -d' ' -f2)"

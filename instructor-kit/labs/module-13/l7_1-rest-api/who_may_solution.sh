# who_may_solution.sh: the instructor's reference for who_may_starter.sh (Session 13, Lesson 7.1, lab B)
# state: after:lesson_22
# expect: books/30?context=edit   401  403    200    200
# expect: settings                401  403    403    200

API=http://localhost:8080/wp-json/wp/v2

DEVON=$(wp user application-password create devon "Who may lab" --porcelain)
MARIA=$(wp user application-password create maria "Who may lab" --porcelain)
ADMIN=$(wp user application-password create admin "Who may lab" --porcelain)

printf '%-23s %-4s %-6s %-6s %s\n' "request" "anon" "devon" "maria" "admin"
for path in "users/me" "books/30?context=edit" "books?status=draft" "users?context=edit" "settings"; do
	anon=$(curl -s -o /dev/null -w '%{http_code}' "$API/$path")
	devon=$(curl -s -o /dev/null -w '%{http_code}' --user "devon:$DEVON" "$API/$path")
	maria=$(curl -s -o /dev/null -w '%{http_code}' --user "maria:$MARIA" "$API/$path")
	admin=$(curl -s -o /dev/null -w '%{http_code}' --user "admin:$ADMIN" "$API/$path")
	printf '%-23s %-4s %-6s %-6s %s\n' "$path" "$anon" "$devon" "$maria" "$admin"
done

# Revoke the three passwords: a lab leaves no credentials behind.
for user in devon maria admin; do
	wp user application-password delete "$user" "$(wp user application-password list "$user" --name='Who may lab' --field=uuid)" > /dev/null
done
echo "Lab passwords revoked."

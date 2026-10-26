# who_may_starter.sh: who may ask what? Five requests, four callers, one status code each (Session 13, Lesson 7.1, lab B)
# state: after:lesson_22
# expect: users/me                401  TODO   TODO   TODO
# expect: Lab passwords revoked.
#
# Lesson 7.1's error table, measured: 401 = "who are you?", 403 = "I know you, and no", 200 = yes. The script
# gives Devon (author), Maria (editor) and admin a throwaway application password each, sends the same five GET
# requests as each of them and anonymously, and revokes the passwords at the end. From your project folder:
#     cp labs/module-13/l7_1-rest-api/who_may_starter.sh wordpress/
#     docker compose run --rm wpcli sh who_may_starter.sh
# PREDICT the whole table on paper first. Then fill in the TODOs and compare with "Expected when done".
# When you are done: rm wordpress/who_may_starter.sh

API=http://localhost:8080/wp-json/wp/v2

DEVON=$(wp user application-password create devon "Who may lab" --porcelain)
MARIA=$(wp user application-password create maria "Who may lab" --porcelain)
ADMIN=$(wp user application-password create admin "Who may lab" --porcelain)

printf '%-23s %-4s %-6s %-6s %s\n' "request" "anon" "devon" "maria" "admin"
for path in "users/me" "books/30?context=edit" "books?status=draft" "users?context=edit" "settings"; do
	anon=$(curl -s -o /dev/null -w '%{http_code}' "$API/$path")     # done for you: the status code only
	# TODO 1 to 3: the same request with --user "devon:$DEVON", then as maria and as admin (their variables above).
	devon=TODO
	maria=TODO
	admin=TODO
	printf '%-23s %-4s %-6s %-6s %s\n' "$path" "$anon" "$devon" "$maria" "$admin"
done

# Revoke the three passwords: a lab leaves no credentials behind (keep this part as it is).
for user in devon maria admin; do
	wp user application-password delete "$user" "$(wp user application-password list "$user" --name='Who may lab' --field=uuid)" > /dev/null
done
echo "Lab passwords revoked."

# Expected when done (who_may_solution.sh, the site after Lesson 6.4):
# request                 anon devon  maria  admin
# users/me                401  200    200    200
# books/30?context=edit   401  403    200    200
# books?status=draft      400  200    200    200
# users?context=edit      401  403    403    200
# settings                401  403    403    200
# Lab passwords revoked.

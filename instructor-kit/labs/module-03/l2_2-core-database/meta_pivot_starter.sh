# meta_pivot_starter.sh: turn key-value rows back into columns, in SQL and with WP-CLI (Session 3, Lesson 2.2, lab A)
# state: after:lesson_04
# expect: Step 2: TODO
#
# wp_usermeta stores every extra field of a user as one row: user_id, meta_key, meta_value (Lesson 2.2, the
# key-value pattern). Reports want one row per user with a column per field. This lab builds that "pivot" in SQL,
# then lets WordPress do it. The script runs in the WP-CLI container; from your project folder:
#     cp labs/module-03/l2_2-core-database/meta_pivot_starter.sh wordpress/
#     docker compose run --rm wpcli sh meta_pivot_starter.sh
# Replace each echo "Step N: TODO" line with the command its comment describes (try each query at the
# wp db cli prompt first), run the script again, compare with "Expected when done" at the end.
# When you are done: rm wordpress/meta_pivot_starter.sh

echo "== Step 1: the users =="
wp db query "SELECT ID, user_login, display_name FROM wp_users ORDER BY ID"      # done for you

echo "== Step 2: first names, one join =="
# TODO 2: every user's ID, user_login and first name: JOIN wp_usermeta AS um ON um.user_id = u.ID
#         AND um.meta_key = 'first_name' (the key condition goes in the ON clause), name the column first_name.
echo "Step 2: TODO"

echo "== Step 3: one row per user, two fields =="
# TODO 3: first_name AND last_name as two columns, one row per user: join wp_usermeta once (no key condition),
#         GROUP BY u.ID, u.user_login, and pick each field with MAX(CASE WHEN um.meta_key = '...' THEN um.meta_value END).
echo "Step 3: TODO"

echo "== Step 4: the same through WordPress =="
# TODO 4: wp user list, oldest ID first, with the fields ID, user_login, first_name and last_name
#         (WP-CLI reads the meta fields for you).
echo "Step 4: TODO"

echo "== Step 5: meta rows per user =="
# TODO 5: how many rows each user has in wp_usermeta: GROUP BY user_id, the count named meta_rows.
echo "Step 5: TODO"

# Expected when done (meta_pivot_solution.sh, the site after Lesson 2.1):
# == Step 1: the users ==
# ID	user_login	display_name
# 1	admin	admin
# 2	maria	Maria Lopez
# 3	devon	Devon Park
# == Step 2: first names, one join ==
# ID	user_login	first_name
# 1	admin
# 2	maria	Maria
# 3	devon	Devon
# == Step 3: one row per user, two fields ==
# ID	user_login	first_name	last_name
# 1	admin
# 2	maria	Maria	Lopez
# 3	devon	Devon	Park
# == Step 4: the same through WordPress ==
# +----+------------+------------+-----------+
# | ID | user_login | first_name | last_name |
# +----+------------+------------+-----------+
# | 1  | admin      |            |           |
# | 2  | maria      | Maria      | Lopez     |
# | 3  | devon      | Devon      | Park      |
# +----+------------+------------+-----------+
# == Step 5: meta rows per user ==
# user_id	meta_rows
# 1	16
# 2	15
# 3	16

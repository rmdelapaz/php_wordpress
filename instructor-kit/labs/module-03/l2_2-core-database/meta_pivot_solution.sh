# meta_pivot_solution.sh: the instructor's reference for meta_pivot_starter.sh (Session 3, Lesson 2.2, lab A)
# state: after:lesson_04
# expect: 2	maria	Maria	Lopez
# expect: | 3  | devon      | Devon      | Park      |

echo "== Step 1: the users =="
wp db query "SELECT ID, user_login, display_name FROM wp_users ORDER BY ID"

echo "== Step 2: first names, one join =="
wp db query "SELECT u.ID, u.user_login, um.meta_value AS first_name FROM wp_users AS u JOIN wp_usermeta AS um ON um.user_id = u.ID AND um.meta_key = 'first_name' ORDER BY u.ID"

echo "== Step 3: one row per user, two fields =="
wp db query "SELECT u.ID, u.user_login, MAX(CASE WHEN um.meta_key = 'first_name' THEN um.meta_value END) AS first_name, MAX(CASE WHEN um.meta_key = 'last_name' THEN um.meta_value END) AS last_name FROM wp_users AS u JOIN wp_usermeta AS um ON um.user_id = u.ID GROUP BY u.ID, u.user_login ORDER BY u.ID"

echo "== Step 4: the same through WordPress =="
wp user list --orderby=ID --fields=ID,user_login,first_name,last_name

echo "== Step 5: meta rows per user =="
wp db query "SELECT user_id, COUNT(*) AS meta_rows FROM wp_usermeta GROUP BY user_id ORDER BY user_id"

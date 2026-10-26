# test_opening_hours.sh: five requests to the opening-hours route, as any client would send them (Session 14, Lesson 7.2, lab A)
# serve: opening_hours
# install: plugin pagesco-opening-hours
# state: after:lesson_23
# expect-starter: {"todo":"TODO: the hours"}
# expect-solution: {"day":"saturday","closed":false,"opens":"10:00","closes":"16:00"}
# expect-solution: day is not one of monday, tuesday, wednesday, thursday, friday, saturday, and sunday.
#
# From your project folder, with the plugin folder copied and activated:
#     cp -r labs/module-14/l7_2-custom-endpoints/opening_hours_starter wordpress/wp-content/plugins/pagesco-opening-hours
#     wp plugin activate pagesco-opening-hours
#     cp labs/module-14/l7_2-custom-endpoints/test_opening_hours.sh wordpress/
#     docker compose run --rm wpcli sh test_opening_hours.sh
# When you are done: wp plugin deactivate pagesco-opening-hours, then
#     rm -r wordpress/wp-content/plugins/pagesco-opening-hours wordpress/test_opening_hours.sh

API=http://localhost:8080/wp-json/pagesco/v1/opening-hours

echo "== Saturday"
curl -s "$API?day=saturday"; echo
echo "== Sunday"
curl -s "$API?day=sunday"; echo
echo "== A day that does not exist"
curl -s "$API?day=funday"; echo
echo "== The whole week: how many days, and Thursday"
curl -s "$API" | grep -o '"day":"[a-z]*"' | wc -l
curl -s "$API" | grep -o '{"day":"thursday"[^}]*}' || echo "(no Thursday)"
echo "== What OPTIONS says about the argument"
curl -s -X OPTIONS "$API" | grep -o '"day":{[^}]*"description":"[^"]*"' || echo "(no day argument)"

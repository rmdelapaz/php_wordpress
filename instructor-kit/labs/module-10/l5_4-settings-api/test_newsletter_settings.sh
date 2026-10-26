# test_newsletter_settings.sh: the newsletter screen, saved the way a browser saves it (Session 10, Lesson 5.4, lab A)
# serve: newsletter_settings
# install: mu-plugin
# state: after:lesson_16
# expect-starter: rows: 1
# expect-starter: "frequency":"daily"
# expect-solution: rows: 3
# expect-solution: Frequency must be weekly or monthly.
# expect-solution: {"signup_text":"Join our list","frequency":"monthly","show_form":false}
# expect-solution: as maria: 403
#
# Like Lesson 5.4's pagesco-save.sh, the test logs in as admin, reads the form's hidden fields and posts it to
# options.php: a sign-up text with tags, a frequency the screen does not offer, the checkbox unticked. From your
# project folder, with the plugin file copied into wordpress/wp-content/mu-plugins/:
#     cp labs/module-10/l5_4-settings-api/newsletter_settings_starter/pagesco-lab-newsletter.php wordpress/wp-content/mu-plugins/
#     cp labs/module-10/l5_4-settings-api/test_newsletter_settings.sh wordpress/
#     docker compose run --rm wpcli sh test_newsletter_settings.sh
# The test deletes the option it saved. When you are done:
#     rm wordpress/test_newsletter_settings.sh wordpress/wp-content/mu-plugins/pagesco-lab-newsletter.php

SITE=http://localhost:8080
PAGE="$SITE/wp-admin/options-general.php?page=pagesco-lab-newsletter"
JAR=/tmp/pagesco-lab-cookies.txt
curl -s -o /dev/null -c "$JAR" "$SITE/wp-login.php"
curl -s -o /dev/null -b "$JAR" -c "$JAR" -d log=admin -d pwd=password -d testcookie=1 "$SITE/wp-login.php"
FORM=$(curl -s -b "$JAR" "$PAGE")
echo "rows: $(echo "$FORM" | grep -o '<th scope="row">' | wc -l)"
echo "$FORM" | grep -o '<label for="pagesco-lab-[^"]*">[^<]*</label>'
NONCE=$(echo "$FORM" | grep -o 'name="_wpnonce" value="[^"]*"' | cut -d'"' -f4)
ANSWER=$(curl -s -b "$JAR" -c "$JAR" -o /dev/null -w '%{http_code}' -d option_page=pagesco_lab_newsletter -d action=update \
	-d "_wpnonce=$NONCE" --data-urlencode "_wp_http_referer=/wp-admin/options-general.php?page=pagesco-lab-newsletter" \
	--data-urlencode 'pagesco_lab_newsletter[signup_text]=<b>Join</b> our list' --data-urlencode 'pagesco_lab_newsletter[frequency]=daily' \
	"$SITE/wp-admin/options.php")
echo "options.php answered: $ANSWER"
curl -s -b "$JAR" "$PAGE&settings-updated=true" | grep -o '<p><strong>[^<]*</strong></p>' | sed 's/<[^>]*>//g'
echo "stored: $(wp option get pagesco_lab_newsletter --format=json)"
curl -s -o /dev/null -c "$JAR.m" "$SITE/wp-login.php"
curl -s -o /dev/null -b "$JAR.m" -c "$JAR.m" -d log=maria -d pwd=maria-pass -d testcookie=1 "$SITE/wp-login.php"
echo "as maria: $(curl -s -o /dev/null -w '%{http_code}' -b "$JAR.m" "$PAGE")"
wp option delete pagesco_lab_newsletter > /dev/null
rm -f "$JAR" "$JAR.m"

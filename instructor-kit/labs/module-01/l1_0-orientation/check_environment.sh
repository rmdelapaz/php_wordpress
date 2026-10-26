#!/usr/bin/env bash
# check_environment.sh: is this computer ready for PHP and WordPress Development? (Session 1; Session 9 with --part2)
# host: compose
# expect: READY for PHP and WordPress Development
#
# Run it on YOUR computer (not in a container), from your project folder (pagesco-dev, Lesson 1.2), with the site
# started (docker compose up -d):
#     cd ~/pagesco-dev
#     bash labs/module-01/l1_0-orientation/check_environment.sh
#     bash labs/module-01/l1_0-orientation/check_environment.sh --part2      (Session 9: Node 24, npm, Composer,
#                                                                            and the site as Lesson 4.3 left it)
# Each line says OK, CHECK (works, read the note), INFO (for your information) or FIX (what to do next).
# The last line is the verdict: READY, READY WITH NOTES, or NOT READY (exit status 1).
# It changes nothing on your site; it sends one test email, which Mailpit catches.

PART2=0
[ "${1:-}" = "--part2" ] && PART2=1
PORT="${PAGESCO_PORT:-8080}"              # the host ports of compose.yaml (the kit's checker maps others)
MAILPORT="${PAGESCO_MAILPIT_PORT:-8025}"
fails=0
notes=0
ok()    { printf 'OK    %s\n' "$*"; }
check() { printf 'CHECK %s\n' "$*"; notes=$((notes + 1)); }
info()  { printf 'INFO  %s\n' "$*"; }
fix()   { printf 'FIX   %s\n' "$*"; fails=$((fails + 1)); }
verdict() {
	if [ "$fails" -gt 0 ]; then
		echo "NOT READY: fix the FIX lines (top to bottom), then run this check again"
		exit 1
	elif [ "$notes" -gt 0 ]; then
		echo "READY WITH NOTES for PHP and WordPress Development"
	else
		echo "READY for PHP and WordPress Development"
	fi
	exit 0
}
WP="docker compose --progress quiet run --rm -T wpcli wp"
INSIDE="docker compose --progress quiet run --rm -T wpcli"

echo "PHP and WordPress Development: environment check$([ "$PART2" = 1 ] && echo ' (Part 2)')"

# 1. Docker and Compose -------------------------------------------------------------------------------------
if ! command -v docker >/dev/null 2>&1; then
	fix "docker: command not found. Install Docker Desktop (Windows with WSL 2, macOS) or Docker Engine (Linux): Lesson 1.2"
	verdict
fi
server=$(docker version --format '{{.Server.Version}}' 2>/dev/null)
if [ -z "$server" ]; then
	fix "Docker is installed but not running (or you may not use it). Start Docker Desktop; on Linux: sudo usermod -aG docker \"\$USER\", then log out and in"
	verdict
fi
ok "Docker $server"
compose=$(docker compose version --short 2>/dev/null)
case "$compose" in
	"") fix "docker compose (with a space) does not work: install the Compose plugin (Lesson 1.2)"; verdict ;;
	1.*) fix "Docker Compose $compose is the retired version 1: update Docker (Lesson 1.2)"; verdict ;;
	*) ok "Docker Compose $compose" ;;
esac

# 2. The project folder and its services --------------------------------------------------------------------
if [ ! -f compose.yaml ] || ! grep -q '^name: pagesco' compose.yaml; then
	fix "no Pages & Co. compose.yaml in $(pwd): cd into your project folder first (cd ~/pagesco-dev)"
	verdict
fi
ok "project folder $(basename "$(pwd)") (compose.yaml of project pagesco)"
case "$(pwd)" in
	/mnt/[a-z]/*) check "the project is on the Windows drive ($(pwd)): it works, but slowly. Lesson 1.2 keeps it in your Linux home folder" ;;
esac
running=$(docker compose ps --services --status running 2>/dev/null | sort | tr '\n' ' ')
missing=""
for s in db mailpit wordpress; do
	case " $running" in *" $s "*) ;; *) missing="$missing $s" ;; esac
done
if [ -n "$missing" ]; then
	fix "not running:$missing. Start the site: docker compose up -d (then docker compose ps)"
	case "$missing" in *wordpress*|*db*) verdict ;; esac
else
	ok "services running: db, mailpit, wordpress"
fi
if [ "$(uname -s)" = "Linux" ] && [ -d wordpress ]; then
	owner=$(stat -c %u wordpress)
	if [ "$owner" = "$(id -u)" ]; then
		ok "wordpress/ belongs to you (uid $owner): your editor can save in wp-content/"
	else
		fix "wordpress/ belongs to uid $owner, not to you ($(id -u)): Lesson 1.2, \"Linux and WSL: Run WordPress as You\" (the repair box)"
	fi
fi

# 3. WordPress, PHP and WP-CLI ------------------------------------------------------------------------------
cli=$($WP cli version 2>&1 | tail -n 1)
case "$cli" in
	"WP-CLI "*) ok "$cli (the course's wpcli image)" ;;
	*) fix "WP-CLI did not answer: $cli"; verdict ;;
esac
if ! $WP core is-installed >/dev/null 2>&1; then
	fix "WordPress is not installed yet: run the two install commands of Lesson 1.2 (wp core install ..., wp rewrite structure ...)"
	verdict
fi
wpver=$($WP core version 2>/dev/null)
case "$wpver" in
	7.1|7.1.*) ok "WordPress $wpver" ;;
	7.*) check "WordPress $wpver: the course is built on 7.1; most lessons work, some outputs differ" ;;
	*) fix "WordPress $wpver: the course needs 7.1 (the image wordpress:7.1-php8.5-apache in compose.yaml)" ;;
esac
webphp=$(docker compose exec -T wordpress php -r 'echo PHP_VERSION;' 2>/dev/null)
cliphp=$($WP eval 'echo PHP_VERSION;' 2>/dev/null)
case "$webphp" in
	8.5.*) ok "PHP $webphp (web server), $cliphp (WP-CLI)" ;;
	8.4.*) check "PHP $webphp (web server), $cliphp (WP-CLI): 8.4 works; the lessons note where its output differs" ;;
	*) fix "PHP ${webphp:-?} on the web server: the course uses 8.5 (or 8.4); check the image name in compose.yaml" ;;
esac
siteurl=$($WP option get siteurl 2>/dev/null)
if [ "$siteurl" = "http://localhost:8080" ]; then
	ok "site address $siteurl"
else
	fix "site address is '$siteurl', not http://localhost:8080: reinstall with --url=http://localhost:8080 (Lesson 1.2)"
fi
perma=$($WP option get permalink_structure 2>/dev/null)
if [ "$perma" = "/%postname%/" ]; then
	ok "pretty permalinks $perma"
else
	fix "permalinks are '${perma:-plain}': wp rewrite structure '/%postname%/'"
fi
code=$($INSIDE curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/ 2>/dev/null)
if [ "$code" = "200" ]; then
	ok "the home page answers 200 inside the containers"
else
	fix "the home page answers '${code:-nothing}' inside the containers: docker compose logs wordpress"
fi
if $WP cron test 2>&1 | grep -q '^Success'; then
	ok "WordPress can call itself (wp cron test)"
else
	fix "wp cron test fails: is config/apache-8080.conf still mounted in compose.yaml? (Lesson 1.2, the port-8080 setup)"
fi
dbg=$($WP eval 'echo ( WP_DEBUG && WP_DEBUG_LOG && WP_DEBUG_DISPLAY ) ? "on" : "off", " ", wp_get_environment_type(), " ", wp_is_writable( WP_CONTENT_DIR ) ? "writable" : "read-only";' 2>/dev/null)
if [ "$dbg" = "on local writable" ]; then
	ok "debugging on (WP_DEBUG, WP_DEBUG_LOG, WP_DEBUG_DISPLAY), environment local, wp-content writable"
else
	fix "debug settings: '$dbg' (expected 'on local writable'): the WORDPRESS_* lines of compose.yaml (Lesson 1.2)"
fi

# 4. Email -----------------------------------------------------------------------------------------------
if [ -f wordpress/wp-content/mu-plugins/mailpit-smtp.php ]; then
	sent=$($WP eval 'echo wp_mail( "admin@example.com", "Environment check", "check_environment.sh can send email." ) ? "sent" : "failed";' 2>/dev/null)
	caught=$($INSIDE curl -s 'http://mailpit:8025/api/v1/messages?limit=1' 2>/dev/null)
	case "$sent:$caught" in
		sent:*'"Subject":"Environment check"'*) ok "wp_mail() sent a test message and Mailpit caught it" ;;
		sent:*) fix "wp_mail() said yes but Mailpit has no message: is the mailpit service running?" ;;
		*) fix "wp_mail() failed: Lesson 1.2, Common Mistakes 3" ;;
	esac
else
	fix "wordpress/wp-content/mu-plugins/mailpit-smtp.php is missing: cp config/mailpit-smtp.php wordpress/wp-content/mu-plugins/"
fi

# 5. From your browser's side -------------------------------------------------------------------------------
if command -v curl >/dev/null 2>&1; then
	# (the Host header is what your browser sends for http://localhost:8080/; it keeps WordPress from redirecting
	#  when the kit's checker reaches the same container through another port)
	hc=$(curl -s -o /dev/null -w '%{http_code}' -H 'Host: localhost:8080' "http://localhost:$PORT/" 2>/dev/null)
	mc=$(curl -s -o /dev/null -w '%{http_code}' "http://localhost:$MAILPORT/" 2>/dev/null)
	if [ "$hc" = "200" ] && [ "$mc" = "200" ]; then
		ok "this computer reaches http://localhost:$PORT/ (the site) and http://localhost:$MAILPORT/ (Mailpit)"
	else
		fix "from this computer: the site answers '$hc', Mailpit '$mc' (200 expected): docker compose ps, the PORTS column"
	fi
else
	info "curl is not installed here: open http://localhost:$PORT/ and http://localhost:$MAILPORT/ in your browser instead"
fi

# 6. Part 2 (Session 9) -------------------------------------------------------------------------------------
if [ "$PART2" = 1 ]; then
	nv=$(node --version 2>/dev/null)
	case "$nv" in
		v24.*) ok "Node $nv and npm $(npm --version 2>/dev/null)" ;;
		v2[5-9].*|v[3-9][0-9].*) check "Node $nv: the course uses Node 24 LTS; newer usually works" ;;
		*) if docker image inspect node:24 >/dev/null 2>&1 || docker pull -q node:24 >/dev/null 2>&1; then
			check "no Node 24 on this computer ($nv): use the node:24 image as Lesson 6.1 shows (docker run ... node:24 npm ...)"
		else
			fix "no Node 24 and no node:24 image: install Node 24 LTS (nvm install 24) before Module 6"
		fi ;;
	esac
	cv=$(docker run --rm composer:2 --version 2>/dev/null | head -n 1)
	case "$cv" in
		"Composer version 2"*) ok "$(echo "$cv" | cut -d' ' -f1-3) (the composer:2 image, Lesson 5.1)" ;;
		*) fix "the composer:2 image does not run: docker pull composer:2 (Lesson 1.3)" ;;
	esac
	theme=$($WP theme list --status=active --field=name 2>/dev/null)
	if [ "$theme" = "pagesco" ] && $WP theme is-installed pagesco-classic >/dev/null 2>&1 && [ -f wordpress/wp-content/mu-plugins/pagesco-site.php ]; then
		ok "the site as Lesson 4.3 left it: pagesco active, pagesco-classic installed, mu-plugins/pagesco-site.php"
	else
		fix "the site is not where Part 2 starts (active theme '$theme'): finish Lesson 4.3, or import the Part 2 starting site (the course download pagesco-part2-start.zip: its README.txt)"
	fi
fi

verdict

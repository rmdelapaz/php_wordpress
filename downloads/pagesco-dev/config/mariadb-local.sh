#!/bin/sh
# Wrapper for the MariaDB client tools that "wp db ..." runs (mariadb, mariadb-dump, mariadb-check).
# MySQL 9.7's development certificate is self-signed, so the client's certificate check fails with
# "ERROR 2026 ... self-signed certificate in certificate chain". This turns the check off for the local
# database only. WP-CLI passes --no-defaults, which must stay the first option.
tool="/usr/bin/$(basename "$0")"
if [ "$1" = "--no-defaults" ]; then
	shift
	exec "$tool" --no-defaults --ssl-verify-server-cert=0 "$@"
fi
exec "$tool" --ssl-verify-server-cert=0 "$@"

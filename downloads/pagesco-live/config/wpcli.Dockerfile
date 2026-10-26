# The course's WP-CLI container: the official wordpress:cli image + three fixes for MySQL 9.7 and PHP 8.5.
ARG BASE=wordpress:cli-php8.5
FROM ${BASE}
USER root
# 1. "wp db ..." needs the caching_sha2_password login plugin (MySQL 8+ default), missing from the image.
RUN apk add --no-cache mariadb-connector-c
# 2. Accept MySQL's self-signed development certificate (see mariadb-local.sh).
COPY mariadb-local.sh /usr/local/bin/mariadb
COPY mariadb-local.sh /usr/local/bin/mariadb-dump
COPY mariadb-local.sh /usr/local/bin/mariadb-check
RUN chmod 755 /usr/local/bin/mariadb /usr/local/bin/mariadb-dump /usr/local/bin/mariadb-check
# 3. Hide WP-CLI 2.12's own PHP 8.5 deprecation notices (see quiet-wp-cli-deprecations.php).
COPY wp-cli.yml /etc/wp-cli/config.yml
COPY quiet-wp-cli-deprecations.php /etc/wp-cli/quiet-wp-cli-deprecations.php
ENV WP_CLI_CONFIG_PATH=/etc/wp-cli/config.yml
USER www-data

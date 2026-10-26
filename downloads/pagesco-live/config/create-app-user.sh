#!/bin/sh
# Runs once, when the database is created (an initialization script of the mysql image).
# WordPress gets its own account with the rights it needs for its own database, and nothing else:
# no other databases, no user management, no server administration (MySQL Foundations, Lesson 7.4).
# CREATE, ALTER, INDEX and DROP are for updates that change tables (core, plugins: dbDelta).
# What backups need on top of this, Lesson 8.4 finds out (Step 6).
mysql -uroot -p"$MYSQL_ROOT_PASSWORD" <<SQL
CREATE USER 'pagesco_app'@'%' IDENTIFIED BY '${DB_APP_PASSWORD}';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, INDEX, DROP ON pagesco.* TO 'pagesco_app'@'%';
SQL

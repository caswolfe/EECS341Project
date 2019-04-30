# EECS341Project

<B>Final Class Project for EECS341 Intro to Databases</B>
Andrew Duffield, Ben Pierce, Andrew Szabo and Chad

The database is hosted on the eecslab9 server, under the "team_12" database. It is intended for
the web-server to be run locally while connecting to the database, and therefore must occur
physically at CWRU or with the VPN on.


Requirements:
  - Python
    - configparser
    - flask
    - mysql-connector
  - MySQL

<B>Instillation Instructions:</B>
  1) install MySQL
  2) install pyton, python3, and pip
  3) clone the repository
  4) run "bash setup.sh"
  5) edit "config.ini" as appropriate
  6) if you need a copy of our database, "create_db.sql" will create the database and populate it
  7) "python run.py" to run the actual server, it will print an ip to use in the local web-browser

To access MySQL Database:
mysql -u team_12 -p -h eecslab-9 -P 3306

Password:
50ab6263

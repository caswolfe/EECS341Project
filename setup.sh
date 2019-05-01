#!/bin/bash

#Setup

echo "you must have python and pip installed..."

echo
echo "installing configparser"
pip install configparser

echo
echo "installing flask"
pip install flask

echo
echo "installing mysql-connector"
pip install mysql-connector

echo
echo "creating config.ini"

#creates the config file
FILE="config.ini"
/bin/cat <<EOM >$FILE
[app]
debug = True
host = 127.3.4.1
port = 3306

[mysql.connector]
host = eecslab-9
user = team_12
passwd = 50ab6263
database = team_12
EOM

echo
echo "finished"

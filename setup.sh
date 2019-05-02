#!/bin/bash

#Setup

echo "you must have python and pip installed..."

echo
echo "settting up virtual environment"
virtualenv env
source env/bin/activate
sleep 2s

echo
echo "installing configparser"
pip install configparser
sleep 2s

echo
echo "installing flask"
pip install flask
sleep 2s

echo
echo "installing mysql-connector"
pip install mysql-connector
sleep 2s

echo
echo "creating config.ini"

#creates the config file
FILE="config.ini"
/bin/cat <<EOM >$FILE
[app]
debug = True
host = eecslab-9.case.edu
port = 34405

[mysql.connector]
host = eecslab-9
user = team_12
passwd = 50ab6263
database = team_12
EOM
sleep 2s

echo
echo "finished"

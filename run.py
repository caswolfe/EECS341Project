import configparser
from flask import Flask, render_template, request, url_for, redirect
from flask_table import Table, Col
import mysql.connector

# Read configuration from file.
config = configparser.ConfigParser()
config.read('config.ini')

# Set up application server.
app = Flask(__name__)

# Create a function for fetching data from the database.
def sql_query(sql):
    db = mysql.connector.connect(**config['mysql.connector'])
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result


def sql_execute(sql):
    db = mysql.connector.connect(**config['mysql.connector'])
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()

# For this example you can select a handler function by
# uncommenting one of the @app.route decorators.


# @app.route('/')
def template_response():
    return render_template('home-w-data.html')

@app.route('/create-account')
def create_account():
    return render_template('create_account.html')

@app.route('/home')
def home():
    sql = "select distinct product.name, product.price, product.quantity from user,product where user.uid = product.sellerid;"
    result = sql_query(sql)
    return render_template('user_homepage.html', template_data = result)


@app.route('/', methods=['GET', 'POST'])
def template_response_with_data():
    template_data = ""
    if request.method == 'POST':
        result = request.form
        print(result)
        if "Login" in result:
            uname = str(result['username'])
            pswd = str(result['password'])
            sql = "select uid as id from user where user.username='{uname}' and user.password='{pswd}'".format(uname=uname,pswd=pswd)
            sql_result = sql_query(sql)
            if not sql_result:
                template_data="User not found. Please try again"
                return render_template('home-w-data.html', template_data = template_data)
            else:
                return redirect(url_for('home'))
                #return render_template('user_homepage.html', template_data = uname)
        elif "Create_Account" in result:
            return redirect(url_for('create_account'))

    else:
        template_data = ""

    return render_template('home-w-data.html', template_data = template_data)

# @app.route('/login',methods = ['POST','GET'])
# def login():
#     if request.method == 'POST':
#         result = request.form
#         print(result)

if __name__ == '__main__':
    app.run(**config['app'])

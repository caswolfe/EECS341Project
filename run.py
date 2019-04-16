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




@app.route('/create-account')
def create_account():
    return render_template('create_account.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        result = request.form
        if "Shop" in result:
            return redirect(url_for('shop'))
    sql = "select distinct product.name, product.price, product.quantity from user,product where user.uid = product.sellerid;"
    result = sql_query(sql)
    return render_template('user_homepage.html', template_data = result)

@app.route('/shop', methods=['GET', 'POST'])
def shop():
    if "buy" in request.form:
        #print("button press")
        id = int(request.form["buy"])
        return redirect(url_for('purchase'))
    sql = "select * from product"
    template_data = sql_query(sql)
    return render_template('shop.html',template_data = template_data)


@app.route('/purchase' ,methods=['GET', 'POST'])
def purchase(productid=None, buyerid = None):
    return render_template('purchase.html')

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

if __name__ == '__main__':
    app.run(**config['app'])

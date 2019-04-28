import configparser
from flask import Flask, render_template, request, url_for, redirect, session
from flask_table import Table, Col
import mysql.connector

# Read configuration from file.
config = configparser.ConfigParser()
config.read('config.ini')

# Set up application server.
app = Flask(__name__)

#set up key for session cookies
app.secret_key = b'Jinormous_jungle'

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
        print("product id: "+ str(id))
        return redirect(url_for('purchase',pid = id))

    uname = session['uname']
    print(uname)
    sql = "select * from product p, user u where p.sellerid = u.uid and u.username != '{uname}'".format(uname=uname)
    template_data = sql_query(sql)
    return render_template('shop.html',template_data = template_data)


@app.route('/purchase' ,methods=['GET', 'POST'])
def purchase():
    if request.method == 'POST':
        #TODO:purchase logic

        return redirect(url_for('shop'))

    pid = request.args.get('pid')
    print("pid is:" + str(pid))
    sql = "select p.name, s.name, p.price from product p, user s where p.pid = '{pid}' and s.uid = p.sellerid;".format(pid = str(pid))
    product_info = sql_query(sql)
    print("template_data:")
    print(product_info)
    return render_template('purchase.html', template_data = product_info)

@app.route('/', methods=['GET', 'POST'])
def template_response_with_data():
    template_data = ""
    if request.method == 'POST':
        result = request.form
        print(result)
        if "Login" in result:
            uname = str(result['username'])
            session['uname'] = uname
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

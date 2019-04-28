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
#sessions give us a mechanism to store info locally. We use it to store a username so we know
#who's buying something
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

#note that we're establishing and closing a connection to the db with each request
#is this the optimal way to do this?


#TODO
@app.route('/createaccount')
def createaccount():
    if request.method == 'POST':
        pass #python for do nothing
        #TODO create user in database, verify that user does not already exist
    return render_template('createaccount.html')


#the user home. Lists their products, balance, etc
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        result = request.form
        if "Shop" in result:
            return redirect(url_for('shop'))
    sql = "select distinct product.name, product.price, product.quantity from user,product where user.uid = product.sellerid;"
    #TODO: we need to add some form of balance or way of keeping track amount spent, gained
    #another attribute in the user table? Or some other way?
    result = sql_query(sql)

    #we can pass data to html by giving something to the template_data arg
    #from html, we can run embedded python by using {{*embedded python code*}}
    #we can then access whatever data we store in the arguement we passed
    #typically, we pass data as a list or dict, which are analogous to vectors/arraylists and hashmaps, respectivily
    return render_template('user_homepage.html', template_data = result)

#the basic shop page
@app.route('/shop', methods=['GET', 'POST'])
def shop():
    #when the user clicks the buy button
    if "buy" in request.form:
        id = int(request.form["buy"])
        print("product id: "+ str(id))
        return redirect(url_for('purchase',pid = id)) #sends pid to request.args

    uname = session['uname'] #uses session to get username. Setup on the '/' page
    print(uname)
    #show all products that are not owned by the user
    sql = "select * from product p, user u where p.sellerid = u.uid and u.username != '{uname}'".format(uname=uname)
    #python string.format operates similarily to printf() in C
    template_data = sql_query(sql)
    return render_template('shop.html',template_data = template_data)


@app.route('/purchase' ,methods=['GET', 'POST'])
def purchase():
    if request.method == 'POST':
        #TODO:purchase logic
        #delete from user inventory?
        #update user balance?
        #quantity options?
        return redirect(url_for('shop'))

    pid = request.args.get('pid') #passed from '/shop'
    print("pid is:" + str(pid))
    #aquire particular info about the product
    sql = "select p.name, s.name, p.price from product p, user s where p.pid = '{pid}' and s.uid = p.sellerid;".format(pid = str(pid))
    product_info = sql_query(sql)
    print("template_data:")
    print(product_info)
    return render_template('purchase.html', template_data = product_info)


#what you see when you first login
@app.route('/', methods=['GET', 'POST'])
def template_response_with_data():
    if request.method == 'POST': #if the user has clicked a button
        result = request.form
        print(result)
        if "Login" in result: #if the user clicked the "login" button
            uname = str(result['username']) #get data from the form, sent from the html <form> tag
            session['uname'] = uname #save the username to the session, for use when purchasing
            pswd = str(result['password'])

            #see if we have an existing user
            sql = "select uid as id from user where user.username='{uname}' and user.password='{pswd}'".format(uname=uname,pswd=pswd)
            sql_result = sql_query(sql)
            if not sql_result: #if query returns empty set
                template_data="User not found. Please try again"
                return render_template('home-w-data.html', template_data = template_data) #sends us back to the start
            else: #we've got a user that matches username, password
                return redirect(url_for('home'))
        elif "Create_Account" in result:
            return redirect(url_for('createaccount')) #send us to the homepage
    return render_template('home-w-data.html')



#analogous to int main() in C/++/Java/etc
if __name__ == '__main__':
    app.run(**config['app'])

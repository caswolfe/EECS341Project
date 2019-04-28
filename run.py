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
        sql = "select uid as id from user where user.username='{uname}'".format(uname=uname)
        sql_result = sql_query(sql)

        #if query returns empty set, can create account
        if not sql_result:
            print("add the user")
            n_username =    str(result['username'])
            n_password =    str(result['password'])
            n_name =        str(result['name'])
            n_email =       str(result['email'])

            insert_command = "INSERT INTO user (username, password, name, email) VALUES ({uname}, {pswd}, {nm}, {eml})".format(uname=n_username, pswd=n_password, nm=n_name, eml=n_email)
            sql_execute(insert_command)
            return redirect(url_for('home'))

        #we've got a user that matches username, can't create account
        else:
            template_data="Username allready in use,pPlease try again"
            return render_template('createaccount.html', template_data = template_data) #sends us back to the start

    template_data = ""
    return render_template('createaccount.html', template_data = template_data)


#the user home. Lists their products, balance, etc
@app.route('/home', methods=['GET', 'POST'])
def home():
    pid = 0
    if request.method == 'POST':
        result = request.form
        if "sell" in result:
            return redirect(url_for('sell'))
        if "Shop" in result:
            return redirect(url_for('shop'))
        if "update" in result:
            pid = int(request.form['update'])
            #print(pid)
        if "submit" in result:
            pid = int(request.form['pid'])
            name = str(request.form['name'])
            price = str(request.form['price'])
            quant = str(request.form['quantity'])
            sql = "update product set name ='{name}',price = '{price}',quantity = '{quant}' where pid = '{pid}'".format(name=name,price=price,quant=quant,pid=pid)
            sql_execute(sql)
            print(pid,name,price,quant)
            pid = 0

    uname = session['uname']
    sql = "select u.uid from user u where u.username = '{uname}'".format(uname=uname)
    uid = sql_query(sql)[0][0]

    sql = "select distinct product.name, product.price, product.quantity, product.pid from user,product where user.uid = product.sellerid and user.uid = '{uid}';".format(uid=uid)
    #TODO: we need to add some form of balance or way of keeping track amount spent, gained
    #another attribute in the user table? Or some other way?
    result = sql_query(sql)
    ret = []
    #need to return true if update button is pushed
    if pid:
        #print("test")
        for i in result:
            if i[3] == pid:
                j = i + (True,)
                ret.append(j)
            else:
                j = i + (False,)
                ret.append(j)
    else:
        ret = result

    print(ret)
    #we can pass data to html by giving something to the template_data arg
    #from html, we can run embedded python by using {{*embedded python code*}}
    #we can then access whatever data we store in the arguement we passed
    #typically, we pass data as a list or dict, which are analogous to vectors/arraylists and hashmaps, respectivily
    return render_template('user_homepage.html', template_data = ret)

#the basic shop page
@app.route('/shop', methods=['GET', 'POST'])
def shop():
    #when the user clicks the buy button
    if request.method == 'POST':
        print("post recieved")
        if "buy" in request.form:
            print("Clicked buy")
            id = request.form["pid"]
            quant = request.form["quantity"]
            print("product id: "+ str(id))
            return redirect(url_for('purchase',pid = id,quant = quant )) #sends pid to request.args

    uname = session['uname'] #uses session to get username. Setup on the '/' page
    #print(uname)
    #show all products that are not owned by the user
    sql = "select * from product p, user u where p.sellerid = u.uid and u.username <> '{uname}'".format(uname=uname)
    #python string.format operates similarily to printf() in C
    template_data = sql_query(sql)
    return render_template('shop.html',template_data = template_data)


@app.route('/sell',methods=['GET','POST'])
def sell():
    ret = ""
    if request.method == 'POST':
        if 'add_item' in request.form:
            name = request.form['Item Name']
            price = request.form['Price(USD)']
            quantity = request.form['Quantity']
            uname = session['uname']
            sql = "select u.uid from user u where u.username = '{uname}'".format(uname=uname)
            uid = sql_query(sql)[0][0]
            sql = "insert into product (sellerid,name,price,quantity) values('{uid}','{name}','{price}','{quantity}')".format(uid=uid,name=name,price=price,quantity=quantity)
            sql_execute(sql)
            return redirect(url_for('home'))
    return render_template('sell.html',template_data = ret)


@app.route('/purchase' ,methods=['GET', 'POST'])
def purchase():
    pid = request.args.get('pid') #passed from '/shop'
    current_pid = pid
    print("pid is:" + str(pid))
    #aquire particular info about the product
    sql = "select p.name, s.uid, p.price from product p, user s where p.pid = '{pid}' and s.uid = p.sellerid;".format(pid=pid)
    product_info = sql_query(sql)
    print(product_info)
    #print("got product info")
    if request.method == 'POST':
        print("posted")
        #TODO:purchase logic
        #delete from user inventory?
        #update user balance?
        #quantity options?
        uname=session['uname']
        sql = "select u.uid from user u where u.username = '{uname}'".format(uname=uname)
        uid = sql_query(sql)[0][0]

        #create transaction
        pid = current_pid
        sql = "select p.name, s.uid, p.price from product p, user s where p.pid = '{pid}' and s.uid = p.sellerid;".format(pid=pid)
        product_info = sql_query(sql)
        name = product_info[0]
        sid = product_info[1]
        price = product_info[2]
        #need quantity
        quant = request.args.get('quant')
        print(name,sid,price,quant)


        sql = "insert into transaction"

        return redirect(url_for('shop',pid=pid))


    #print("template_data:")
    #print(product_info)
    return render_template('purchase.html', template_data = product_info)


#what you see when you first login
@app.route('/', methods=['GET', 'POST'])
def template_response_with_data():
    template_data = ""
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
    return render_template('home-w-data.html', template_data = template_data)



#analogous to int main() in C/++/Java/etc
if __name__ == '__main__':
    app.run(**config['app'])

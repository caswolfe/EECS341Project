import configparser
from flask import Flask, render_template, request, url_for, redirect, session
#from flask_table import Table, Col
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
        #pass #python for do nothing
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
            #print(pid,name,price,quant)
            pid = 0


        #we also need to look at this delete
        #as it will fail if we try to delete something with a foregin key, in this case a previous transaction
        #see in the purchase function
        if "delete" in result:
            print("TIEM FOR DELETE")
            to_del = request.form.getlist('check')
            print(to_del)
            for pid in to_del:
                sql = "update product set quantity=-1 where product.pid = '{pid}'".format(pid=pid)
                sql_execute(sql)
                # sql = "delete from product where product.pid = '{pid}'".format(pid=pid)
                # sql_execute(sql)

    uname = session['uname']
    sql = "select u.uid from user u where u.username = '{uname}'".format(uname=uname)
    uid = sql_query(sql)[0][0]

    sql = "select distinct product.name, product.price, product.quantity, product.pid from user,product where user.uid = product.sellerid and user.uid = '{uid}' and product.quantity >=0;".format(uid=uid)
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


    #now do transactions
    sql = "select p.name, t.ppunit, t.quantity, t.ts, t.pid, now()  from transaction t, product p  where t.buyerid = '{bid}' and t.ts >= DATE_SUB(now(),INTERVAL 1 DAY) and p.pid = t.pid;".format(bid=uid)
    result = sql_query(sql)
    #print(result)
    transactions = []
    for tup in result:
        name,ppunit,quant,ts,pid,rn = tup
        total_price = float(ppunit) * float(quant)
        transactions.append([pid,name,ppunit,quant,total_price,str(ts)])

    #print(transactions)


    #now do aggregates
    aggregate_data = []
    sql = "select count(distinct t.pid),sum(t.quantity),sum(t.ppunit*t.quantity) from transaction t where t.buyerid = '{pid}'".format(pid=uid)
    buy_result = sql_query(sql)
    sql = "select count(distinct t.pid),sum(t.quantity),sum(t.ppunit*t.quantity) from transaction t where t.sellerid = '{pid}'".format(pid=uid)
    sell_result = sql_query(sql)

    #print(result)
    num_distinct_buy_t,quant_bought_b,total_spendings_b = buy_result[0]
    num_distinct_sell_t,quant_bought_s,total_spendings_s = sell_result[0]
    aggregate_data = [num_distinct_buy_t,int(quant_bought_b),format(total_spendings_b,'.2f'),num_distinct_sell_t,int(quant_bought_s),format(total_spendings_s,'.2f')]
    print(aggregate_data)


    #print(ret)
    #we can pass data to html by giving something to the template_data arg
    #from html, we can run embedded python by using {{*embedded python code*}}
    #we can then access whatever data we store in the arguement we passed
    #typically, we pass data as a list or dict, which are analogous to vectors/arraylists and hashmaps, respectivily
    return render_template('user_homepage.html', template_data = ret, aggregate_data=aggregate_data,transactions = transactions)

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
            print("quantity:" + str(quant))
            print("product id: "+ str(id))
            return redirect(url_for('purchase',pid = id,quant = quant )) #sends pid to request.args

    uname = session['uname'] #uses session to get username. Setup on the '/' page
    #print(uname)
    #show all products that are not owned by the user
    sql = "select * from product p, user u where p.sellerid = u.uid and u.username <> '{uname}' and p.quantity>0".format(uname=uname)
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
    quant = request.args.get('quant')
    if pid is None:
        pid =session['pid']
    if quant is None:
        quant = session['quant']
    sql = "select p.name, s.uid, p.price from product p, user s where p.pid = '{pid}' and s.uid = p.sellerid;".format(pid=pid)
    pf = sql_query(sql)
    name,side,price = pf[0]
    total = float(price)*float(quant)

    pf = [name,quant,total]
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
        print("STORED PID = "+str(session['pid']))
        newpid = session['pid']


        #create transaction
        sql = "select p.name, s.uid, p.price from product p, user s where p.pid = '{pid}' and s.uid = p.sellerid;".format(pid=newpid)
        product_info = sql_query(sql)
        name,sid,price = product_info[0]
        #need quantity
        squant = session['quant']

        print(name,sid,price,squant)
        sql = "insert into transaction (pid,sellerid,buyerid,quantity,ppunit) values('{newpid}','{sid}','{uid}','{quant}','{price}')".format(newpid=newpid,sid=sid,uid=uid,quant=squant,price=price)
        sql_execute(sql)


        #reduce seller amount of goods
        sql = "select p.quantity from product p where p.pid = '{pid}'".format(pid=newpid)
        original_quantity = int(sql_query(sql)[0][0])
        new_quantity = original_quantity-int(squant)
        print("newquantiy = " + str(new_quantity))

###########################################################################################################
        #design: we never delete products, as they are refrenced in transaction
        #instead, the SQL query that displays products in the shop just doesn't display
        #products with quantity > 0
        #this could be good or bad. It is helpful to see if the store has ever carried
        #a product, and leaves open the possibility of restocking
        #this could be bad in the case that a product is removed and never dealt with again

        #an additional option is to set the foregin key NULL on delete (set during CREATE TABLE)
        #I also like this, as it enables a search for products we no longer carry by looking for NULL


        # if new_quantity < 1:
        #     sql= "delete from product where product.pid = '{pid}'".format(pid=newpid)
        #     sql_execute(sql)
        # else:
################################################################################################################
        sql = "update product set quantity = '{new_quantity}' where product.pid = '{pid}'".format(new_quantity=new_quantity,pid=newpid)
        sql_execute(sql)

        #adjust user balanaces
        #the current user
        total = float(price)*float(squant)
        print(total)
        sql = "select u.balance from user u where u.uid = '{uid}'".format(uid=uid)
        current_bal = sql_query(sql)[0][0]
        new_bal = current_bal-total
        print(new_bal)
        sql = "update user set balance= '{new_bal}' where user.uid = '{uid}'".format(new_bal=new_bal,uid=uid)
        sql_execute(sql)


        #the seller
        sql = "select u.balance from user u where u.uid = '{sid}'".format(sid=sid)
        current_bal = sql_query(sql)[0][0]
        new_bal = current_bal+total
        print(new_bal)
        sql = "update user set balance= '{new_bal}' where user.uid = '{sid}'".format(new_bal=new_bal,sid=sid)
        sql_execute(sql)
        return redirect(url_for('shop',pid=pid))
    else:
        session['pid'] = pid
        session['quant'] = quant


    #print("template_data:")
    #print(product_info)
    return render_template('purchase.html', template_data = pf)


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

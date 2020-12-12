from flask import Flask, render_template, redirect, request, session
import mysql.connector as mysql
import os
import random

def connection():
    global con, cur
    con = mysql.connect(host = "localhost",
                        user = "root",
                        passwd = "rootpassword",
                        db = "cardb")
    cur = con.cursor()

app = Flask(__name__)
app.secret_key = os.urandom(16)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/admin_insert', methods=['GET', 'POST'])
def admin_insert():
    if request.method == "GET":
        return render_template("admin_insert.html")
    else:
        print("Hello")
        model = request.form['model']
        color = request.form['color']
        price = request.form['price']
        grade = request.form['grade']
        car_type = request.form['car_type']
        engine_power = request.form['engine_power']
        tax = request.form['tax']
        img = request.files['img']
        filename = img.filename
        fpath = str("static/img/car_photos/"+filename)
        img.save(fpath)
        connection()
        cur.execute("INSERT INTO car (model,color,price,grade,car_type,engine_power,tax_price,photo) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (model,color,price,grade,car_type,engine_power,tax,img))
        con.commit()
        row = cur.fetchone()
        return render_template("faq.html", row = row,)

@app.route('/admin_update', methods=['GET', 'POST'])
def admin_update():
    # if request.method == "GET":
        return render_template("admin_update.html")
    # else:

@app.route('/admin_delete', methods=['GET', 'POST'])
def admin_delete():
    # if request.method == "GET":
        return render_template("admin_delete.html")
    # else:


@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        role = request.form['role']
        session['role'] = role
        password = request.form['password']
        connection()
        cur.execute("SELECT * from employee where emp_role LIKE %s",[role])
        Password = cur.fetchone()
        if role == None:
            return "Username does not exist!!"
        elif role == "admin" and password == "admin":
            return render_template("admin_insert.html")
        else:
            passwd = Password[3]
            if password == passwd:
                return render_template("about.html")
            else:
                return "Password is incorrect"

@app.route("/signup", methods=["POST","GET"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        role = request.form['role']
        department = request.form['department']
        username = request.form['username']
        address = request.form['address']
        phone = request.form['phone']
        password = request.form['password']
        connection()
        cur.execute("INSERT INTO employee (emp_role,demp,emp_name,emp_address,emp_phone,emp_pass) VALUES (%s,%s,%s,%s,%s,%s)", (role,department,username,address,phone,password))
        con.commit()
        row = cur.fetchone()
        return render_template("index.html", row = row,)

@app.route("/admin_logout")
def admin_logout():
    if request.method== "GET":
        return redirect('/')

@app.route('/about', methods=['GET'])
def about():
    return render_template("about.html")

@app.route('/faq', methods=['GET'])
def faq():
    return render_template("faq.html")

@app.route('/blog', methods=['GET'])
def blog():
    return render_template("blog-details.html")

@app.route('/terms', methods=['GET'])
def terms():
    return render_template("terms.html")

@app.route('/contact', methods=['GET'])
def contact():
    return render_template("contact.html")

@app.route('/cars', methods=['GET', 'POST'])
def cars():
    return render_template("cars.html")

if __name__ == '__main__':
    app.run(debug=True)
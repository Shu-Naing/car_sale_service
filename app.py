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
        model = request.form['model']
        color = request.form['color']
        price = request.form['price']
        grade = request.form['grade']
        car_type = request.form['car_type']
        engine_power = request.form['engine_power']
        tax = request.form['tax']
        file = request.files['file']
        filename = file.filename
        fpath = str("static/img/car_photos/"+filename)
        file.save(fpath)
        connection()
        cur.execute("INSERT INTO car (model,color,price,grade,car_type,engine_power,tax_price,photo) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (model,color,price,grade,car_type,engine_power,tax,fpath))
        con.commit()
        row = cur.fetchone()
        return render_template("admin_insert.html", row = row,)

@app.route('/view_update', methods=['GET', 'POST'])
def view_update():
    if request.method=="GET":
        connection()
        cur.execute("SELECT model FROM car")
        rows = cur.fetchall()
        return render_template("update_start.html",rows = rows)
    else:
        model = request.form['model']
        connection()
        cur.execute("SELECT * FROM car WHERE model LIKE %s",[model])
        row = cur.fetchone()
        return render_template("update_ed.html", row = row)

@app.route("/admin_update",methods=["POST", "GET"])
def admin_update():
    if request.method == "POST":
        car_id = request.form['car_id']
        model = request.form['model']
        color = request.form['color']
        price = request.form['price']
        grade = request.form['grade']
        car_type = request.form['car_type']
        engine_power = request.form['engine_power']
        tax_price = request.form['tax_price']
        connection()
        cur.execute("update car set model = %s, color = %s, price = %s, grade = %s, car_type = %s, engine_power = %s, tax_price = %s where car_id = %s",(model,color,price,grade,car_type,engine_power,tax_price,car_id))
        con.commit()
        return redirect("/view_update")


@app.route('/admin_delete', methods=['GET', 'POST'])
def admin_delete():
    if request.method == "GET":
        connection()
        cur.execute("select model from car")
        row = cur.fetchall()
        return render_template("admin_delete.html", row = row)
    else:
        connection()
        model = request.form['model']
        cur.execute("delete from car where model=%s", [model])
        con.commit()
        return redirect("/admin_delete")



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

@app.route('/cars', methods=['GET', 'POST'])
def cars():
     if request.method=="GET":
        connection()
        cur.execute("SELECT * FROM car")
        row = cur.fetchall()
        return render_template("cars.html",row = row)

@app.route("/admin_logout")
def admin_logout():
    if request.method== "GET":
        return redirect('/')

@app.route("/update_list")
def update_list():
    if request.method== "GET":
        return render_template("update_select.html")

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

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, redirect, request
import mysql.connector as mysql

def connection():
    global con, cur
    con = mysql.connect(host = "localhost",
                        user = "root",
                        passwd = "rootpassword",
                        db = "cardb")
    cur = con.cursor()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST","GET"])
def login():
    # if request.method == "GET":
        return render_template("login.html")

@app.route("/signup", methods=["POST","GET"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        print("Hello")
        role = request.form['role']
        print("---------->",role)
        department = request.form['department']
        username = request.form['username']
        address = request.form['address']
        phone = request.form['phone']
        password = request.form['password']
        connection()
        cur.execute("INSERT INTO employee (role,department,username,address,phone,password) VALUES (%s,%s,%s,%s,%s,%s)", (role,department,username,address,phone,password))
        con.commit()
        row = cur.fetchone()
        return render_template("index", row = row,)

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
from flask import Flask, render_template
import mysql.connector as mysql

db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "rootpassword",
    db = "cardb"
)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

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
from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# MySQL connection
db = mysql.connector.connect(
    host="db",
    user="root",
    password="rootpassword",
    database="mydatabase"
)

cursor = db.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255)
)
""")

@app.route("/")
def index():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return render_template("index.html", users=users)

@app.route("/add", methods=["POST"])
def add_user():
    name = request.form["name"]
    email = request.form["email"]

    sql = "INSERT INTO users (name, email) VALUES (%s, %s)"
    val = (name, email)
    cursor.execute(sql, val)
    db.commit()

    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

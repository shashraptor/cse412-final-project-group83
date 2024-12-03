from flask import Flask, request, render_template
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(database="airline",
host="localhost",
user="postgres",
password="password",
port=5432)

cursor = conn.cursor()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password,))
        user = cursor.fetchone()
        if user:
            name = user[1]
            return render_template("home.html", name=name)
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
from flask import Flask, request, url_for, render_template, redirect, session
import psycopg2

app = Flask(__name__)

app.secret_key = "0fba08b30f04cf531dabf1a56f35aab98091bfd3930c757573dbc02c152f23d8"

conn = psycopg2.connect(database="airline",
host="localhost",
user="postgres",
password="Shash123@postgresql",
port=5433)

cursor = conn.cursor()

@app.route("/", methods=["GET", "POST"])
def index():
    msg = ""
    if "userid" in session:
        return redirect(url_for("home"))
    elif request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")
            cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password,))
            user = cursor.fetchone()
            if user:
                session["userid"] = user[0]
                session["name"] = user[1]
                return redirect(url_for("home"))
            else:
                msg = "Invalid login"
    return render_template("index.html", msg=msg)

@app.route("/home", methods=["GET", "POST"])
def home():
    if "userid" not in session:
        return redirect(url_for("index"))
    
    user_id = session["userid"]
    cursor.execute("SELECT * FROM booking WHERE userid = %s ORDER BY flightid", (user_id,))
    user_bookings = cursor.fetchall()

    return render_template("homeplaceholder.html", bookings=user_bookings) # TODO: change to home.html

@app.route("/booking", methods=["GET", "POST"])
def booking():
    if "userid" not in session:
        return redirect(url_for("index"))
    return render_template("bookingplaceholder.html") # TODO: change to booking.html

@app.route("/logout")
def logout():
    if "userid" not in session:
        return redirect(url_for("index"))
    session.pop("userid", None)
    session.pop("name", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run()
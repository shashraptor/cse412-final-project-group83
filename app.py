from flask import Flask, request, url_for, render_template, redirect, session, jsonify
from datetime import date
import psycopg2

app = Flask(__name__)

app.secret_key = "0fba08b30f04cf531dabf1a56f35aab98091bfd3930c757573dbc02c152f23d8"

conn = psycopg2.connect(database="airline",
host="localhost",
user="postgres",
password="Chaitu2003",
port=5432)

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
    
    user_id = session["userid"]
    cursor.execute("SELECT * FROM Flight")
    user_flights = cursor.fetchall()
    cursor.execute("SELECT * FROM Seat WHERE bookingID IS NULL;")
    user_seats = cursor.fetchall()

    return render_template("bookingpage.html", flights=user_flights, seats=user_seats)


@app.route("/get_seats/<int:flight_id>")
def get_seats(flight_id):
    cursor.execute("""
        SELECT seatNum, class 
        FROM Seat 
        WHERE flightID = %s AND bookingID IS NULL
    """, (flight_id,))
    available_seats = cursor.fetchall()
    
    seats = [{"seatNum": seat[0], "class": seat[1]} for seat in available_seats]
    
    return jsonify({"seats": seats})

@app.route("/book_flight", methods=["POST"])
def book_flight():
    if "userid" not in session:
        return jsonify({"status": "error", "message": "Please log in first"})
    
    try:
        # Get data from the request
        booking_data = request.get_json()
        
        # Add detailed logging for debugging
        print("Received booking data:", booking_data)
        
        flight_id = booking_data.get('flightId')
        seat_id = booking_data.get('seatId')
        payment_method = booking_data.get('paymentMethod')
        price = booking_data.get('price')
        user_id = session["userid"]

        # Validate input data
        if not all([flight_id, seat_id, payment_method, price, user_id]):
            print("Missing booking information")
            return jsonify({"status": "error", "message": "Missing booking information"})

        # Insert booking
        cursor.execute("""
            INSERT INTO Booking (userID, flightID, bookingDate, price, paymentMethod) 
            VALUES (%s, %s, %s, %s, %s) 
            RETURNING bookingID
        """, (user_id, flight_id, date.today(), price, payment_method))
        booking_id = cursor.fetchone()[0]

        # Update seat with booking ID
        cursor.execute("""
            UPDATE Seat 
            SET bookingID = %s 
            WHERE flightID = %s AND seatNum = %s
        """, (booking_id, flight_id, seat_id))

        # Commit the transaction
        conn.commit()

        return jsonify({"status": "success"})

    except Exception as e:
        # Rollback in case of error
        conn.rollback()
        print(f"Booking error: {e}")
        return jsonify({"status": "error", "message": str(e)})
    

@app.route("/logout")
def logout():
    if "userid" not in session:
        return redirect(url_for("index"))
    session.pop("userid", None)
    session.pop("name", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run()
import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///cinema.db")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        user = db.execute("SELECT is_admin FROM users WHERE id = ?", session["user_id"])
        if not user or user[0]["is_admin"] != 1:
            return render_template("apology.html", message="Access Denied: Admins only")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
@login_required
def index():
    screenings = db.execute("""
        SELECT screenings.id, movies.title, movies.description, screenings.screening_time, screenings.is_3d, screenings.price 
        FROM screenings 
        JOIN movies ON screenings.movie_id = movies.id
    """)
    user = db.execute("SELECT is_admin FROM users WHERE id = ?", session["user_id"])[0]
    return render_template("index.html", screenings=screenings, is_admin=user["is_admin"])

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if not username or not password:
            return render_template("apology.html", message="must provide username and password")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return render_template("apology.html", message="invalid username and/or password")

        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or password != confirmation:
            return render_template("apology.html", message="Invalid registration details")

        hash_pw = generate_password_hash(password)
        try:
            new_user_id = db.execute("INSERT INTO users (username, hash, is_admin) VALUES (?, ?, 0)", username, hash_pw)
        except:
            return render_template("apology.html", message="Username already exists")

        session["user_id"] = new_user_id
        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/book", methods=["POST"])
@login_required
def book():
    screening_id = request.form.get("screening_id")
    row_letter = request.form.get("row_letter")
    seat_number = request.form.get("seat_number")

    if not screening_id or not row_letter or not seat_number:
        return render_template("apology.html", message="Missing booking details")

    existing = db.execute("SELECT * FROM tickets WHERE screening_id = ? AND row_letter = ? AND seat_number = ?", screening_id, row_letter, seat_number)
    if len(existing) > 0:
        return render_template("apology.html", message="Seat already taken!")

    db.execute("INSERT INTO tickets (user_id, screening_id, row_letter, seat_number) VALUES (?, ?, ?, ?)",
               session["user_id"], screening_id, row_letter, seat_number)

    return redirect("/history")

@app.route("/history")
@login_required
def history():
    tickets = db.execute("""
        SELECT movies.title, screenings.screening_time, screenings.is_3d, screenings.price, tickets.row_letter, tickets.seat_number, tickets.purchase_date
        FROM tickets
        JOIN screenings ON tickets.screening_id = screenings.id
        JOIN movies ON screenings.movie_id = movies.id
        WHERE tickets.user_id = ?
    """, session["user_id"])
    return render_template("history.html", tickets=tickets)

@app.route("/admin/add_movie", methods=["GET", "POST"])
@admin_required
def add_movie():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        duration = request.form.get("duration")

        if not title or not duration:
            return render_template("apology.html", message="Missing movie details")

        db.execute("INSERT INTO movies (title, description, duration) VALUES (?, ?, ?)", title, description, duration)
        return redirect("/")
    return render_template("add_movie.html")

@app.route("/admin/add_screening", methods=["GET", "POST"])
@admin_required
def add_screening():
    if request.method == "POST":
        movie_id = request.form.get("movie_id")
        screening_time = request.form.get("screening_time")
        is_3d = 1 if request.form.get("is_3d") else 0
        price = request.form.get("price")

        if not movie_id or not screening_time or not price:
            return render_template("apology.html", message="Missing screening details")

        db.execute("INSERT INTO screenings (movie_id, screening_time, is_3d, price) VALUES (?, ?, ?, ?)",
                   movie_id, screening_time, is_3d, price)
        return redirect("/")
    
    movies = db.execute("SELECT * FROM movies")
    return render_template("add_screening.html", movies=movies)

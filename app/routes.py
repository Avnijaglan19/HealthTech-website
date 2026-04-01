"""
Main Backend for HealthTech! This file will initialize Flask
"""
from flask import render_template, request, redirect, url_for, session, flash
from app import app
from supabase_client import supabase


@app.route("/")
def first_page():
    return redirect(url_for("signup"))


# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        try:
            result = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            session["user_id"] = result.user.id
            session["email"] = result.user.email

            flash("Login successful!")
            return redirect(url_for("home"))

        except Exception:
            flash("Invalid email or password.")
            return redirect(url_for("login"))

    return render_template("login.html")


# SIGNUP
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        print(first_name, last_name, email, password)
        if password != confirm_password:
            return "Passwords do not match"

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (first_name, last_name, email, password)
            VALUES (?, ?, ?, ?)
        """, (first_name, last_name, email, password))

        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template("signup.html")


# HOME
@app.route("/home")
def home():
    return render_template("home.html")


# MANUAL PAGE
@app.route("/manual")
def manual():
    return render_template("manual.html")


# VIRTUAL 
@app.route("/virtual")
def virtual():
    return render_template("virtual.html")
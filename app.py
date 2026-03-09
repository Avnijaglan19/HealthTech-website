"""
Main Backend for HealthTech! This file will initialize Flask
"""
from flask import Flask, render_template
from __init__ import Workout # importing workout class

app = Flask(__name__)

# ------------------------------------------
# Route for home page
# Will render home.html when user visits "/"
# ------------------------------------------
@app.route("/")
def home():
    return render_template("home.html")

# ------------------------------------------
# Route for login
# Will render login.html when user visits "/login"
# ------------------------------------------ 
@app.route("/login")
def login():
    return render_template("login.html")

# ------------------------------------------
# Route for manual
# Will handle the "get" and "post"
# ------------------------------------------ 
@app.route("/manual", methods=["GET", "POST"])
def manual():
    return render_template("manual.html")

# ------------------------------------------
# Route for virtual
# Will render virtual.html
# ------------------------------------------
@app.route("/virtual")
def virtual():
    return render_template("virtual.html")

# runs Flask
if __name__ == "__main__":
    app.run(debug=True)
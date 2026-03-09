"""
Main Backend for HealthTech! This file will initialize Flask
"""
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")
@app.route("/login")
def login():
    return render_template("login.html")
@app.route("/manual")
def manual():
    return render_template("manual.html")
@app.route("/virtual")
def virtual():
    return render_template("virtual.html")

if __name__ == "__main__":
    app.run(debug=True)
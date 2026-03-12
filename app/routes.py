"""
Main Backend for HealthTech! This file will initialize Flask
"""
from flask import render_template, request, redirect, url_for
from app import app


# LOGIN PAGE
@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return redirect(url_for("home"))
    return render_template("login.html")


# HOME PAGE
@app.route("/home")
def home():
    return render_template("home.html")


# MANUAL PAGE
@app.route("/manual")
def manual():
    return render_template("manual.html")


# VIRTUAL PAGE
@app.route("/virtual")
def virtual():
    return render_template("virtual.html")
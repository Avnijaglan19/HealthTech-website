"""
Main Backend for HealthTech! This file will initialize Flask
"""
import re

from flask import render_template, request, redirect, url_for, session, flash
from app import app
from app.forms import LoginForm, WorkoutForm
from app.workout import Workout
from app.openaiapi import generateWorkoutPlan
from supabase_client import supabase


YOUTUBE_URL_RE = re.compile(
    r"(?:https?://)?(?:www\.)?(?:youtube\.com/(?:watch\?v=|embed/|shorts/)|youtu\.be/)([A-Za-z0-9_-]{11})",
    re.IGNORECASE,
)


def extract_youtube_embed_urls(text):
    embed_urls = []
    seen = set()

    for video_id in YOUTUBE_URL_RE.findall(text or ""):
        embed_url = f"https://www.youtube.com/embed/{video_id}"
        if embed_url not in seen:
            seen.add(embed_url)
            embed_urls.append(embed_url)

    return embed_urls


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
            print(f"Attempting login with email: {email}")
            result = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            print(f"Login successful. User ID: {result.user.id}")
            session["user_id"] = result.user.id
            session["email"] = result.user.email

            flash("Login successful!")
            return redirect(url_for("home"))

        except Exception as e:
            print(f"Login error: {str(e)}")
            print(f"Error type: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            flash(f"Login failed: {str(e)}")
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

        if password != confirm_password:
            flash("Passwords do not match.")
            return redirect(url_for('signup'))

        try:
            supabase.auth.sign_up({
                "email": email,
                "password": password
            })

            flash("Signup successful! Please log in.")
            return redirect(url_for('login'))

        except Exception:
            flash("Unable to create account. Please check your details and try again.")
            return redirect(url_for('signup'))

    return render_template("signup.html")


# HOME
@app.route("/home")
def home():
    return render_template("home.html")


# MANUAL PAGE
@app.route("/manual", methods=["GET", "POST"])
def manual():
    wform = WorkoutForm()
    if wform.validate_on_submit():
        # Create Workout object with form data
        workout = Workout(
            wform.difficulty.data,
            wform.duration.data,
            wform.goal.data,
            wform.equip.data,
            wform.muscle_group.data,
        )
        
        # Generate the prompt
        workout.PromptGenerator()
        
        # Store workout object in session
        session["workout"] = {
            "difficulty": workout.get__diff(),
            "duration": workout.get__duration(),
            "goal": workout.get__goal(),
            "equipment": workout.get__equipment(),
            "muscle_group": workout.get__mGroup(),
            "prompt": workout.get__prompt()
        }

        return redirect(url_for("results"))


    return render_template("manual.html", title="Workout Generator", form=wform)


# VIRTUAL 
@app.route("/virtual")
def virtual():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("virtual.html")

@app.route("/results")
def results():
    if "user_id" not in session:
        return redirect(url_for("login"))

    workout_data = session.get("workout", None)
    if workout_data is None:
        flash("No workout data found. Please submit the form first.")
        return redirect(url_for("manual"))

    prompt = workout_data.get("prompt", "")
    if not prompt:
        flash("Workout prompt is missing. Please submit the form again.")
        return redirect(url_for("manual"))

    try:
        generated_plan = generateWorkoutPlan(prompt)
    except Exception:
        flash("Unable to generate workout plan right now. Please try again.")
        return redirect(url_for("manual"))

    youtube_embeds = extract_youtube_embed_urls(generated_plan)

    return render_template(
        "results.html",
        workout=workout_data,
        generated_plan=generated_plan,
        youtube_embeds=youtube_embeds,
    )

@app.route ("/forgot-password")
def forgot_password():
    return render_template("forgot_password.html")
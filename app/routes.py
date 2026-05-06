"""
Main Backend for HealthTech! This file will initialize Flask
"""
import re, os, cv2, tempfile, base64, time

from flask import render_template, request, redirect, url_for, session, flash, jsonify, send_from_directory
from . import app, openaiAPI, camera, workout
from app.forms import LoginForm, WorkoutForm
from supabase_client import supabase
from datetime import date
from collections import Counter
from app.workout import Workout
from .openaiapi import generateWorkoutPlan



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

# ROOT
@app.route("/")
def first_page():
    print("DEBUG: Root route (/) called")
    print(f"DEBUG: Session content: {session}")
    print("DEBUG: About to render onboarding.html")
    return render_template("onboarding.html")


# ONBOARDING
@app.route("/onboarding")
def onboarding():
    return render_template("onboarding.html")


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
            }) #type: ignore

            print(f"Login successful. User ID: {result.user.id}") #type: ignore
            session["user_id"] = result.user.id #type: ignore
            session["email"] = result.user.email #type: ignore

            flash("Login successful!")
            return redirect(url_for("dashboard"))

        except Exception as e:
            print(f"Login error: {str(e)}")
            print(f"Error type: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            flash(f"Login failed: {str(e)}")
            return redirect(url_for("login"))

    return render_template("login.html")

# DASHBOARD
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    response = supabase.table("workout_logs") \
        .select("*") \
        .eq("user_id", user_id) \
        .execute()

    workouts = response.data or []

    total_workouts = len(workouts)
    total_duration = sum([w["duration_minutes"] for w in workouts]) if workouts else 0  #type: ignore
    weekly_goal = min(total_workouts * 20, 100)

    latest_workout = workouts[-1] if workouts else None

    return render_template(
        "dashboard.html",
        total_workouts=total_workouts,
        total_duration=total_duration,
        weekly_goal=weekly_goal,
        latest_workout=latest_workout
    )

# GUIDE
@app.route("/guide")
def guide():
    return render_template("guide.html")

# PROGRESS
@app.route("/progress")
def progress():
    if "user_id" not in session:
        return redirect(url_for("login"))

    try:
        from datetime import datetime, date
        
        user_id = session["user_id"]

        response = supabase.table("workout_logs") \
            .select("*") \
            .eq("user_id", user_id) \
            .order("workout_date", desc=True) \
            .execute()

        workouts = response.data or []

        total_workouts = len(workouts)

        total_duration = sum(
            int(w.get("duration_minutes") or 0) for w in workouts #type: ignore
        )

        longest_workout = max(
            [int(w.get("duration_minutes") or 0) for w in workouts], #type: ignore
            default=0
        ) 

        workout_types = [
            w.get("workout_type", "Other") for w in workouts #type: ignore
        ]

        type_counts = Counter(workout_types)

        pie_labels = list(type_counts.keys())
        pie_values = list(type_counts.values())

        # Get current month and year for calendar
        today = date.today()
        current_month = today.month
        current_year = today.year
        
        # Get what day of week the 1st of the month is (0=Monday, 6=Sunday)
        first_day = date(current_year, current_month, 1)
        first_weekday = first_day.weekday()  # 0=Monday, 6=Sunday
        
        # Get number of days in current month
        if current_month == 12:
            next_month = date(current_year + 1, 1, 1)
        else:
            next_month = date(current_year, current_month + 1, 1)
        last_day = next_month - __import__('datetime').timedelta(days=1)
        days_in_month = last_day.day
        
        # Extract and format workout dates (YYYY-MM-DD format)
        workout_dates = set()
        for w in workouts:
            date_value = w.get("workout_date") #type: ignore
            if date_value:
                # Handle both string and date formats
                if isinstance(date_value, str):
                    workout_dates.add(date_value[:10])  # Get YYYY-MM-DD part
                else:
                    workout_dates.add(str(date_value))

        recent_workouts = workouts[:5]

        return render_template(
            "progress.html",
            workouts=workouts,
            total_workouts=total_workouts,
            total_duration=total_duration,
            longest_workout=longest_workout,
            pie_labels=pie_labels,
            pie_values=pie_values,
            workout_dates=list(workout_dates),
            recent_workouts=recent_workouts,
            current_month=current_month,
            current_year=current_year,
            first_weekday=first_weekday,
            days_in_month=days_in_month
        )
    except Exception as e:
        print(f"Progress route error: {str(e)}")
        import traceback
        traceback.print_exc()
        flash(f"Error loading progress: {str(e)}")
        return redirect(url_for("dashboard"))
# SIGNUP
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if len(password) < 6: #type: ignore
            flash("Password must be at least 6 characters long.")
            return redirect(url_for("signup"))

        if password != confirm_password:
            flash("Passwords do not match.")
            return redirect(url_for('signup'))

        try:
            response = supabase.auth.sign_up({
                "email": email,
                "password": password
            }) #type: ignore

            print("SIGNUP RESPONSE:", response)

            if response.user is None:
                flash("Signup failed. Email may already be in use or is invalid.")
                return redirect(url_for('signup'))
            
            flash("Signup successful! Please log in.")
            return redirect(url_for('login'))
        except Exception as e:
            print("SIGNUP ERROR:", e)
            flash("Error creating account. Please check your details and try again.")
            return redirect(url_for('login'))
    return render_template('signup.html')

        
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
        workout_obj = Workout(
            wform.difficulty.data,
            wform.duration.data,
            wform.goal.data,
            wform.equip.data,
            wform.muscle_group.data,
        )
        
        # Generate the prompt
        workout_obj.PromptGenerator()
        
        # Store workout object in session
        session["workout"] = {
            "difficulty": workout_obj.get__diff(),
            "duration": workout_obj.get__duration(),
            "goal": workout_obj.get__goal(),
            "equipment": workout_obj.get__equipment(),
            "muscle_group": workout_obj.get__mGroup(),
            "prompt": workout_obj.get__prompt()
        }
        supabase.table("workout_logs").insert({
            "user_id": session["user_id"],
            "workout_type": workout_obj.get__goal(),
            "duration_minutes": int(''.join(filter(str.isdigit, workout_obj.get__duration()))),
            "equipment": workout_obj.get__equipment(),
            "goal": workout_obj.get__goal(),
            "notes": workout_obj.get__mGroup(),
            "workout_date": str(date.today())
        }).execute()


        return redirect(url_for("results"))


    return render_template("manual.html", title="Workout Generator", form=wform)


# VIRTUAL 
@app.route("/virtual", methods=["GET", "POST"])
def virtual():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    wform = WorkoutForm()

    if wform.validate_on_submit():

        image_path = camera.capture_image()

        if image_path:
            detected_equipment = openaiAPI.generateEquipment(image_path)
            session['detected_equipment'] = detected_equipment
            
            if detected_equipment:
                if wform.equip.data is None:
                    wform.equip.data = []
                    wform.equip.data.append(detected_equipment)
        else:
            detected_equipment = None
            flash('No image was captured, so equipment could not be detected.')
        

        # Create Workout object with form data with equipment parameter in correct position
        workout = Workout(
            wform.difficulty.data,      # diff
            wform.duration.data,        # duration
            wform.goal.data,            # goal
#            wform.equip.data,   # equipment (4th parameter)
            detected_equipment,  # equipment (4th parameter)
            wform.muscle_group.data,    # muscleGroup (5th parameter)
        ) # type: ignore

        #workout.extend__equipment(detected_equipment)
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
        
        return redirect(url_for('results'))
    
    return render_template("virtual.html", title="Image Recognition", form=wform)


@app.route('/capture', methods=['POST'])
def capture():
    try:
        payload = request.get_json(silent=True) or {}
        image_data = payload.get('image')

        if not image_data:
            return jsonify({"ok": False, "error": "No image data received"}), 400

        # data URL -> raw base64
        if ',' in image_data:
            image_data = image_data.split(',', 1)[1]

        binary = base64.b64decode(image_data)

        repo_root = os.path.dirname(app.root_path)
        tmp_dir = os.path.join(repo_root, 'tmp')
        os.makedirs(tmp_dir, exist_ok=True)

        # Always overwrite the previous capture so only the latest PNG is kept.
        filename = "capture.png"
        path = os.path.join(tmp_dir, filename)
        with open(path, 'wb') as f:
            f.write(binary)

        image_url = url_for('tmp_file', filename=filename)
        session['captured_image_path'] = path
        session['captured_image'] = image_url
        return jsonify({"ok": True, "image_url": image_url})
    except Exception as e:
        return jsonify({"ok": False, "error": f"Camera error: {e}"}), 500


@app.route('/tmp/<path:filename>')
def tmp_file(filename):
    repo_root = os.path.dirname(app.root_path)
    tmp_dir = os.path.join(repo_root, 'tmp')
    return send_from_directory(tmp_dir, filename)


# RESULTS
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
        captured_image=session.get('captured_image', None),
        detected_equipment=session.get('detected_equipment', "No equipment detected")
    )


# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("login"))
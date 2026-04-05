# =====================================================
#  routes.py  –  All URL Endpoints (Pages & API)
# =====================================================

from flask import (Blueprint, render_template, request,
                   redirect, url_for, session, flash, jsonify, current_app)
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from models import User, WorkoutLog, ExerciseProgress
from workout_engine import generate_workout_plan, format_plan_as_text, GOAL_LABELS
import datetime

bp = Blueprint("main", __name__)


# ─────────────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────────────
def current_user():
    uid = session.get("user_id")
    if uid:
        return User.query.get(uid)
    return None


def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in to access that page.", "warning")
            return redirect(url_for("main.login"))
        return f(*args, **kwargs)
    return decorated


def _get_or_create_today_log(user, plan):
    """
    Find an existing WorkoutLog for today, or create a fresh one.
    Also seeds ExerciseProgress rows if they don't exist yet.
    Returns the WorkoutLog instance (or None if user has no profile).
    """
    if not plan:
        return None

    today = datetime.date.today()

    log = (WorkoutLog.query
           .filter_by(user_id=user.id)
           .filter(WorkoutLog.log_date == today)
           .first())

    if not log:
        day_name = datetime.datetime.now().strftime("%A")
        log = WorkoutLog(
            user_id    = user.id,
            day_name   = day_name,
            plan_text  = format_plan_as_text(plan, user.name, day_name),
            email_sent = False,
            log_date   = today,
        )
        db.session.add(log)
        db.session.flush()   # get log.id without committing yet

        # Seed one ExerciseProgress row per exercise (all uncompleted)
        for ex in plan["exercises"]:
            prog = ExerciseProgress(log_id=log.id, exercise_name=ex["name"])
            db.session.add(prog)

        db.session.commit()

    else:
        # Log exists – make sure all exercises from today's plan have rows
        # (handles the case where the plan changed or exercises were added)
        existing_names = {p.exercise_name for p in log.exercises}
        added = False
        for ex in plan["exercises"]:
            if ex["name"] not in existing_names:
                db.session.add(ExerciseProgress(log_id=log.id, exercise_name=ex["name"]))
                added = True
        if added:
            db.session.commit()

    return log


def _recalculate_completion(log):
    """Recompute completion_pct from exercise rows and save."""
    total = len(log.exercises)
    if total == 0:
        log.completion_pct = 0
    else:
        done = sum(1 for e in log.exercises if e.completed)
        log.completion_pct = round((done / total) * 100)
    db.session.commit()


# ─────────────────────────────────────────────────────
#  Home  /
# ─────────────────────────────────────────────────────
@bp.route("/")
def index():
    return render_template("index.html", user=current_user())


# ─────────────────────────────────────────────────────
#  Register  /register
# ─────────────────────────────────────────────────────
@bp.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        name     = request.form.get("name", "").strip()
        email    = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or not password:
            flash("All fields are required.", "danger")
            return render_template("register.html")
        if len(password) < 6:
            flash("Password must be at least 6 characters.", "danger")
            return render_template("register.html")
        if User.query.filter_by(email=email).first():
            flash("An account with that email already exists.", "danger")
            return render_template("register.html")

        user = User(
            name=name, email=email,
            password_hash=generate_password_hash(password),
        )
        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id
        flash(f"Welcome, {name}! Please complete your fitness profile.", "success")
        return redirect(url_for("main.profile"))

    return render_template("register.html")


# ─────────────────────────────────────────────────────
#  Login  /login
# ─────────────────────────────────────────────────────
@bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        email    = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            flash(f"Welcome back, {user.name}!", "success")
            return redirect(url_for("main.dashboard"))
        flash("Invalid email or password.", "danger")

    return render_template("login.html")


# ─────────────────────────────────────────────────────
#  Logout  /logout
# ─────────────────────────────────────────────────────
@bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.index"))


# ─────────────────────────────────────────────────────
#  Profile  /profile
# ─────────────────────────────────────────────────────
@bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user = current_user()

    if request.method == "POST":
        user.fitness_goal     = request.form.get("fitness_goal")
        user.experience_level = request.form.get("experience_level")
        user.days_per_week    = int(request.form.get("days_per_week", 3))
        user.age              = int(request.form.get("age") or 0) or None
        user.weight_kg        = float(request.form.get("weight_kg") or 0) or None
        user.height_cm        = float(request.form.get("height_cm") or 0) or None
        user.email_time       = request.form.get("email_time", "07:00")
        db.session.commit()
        flash("Profile updated! Your daily emails are scheduled.", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("profile.html", user=user)


# ─────────────────────────────────────────────────────
#  Dashboard  /dashboard
# ─────────────────────────────────────────────────────
@bp.route("/dashboard")
@login_required
def dashboard():
    user = current_user()

    from scheduler import _get_day_index
    day_index = _get_day_index(user)
    plan = generate_workout_plan(user, day_index)

    today_log = _get_or_create_today_log(user, plan)

    # ✅ INSIDE FUNCTION
    progress_map = {}
    if today_log and today_log.exercises:
        for p in today_log.exercises:
            progress_map[p.exercise_name] = p

    logs = (WorkoutLog.query
        .filter_by(user_id=user.id)
        .order_by(WorkoutLog.sent_at.desc())
        .limit(10).all()
    )

    today_str = datetime.datetime.now().strftime("%A, %d %B %Y")

    return render_template(
        "dashboard.html",
        user=user,
        plan=plan,
        logs=logs,
        today=today_str,
        day_index=day_index,
        today_log=today_log,
        progress_map=progress_map
    )
# ─────────────────────────────────────────────────────
#  API – Toggle a single exercise  /api/toggle-exercise
# ─────────────────────────────────────────────────────
@bp.route("/api/toggle-exercise", methods=["POST"])
@login_required
def api_toggle_exercise():
    """
    Body JSON: { "log_id": int, "exercise_name": str }
    Toggles the completed flag and returns updated progress stats.
    """
    data          = request.get_json()
    log_id        = data.get("log_id")
    exercise_name = data.get("exercise_name", "").strip()

    if not log_id or not exercise_name:
        return jsonify({"success": False, "error": "Missing fields"}), 400

    # Security: make sure the log belongs to the logged-in user
    log = WorkoutLog.query.get(log_id)
    if not log or log.user_id != session["user_id"]:
        return jsonify({"success": False, "error": "Not found"}), 404

    # Find or create the progress row
    prog = ExerciseProgress.query.filter_by(
        log_id=log_id, exercise_name=exercise_name
    ).first()

    if not prog:
        prog = ExerciseProgress(log_id=log_id, exercise_name=exercise_name)
        db.session.add(prog)

    # Toggle
    prog.completed   = not prog.completed
    prog.completed_at = datetime.datetime.utcnow() if prog.completed else None
    db.session.commit()

    # Recalculate overall completion %
    _recalculate_completion(log)

    # Count for response
    total     = len(log.exercises)
    done      = sum(1 for e in log.exercises if e.completed)
    pct       = log.completion_pct

    return jsonify({
        "success":   True,
        "completed": prog.completed,
        "done":      done,
        "total":     total,
        "pct":       pct,
    })


# ─────────────────────────────────────────────────────
#  API – Send workout email right now  /api/send-now
# ─────────────────────────────────────────────────────
@bp.route("/api/send-now", methods=["POST"])
@login_required
def api_send_now():
    from scheduler import send_now
    user    = current_user()
    ok, msg = send_now(current_app._get_current_object(), user.id)
    return jsonify({"success": ok, "message": msg})


# ─────────────────────────────────────────────────────
#  API – Preview plan as JSON  /api/preview-plan
# ─────────────────────────────────────────────────────
@bp.route("/api/preview-plan")
@login_required
def api_preview_plan():
    user = current_user()
    if not user.fitness_goal:
        return jsonify({"error": "Profile not set up yet"}), 400
    from scheduler import _get_day_index
    day_index = _get_day_index(user)
    plan      = generate_workout_plan(user, day_index)
    return jsonify(plan)


# ─────────────────────────────────────────────────────
#  History  /history
# ─────────────────────────────────────────────────────
@bp.route("/history")
@login_required
def history():
    user = current_user()
    logs = (WorkoutLog.query
            .filter_by(user_id=user.id)
            .order_by(WorkoutLog.sent_at.desc())
            .all())
    return render_template("history.html", user=user, logs=logs)

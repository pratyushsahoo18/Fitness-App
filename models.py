# =====================================================
#  models.py  –  Database Tables
# =====================================================
from datetime import datetime
import datetime as dt
from extensions import db


# ─────────────────────────────────────────────────────
#  Table 1 – Users
# ─────────────────────────────────────────────────────
class User(db.Model):
    __tablename__ = "users"

    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(100), nullable=False)
    email         = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    # Fitness profile
    fitness_goal     = db.Column(db.String(50))
    experience_level = db.Column(db.String(50))
    days_per_week    = db.Column(db.Integer)
    age              = db.Column(db.Integer)
    weight_kg        = db.Column(db.Float)
    height_cm        = db.Column(db.Float)

    email_time = db.Column(db.String(5), default="07:00")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    logs = db.relationship("WorkoutLog", backref="user", lazy=True)

    def __repr__(self):
        return f"<User {self.email}>"


# ─────────────────────────────────────────────────────
#  Table 2 – Workout Logs
# ─────────────────────────────────────────────────────
class WorkoutLog(db.Model):
    __tablename__ = "workout_logs"

    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    day_name   = db.Column(db.String(20))
    plan_text  = db.Column(db.Text)

    sent_at    = db.Column(db.DateTime, default=datetime.utcnow)
    email_sent = db.Column(db.Boolean, default=False)

    # ── NEW: progress tracking ──────────────────────
    # Stores the calendar date (no time) for easy "today" lookups
    log_date       = db.Column(db.Date, default=dt.date.today)
    # 0–100 integer, recalculated whenever an exercise is toggled
    completion_pct = db.Column(db.Integer, default=0)

    # One log → many exercise progress rows
    exercises = db.relationship(
        "ExerciseProgress", backref="log",
        lazy=True, cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<WorkoutLog user={self.user_id} day={self.day_name}>"


# ─────────────────────────────────────────────────────
#  Table 3 – Exercise Progress  (NEW)
# ─────────────────────────────────────────────────────
class ExerciseProgress(db.Model):
    """
    One row per exercise per workout day.
    Tracks whether the user completed that exercise.
    """
    __tablename__ = "exercise_progress"

    id            = db.Column(db.Integer, primary_key=True)
    log_id        = db.Column(
        db.Integer, db.ForeignKey("workout_logs.id"), nullable=False
    )
    exercise_name = db.Column(db.String(150), nullable=False)
    completed     = db.Column(db.Boolean, default=False)
    completed_at  = db.Column(db.DateTime, nullable=True)  # timestamp of toggle

    def __repr__(self):
        status = "done" if self.completed else "todo"
        return f"<ExerciseProgress log={self.log_id} ex={self.exercise_name} {status}>"

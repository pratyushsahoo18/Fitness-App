# =====================================================
#  email_sender.py  –  Send Workout Emails
# =====================================================
# This file contains one main function: send_workout_email()
# It takes a user and their workout plan, then emails it.

from flask_mail import Message
from extensions import mail
from workout_engine import format_plan_as_text
import datetime


def send_workout_email(app, user, plan: dict, day_index: int):
    """
    Send a workout plan email to a single user.

    Parameters
    ----------
    app       : the Flask app instance (needed for app context)
    user      : User model instance
    plan      : dict returned by generate_workout_plan()
    day_index : used to track which workout day this is
    """
    # We need to work inside Flask's "application context"
    # because Flask-Mail requires it.
    with app.app_context():
        from models import WorkoutLog
        from extensions import db

        day_name = datetime.datetime.now().strftime("%A")   # e.g. "Monday"

        # Build the plain-text body of the email
        body_text = format_plan_as_text(plan, user.name, day_name)

        # Build the HTML body (nicer version for email clients)
        body_html = _build_html_email(plan, user.name, day_name)

        # Create the email message
        msg = Message(
            subject=f"💪 Your {day_name} Workout Plan – Fitness App",
            recipients=[user.email],
            body=body_text,          # plain-text fallback
            html=body_html,          # HTML for modern email clients
        )

        try:
            mail.send(msg)
            sent = True
            print(f"[EMAIL] Sent to {user.email} for {day_name}")
        except Exception as e:
            sent = False
            print(f"[EMAIL] Failed to send to {user.email}: {e}")

        # Save a record in workout_logs table
        log = WorkoutLog(
            user_id   = user.id,
            day_name  = day_name,
            plan_text = body_text,
            email_sent= sent,
        )
        db.session.add(log)
        db.session.commit()


def _build_html_email(plan: dict, name: str, day_name: str) -> str:
    """Build a nice HTML email body."""

    rows = ""
    for ex in plan["exercises"]:
        sets     = str(ex["sets"])  if ex["sets"]     else "—"
        reps     = str(ex["reps"])  if ex["reps"]     else "—"
        duration = ex["duration"]   if ex["duration"] else "—"
        rest     = ex["rest"]       if ex["rest"]     else "—"
        rows += f"""
        <tr>
            <td style="padding:10px 12px; border-bottom:1px solid #2d2d44;">{ex['name']}</td>
            <td style="padding:10px 12px; border-bottom:1px solid #2d2d44; text-align:center;">{sets}</td>
            <td style="padding:10px 12px; border-bottom:1px solid #2d2d44; text-align:center;">{reps}</td>
            <td style="padding:10px 12px; border-bottom:1px solid #2d2d44; text-align:center;">{duration}</td>
            <td style="padding:10px 12px; border-bottom:1px solid #2d2d44; text-align:center;">{rest}</td>
        </tr>"""

    return f"""
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="margin:0; padding:0; background:#0f0f1a; font-family:'Segoe UI',Arial,sans-serif;">

  <div style="max-width:600px; margin:40px auto; background:#1a1a2e; border-radius:16px; overflow:hidden; box-shadow:0 8px 32px rgba(0,0,0,0.5);">

    <!-- Header -->
    <div style="background:linear-gradient(135deg,#6c63ff,#e040fb); padding:36px 32px; text-align:center;">
      <h1 style="color:#fff; margin:0; font-size:28px; letter-spacing:1px;">🏋️ Fitness App</h1>
      <p style="color:rgba(255,255,255,0.85); margin:8px 0 0; font-size:15px;">Your Daily Workout Planner</p>
    </div>

    <!-- Greeting -->
    <div style="padding:28px 32px 16px;">
      <h2 style="color:#e0e0ff; margin:0 0 6px; font-size:22px;">Good morning, {name}! 💪</h2>
      <p style="color:#9090b0; margin:0;">Here is your personalised workout for <strong style="color:#c77dff;">{day_name}</strong>.</p>
    </div>

    <!-- Badges -->
    <div style="padding:0 32px 20px; display:flex; gap:10px; flex-wrap:wrap;">
      <span style="background:#6c63ff22; color:#a78bfa; padding:6px 14px; border-radius:999px; font-size:13px; font-weight:600; border:1px solid #6c63ff55;">🎯 {plan['goal_label']}</span>
      <span style="background:#e040fb22; color:#f0abfc; padding:6px 14px; border-radius:999px; font-size:13px; font-weight:600; border:1px solid #e040fb55;">🔥 {plan['day_type']}</span>
      <span style="background:#06b6d422; color:#67e8f9; padding:6px 14px; border-radius:999px; font-size:13px; font-weight:600; border:1px solid #06b6d455;">⭐ {plan['experience']}</span>
    </div>

    <!-- Exercise Table -->
    <div style="padding:0 32px 24px;">
      <table style="width:100%; border-collapse:collapse; background:#12122a; border-radius:12px; overflow:hidden;">
        <thead>
          <tr style="background:#6c63ff30;">
            <th style="padding:12px; text-align:left; color:#a78bfa; font-size:13px; text-transform:uppercase; letter-spacing:.5px;">Exercise</th>
            <th style="padding:12px; text-align:center; color:#a78bfa; font-size:13px; text-transform:uppercase;">Sets</th>
            <th style="padding:12px; text-align:center; color:#a78bfa; font-size:13px; text-transform:uppercase;">Reps</th>
            <th style="padding:12px; text-align:center; color:#a78bfa; font-size:13px; text-transform:uppercase;">Duration</th>
            <th style="padding:12px; text-align:center; color:#a78bfa; font-size:13px; text-transform:uppercase;">Rest</th>
          </tr>
        </thead>
        <tbody style="color:#d0d0e8;">
          {rows}
        </tbody>
      </table>
    </div>

    <!-- Tip -->
    <div style="margin:0 32px 28px; background:#6c63ff18; border-left:4px solid #6c63ff; border-radius:8px; padding:14px 18px;">
      <p style="margin:0; color:#c4b5fd; font-size:15px;"><strong>Tip of the day:</strong> {plan['tip']}</p>
    </div>

    <!-- Footer -->
    <div style="background:#12122a; padding:20px 32px; text-align:center;">
      <p style="color:#555570; font-size:13px; margin:0;">Stay consistent and keep pushing! 🚀</p>
      <p style="color:#444460; font-size:12px; margin:6px 0 0;">– Your Fitness App</p>
    </div>

  </div>
</body>
</html>"""

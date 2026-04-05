# =====================================================
#  scheduler.py  –  Automated Daily Email Scheduler
# =====================================================
# APScheduler checks every minute whether any user's
# preferred email time has arrived, then sends their
# daily workout plan automatically.

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import datetime

# We store the scheduler as a module-level singleton
_scheduler = None


def start_scheduler(app):
    """
    Start the background scheduler.
    Call this once when the Flask app boots up.
    """
    global _scheduler

    if _scheduler and _scheduler.running:
        return  # already running – don't start twice

    _scheduler = BackgroundScheduler(timezone="UTC")

    # Run the check_and_send_emails job every minute
    _scheduler.add_job(
        func      = check_and_send_emails,
        trigger   = CronTrigger(minute="*"),  # fires at :00 of every minute
        args      = [app],
        id        = "daily_workout_emailer",
        replace_existing = True,
    )

    _scheduler.start()
    print("[SCHEDULER] Background scheduler started.")


def stop_scheduler():
    """Gracefully stop the scheduler (called on app shutdown)."""
    global _scheduler
    if _scheduler and _scheduler.running:
        _scheduler.shutdown(wait=False)
        print("[SCHEDULER] Stopped.")


def check_and_send_emails(app):
    """
    This function runs every minute.
    It looks at each user's preferred email_time and, if it
    matches the current UTC time (HH:MM), sends the workout.

    NOTE: For simplicity we use UTC. In a real app you would
    store the user's timezone and convert accordingly.
    """
    now_hhmm = datetime.datetime.utcnow().strftime("%H:%M")
    print(f"[SCHEDULER] Tick at {now_hhmm} UTC")

    # Run inside the Flask app context so we can access DB + email
    with app.app_context():
        from models import User, WorkoutLog
        from extensions import db
        from workout_engine import generate_workout_plan
        from email_sender import send_workout_email

        users = User.query.all()

        for user in users:
            # Only send if the user has set up their profile
            if not user.fitness_goal or not user.email_time:
                continue

            # Check if it's this user's send time
            if user.email_time != now_hhmm:
                continue

            # Work out which day index we're on for this user
            day_index = _get_day_index(user)

            # Generate the plan
            plan = generate_workout_plan(user, day_index)

            # Send it
            send_workout_email(app, user, plan, day_index)


def _get_day_index(user) -> int:
    """
    Determine which day of the user's rotation to use.

    Logic: count how many workout logs already exist for this
    user and use that as the rotation index.
    """
    from models import WorkoutLog
    count = WorkoutLog.query.filter_by(user_id=user.id).count()
    return count % (user.days_per_week or 7)


def send_now(app, user_id: int):
    """
    Manually trigger an immediate email for a specific user.
    Called from the dashboard "Send Now" button.
    """
    with app.app_context():
        from models import User
        from workout_engine import generate_workout_plan
        from email_sender import send_workout_email

        user = User.query.get(user_id)
        if not user:
            return False, "User not found"

        day_index = _get_day_index(user)
        plan      = generate_workout_plan(user, day_index)
        send_workout_email(app, user, plan, day_index)
        return True, "Email sent successfully!"

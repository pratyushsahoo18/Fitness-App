# =====================================================
#  app.py  –  Main Flask Application Entry Point
# =====================================================
# This is the file you run to start the whole app.
# It ties together: config, database, email, routes,
# and the background scheduler.

from flask import Flask
from config import Config
from extensions import db, mail
from routes import bp
import atexit


def create_app():
    """
    Application Factory Pattern.
    Creates and fully configures the Flask app.
    Returns the ready-to-use app object.
    """
    app = Flask(__name__)

    # 1️⃣  Load settings from config.py
    app.config.from_object(Config)

    # 2️⃣  Connect extensions to this app
    db.init_app(app)       # database
    mail.init_app(app)     # email

    # 3️⃣  Register our routes (Blueprint)
    app.register_blueprint(bp)

    # 4️⃣  Create all database tables (if they don't exist yet)
    with app.app_context():
        db.create_all()
        print("[DB] Database tables ready.")

    # 5️⃣  Start the background email scheduler
    from scheduler import start_scheduler, stop_scheduler
    start_scheduler(app)

    # Make sure the scheduler stops cleanly when the app exits
    atexit.register(stop_scheduler)

    return app


# ─────────────────────────────────────────────────────
#  Run the app
# ─────────────────────────────────────────────────────
if __name__ == "__main__":
    app = create_app()
    print("\nFitness App is running!")
    print("   Open your browser -> http://127.0.0.1:5000\n")
    # debug=True gives helpful error pages and auto-reloads on code changes
    # use_reloader=False prevents the scheduler from starting twice
    app.run(debug=True, use_reloader=False, port=5000)

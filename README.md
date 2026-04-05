# FitPlanner – Automated Workout Planner 🏋️

A beginner-friendly **Flask** web app that generates personalised daily workout
plans and emails them to users automatically every day.

---

## Project Folder Structure

```
fitness_app/
│
├── app.py               # Entry point – run this to start the app
├── config.py            # Settings loaded from .env
├── extensions.py        # Shared Flask extensions (db, mail)
├── models.py            # Database tables (User, WorkoutLog)
├── routes.py            # All URL pages & API endpoints
├── workout_engine.py    # Workout plan generator (exercise library)
├── email_sender.py      # Sends HTML/text emails via Flask-Mail
├── scheduler.py         # APScheduler – fires emails daily automatically
│
├── requirements.txt     # Python package list
├── .env                 # Your secret config (never commit this!)
│
├── templates/           # HTML pages (Jinja2 templates)
│   ├── base.html        # Shared navbar/footer layout
│   ├── index.html       # Homepage / landing page
│   ├── register.html    # Sign-up page
│   ├── login.html       # Login page
│   ├── profile.html     # Fitness profile setup
│   ├── dashboard.html   # Today's workout + stats
│   └── history.html     # Past workout logs
│
├── static/
│   ├── css/style.css    # Full dark-mode design system
│   └── js/main.js       # Frontend JavaScript helpers
│
└── instance/
    └── fitness.db       # SQLite database (auto-created on first run)
```

---

## Step-by-Step Setup (Beginner Friendly)

### Step 1 – Install Python
Download Python 3.10+ from https://python.org and install it.
During install, **tick "Add Python to PATH"**.

### Step 2 – Open a terminal in the project folder
```
cd d:\Coding\fitness_app
```

### Step 3 – Create a virtual environment
```
python -m venv venv
```
This creates an isolated Python sandbox so packages don't conflict.

### Step 4 – Activate the virtual environment
```
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```
You will see `(venv)` at the start of your prompt.

### Step 5 – Install dependencies
```
pip install -r requirements.txt
```

### Step 6 – Configure your email in `.env`

Open `.env` and fill in your Gmail details:
```
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_16_char_app_password
MAIL_DEFAULT_SENDER=your_email@gmail.com
```

> **How to get Gmail App Password:**
> 1. Go to https://myaccount.google.com/security
> 2. Enable 2-Step Verification
> 3. Go to https://myaccount.google.com/apppasswords
> 4. Create a new app password → copy the 16-character code
> 5. Paste it as `MAIL_PASSWORD` in your `.env` file

### Step 7 – Run the app
```
python app.py
```

### Step 8 – Open in browser
Visit: **http://127.0.0.1:5000**

---

## How to Use the App

1. **Register** – Create a free account
2. **Set up Profile** – Choose your goal, level, weekly days, and email time
3. **Dashboard** – See today's personalised workout plan
4. **Send Email Now** – Click the button to test email delivery immediately
5. **History** – View all past plans sent to you

---

## How the Automated Emails Work

- The **APScheduler** runs a background job every minute
- It checks if any user's `email_time` matches the current UTC time
- If yes, it generates that user's next workout plan and sends it by email
- A log entry is saved in the database so History stays up to date

**Example:** If you set your email time to `07:00` UTC, you will receive a
workout email every day at 7 AM UTC.

> **Note on time zones:** The app currently uses UTC for scheduling.
> If you are in India (IST = UTC+5:30) and want emails at 7 AM IST,
> set your email time to `01:30` UTC.

---

## How to Stop the App
Press `Ctrl + C` in the terminal window.

---

## How to Extend It Later

| Feature | What to do |
|---|---|
| **Add more exercises** | Edit `EXERCISE_LIBRARY` in `workout_engine.py` |
| **Add a new fitness goal** | Add entries to `EXERCISE_LIBRARY`, `DAY_ROTATION`, and `GOAL_LABELS` |
| **Support timezones** | Add a `timezone` column to `User`; convert in `check_and_send_emails()` |
| **REST API** | Add more routes in `routes.py` returning `jsonify(...)` |
| **User-uploaded photos** | Add `Flask-Uploads` and a photo column to `User` |
| **Deploy online** | Use **Railway**, **Render**, or **Heroku** + swap SQLite for PostgreSQL |
| **Admin panel** | Add `Flask-Admin` – one line of code |
| **Google OAuth login** | Use `Flask-Dance` for social login |
| **Progress tracking** | Add weight/reps logging and Chart.js graphs on the dashboard |

---

## Tech Stack

| Layer | Technology | Why |
|---|---|---|
| Backend | Python + Flask | Simple, beginner-friendly |
| Database | SQLite via SQLAlchemy | Zero setup, file-based |
| Email | Flask-Mail + Gmail SMTP | Free, easy |
| Scheduler | APScheduler | Runs inside Flask, no cron needed |
| Frontend | HTML + Vanilla CSS + JS | No framework bloat |

---

## Troubleshooting

**"UnicodeEncodeError" on Windows?**
Your terminal doesn't support emoji in `print()`. All print statements
have been made safe – this should not occur in the current version.

**Emails not arriving?**
- Check your `.env` has the correct App Password (not your Gmail password)
- Check your spam folder
- Make sure 2FA is enabled on your Google account

**"Port 5000 already in use"?**
Change the port in `app.py`:
```python
app.run(debug=True, use_reloader=False, port=5001)
```

**Database issues?**
Delete `instance/fitness.db` and restart – it will be recreated fresh.

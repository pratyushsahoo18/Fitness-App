# =====================================================
#  workout_engine.py  –  Workout Plan Generator
# =====================================================
# This is the "brain" of the app.  It picks exercises
# based on the user's goal, experience, and day number.

# ─────────────────────────────────────────────────────
#  Exercise Library
#  Structure: { goal: { experience: { day_type: [exercises] } } }
# ─────────────────────────────────────────────────────

EXERCISE_LIBRARY = {

    # ── WEIGHT LOSS ───────────────────────────────────
    "weight_loss": {
        "beginner": {
            "cardio": [
                {"name": "Brisk Walking",       "sets": None, "reps": None, "duration": "30 min",  "rest": "N/A"},
                {"name": "Jumping Jacks",        "sets": 3,    "reps": 20,   "duration": None,       "rest": "30 s"},
                {"name": "High Knees",           "sets": 3,    "reps": 20,   "duration": None,       "rest": "30 s"},
                {"name": "Mountain Climbers",    "sets": 3,    "reps": 15,   "duration": None,       "rest": "45 s"},
            ],
            "strength": [
                {"name": "Bodyweight Squats",    "sets": 3,    "reps": 12,   "duration": None,       "rest": "60 s"},
                {"name": "Push-ups (knee)",      "sets": 3,    "reps": 10,   "duration": None,       "rest": "60 s"},
                {"name": "Glute Bridges",        "sets": 3,    "reps": 15,   "duration": None,       "rest": "45 s"},
                {"name": "Plank",                "sets": 3,    "reps": None, "duration": "20 s",     "rest": "45 s"},
            ],
        },
        "intermediate": {
            "cardio": [
                {"name": "Running",              "sets": None, "reps": None, "duration": "30 min",   "rest": "N/A"},
                {"name": "Burpees",              "sets": 4,    "reps": 15,   "duration": None,        "rest": "30 s"},
                {"name": "Jump Rope",            "sets": None, "reps": None, "duration": "10 min",   "rest": "N/A"},
                {"name": "Box Jumps",            "sets": 4,    "reps": 12,   "duration": None,        "rest": "45 s"},
            ],
            "strength": [
                {"name": "Dumbbell Lunges",      "sets": 4,    "reps": 12,   "duration": None,        "rest": "60 s"},
                {"name": "Push-ups",             "sets": 4,    "reps": 15,   "duration": None,        "rest": "45 s"},
                {"name": "Dumbbell Rows",        "sets": 3,    "reps": 12,   "duration": None,        "rest": "60 s"},
                {"name": "Bicycle Crunches",     "sets": 3,    "reps": 20,   "duration": None,        "rest": "30 s"},
            ],
        },
        "advanced": {
            "cardio": [
                {"name": "HIIT Sprint Intervals","sets": None, "reps": None, "duration": "20 min",   "rest": "N/A"},
                {"name": "Plyometric Burpees",   "sets": 5,    "reps": 15,   "duration": None,        "rest": "20 s"},
                {"name": "Battle Ropes",         "sets": None, "reps": None, "duration": "15 min",   "rest": "N/A"},
            ],
            "strength": [
                {"name": "Barbell Squats",       "sets": 5,    "reps": 10,   "duration": None,        "rest": "90 s"},
                {"name": "Deadlifts",            "sets": 4,    "reps": 8,    "duration": None,        "rest": "90 s"},
                {"name": "Pull-ups",             "sets": 4,    "reps": 10,   "duration": None,        "rest": "60 s"},
                {"name": "Hanging Leg Raises",   "sets": 3,    "reps": 15,   "duration": None,        "rest": "45 s"},
            ],
        },
    },

    # ── MUSCLE GAIN ───────────────────────────────────
    "muscle_gain": {
        "beginner": {
            "push": [
                {"name": "Push-ups",             "sets": 3,    "reps": 10,   "duration": None,        "rest": "90 s"},
                {"name": "Dumbbell Shoulder Press","sets": 3,  "reps": 10,   "duration": None,        "rest": "90 s"},
                {"name": "Dumbbell Chest Fly",   "sets": 3,    "reps": 12,   "duration": None,        "rest": "60 s"},
                {"name": "Tricep Dips",          "sets": 3,    "reps": 10,   "duration": None,        "rest": "60 s"},
            ],
            "pull": [
                {"name": "Dumbbell Rows",        "sets": 3,    "reps": 10,   "duration": None,        "rest": "90 s"},
                {"name": "Resistance Band Pulls","sets": 3,    "reps": 15,   "duration": None,        "rest": "60 s"},
                {"name": "Dumbbell Bicep Curls", "sets": 3,    "reps": 12,   "duration": None,        "rest": "60 s"},
                {"name": "Superman Hold",        "sets": 3,    "reps": 12,   "duration": None,        "rest": "45 s"},
            ],
            "legs": [
                {"name": "Bodyweight Squats",    "sets": 3,    "reps": 15,   "duration": None,        "rest": "60 s"},
                {"name": "Dumbbell Lunges",      "sets": 3,    "reps": 12,   "duration": None,        "rest": "60 s"},
                {"name": "Calf Raises",          "sets": 3,    "reps": 20,   "duration": None,        "rest": "45 s"},
                {"name": "Glute Bridges",        "sets": 3,    "reps": 15,   "duration": None,        "rest": "45 s"},
            ],
        },
        "intermediate": {
            "push": [
                {"name": "Bench Press",          "sets": 4,    "reps": 10,   "duration": None,        "rest": "90 s"},
                {"name": "Overhead Press",       "sets": 4,    "reps": 8,    "duration": None,        "rest": "90 s"},
                {"name": "Incline Dumbbell Press","sets": 3,   "reps": 12,   "duration": None,        "rest": "75 s"},
                {"name": "Cable Tricep Pushdown","sets": 3,    "reps": 15,   "duration": None,        "rest": "60 s"},
            ],
            "pull": [
                {"name": "Pull-ups",             "sets": 4,    "reps": 8,    "duration": None,        "rest": "90 s"},
                {"name": "Barbell Rows",         "sets": 4,    "reps": 10,   "duration": None,        "rest": "90 s"},
                {"name": "Face Pulls",           "sets": 3,    "reps": 15,   "duration": None,        "rest": "60 s"},
                {"name": "Hammer Curls",         "sets": 3,    "reps": 12,   "duration": None,        "rest": "60 s"},
            ],
            "legs": [
                {"name": "Barbell Squats",       "sets": 4,    "reps": 10,   "duration": None,        "rest": "90 s"},
                {"name": "Romanian Deadlifts",   "sets": 4,    "reps": 10,   "duration": None,        "rest": "90 s"},
                {"name": "Leg Press",            "sets": 3,    "reps": 12,   "duration": None,        "rest": "75 s"},
                {"name": "Standing Calf Raises", "sets": 4,    "reps": 20,   "duration": None,        "rest": "45 s"},
            ],
        },
        "advanced": {
            "push": [
                {"name": "Heavy Bench Press",    "sets": 5,    "reps": 5,    "duration": None,        "rest": "2 min"},
                {"name": "Military Press",       "sets": 4,    "reps": 8,    "duration": None,        "rest": "90 s"},
                {"name": "Weighted Dips",        "sets": 4,    "reps": 10,   "duration": None,        "rest": "90 s"},
                {"name": "Skull Crushers",       "sets": 3,    "reps": 12,   "duration": None,        "rest": "60 s"},
            ],
            "pull": [
                {"name": "Weighted Pull-ups",    "sets": 5,    "reps": 6,    "duration": None,        "rest": "2 min"},
                {"name": "T-Bar Rows",           "sets": 4,    "reps": 8,    "duration": None,        "rest": "90 s"},
                {"name": "Cable Rows",           "sets": 3,    "reps": 12,   "duration": None,        "rest": "75 s"},
                {"name": "Preacher Curls",       "sets": 3,    "reps": 10,   "duration": None,        "rest": "60 s"},
            ],
            "legs": [
                {"name": "Barbell Back Squats",  "sets": 5,    "reps": 5,    "duration": None,        "rest": "2 min"},
                {"name": "Deadlifts",            "sets": 4,    "reps": 6,    "duration": None,        "rest": "2 min"},
                {"name": "Bulgarian Split Squats","sets": 4,   "reps": 10,   "duration": None,        "rest": "90 s"},
                {"name": "Leg Curls",            "sets": 3,    "reps": 12,   "duration": None,        "rest": "60 s"},
            ],
        },
    },

    # ── GENERAL FITNESS ───────────────────────────────
    "general_fitness": {
        "beginner": {
            "full_body": [
                {"name": "Bodyweight Squats",    "sets": 3,    "reps": 12,   "duration": None,        "rest": "60 s"},
                {"name": "Push-ups (knee)",      "sets": 3,    "reps": 10,   "duration": None,        "rest": "60 s"},
                {"name": "Plank",                "sets": 3,    "reps": None, "duration": "20 s",      "rest": "30 s"},
                {"name": "Jumping Jacks",        "sets": 3,    "reps": 20,   "duration": None,        "rest": "30 s"},
                {"name": "Glute Bridges",        "sets": 3,    "reps": 15,   "duration": None,        "rest": "45 s"},
            ],
        },
        "intermediate": {
            "full_body": [
                {"name": "Dumbbell Squats",      "sets": 4,    "reps": 12,   "duration": None,        "rest": "60 s"},
                {"name": "Push-ups",             "sets": 4,    "reps": 15,   "duration": None,        "rest": "45 s"},
                {"name": "Dumbbell Rows",        "sets": 3,    "reps": 12,   "duration": None,        "rest": "60 s"},
                {"name": "Russian Twists",       "sets": 3,    "reps": 20,   "duration": None,        "rest": "30 s"},
                {"name": "Burpees",              "sets": 3,    "reps": 10,   "duration": None,        "rest": "45 s"},
            ],
        },
        "advanced": {
            "full_body": [
                {"name": "Barbell Squats",       "sets": 5,    "reps": 8,    "duration": None,        "rest": "90 s"},
                {"name": "Pull-ups",             "sets": 4,    "reps": 10,   "duration": None,        "rest": "75 s"},
                {"name": "Dips",                 "sets": 4,    "reps": 12,   "duration": None,        "rest": "60 s"},
                {"name": "Deadlifts",            "sets": 4,    "reps": 6,    "duration": None,        "rest": "2 min"},
                {"name": "Dragon Flags",         "sets": 3,    "reps": 8,    "duration": None,        "rest": "60 s"},
            ],
        },
    },
}

# Day-type rotation templates per goal
# Maps: goal → list of day_types to rotate through
DAY_ROTATION = {
    "weight_loss":     ["cardio", "strength", "cardio", "strength", "cardio", "strength", "cardio"],
    "muscle_gain":     ["push", "pull", "legs", "push", "pull", "legs", "push"],
    "general_fitness": ["full_body", "full_body", "full_body", "full_body", "full_body", "full_body", "full_body"],
}

# Human-readable goal labels
GOAL_LABELS = {
    "weight_loss":     "Weight Loss",
    "muscle_gain":     "Muscle Gain",
    "general_fitness": "General Fitness",
}

# Tips shown at the bottom of every email
TIPS = [
    "💧 Drink at least 2–3 litres of water today.",
    "😴 Aim for 7–9 hours of quality sleep tonight.",
    "🥗 Focus on protein and vegetables at every meal.",
    "🧘 Take 5 minutes to stretch after your workout.",
    "📈 Progress takes time – stay consistent!",
    "🚶 Even a 10-minute walk counts on rest days.",
    "🧠 Visualise completing your workout before you start.",
]

import random


def generate_workout_plan(user, day_index: int = 0) -> dict:
    """
    Build a workout plan for a single day.

    Parameters
    ----------
    user       : User model instance
    day_index  : which day of the user's rotation (0 = first training day)

    Returns
    -------
    dict with keys: day_type, exercises, tip, label
    """
    goal       = user.fitness_goal or "general_fitness"
    experience = user.experience_level or "beginner"

    # Get the rotation for this goal
    rotation   = DAY_ROTATION.get(goal, DAY_ROTATION["general_fitness"])
    day_type   = rotation[day_index % len(rotation)]

    # Fetch the exercise list (fall back gracefully)
    try:
        exercises = EXERCISE_LIBRARY[goal][experience][day_type]
    except KeyError:
        exercises = EXERCISE_LIBRARY["general_fitness"]["beginner"]["full_body"]

    tip = random.choice(TIPS)

    return {
        "goal_label": GOAL_LABELS.get(goal, goal),
        "day_type":   day_type.replace("_", " ").title(),
        "experience": experience.title(),
        "exercises":  exercises,
        "tip":        tip,
    }


def format_plan_as_text(plan: dict, user_name: str, day_name: str) -> str:
    """Convert the plan dict into a plain-text string (used for email body)."""
    lines = [
        f"Good morning, {user_name}! 💪",
        "",
        f"Here is your {day_name} workout plan:",
        f"Goal: {plan['goal_label']}  |  Type: {plan['day_type']}  |  Level: {plan['experience']}",
        "",
        "─" * 50,
        f"{'Exercise':<28} {'Sets':>4} {'Reps':>6} {'Duration':>10} {'Rest':>8}",
        "─" * 50,
    ]

    for ex in plan["exercises"]:
        sets     = str(ex["sets"])     if ex["sets"]     else "—"
        reps     = str(ex["reps"])     if ex["reps"]     else "—"
        duration = ex["duration"]      if ex["duration"] else "—"
        rest     = ex["rest"]          if ex["rest"]     else "—"
        lines.append(f"{ex['name']:<28} {sets:>4} {reps:>6} {duration:>10} {rest:>8}")

    lines += [
        "─" * 50,
        "",
        f"Tip of the day: {plan['tip']}",
        "",
        "Stay consistent and keep pushing!",
        "– Your Fitness App 🏋️",
    ]
    return "\n".join(lines)

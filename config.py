# =====================================================
#  config.py  –  App Configuration
# =====================================================
# This file loads settings from .env and makes them
# available throughout the whole app.

import os
from dotenv import load_dotenv

# Load variables from the .env file into the environment
load_dotenv()


class Config:
    # ── Security ──────────────────────────────────────
    # Used to encrypt session cookies – keep it secret!
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")

    # ── Database ──────────────────────────────────────
    # SQLite stores everything in a single file.
    # "instance/fitness.db" lives inside the project folder.
    SQLALCHEMY_DATABASE_URI = "sqlite:///fitness.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False   # silence a noisy warning

    # ── Email (Gmail SMTP) ────────────────────────────
    MAIL_SERVER   = "smtp.gmail.com"
    MAIL_PORT     = 587
    MAIL_USE_TLS  = True                             # encrypt the connection
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")

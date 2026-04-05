# =====================================================
#  extensions.py  –  Shared Flask Extensions
# =====================================================
# We create these objects here (without binding them
# to an app yet) so that every other file can safely
# import them without causing circular imports.
#
# Think of it as a "toolbox" that gets connected to
# the real app later inside app.py via init_app().

from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

db   = SQLAlchemy()   # database helper
mail = Mail()          # email helper

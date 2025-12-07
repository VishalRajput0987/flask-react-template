# backend/routes/__init__.py
# backend/routes/__init__.py (or wherever you register blueprints/in app.py)
from flask import Flask
from .comments import comments_bp
# from .tasks import tasks_bp # Existing Task Blueprint

def register_blueprints(app: Flask):
    # app.register_blueprint(tasks_bp) # Existing registration
    app.register_blueprint(comments_bp) # NEW registration
    # ...
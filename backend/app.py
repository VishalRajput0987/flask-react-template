# # # backend/app.py

# # from flask import Flask
# # from backend.db import db # Use package import
# # import os 
# # from dotenv import load_dotenv

# # # Load environment variables (optional, but good practice)
# # load_dotenv()

# # def create_app(config_class=None):
# #     """Initializes and configures the Flask application instance."""
# #     app = Flask(__name__)
    
# #     # --- Configuration ---
# #     app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
# #         "DATABASE_URL", 
# #         "sqlite:///dev.db" 
# #     )
# #     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# #     app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "a_strong_dev_secret")
    
# #     # --- Extensions Initialization ---
# #     db.init_app(app)
    
# #     # --- Blueprint Registration ---
    
# #     # 1. Import models and blueprints (using explicit package imports)
# #     from backend.models import Task # Import Task just to ensure models are loaded
# #     from backend.routes.comments import comments_bp
    
# #     # 2. Register blueprints
# #     # Assuming an existing tasks_bp for CRUD on tasks needs registration here too
# #     app.register_blueprint(comments_bp, url_prefix='/api')
    
    
# #     # --- Database Setup (Creates tables if they don't exist) ---
    
# #     with app.app_context():
# #         db.create_all()
        
# #         # Optional: Seed data for quick testing if database is empty
# #         if Task.query.count() == 0:
# #             task1 = Task(title="Complete Assessment Task 1")
# #             task2 = Task(title="Work on Task 2 Bonus")
# #             db.session.add_all([task1, task2])
# #             db.session.commit()
# #             print("Seeded initial tasks.")

# #     return app

# # # --- Entry Point ---

# # if __name__ == '__main__':
# #     app = create_app()
# #     app.run(debug=True)


# # backend/app.py

# # from flask import Flask
# # from backend.db import db
# # import os 
# # from dotenv import load_dotenv

# # load_dotenv()

# # def create_app(config_class=None):
# #     """Initializes and configures the Flask application instance."""
# #     app = Flask(__name__)
    
# #     # --- Configuration ---
# #     app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
# #         "DATABASE_URL", 
# #         "sqlite:///dev.db" 
# #     )
# #     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# #     app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "a_strong_dev_secret")
    
# #     # --- Extensions Initialization ---
# #     db.init_app(app)
    
# #     # --- Blueprint Registration ---
    
# #     # 1. Import models and blueprints (using explicit package imports)
# #     from backend.models import Task 
# #     from backend.routes.comments import comments_bp
    
# #     # ASSUMPTION: You have an existing blueprint for Task CRUD
# #     try:
# #         from backend.routes.tasks import tasks_bp 
# #     except ImportError:
# #         # Handle case where tasks.py might not exist, but app needs it for context
# #         tasks_bp = None
    
# #     # 2. Register blueprints
# #     # This is required for the /api/tasks part of the URL to be recognized
# #     if tasks_bp is not None:
# #         app.register_blueprint(tasks_bp, url_prefix='/api')
    
# #     # This registers the comment endpoints as a nested resource
# #     app.register_blueprint(comments_bp, url_prefix='/api') 
    
    
# #     # --- Database Setup (Creates tables if they don't exist) ---
    
# #     with app.app_context():
# #         db.create_all()
        
# #         # Optional: Seed data for quick testing if database is empty
# #         if Task.query.count() == 0:
# #             task1 = Task(title="Complete Assessment Task 1")
# #             task2 = Task(title="Work on Task 2 Bonus")
# #             db.session.add_all([task1, task2])
# #             db.session.commit()
# #             print("Seeded initial tasks.")

# #     return app

# # # --- Entry Point ---

# # if __name__ == '__main__':
# #     app = create_app()
# #     app.run(debug=True)


# # backend/app.py

# from flask import Flask
# from backend.db import db # Explicit package import
# import os 
# from dotenv import load_dotenv

# from flask_cors import CORS

# load_dotenv()

# def create_app(config_class=None):
#     """Initializes and configures the Flask application instance."""
#     app = Flask(__name__)
    
#     # --- Configuration ---
#     app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
#         "DATABASE_URL", 
#         "sqlite:///dev.db" 
#     )
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#     app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "a_strong_dev_secret")
    
#     # --- Extensions Initialization ---
#     db.init_app(app)
    
#     # --- Blueprint Registration ---
    
#     # 1. Import models and BOTH blueprints (using explicit package imports)
#     from backend.models import Task 
#     from backend.routes.tasks import tasks_bp       # <-- Import the new tasks blueprint
#     from backend.routes.comments import comments_bp
    
#     # 2. Register BOTH blueprints
#     # MUST be registered: handles the base /api/tasks URL segments
#     app.register_blueprint(tasks_bp, url_prefix='/api')
    
#     # Registers the nested comment endpoints
#     app.register_blueprint(comments_bp, url_prefix='/api') 
    
    
#     # --- Database Setup ---
    
#     with app.app_context():
#         db.create_all()
        
#         # Optional: Seed data for quick testing
#         if Task.query.count() == 0:
#             task1 = Task(title="Complete Assessment Task 1")
#             task2 = Task(title="Work on Task 2 Bonus")
#             db.session.add_all([task1, task2])
#             db.session.commit()
#             print("Seeded initial tasks.")

#     return app

# # --- Entry Point ---

# if __name__ == '__main__':
#     app = create_app()
#     app.run(debug=True)



# backend/app.py

from flask import Flask
from backend.db import db # Explicit package import
import os 
from dotenv import load_dotenv

# --- New Import ---
from flask_cors import CORS # This is the key fix for "Failed to fetch"
# ------------------

load_dotenv()

def create_app(config_class=None):
    """Initializes and configures the Flask application instance."""
    app = Flask(__name__)
    
    # --- Configuration ---
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", 
        "sqlite:///dev.db" 
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "a_strong_dev_secret")
    
    # --- Extensions Initialization ---
    db.init_app(app)
    
    # --- CORS CONFIGURATION (CRITICAL FIX) ---
    # Allow the React frontend (http://localhost:3000) to access the API endpoints
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
    # ------------------------------------------
    
    # --- Blueprint Registration ---
    
    # 1. Import models and BOTH blueprints (using explicit package imports)
    from backend.models import Task 
    from backend.routes.tasks import tasks_bp 
    from backend.routes.comments import comments_bp
    
    # 2. Register BOTH blueprints
    # Registers the base /api/tasks URLs
    app.register_blueprint(tasks_bp, url_prefix='/api')
    
    # Registers the nested comment endpoints
    app.register_blueprint(comments_bp, url_prefix='/api') 
    
    
    # --- Database Setup ---
    
    with app.app_context():
        db.create_all()
        
        # Optional: Seed data for quick testing
        if Task.query.count() == 0:
            task1 = Task(title="Complete Assessment Task 1")
            task2 = Task(title="Work on Task 2 Bonus")
            db.session.add_all([task1, task2])
            db.session.commit()
            print("Seeded initial tasks.")

    return app

# --- Entry Point ---

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
# backend/routes/tasks.py

from flask import Blueprint, jsonify, request, abort
from backend.models import Task
from backend.db import db
import json

# Define the tasks blueprint
tasks_bp = Blueprint('tasks', __name__)

# @tasks_bp.route('/tasks', methods=['GET'])
# def list_tasks():
#     """Handles GET /api/tasks to list all tasks."""
#     # This assumes Task models are needed for the frontend.
#     tasks = Task.query.all()
#     # Serialize tasks, including the count of associated comments
#     return jsonify([
#         {'id': t.id, 'title': t.title, 'comment_count': len(t.comments)} 
#         for t in tasks
#     ]), 200

@tasks_bp.route('/tasks', methods=['GET'])
def list_tasks():
    """Handles GET /api/tasks to list all tasks."""
    tasks = Task.query.all()
    # Serialize tasks, using the .count() method or len(list(.all()))
    return jsonify([
        {
            'id': t.id, 
            'title': t.title, 
            # FIX: Use .count() instead of len() on the SQLAlchemy relationship object
            'comment_count': t.comments.count() 
        } 
        for t in tasks
    ]), 200




# --- Minimal Task CRUD Endpoints (Required for a functional system) ---

@tasks_bp.route('/tasks', methods=['POST'])
def create_task():
    """Handles POST /api/tasks to create a new task."""
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({"message": "Missing task title"}), 400
    
    new_task = Task(title=data['title'])
    db.session.add(new_task)
    db.session.commit()
    
    return jsonify({
        'id': new_task.id, 
        'title': new_task.title, 
        'comment_count': 0
    }), 201

@tasks_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Handles DELETE /api/tasks/<id> to delete a task."""
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"message": "Task not found"}), 404
        
    # Deleting the task will automatically delete linked comments due to cascade='all, delete-orphan'
    db.session.delete(task)
    db.session.commit()
    return '', 204
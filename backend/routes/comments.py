# backend/routes/comments.py

from flask import Blueprint, request, jsonify, abort
from backend.db import db
from backend.models import Task, Comment


# -----------------------------------------------------------------------------------------
# Define the blueprint with NO URL PREFIX here. The prefix will be added in app.py.
# -----------------------------------------------------------------------------------------
comments_bp = Blueprint('comments', __name__)


# --- Helpers ---
def get_task_or_404(task_id):
    task = Task.query.get(task_id)
    if task is None:
        abort(404, description=f"Task with ID {task_id} not found.")
    return task

def get_comment_or_404(comment_id):
    comment = Comment.query.get(comment_id)
    if comment is None:
        abort(404, description=f"Comment with ID {comment_id} not found.")
    return comment
# -----------------------------------------------------------

# POST (CREATE) & GET (READ ALL)
@comments_bp.route('/tasks/<int:task_id>/comments', methods=['POST', 'GET'])
def task_comments_collection(task_id):
    task = get_task_or_404(task_id)

    if request.method == 'POST':
        data = request.get_json()
        
        # --- FIX: Change 'text' to 'content' for API compatibility ---
        if not data or not data.get('content', '').strip(): 
            # Input Validation (400 Bad Request)
            abort(400, description="Comment content is required.")

        new_comment = Comment(content=data['content'], task_id=task.id) # Use 'content' for model field
        # -------------------------------------------------------------
        
        db.session.add(new_comment)
        db.session.commit()
        
        return jsonify(new_comment.to_dict()), 201 # 201 Created

    # GET (Read All)
    # CRITICAL FIX: Change Comment.created_at to Comment.created_on to match models.py
    comments = task.comments.order_by(Comment.created_on.desc()).all()
    # -------------------------------------------------------------------
    return jsonify([c.to_dict() for c in comments]), 200


# GET, PUT (UPDATE), DELETE
@comments_bp.route('/tasks/<int:task_id>/comments/<int:comment_id>', methods=['GET', 'PUT', 'DELETE'])
def task_comment_resource(task_id, comment_id):
    task = get_task_or_404(task_id)
    comment = get_comment_or_404(comment_id)
    
    # Critical Integrity Check
    if comment.task_id != task.id:
        abort(404, description=f"Comment {comment_id} not found for Task {task_id}.")

    if request.method == 'GET':
        return jsonify(comment.to_dict()), 200

    elif request.method == 'PUT':
        data = request.get_json()
        
        # --- FIX: Change 'text' to 'content' for API compatibility ---
        if not data or not data.get('content', '').strip():
            abort(400, description="Comment content is required for update.")

        comment.content = data['content'] # Use 'content' for model field
        # -------------------------------------------------------------
        
        db.session.commit()
        
        return jsonify(comment.to_dict()), 200

    elif request.method == 'DELETE':
        db.session.delete(comment)
        db.session.commit()
        
        return '', 204 # 204 No Content
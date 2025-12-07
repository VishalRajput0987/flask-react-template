# backend/tests/test_comments.py
import pytest
import json
# Assuming you import your app factory, db object, and models like this
# from app import create_app 
# from db import db
# from models import Task, Comment 

from backend.app import create_app # Specify the full path to app.py
from backend.db import db
from backend.models import Task, Comment

# --- FIXTURES (Setup/Teardown) ---

@pytest.fixture(scope='session')
def app():
    """Sets up a testing Flask app environment."""
    app = create_app() 
    app.config.update({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    with app.app_context():
        db.create_all() 
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Provides a test client for making simulated API requests."""
    return app.test_client()

@pytest.fixture(autouse=True)
def db_session_setup(app):
    """Resets and injects test data before each test."""
    with app.app_context():
        # Setup: Clear and create test Tasks and initial Comment
        Comment.query.delete()
        Task.query.delete()
        task1 = Task(title="Test Task 1")
        task2 = Task(title="Test Task 2") 
        db.session.add_all([task1, task2])
        db.session.commit()
        comment1 = Comment(text="Initial Comment for Task 1", task_id=task1.id)
        db.session.add(comment1)
        db.session.commit()
        yield task1, comment1, task2
        db.session.remove()

# --- API Test Cases ---

def test_1_create_comment_success(client, db_session_setup):
    """Test POST /api/tasks/<task_id>/comments (201 Created)."""
    task, _, _ = db_session_setup
    url = f'/api/tasks/{task.id}/comments'
    response = client.post(url, json={'text': 'New comment.'})
    assert response.status_code == 201

def test_2_read_all_comments_success(client, db_session_setup):
    """Test GET /api/tasks/<task_id>/comments (200 OK)."""
    task, _, _ = db_session_setup
    url = f'/api/tasks/{task.id}/comments'
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.json) == 1

def test_3_update_comment_success(client, db_session_setup):
    """Test PUT /api/tasks/<task_id>/comments/<comment_id> (200 OK)."""
    task, comment, _ = db_session_setup
    url = f'/api/tasks/{task.id}/comments/{comment.id}'
    updated_text = 'Updated Comment Text.'
    response = client.put(url, json={'text': updated_text})
    assert response.status_code == 200
    assert response.json['text'] == updated_text

def test_4_delete_comment_success(client, db_session_setup):
    """Test DELETE /api/tasks/<task_id>/comments/<comment_id> (204 No Content)."""
    task, comment, _ = db_session_setup
    url = f'/api/tasks/{task.id}/comments/{comment.id}'
    response = client.delete(url)
    assert response.status_code == 204
    assert Comment.query.get(comment.id) is None

def test_5_create_comment_invalid_input_400(client, db_session_setup):
    """Test POST fails with missing 'text' (400 Bad Request)."""
    task, _, _ = db_session_setup
    url = f'/api/tasks/{task.id}/comments'
    response = client.post(url, json={}) 
    assert response.status_code == 400

def test_6_delete_wrong_task_comment_404(client, db_session_setup):
    """Test DELETE fails if comment doesn't belong to task (404 Not Found)."""
    task1, comment1, task2 = db_session_setup
    url = f'/api/tasks/{task2.id}/comments/{comment1.id}' # Using task2's URL for task1's comment
    response = client.delete(url)
    assert response.status_code == 404
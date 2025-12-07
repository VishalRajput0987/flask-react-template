from backend.db import db
from datetime import datetime

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    
    comments = db.relationship(
        'Comment', 
        backref='task', 
        lazy='dynamic', 
        cascade='all, delete-orphan' 
    )

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'comment_count': self.comments.count() 
        }

class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # CRITICAL FIX: Changed 'text' to 'content'
    content = db.Column(db.Text, nullable=False) 
    
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content, 
            'task_id': self.task_id,
            'created_on': self.created_on.isoformat() + 'Z',
            'updated_at': self.updated_at.isoformat() + 'Z',
        }
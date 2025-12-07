// frontend/src/components/CommentForm.jsx
import React, { useState } from 'react';
import { addComment } from '../api/tasks';

const CommentForm = ({ taskId, onCommentAdded }) => {
  const [text, setText] = useState('');
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!text.trim()) return;

    try {
      await addComment(taskId, text);
      setText('');
      onCommentAdded(); 
    } catch (error) {
      console.error('Error adding comment:', error);
      alert('Failed to add comment.');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="comment-form">
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Add a new comment..."
        rows="3"
        required
      />
      <button type="submit">Post Comment</button>
    </form>
  );
};

export default CommentForm;
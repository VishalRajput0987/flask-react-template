
import React, { useEffect, useState } from 'react';
import { getComments, deleteComment } from '../api/tasks'; 
import CommentForm from './CommentForm';

const CommentList = ({ taskId, refetchTasks }) => {
    const [comments, setComments] = useState([]);
    const [isCommentsLoading, setIsCommentsLoading] = useState(false);

    const fetchComments = async () => {
        setIsCommentsLoading(true);
        try {
            const data = await getComments(taskId);
            setComments(data);
        } catch (error) {
            console.error('Error fetching comments:', error);
        } finally {
            setIsCommentsLoading(false);
        }
    };

    useEffect(() => {
        fetchComments();
    }, [taskId]);


    const handleDelete = async (commentId) => {
    try {
        await deleteComment(taskId, commentId);
        fetchComments(); 
        
        // CRITICAL FIX: Guard check before calling refetchTasks
        if (typeof refetchTasks === 'function') {
            refetchTasks(); 
        }
    } catch (error) {
        console.error("Delete failed:", error);
        alert("Delete failed: " + error.message);
    }
};

    if (isCommentsLoading) return <div>Loading comments...</div>;

    return (
        <div className="comment-section">
            <h4>Comments</h4>

            <CommentForm 
  taskId={taskId} 
  onCommentAdded={() => { 
    fetchComments(); 
    // CRITICAL FIX: Guard check before calling refetchTasks
    if (typeof refetchTasks === 'function') {
      refetchTasks(); 
    }
  }} 
/>
            
            {comments.length === 0 ? (<p>No comments yet.</p>) : (
                <ul className="comment-list">
                    {comments.map((comment) => (
                        <li key={comment.id} className="comment-item">
                            
                            <p>{comment.content}</p>
                            
                            <small>Posted: {new Date(comment.created_on).toLocaleDateString()}</small>
                            
                            <button onClick={() => handleDelete(comment.id)}>X</button>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default CommentList;
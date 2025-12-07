import React, { useState } from 'react';
import { useTasks } from '../hooks/useTasks';
import CommentList from './CommentList';
import { createTask, deleteTask } from '../api/tasks';

const TaskList = () => {
  const { tasks, isLoading, refetchTasks } = useTasks();
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [selectedTaskId, setSelectedTaskId] = useState(null);

  const handleCreateTask = async (e) => { 
    e.preventDefault();
  };

  const handleDeleteTask = async (taskId) => {
    if (window.confirm('Confirm delete task?')) {
        try {
            await deleteTask(taskId);
            refetchTasks();
        } catch (error) {
            console.error('Deletion error:', error);
            alert('Failed to delete task.');
        }
    }
  };

  if (isLoading) return <div>Loading Tasks...</div>;

  return (
    <div className="task-container">
      <h2>Tasks & Comments</h2>
      
      <form onSubmit={handleCreateTask}> {/* ... form content ... */} </form>
      
      <ul className="task-list">
        {tasks.map((task) => (
          <li key={task.id} className="task-item">
            <span>{task.title}</span>
            <div className="task-actions">
              <button onClick={() => handleDeleteTask(task.id)} className="delete-btn">Delete</button>
              <button 
                onClick={() => setSelectedTaskId(selectedTaskId === task.id ? null : task.id)}
                className="comment-btn"
              >
                {selectedTaskId === task.id ? 'Hide Comments' : `Show Comments (${task.comment_count || 0})`}
              </button>
            </div>
            
            {/* Task 1 Integration */}
            {selectedTaskId === task.id && (
              <CommentList taskId={task.id} refetchTasks={refetchTasks} />
            )}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TaskList;
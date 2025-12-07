// frontend/src/pages/TasksPage.jsx
import React, { useState } from 'react';
// Import the necessary functions (createTask, deleteTask) from the custom hook
import { useTasks } from '../hooks/useTasks';
import CommentList from '../components/CommentList';

const TasksPage = () => {
    // CRITICAL FIX: Destructure the state AND the functions from the hook
    const { tasks, isLoading, error, createTask, deleteTask, refetchTasks } = useTasks();
    
    const [newTaskTitle, setNewTaskTitle] = useState('');
    const [selectedTaskId, setSelectedTaskId] = useState(null);
    
    // --- Task 2: Create Task Logic ---
    const handleCreateTask = async (e) => {
        e.preventDefault();
        if (!newTaskTitle.trim()) return;

        // FIX: Call the createTask function returned by the useTasks hook
        await createTask(newTaskTitle); 
        
        setNewTaskTitle(''); // Clear the input field
    };
    
    // --- Task 2: Delete Task Logic ---
    const handleDeleteTask = async (taskId) => {
        // FIX: Call the deleteTask function returned by the useTasks hook
        await deleteTask(taskId);
        
        // Optional: Hide comments if the deleted task was selected
        if (selectedTaskId === taskId) {
            setSelectedTaskId(null);
        }
    };

    if (isLoading) return <div>Loading Tasks...</div>;
    if (error) return <div>Error loading tasks: {error}</div>; // Display error state

    return (
        <div className="main-app-container">
            <h1>Project Management Dashboard</h1>
            
            {/* Task 2: Add Task Form */}
            <form onSubmit={handleCreateTask} className="task-form">
                <input
                    type="text"
                    value={newTaskTitle}
                    onChange={(e) => setNewTaskTitle(e.target.value)}
                    placeholder="Enter new task title"
                    required
                />
                <button type="submit">Add Task</button>
            </form>
            
            {/* Task List and Comment Integration (Task 1 & 2) */}
            <ul className="task-list">
                {/* FIX: Ensure tasks is a valid array before mapping */}
                {tasks && tasks.map((task) => (
                    <li key={task.id} className="task-item">
                        <span>{task.title}</span>
                        <div className="task-actions">
                            <button 
                                onClick={() => handleDeleteTask(task.id)} 
                                className="delete-btn"
                            >
                                Delete
                            </button>
                            <button 
                                onClick={() => setSelectedTaskId(selectedTaskId === task.id ? null : task.id)}
                                className="comment-btn"
                            >
                                {/* Ensure comment_count is handled gracefully */}
                                {selectedTaskId === task.id ? 'Hide Comments' : `Show Comments (${task.comment_count || 0})`}
                            </button>
                        </div>
                        
                        {/* Renders Comment Section when selected */}
                        {selectedTaskId === task.id && (
                            // Correctly passing refetchTasks function
                            <CommentList taskId={task.id} refetchTasks={refetchTasks} />
                        )}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default TasksPage;
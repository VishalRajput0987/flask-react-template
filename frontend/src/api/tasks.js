// frontend/src/api/tasks.js
// --- CRITICAL FIX: Base URL should only be '/api' ---
const API_BASE_URL = '/api';

// --- Task CRUD (Task 2) ---
export const getTasks = async () => { 
    // ... implementation ... 
    const response = await fetch(`${API_BASE_URL}/tasks`); // Use /api/tasks
    if (!response.ok) throw new Error('Failed to fetch tasks.');
    return response.json();
};

export const createTask = async (title) => { 
    // ... API call to POST /api/tasks ... 
    const response = await fetch(`${API_BASE_URL}/tasks`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title }),
    });
    if (response.status !== 201) throw new Error('Failed to create task.');
    return response.json();
};

export const deleteTask = async (taskId) => { 
    // Use /api/tasks/{taskId}
    const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, { method: 'DELETE' });
    if (response.status !== 204) throw new Error('Failed to delete task.');
    return true;
};

// --- Comment CRUD (Task 1 Integration) ---
export const getComments = async (taskId) => {
    // Use /api/tasks/{taskId}/comments
    const response = await fetch(`${API_BASE_URL}/tasks/${taskId}/comments`);
    if (!response.ok) throw new Error('Failed to fetch comments.');
    return response.json();
};

export const addComment = async (taskId, text) => {
    // Use /api/tasks/{taskId}/comments
    // FIX 1: Send 'content' key instead of 'text' to match backend
    const response = await fetch(`${API_BASE_URL}/tasks/${taskId}/comments`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ content: text }), // FIX: Use 'content'
    });
    // FIX 2: Check for 201 (Created) status
    if (response.status !== 201) throw new Error('Failed to add comment.');
    return response.json();
};

export const deleteComment = async (taskId, commentId) => {
    // Use /api/tasks/{taskId}/comments/{commentId}
    const response = await fetch(`${API_BASE_URL}/tasks/${taskId}/comments/${commentId}`, {
        method: 'DELETE',
    });
    if (response.status !== 204) throw new Error('Failed to delete comment.');
    return true;
};
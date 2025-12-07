// frontend/src/hooks/useTasks.js

import { useState, useEffect } from 'react';

// Define the API base URL
const API_BASE_URL = 'http://127.0.0.1:5000/api/tasks';

// Define and EXPORT the hook
export const useTasks = () => { // <-- Use NAMED export
    const [tasks, setTasks] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    // --- 1. Fetch Tasks ---
    const fetchTasks = async () => {
        setIsLoading(true);
        setError(null);
        try {
            const response = await fetch(API_BASE_URL);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            setTasks(data);
        } catch (err) {
            setError(err.message);
            console.error("Failed to fetch tasks:", err);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchTasks();
    }, []);

    // --- 2. Create Task ---
    const createTask = async (title) => {
        try {
            const response = await fetch(API_BASE_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ title }),
            });

            if (response.status === 201) {
                const newTask = await response.json();
                setTasks(prevTasks => [...prevTasks, newTask]);
            } else {
                throw new Error("Failed to create task");
            }
        } catch (err) {
            setError(err.message);
            console.error("Failed to create task:", err);
        }
    };

    // --- 3. Delete Task ---
    const deleteTask = async (id) => {
        try {
            const response = await fetch(`${API_BASE_URL}/${id}`, {
                method: 'DELETE',
            });

            if (response.status === 204) {
                setTasks(prevTasks => prevTasks.filter(task => task.id !== id));
            } else {
                throw new Error("Failed to delete task");
            }
        } catch (err) {
            setError(err.message);
            console.error("Failed to delete task:", err);
        }
    };

    // Return the state and functions required by components
    return {
        tasks,
        isLoading,
        error,
        createTask,
        deleteTask,
        fetchTasks // Expose fetchTasks for re-fetching when comments change
    };
};
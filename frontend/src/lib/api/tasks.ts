// src/lib/api/tasks.ts
import apiClient from "@/lib/api/clients";
import { Task, TaskCreateRequest, TaskUpdateRequest, TaskListResponse } from "@/types/tasks";

// Get all tasks (paginated)
export const getTasks = async (userId: string, page = 1, page_size = 20): Promise<TaskListResponse> => {
  const response = await apiClient.get<{ tasks: Task[] }>(`/api/users/${userId}/tasks?page=${page}&page_size=${page_size}`);
  const tasks = response.data.tasks || [];
  const total = tasks.length; // Assuming all tasks are returned for simplicity for now
  const total_pages = Math.ceil(total / page_size);

  return {
    items: tasks,
    total: total,
    page: page,
    page_size: page_size,
    total_pages: total_pages,
  };
};

// Get single task
export const getTask = async (userId: string, id: string): Promise<Task> => {
  const response = await apiClient.get<Task>(`/api/users/${userId}/tasks/${id}`);
  return response.data;
};

// Create task
export const createTask = async (userId: string, data: TaskCreateRequest): Promise<Task> => {
  const response = await apiClient.post<Task>(`/api/users/${userId}/tasks`, data);
  return response.data;
};

// Update task
export const updateTask = async (userId: string, id: string, data: TaskUpdateRequest): Promise<Task> => {
  const response = await apiClient.patch<Task>(`/api/users/${userId}/tasks/${id}`, data);
  return response.data;
};

// Delete task
export const deleteTask = async (userId: string, id: string): Promise<void> => {
  await apiClient.delete(`/api/users/${userId}/tasks/${id}`);
};

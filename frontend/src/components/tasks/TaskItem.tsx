'use client';

import React, { useState } from 'react';
import { Task, TaskUpdateRequest } from '@/types/tasks';
import { Button } from '@/components/ui/Button';

interface TaskItemProps {
  task: Task;
  toggleComplete: (taskId: string) => Promise<void>;
  deleteTask: (taskId: string) => Promise<void>;
  updateTask: (taskId: string, data: TaskUpdateRequest) => Promise<void>;
  userId: string;
}

export function TaskItem({
  task,
  toggleComplete,
  deleteTask,
  updateTask,
}: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editedTitle, setEditedTitle] = useState(task.title);
  const [editedDescription, setEditedDescription] = useState(task.description || '');

  const handleUpdate = async () => {
    try {
      await updateTask(task.id, {
        title: editedTitle,
        description: editedDescription,
      });
      setIsEditing(false);
    } catch (error) {
      console.error('Failed to update task:', error);
    }
  };

  return (
    <li className="group relative p-5 rounded-xl bg-white/5 backdrop-blur-md border border-white/10 shadow-lg hover:shadow-purple-500/20 hover:scale-[1.01] transition-all duration-300">
      {isEditing ? (
        <div className="flex flex-col gap-3">
          <input
            type="text"
            value={editedTitle}
            onChange={(e) => setEditedTitle(e.target.value)}
            className="bg-black/40 border border-gray-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
            placeholder="Task title"
          />

          <textarea
            value={editedDescription}
            onChange={(e) => setEditedDescription(e.target.value)}
            className="bg-black/40 border border-gray-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
            rows={3}
            placeholder="Description"
          />

          <div className="flex gap-2">
            <Button size="sm" onClick={handleUpdate}>
              Save
            </Button>
            <Button
              size="sm"
              variant="secondary"
              onClick={() => setIsEditing(false)}
            >
              Cancel
            </Button>
          </div>
        </div>
      ) : (
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div className="flex-1">
            <div className="flex items-start gap-3">
              <div className="flex-shrink-0 pt-1">
                <input
                  type="checkbox"
                  checked={task.is_complete}
                  onChange={() => toggleComplete(task.id)}
                  className="w-5 h-5 rounded border-gray-600 bg-gray-800 text-purple-500 focus:ring-purple-500 focus:ring-offset-gray-900"
                />
              </div>
              <div className="flex-1">
                <h3
                  className={`text-lg font-semibold ${
                    task.is_complete
                      ? 'line-through text-gray-500'
                      : 'text-white'
                  }`}
                >
                  {task.title}
                </h3>

                {task.description && (
                  <p
                    className={`text-sm mt-1 ${
                      task.is_complete
                        ? 'line-through text-gray-600'
                        : 'text-gray-400'
                    }`}
                  >
                    {task.description}
                  </p>
                )}

                <div className="flex items-center gap-4 mt-2 text-xs text-gray-500">
                  <span className="flex items-center gap-1">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    {new Date(task.created_at).toLocaleDateString()}
                  </span>
                  {task.is_complete && (
                    <span className="flex items-center gap-1 text-green-500">
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                      Completed
                    </span>
                  )}
                </div>
              </div>
            </div>
          </div>

          <div className="flex flex-wrap gap-2">
            <Button
              size="sm"
              onClick={() => toggleComplete(task.id)}
              variant={task.is_complete ? 'outline' : 'gradient'}
              className={`${task.is_complete ? 'border-green-500/30 text-green-400 hover:bg-green-500/10' : 'bg-gradient-to-r from-purple-600 to-cyan-500 hover:from-purple-700 hover:to-cyan-600'} transform transition-none hover:scale-100 hover:shadow-none`}
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                {task.is_complete ? (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                )}
              </svg>
              {task.is_complete ? 'Undo' : 'Complete'}
            </Button>

            <Button
              size="sm"
              onClick={() => setIsEditing(true)}
              variant="outline"
              className="border-gray-600 text-gray-300 hover:bg-gray-800/50 transform transition-none hover:scale-100 hover:shadow-none"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
              Edit
            </Button>

            <Button
              size="sm"
              onClick={() => deleteTask(task.id)}
              variant="outline"
              className="border-red-500/30 text-red-400 hover:bg-red-500/10 transform transition-none hover:scale-100 hover:shadow-none"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
              Delete
            </Button>
          </div>
        </div>
      )}
    </li>
  );
}

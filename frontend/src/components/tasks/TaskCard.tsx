// T036: TaskCard component with task display and actions

'use client';

import React from 'react';
import { Task } from '@/types/tasks';
import { Checkbox } from '../ui/Checkbox';
import { Button } from '../ui/Button';

interface TaskCardProps {
  task: Task;
  onToggleComplete: () => void;
  onEdit: () => void;
  onDelete: () => void;
}

export function TaskCard({ task, onToggleComplete, onEdit, onDelete }: TaskCardProps) {
  return (
    <div className="bg-linear-to-br from-indigo-900/30 via-purple-900/20 to-cyan-900/30 backdrop-blur-sm border border-purple-500/30 rounded-2xl p-5 hover:from-indigo-800/40 hover:via-purple-800/30 hover:to-cyan-800/40 hover:border-purple-400/50 hover:shadow-lg hover:shadow-purple-500/20 transition-all duration-300">
      <div className="flex items-start gap-4">
        <div className="pt-0.5">
          <Checkbox
            checked={task.is_complete}
            onChange={onToggleComplete}
            aria-label={`Mark "${task.title}" as ${task.is_complete ? 'incomplete' : 'complete'}`}
          />
        </div>

        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-3">
            <h3
              className={`text-lg font-semibold ${
                task.is_complete ? 'line-through text-gray-500' : 'text-gray-100'
              }`}
            >
              {task.title}
            </h3>
            {task.is_complete && (
              <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-success-500/10 text-success-400 border border-success-500/20">
                ✓ Done
              </span>
            )}
          </div>

          {task.description && (
            <p className="mt-2 text-sm text-gray-400 line-clamp-2">{task.description}</p>
          )}

          <div className="mt-3 flex items-center gap-2 text-xs text-gray-500">
            <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <span>{new Date(task.created_at).toLocaleDateString()}</span>
          </div>

          <div className="mt-4 flex items-center gap-2">
            <Button
              variant="ghost"
              size="sm"
              onClick={onEdit}
              className="transform transition-none hover:scale-100 hover:shadow-none"
            >
              ✏️ Edit
            </Button>
            <Button
              variant="danger"
              size="sm"
              onClick={onDelete}
              className="transform transition-none hover:scale-100 hover:shadow-none"
            >
              🗑️ Delete
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}

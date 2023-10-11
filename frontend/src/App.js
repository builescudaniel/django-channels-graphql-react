import React from 'react';
import { ApolloProvider, useQuery, useApolloClient } from "@apollo/client";
import gql from 'graphql-tag';
import client from './apolloClient.js';
import './App.css';

import { useSubscription } from '@apollo/client';

const TASK_CREATED_SUBSCRIPTION = gql`
  subscription onTaskCreated {
    taskCreated {
      id
      title
      completed
    }
  }
`;

function TaskUpdates() {
  const client = useApolloClient();
  const { data, loading, error } = useSubscription(TASK_CREATED_SUBSCRIPTION);

  if (error) {
    console.error("Subscription error:", error);
  }

  if (loading) return <div></div>;

  if (data && data.taskCreated) {
    const newTask = data.taskCreated;

    // Try to read the tasks from cache
    const cacheData = client.readQuery({ query: GET_TASKS });

    // If the data exists in cache, update it
    if (cacheData && cacheData.allTasks) {
      // Check if the task is already in the cache
      const taskAlreadyExists = cacheData.allTasks.some(task => task.id === newTask.id);
      if (!taskAlreadyExists) {
        client.writeQuery({
          query: GET_TASKS,
          data: {
            allTasks: [...cacheData.allTasks, newTask],
          },
        });
      }
    }
  }

  return null;
}

const GET_TASKS = gql`
  query GetAllTasks {
    allTasks {
      id
      title
      completed
    }
  }
`;

function TaskList() {
  const { loading, error, data } = useQuery(GET_TASKS);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;

  const completedTasks = data.allTasks.filter(task => task.completed).length;

  return (
    <div className="task-list-container">
      <h2>
        Number of Tasks: {data.allTasks.length}, Tasks Completed: {completedTasks}
      </h2>
      <div className="task-scroll">
        {data.allTasks.map(task => (
          <div key={task.id} className={`task-item ${task.completed ? 'completed' : ''}`}>
            <h3>{task.title}</h3>
            <p>Completed: {task.completed ? 'Yes' : 'No'}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

function App() {
  return (
    <ApolloProvider client={client}>
      <div className="App">
        <header className="App-header">
          {/* ... existing content ... */}
          <TaskList />
          <TaskUpdates />
        </header>
      </div>
    </ApolloProvider>
  );
}

export default App;
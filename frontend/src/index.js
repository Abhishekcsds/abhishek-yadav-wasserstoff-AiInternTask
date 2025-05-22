// Import React core library
import React from 'react';
// Import the createRoot method from React DOM for React 18+ root rendering
import { createRoot } from 'react-dom/client';
// Import the main App component
import App from './App.js';
// Import global stylesheet
import './style.css';

// Create a root container using the DOM element with id 'root'
const root = createRoot(document.getElementById('root'));

// Render the App component wrapped in React.StrictMode for highlighting potential problems
root.render(
  React.createElement(
    React.StrictMode,
    null,
    React.createElement(App)
  )
);


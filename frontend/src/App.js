// Import React library
import React from 'react';
// Import the main Home page component
import Home from './pages/Home.jsx';

// Root component of the app
function App() {
  // Return a container div with Tailwind classes for min height and background color
  // Inside it, render the Home component using React.createElement syntax
  return React.createElement(
    'div',
    { className: 'min-h-screen bg-gray-50' },
    React.createElement(Home)
  );
}

// Export the App component as default export
export default App;

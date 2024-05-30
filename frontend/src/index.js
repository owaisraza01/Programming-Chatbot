import React from 'react';
import ReactDOM from 'react-dom';
import 'tailwindcss/tailwind.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import ChatInterface from './ChatInterface';

ReactDOM.render(
  <React.StrictMode>
    <ChatInterface /> {/* Render the ChatInterface component */}
  </React.StrictMode>,
  document.getElementById('root')
);

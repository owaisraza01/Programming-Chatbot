import React from 'react';
import "../../src/App.css"

const MessageDisplay = ({ messages }) => {
  return (
    <div className="message-display flex-grow overflow-y-auto p-4 bg-gray-100">
      {messages.map((message, index) => (
        <div
          key={index}
          className={`message ${message.isUser ? 'user' : 'response'} p-2 mb-2 rounded-md max-w-lg ${message.isUser ? 'self-end bg-green-500 text-white' : 'self-start bg-gray-300 text-black'}`}
        >
          {message.text}
        </div>
      ))}
    </div>
  );
};

export default MessageDisplay;

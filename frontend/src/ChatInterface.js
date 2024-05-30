import React, { useState } from 'react';
import MessageDisplay from './components/MessageDisplay';
import UserInput from './components/UserInput';
import ChatbotHeader from './components/chatbotheader';
import "../src/App.css"

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);

  const addMessage = (message, isUser = false) => {
    setMessages(prevMessages => [...prevMessages, { text: message, isUser }]);
  };

  return (
    <div className="chat-interface">
      <ChatbotHeader />
      <MessageDisplay messages={messages} />
      <UserInput addMessage={addMessage} />
    </div>
  );
};

export default ChatInterface;

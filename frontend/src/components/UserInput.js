import React, { useState } from 'react';
import { Input, Button } from 'reactstrap';
import { IoSend } from 'react-icons/io5';
import "../../src/App.css"
import axios from 'axios';

const UserInput = ({ addMessage }) => {
  const [inputValue, setInputValue] = useState('');

  const handleChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (inputValue.trim() !== '') {
      // Add query message to messages state
      addMessage(inputValue, true);

      try {
        // Send user query to backend
        const response = await axios.post('http://localhost:5000/programming/programmingchatbot', {
          query: inputValue
        });

        // Display response from backend
        addMessage(response.data.answer, false);

      } catch (error) {
        console.error('Error fetching response from server:', error);
        addMessage('Error fetching response from server.');
      }

      setInputValue('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="user-input-form flex items-center">
      <Input
        type="input"
        className='queryinput'
        value={inputValue}
        onChange={handleChange}
        onKeyPress={handleKeyPress}
        placeholder="Type your message..."
      />
      <Button type="submit" className="ml-2" color="success">
        <IoSend />
      </Button>
    </form>
  );
};

export default UserInput;

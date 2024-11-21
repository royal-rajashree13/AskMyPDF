import React from 'react';

const InputField = () => {
  return (
    <div style={{ marginTop: '20px' }}>
      <input type="text" placeholder="Type your message..." style={{ width: '80%', padding: '10px' }} />
      <button style={{ padding: '10px 20px', marginLeft: '10px', backgroundColor: '#007BFF', color: 'white', border: 'none' }}>
        Send
      </button>
    </div>
  );
};

export default InputField;

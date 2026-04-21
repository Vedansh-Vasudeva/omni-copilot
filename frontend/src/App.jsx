import React, { useState } from 'react';
import ChatInterface from './components/ChatInterface';

function App() {
  return (
    <div className="app-container">
      <header className="app-header">
        <div className="logo-container">
          <div className="logo"></div>
          <h1>Omni-Copilot</h1>
        </div>
        <div className="badge">MVP Version</div>
      </header>
      
      <main className="app-main">
        <ChatInterface />
      </main>
    </div>
  )
}

export default App;

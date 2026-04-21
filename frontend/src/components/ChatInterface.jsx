import React, { useState, useRef, useEffect } from 'react';
import AgentStep from './AgentStep';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      // Use environment variable for production deployment, fallback to localhost
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: 'default_user', message: input }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        throw new Error(errorData?.detail || "API Error");
      }
      
      const data = await response.json();
      
      setMessages(prev => [...prev, {
        role: 'bot',
        content: data.output,
        steps: data.intermediate_steps
      }]);
    } catch (error) {
      setMessages(prev => [...prev, {
        role: 'bot',
        content: `Error connecting to backend: ${error.message}`,
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="messages-area">
        {messages.length === 0 && (
          <div style={{ textAlign: 'center', color: 'var(--text-muted)', marginTop: '2rem' }}>
            <h2>Welcome to Omni-Copilot</h2>
            <p>I am your multi-agent assistant with persistent memory.</p>
          </div>
        )}
        
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            <div className="bubble">
              {msg.role === 'bot' && <strong>Omni-Copilot: </strong>}
              {msg.content}
            </div>
            
            {msg.steps && msg.steps.length > 0 && (
              <div className="reasoning-container">
                <div style={{fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.5rem'}}>
                  Agent Reasoning Trace:
                </div>
                {msg.steps.map((step, i) => (
                  <AgentStep key={i} step={step} />
                ))}
              </div>
            )}
          </div>
        ))}
        
        {isLoading && (
          <div className="message bot">
            <div className="bubble loading">
              Thinking
              <div className="dot-flashing"></div>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <div className="input-area">
        <input 
          type="text" 
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder="What would you like me to do?"
          disabled={isLoading}
        />
        <button onClick={handleSend} disabled={isLoading || !input.trim()}>
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatInterface;

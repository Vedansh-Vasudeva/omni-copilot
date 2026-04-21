import React from 'react';

const AgentStep = ({ step }) => {
  const formatResult = (res) => {
    if (typeof res === 'object') {
      return JSON.stringify(res, null, 2);
    }
    return res;
  };

  return (
    <div className="agent-step">
      <div className="header">
        <span className="name">{step.agent} Agent</span>
        <span className="action">{step.action || (step.tool_used ? `Tool: ${step.tool_used}` : 'Action')}</span>
      </div>
      {(step.result || step.step) && (
        <pre>
          {step.step && `Task: ${step.step}\n`}
          {step.result && `Output: ${formatResult(step.result)}`}
        </pre>
      )}
    </div>
  );
};

export default AgentStep;

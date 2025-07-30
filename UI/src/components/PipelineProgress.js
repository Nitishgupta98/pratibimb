// PipelineProgress.js - Enhanced Progress Component with Retry Functionality
import React, { useState, useEffect } from 'react';
import './PipelineProgress.css';

const PipelineProgress = ({ 
  steps, 
  onRetry, 
  isRunning, 
  onStop,
  downloadableFiles = [],
  onGenerateTelugu,
  onGenerateKannada,
  teluguState = {},
  kannadaState = {}
}) => {
  const [animatingStepId, setAnimatingStepId] = useState(null);

  // Animate step changes
  useEffect(() => {
    const latestStep = steps[steps.length - 1];
    if (latestStep && latestStep.status === 'processing') {
      setAnimatingStepId(latestStep.step);
      
      // Clear animation after delay
      const timer = setTimeout(() => {
        setAnimatingStepId(null);
      }, 1000);
      
      return () => clearTimeout(timer);
    }
  }, [steps]);

  const getStepStatus = (stepNumber) => {
    const step = steps.find(s => s.step === stepNumber);
    return step?.status || 'pending';
  };

  const getStepMessage = (stepNumber) => {
    const step = steps.find(s => s.step === stepNumber);
    return step?.message || '';
  };

  const getStepError = (stepNumber) => {
    const step = steps.find(s => s.step === stepNumber);
    return step?.error || '';
  };

  const isStepRetryable = (stepNumber) => {
    const step = steps.find(s => s.step === stepNumber);
    return step?.retryable === true;
  };

  const getStatusIcon = (status, stepNumber) => {
    switch (status) {
      case 'success':
        return '✅';
      case 'error':
        return '❌';
      case 'processing':
        return <div className="spinner" />;
      default:
        return <div className={`step-number ${animatingStepId === stepNumber ? 'animate' : ''}`}>
          {stepNumber}
        </div>;
    }
  };

  // Only show steps that have started (no placeholders)
  // Always use 13 as the total number of steps for progress accuracy
  const TOTAL_PIPELINE_STEPS = 13;
  const completedSteps = steps.filter(s => s.status === 'success').length;
  const getStepProgress = () => {
    // Progress is based on steps completed or currently processing
    const processingSteps = steps.filter(s => s.status === 'processing').length;
    return Math.round(((completedSteps + processingSteps * 0.5) / TOTAL_PIPELINE_STEPS) * 100);
  };
  const hasErrors = steps.some(s => s.status === 'error');
  const isComplete = steps.length === TOTAL_PIPELINE_STEPS && steps.every(s => s.status === 'success');
  const failedStep = steps.find(s => s.status === 'error');

  // Auto-scroll to the latest step as steps progress
  const stepsListRef = React.useRef(null);
  React.useEffect(() => {
    if (stepsListRef.current && steps.length > 0) {
      // Scroll to the bottom of the steps list
      stepsListRef.current.scrollTo({
        top: stepsListRef.current.scrollHeight,
        behavior: 'smooth'
      });
    }
  }, [steps.length]);

  return (
    <div className="pipeline-progress">
      {/* Progress Header */}
      <div className="progress-header">
        <h3>🔄 Braille Conversion Progress</h3>
        <div className="progress-stats">
          <span className="step-counter">
            {completedSteps} / {TOTAL_PIPELINE_STEPS} steps completed
          </span>
          <div className="progress-percentage">
            {getStepProgress()}%
          </div>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="progress-bar-container">
        <div 
          className="progress-bar" 
          style={{ width: `${getStepProgress()}%`, transition: 'width 0.5s cubic-bezier(0.4,0,0.2,1)' }}
        />
      </div>

      {/* Control Buttons */}
      {isRunning && (
        <div className="progress-controls">
          <button 
            onClick={onStop}
            className="stop-button"
          >
            ⏹️ Stop Processing
          </button>
        </div>
      )}

      {/* Steps List - only show steps that have started, and only one green tick per completed step */}
      <div className="steps-list" ref={stepsListRef} style={{ maxHeight: 400, overflowY: 'auto' }}>
        {steps.map((step, idx) => (
          <div 
            key={step.step}
            className={`step-item ${step.status} ${animatingStepId === step.step ? 'animating' : ''}`}
          >
            <div className="step-icon">
              {step.status === 'success' ? '' : getStatusIcon(step.status, step.step)}
            </div>
            <div className="step-content">
              <div className="step-message">
                {step.message || `Step ${step.step}: ${step.label || step.name}`}
              </div>
              {step.error && (
                <div className="step-error">
                  <span className="error-text">Error: {step.error}</span>
                  {step.retryable && (
                    <button 
                      onClick={() => onRetry(step.step)}
                      className="retry-button"
                      disabled={isRunning}
                    >
                      🔄 Retry from here
                    </button>
                  )}
                </div>
              )}
              {step.status === 'processing' && (
                <div className="step-processing">
                  <div className="processing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Error Summary */}
      {hasErrors && !isRunning && (
        <div className="error-summary">
          <h4>❌ Pipeline Failed</h4>
          <p>
            The pipeline failed at step {failedStep?.step}: {failedStep?.stepName}
          </p>
          <p className="error-message">
            {failedStep?.error}
          </p>
          {failedStep?.retryable && (
            <button 
              onClick={() => onRetry(failedStep.step)}
              className="retry-button-large"
            >
              🔄 Retry from Step {failedStep.step}
            </button>
          )}
        </div>
      )}

      {/* Success Summary and Language Braille Generation */}
      {isComplete && (
        <>
        <div className="success-summary">
          <h4>🎉 Pipeline Completed Successfully!</h4>
          <p>
            Your YouTube video has been successfully converted to Braille format.
            You can now download the generated files below.
          </p>
        </div>
        <div className="lang-braille-actions" style={{ margin: '2rem 0', display: 'flex', gap: '2rem', justifyContent: 'center' }}>
          {/* Telugu Braille Button/Spinner/Downloads */}
          <div>
            {teluguState.status === 'idle' && (
              <button className="lang-braille-btn" onClick={onGenerateTelugu} disabled={teluguState.status === 'loading'}>
                Generate Telugu Braille
              </button>
            )}
            {teluguState.status === 'loading' && (
              <div className="lang-braille-spinner">Generating Telugu Braille...</div>
            )}
            {teluguState.status === 'done' && teluguState.files && (
              <div className="lang-braille-downloads">
                <h5>Telugu Braille Files</h5>
                {teluguState.files.map((file, idx) => (
                  <button key={idx} className="download-button" onClick={() => downloadFile(file)}>
                    📄 Download {file.name}
                  </button>
                ))}
              </div>
            )}
            {teluguState.status === 'error' && (
              <div className="lang-braille-error">{teluguState.error}</div>
            )}
          </div>
          {/* Kannada Braille Button/Spinner/Downloads */}
          <div>
            {kannadaState.status === 'idle' && (
              <button className="lang-braille-btn" onClick={onGenerateKannada} disabled={kannadaState.status === 'loading'}>
                Generate Kannada Braille
              </button>
            )}
            {kannadaState.status === 'loading' && (
              <div className="lang-braille-spinner">Generating Kannada Braille...</div>
            )}
            {kannadaState.status === 'done' && kannadaState.files && (
              <div className="lang-braille-downloads">
                <h5>Kannada Braille Files</h5>
                {kannadaState.files.map((file, idx) => (
                  <button key={idx} className="download-button" onClick={() => downloadFile(file)}>
                    📄 Download {file.name}
                  </button>
                ))}
              </div>
            )}
            {kannadaState.status === 'error' && (
              <div className="lang-braille-error">{kannadaState.error}</div>
            )}
          </div>
        </div>
        </>
      )}

      {/* Download Section */}
      {downloadableFiles.length > 0 && (
        <div className="download-section">
          <h4>📥 Download Generated Files</h4>
          <div className="download-grid">
            {downloadableFiles.map((file, index) => (
              <div key={index} className="download-item">
                <div className="file-info">
                  <span className="file-name">{file.name}</span>
                  <span className="file-size">
                    {(file.size / 1024).toFixed(1)} KB
                  </span>
                </div>
                <button 
                  onClick={() => downloadFile(file)}
                  className="download-button"
                >
                  📄 Download
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

// Helper function to download file content
const downloadFile = (file) => {
  const blob = new Blob([file.content], { type: file.type });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${file.name.replace(/\s+/g, '_')}.txt`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
};

export default PipelineProgress;

import React from 'react';
import './LoadingSpinner.css';

const LoadingSpinner = ({ message = "Processing your request..." }) => {
  return (
    <div className="loading-spinner-container">
      <div className="loading-spinner">
        <div className="simple-spinner"></div>
        <div className="loading-message">
          <p>{message}</p>
          <div className="loading-dots">
            <span>.</span>
            <span>.</span>
            <span>.</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoadingSpinner;

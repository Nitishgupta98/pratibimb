import React from 'react';
import './LoadingSpinner.css';

const LoadingSpinner = ({ message = "" }) => {
  return (
    <div className="loading-spinner-container">
      <div className="loading-spinner">
        <div className="simple-spinner"></div>
        <div className="loading-message">
          <p>{message}</p>
          
          
        </div>
      </div>
    </div>
  );
};

export default LoadingSpinner;

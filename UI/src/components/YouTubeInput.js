import React, { useState } from 'react';
import './YouTubeInput.css';

const YouTubeInput = ({ onSubmit, isLoading, onUrlChange }) => {
  const [url, setUrl] = useState('');
  const [isValid, setIsValid] = useState(false);

  const validateYouTubeUrl = (url) => {
    const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/|youtube\.com\/v\/)[a-zA-Z0-9_-]{11}/;
    return youtubeRegex.test(url);
  };

  const handleUrlChange = (e) => {
    const newUrl = e.target.value.trim();
    setUrl(newUrl);
    
    const valid = validateYouTubeUrl(newUrl);
    setIsValid(valid);
    
    if (onUrlChange) {
      onUrlChange(newUrl, valid);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (isValid && !isLoading && onSubmit) {
      onSubmit(url);
    }
  };

  const handlePaste = (e) => {
    // Handle paste event
    setTimeout(() => {
      const pastedUrl = e.target.value.trim();
      setUrl(pastedUrl);
      const valid = validateYouTubeUrl(pastedUrl);
      setIsValid(valid);
      if (onUrlChange) {
        onUrlChange(pastedUrl, valid);
      }
    }, 10);
  };

  return (
    <div className="youtube-input">
      <form onSubmit={handleSubmit} className="youtube-form">
        <div className="input-group">
          <div className="input-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M22.54 6.42C22.265 5.432 21.568 4.735 20.58 4.46C18.88 4 12 4 12 4S5.12 4 3.42 4.46C2.432 4.735 1.735 5.432 1.46 6.42C1 8.12 1 12 1 12S1 15.88 1.46 17.58C1.735 18.568 2.432 19.265 3.42 19.54C5.12 20 12 20 12 20S18.88 20 20.58 19.54C21.568 19.265 22.265 18.568 22.54 17.58C23 15.88 23 12 23 12S23 8.12 22.54 6.42Z" fill="#FF0000"/>
              <path d="M9.75 15.02L15.5 12L9.75 8.98V15.02Z" fill="white"/>
            </svg>
          </div>
          <input
            type="url"
            value={url}
            onChange={handleUrlChange}
            onPaste={handlePaste}
            placeholder="https://www.youtube.com/watch?v=..."
            className={`youtube-url-input ${isValid ? 'valid' : ''} ${url && !isValid ? 'invalid' : ''}`}
            disabled={isLoading}
            aria-label="YouTube URL"
            autoComplete="off"
          />
          {url && (
            <div className={`validation-indicator ${isValid ? 'valid' : 'invalid'}`}>
              {isValid ? '✓' : '✗'}
            </div>
          )}
        </div>
        
        {url && !isValid && (
          <div className="validation-message error">
            Please enter a valid YouTube URL
          </div>
        )}
        
        {isValid && (
          <div className="validation-message success">
            ✓ Valid YouTube URL detected
          </div>
        )}
        
        <div className="input-help">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M18 13V6C18 4.895 17.105 4 16 4H8C6.895 4 6 4.895 6 6V13" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            <path d="M15 11V18C15 19.105 14.105 20 13 20H11C9.895 20 9 19.105 9 18V11" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            <path d="M18 13L19 14L22 11" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
          <span>Paste any YouTube video URL to convert its transcript to Braille</span>
        </div>
      </form>
    </div>
  );
};

export default YouTubeInput;

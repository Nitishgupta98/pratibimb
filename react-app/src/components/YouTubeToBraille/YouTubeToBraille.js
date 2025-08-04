import React, { useState } from 'react';
import './YouTubeToBraille.css';

const YouTubeToBraille = () => {
  const [youtubeUrl, setYoutubeUrl] = useState('');
  const [isConverting, setIsConverting] = useState(false);
  const [progress, setProgress] = useState(0);
  const [results, setResults] = useState(null);
  const [activeTab, setActiveTab] = useState('transcript');

  const handleConvert = async () => {
    if (!youtubeUrl) return;
    
    setIsConverting(true);
    setProgress(0);
    
    // Simulate conversion progress
    const progressInterval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(progressInterval);
          setIsConverting(false);
          setResults({
            transcript: 'Sample transcript content from YouTube video...',
            braille: '⠞⠓⠊⠎ ⠊⠎ ⠁ ⠎⠁⠍⠏⠇⠑ ⠃⠗⠁⠊⠇⠇⠑ ⠞⠗⠁⠝⠎⠉⠗⠊⠏⠞⠊⠕⠝',
            videoTitle: 'Sample YouTube Video Title'
          });
          return 100;
        }
        return prev + 10;
      });
    }, 200);
  };

  const handleDownload = (type) => {
    const content = type === 'transcript' ? results.transcript : results.braille;
    const filename = `${results.videoTitle}_${type}.txt`;
    
    const element = document.createElement('a');
    const file = new Blob([content], { type: 'text/plain' });
    element.href = URL.createObjectURL(file);
    element.download = filename;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  return (
    <div className="youtube-converter">
      <div className="converter-header">
        <h2><i className="fab fa-youtube"></i> YouTube Videos Made Accessible!</h2>
        <p>Convert YouTube videos to Braille format instantly</p>
      </div>
      
      <div className="converter-form">
        <div className="input-group">
          <div className="input-wrapper">
            <i className="fab fa-youtube input-icon"></i>
            <input 
              type="url" 
              value={youtubeUrl}
              onChange={(e) => setYoutubeUrl(e.target.value)}
              placeholder="Enter YouTube URL (e.g., https://www.youtube.com/watch?v=example)"
              className="url-input"
              disabled={isConverting}
            />
            <button 
              type="button" 
              className="convert-btn" 
              onClick={handleConvert}
              disabled={isConverting || !youtubeUrl}
            >
              <i className="fas fa-magic"></i>
              {isConverting ? 'Converting...' : 'Convert to Braille'}
            </button>
          </div>
        </div>
      </div>

      {isConverting && (
        <div className="progress-container">
          <div className="progress-bar">
            <div className="progress-fill" style={{ width: `${progress}%` }}></div>
          </div>
          <div className="progress-text">Processing... {progress}%</div>
        </div>
      )}

      {results && (
        <div className="results-area">
          <div className="result-tabs">
            <button 
              className={`tab-btn ${activeTab === 'transcript' ? 'active' : ''}`}
              onClick={() => setActiveTab('transcript')}
            >
              <i className="fas fa-download"></i> Download Transcript
            </button>
            <button 
              className={`tab-btn ${activeTab === 'preview' ? 'active' : ''}`}
              onClick={() => setActiveTab('preview')}
            >
              <i className="fas fa-eye"></i> Process Transcript
            </button>
            <button 
              className={`tab-btn ${activeTab === 'braille' ? 'active' : ''}`}
              onClick={() => setActiveTab('braille')}
            >
              <i className="fas fa-braille"></i> Braille Output
            </button>
          </div>

          <div className="tab-content">
            {activeTab === 'transcript' && (
              <div className="transcript-tab">
                <div className="content-box">
                  <h3>Video Transcript</h3>
                  <textarea 
                    value={results.transcript} 
                    readOnly 
                    className="transcript-content"
                  />
                  <button 
                    className="download-btn"
                    onClick={() => handleDownload('transcript')}
                  >
                    <i className="fas fa-download"></i> Download Transcript
                  </button>
                </div>
              </div>
            )}
            
            {activeTab === 'preview' && (
              <div className="preview-tab">
                <div className="content-box">
                  <h3>Processing Options</h3>
                  <div className="processing-options">
                    <label className="option">
                      <input type="checkbox" defaultChecked />
                      <span>Remove timestamps</span>
                    </label>
                    <label className="option">
                      <input type="checkbox" defaultChecked />
                      <span>Clean formatting</span>
                    </label>
                    <label className="option">
                      <input type="checkbox" />
                      <span>Add punctuation</span>
                    </label>
                  </div>
                  <button className="process-btn">
                    <i className="fas fa-cogs"></i> Process Transcript
                  </button>
                </div>
              </div>
            )}
            
            {activeTab === 'braille' && (
              <div className="braille-tab">
                <div className="content-box">
                  <h3>Braille Output</h3>
                  <textarea 
                    value={results.braille} 
                    readOnly 
                    className="braille-content"
                  />
                  <button 
                    className="download-btn"
                    onClick={() => handleDownload('braille')}
                  >
                    <i className="fas fa-download"></i> Download Braille
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default YouTubeToBraille;

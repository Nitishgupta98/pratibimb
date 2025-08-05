import React, { useState } from 'react';
import './YoutubeToBraille.css';

const YoutubeToBraille = () => {
  const [youtubeUrl, setYoutubeUrl] = useState('');
  const [brailleGrade, setBrailleGrade] = useState('grade1');
  const [outputFormat, setOutputFormat] = useState('text');
  const [isConverting, setIsConverting] = useState(false);
  const [convertedContent, setConvertedContent] = useState('');

  const handleConvert = async () => {
    if (!youtubeUrl.trim()) {
      alert('Please enter a YouTube URL');
      return;
    }

    setIsConverting(true);
    
    // Simulate conversion process
    setTimeout(() => {
      setConvertedContent(`⠠⠽⠕⠥⠞⠥⠃⠑ ⠞⠗⠁⠝⠎⠉⠗⠊⠏⠞ ⠉⠕⠝⠧⠑⠗⠞⠑⠙ ⠞⠕ ⠠⠃⠗⠁⠊⠇⠇⠑

⠠⠞⠓⠊⠎ ⠊⠎ ⠁ ⠎⠁⠍⠏⠇⠑ ⠉⠕⠝⠧⠑⠗⠞⠑⠙ ⠞⠗⠁⠝⠎⠉⠗⠊⠏⠞ ⠋⠗⠕⠍ ⠽⠕⠥⠗ ⠠⠽⠕⠥⠞⠥⠃⠑ ⠧⠊⠙⠑⠕⠲

⠠⠞⠓⠑ ⠞⠗⠁⠝⠎⠉⠗⠊⠏⠞ ⠓⠁⠎ ⠃⠑⠑⠝ ⠁⠥⠞⠕⠍⠁⠞⠊⠉⠁⠇⠇⠽ ⠑⠭⠞⠗⠁⠉⠞⠑⠙ ⠁⠝⠙ ⠉⠕⠝⠧⠑⠗⠞⠑⠙ ⠞⠕ ${brailleGrade === 'grade1' ? '⠠⠛⠗⠁⠙⠑ ⠼⠁' : '⠠⠛⠗⠁⠙⠑ ⠼⠃'} ⠠⠃⠗⠁⠊⠇⠇⠑⠲`);
      setIsConverting(false);
    }, 3000);
  };

  const downloadFile = () => {
    if (!convertedContent) return;

    const blob = new Blob([convertedContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `youtube_transcript.${outputFormat}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="youtube-to-braille">
      <div className="page-header">
        <h1><i className="fab fa-youtube"></i> YouTube Videos Made Accessible!</h1>
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
            />
            <button 
              type="button" 
              className="convert-btn" 
              onClick={handleConvert}
              disabled={isConverting}
            >
              <i className="fas fa-magic"></i>
              Convert to Braille
            </button>
          </div>
        </div>

        <div className="conversion-settings">
          <div className="setting-group">
            <label htmlFor="brailleGrade">Braille Grade:</label>
            <select 
              id="brailleGrade"
              value={brailleGrade}
              onChange={(e) => setBrailleGrade(e.target.value)}
            >
              <option value="grade1">Grade 1 Braille</option>
              <option value="grade2">Grade 2 Braille</option>
            </select>
          </div>
          <div className="setting-group">
            <label htmlFor="outputFormat">Output Format:</label>
            <select 
              id="outputFormat"
              value={outputFormat}
              onChange={(e) => setOutputFormat(e.target.value)}
            >
              <option value="text">Text (.txt)</option>
              <option value="brf">BRF (.brf)</option>
              <option value="brl">BRL (.brl)</option>
            </select>
          </div>
        </div>
      </div>

      {/* Progress Indicator */}
      {isConverting && (
        <div className="progress-container">
          <div className="progress-bar">
            <div className="progress-fill"></div>
          </div>
          <div className="progress-text">Processing YouTube video...</div>
        </div>
      )}

      {/* Results Area */}
      {convertedContent && !isConverting && (
        <div className="results-area">
          <div className="conversion-preview">
            <div className="preview-header">
              <h3><i className="fas fa-braille"></i> Braille Output</h3>
              <button 
                className="download-btn"
                onClick={downloadFile}
              >
                <i className="fas fa-download"></i>
                Download
              </button>
            </div>
            <div className="preview-content braille-text">
              {convertedContent}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default YoutubeToBraille;

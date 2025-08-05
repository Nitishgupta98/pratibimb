import React, { useState } from 'react';
import './YoutubeToBraille.css';

const YoutubeToBraille = () => {
  const [youtubeUrl, setYoutubeUrl] = useState('');
  const [brailleGrade, setBrailleGrade] = useState('grade1');
  const [outputFormat, setOutputFormat] = useState('text');
  const [isConverting, setIsConverting] = useState(false);
  const [convertedContent, setConvertedContent] = useState('');
  const [activeTab, setActiveTab] = useState('transcript');
  const [rawTranscript, setRawTranscript] = useState('');
  const [brailleOutput, setBrailleOutput] = useState('');
  const [embosserFormat, setEmbosserFormat] = useState('');

  const handleConvert = async () => {
    if (!youtubeUrl.trim()) {
      alert('Please enter a YouTube URL');
      return;
    }

    setIsConverting(true);
    
    // Simulate conversion process
    setTimeout(() => {
      const transcript = `Youtube Transcript:

The Moon goes through phases
Okay, I'm getting everything ready for this lesson!
Awesome!
I can't wait because we get to talk about the moon again!
I know we've done that already,
but that video was about the moon in general.
We want to have a whole video about the phases of the moon!
The phases of the moon!
Ever wonder why sometimes the moon looks like this,
and you might think, "Hey, that's just what the moon looks like!"
And other times, the moon might look like a complete circle.
What's going on?
Well, the moon goes through phases.

... [Sample transcript content] ...`;

      const braille = `⠠⠞⠓⠑ ⠠⠍⠕⠕⠝ ⠛⠕⠑⠎ ⠞⠓⠗⠕⠥⠛⠓ ⠏⠓⠁⠎⠑⠎

⠠⠕⠅⠁⠽⠂ ⠠⠊⠄⠍ ⠛⠑⠞⠞⠊⠝⠛ ⠑⠧⠑⠗⠽⠞⠓⠊⠝⠛ ⠗⠑⠁⠙⠽ ⠋⠕⠗ ⠞⠓⠊⠎ ⠇⠑⠎⠎⠕⠝⠖
⠠⠁⠺⠑⠎⠕⠍⠑⠖
⠠⠊ ⠉⠁⠝⠄⠞ ⠺⠁⠊⠞ ⠃⠑⠉⠁⠥⠎⠑ ⠺⠑ ⠛⠑⠞ ⠞⠕ ⠞⠁⠇⠅ ⠁⠃⠕⠥⠞ ⠞⠓⠑ ⠍⠕⠕⠝ ⠁⠛⠁⠊⠝⠖`;

      const embosser = `,THE ,MOON GOES THROUGH PHASES

,OKAY1 ,'M GETTING EVERY?+ READY = ? LESSON6
,A:SO[6
, CAN'T WAIT 2C 7 GET TO TALK AB ! MOON AGA9`;

      setRawTranscript(transcript);
      setBrailleOutput(braille);
      setEmbosserFormat(embosser);
      setConvertedContent(transcript);
      setIsConverting(false);
      setActiveTab('transcript');
    }, 3000);
  };

  const copyToClipboard = () => {
    const content = getActiveTabContent();
    navigator.clipboard.writeText(content).then(() => {
      alert('Content copied to clipboard!');
    });
  };

  const downloadFile = () => {
    const content = getActiveTabContent();
    if (!content) return;

    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `youtube_${activeTab}.${outputFormat}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const getActiveTabContent = () => {
    switch (activeTab) {
      case 'transcript':
        return rawTranscript;
      case 'process':
        return rawTranscript;
      case 'braille':
        return brailleOutput;
      case 'embosser':
        return embosserFormat;
      default:
        return '';
    }
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
              placeholder="www.youtube.com/watch?v=wz01pTvuMa0&t=6s"
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
          <div className="result-tabs">
            <button 
              className={`tab-btn ${activeTab === 'transcript' ? 'active' : ''}`}
              onClick={() => setActiveTab('transcript')}
            >
              <i className="fas fa-download"></i> Download Transcript
            </button>
            <button 
              className={`tab-btn ${activeTab === 'process' ? 'active' : ''}`}
              onClick={() => setActiveTab('process')}
            >
              <i className="fas fa-eye"></i> Process Transcript
            </button>
            <button 
              className={`tab-btn ${activeTab === 'braille' ? 'active' : ''}`}
              onClick={() => setActiveTab('braille')}
            >
              <i className="fas fa-braille"></i> Braille Output
            </button>
            <button 
              className={`tab-btn ${activeTab === 'embosser' ? 'active' : ''}`}
              onClick={() => setActiveTab('embosser')}
            >
              <i className="fas fa-print"></i> Embosser Format
            </button>
          </div>
          
          <div className="tab-content">
            <div className="tab-panel active">
              <div className="result-header">
                <h3>
                  <i className="fas fa-file-alt"></i> 
                  {activeTab === 'transcript' && 'Raw Transcript'}
                  {activeTab === 'process' && 'Process Transcript'}
                  {activeTab === 'braille' && 'Braille Output'}
                  {activeTab === 'embosser' && 'Embosser Format'}
                </h3>
                <div className="result-actions">
                  <button className="action-btn" onClick={copyToClipboard}>
                    <i className="fas fa-copy"></i> Copy
                  </button>
                  <button className="action-btn" onClick={downloadFile}>
                    <i className="fas fa-download"></i> Download
                  </button>
                </div>
              </div>
              <div className={`result-content ${activeTab === 'braille' ? 'braille-text' : 'transcript-content'}`}>
                <div className="transcript-text">
                  {getActiveTabContent()}
                </div>
              </div>
            </div>
          </div>

          {/* Statistics */}
          <div className="quick-stats">
            <div className="stats-grid">
              <div className="stat-item">
                <i className="fas fa-clock"></i>
                <div>
                  <strong>8:32</strong>
                  <div>DURATION</div>
                </div>
              </div>
              <div className="stat-item">
                <i className="fas fa-font"></i>
                <div>
                  <strong>2,847</strong>
                  <div>CHARACTERS</div>
                </div>
              </div>
              <div className="stat-item">
                <i className="fas fa-file-word"></i>
                <div>
                  <strong>524</strong>
                  <div>WORDS</div>
                </div>
              </div>
              <div className="stat-item">
                <i className="fas fa-braille"></i>
                <div>
                  <strong>3,156</strong>
                  <div>BRAILLE CHARACTERS</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default YoutubeToBraille;

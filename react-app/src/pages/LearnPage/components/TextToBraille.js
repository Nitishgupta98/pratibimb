import React, { useState } from 'react';
import './TextToBraille.css';

const TextToBraille = () => {
  const [inputText, setInputText] = useState('');
  const [brailleOutput, setBrailleOutput] = useState('');
  const [brfOutput, setBrfOutput] = useState('');
  const [isConverting, setIsConverting] = useState(false);
  const [activeTab, setActiveTab] = useState('braille');
  const [settings, setSettings] = useState({
    grade: 'grade1',
    format: 'text',
    layout: 'standard'
  });

  // Simple Braille conversion mapping
  const brailleMap = {
    'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑', 'f': '⠋', 'g': '⠛', 'h': '⠓',
    'i': '⠊', 'j': '⠚', 'k': '⠅', 'l': '⠇', 'm': '⠍', 'n': '⠝', 'o': '⠕', 'p': '⠏',
    'q': '⠟', 'r': '⠗', 's': '⠎', 't': '⠞', 'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭',
    'y': '⠽', 'z': '⠵', ' ': ' ', '.': '⠲', ',': '⠂', '?': '⠦', '!': '⠖', ';': '⠆',
    ':': '⠒', '-': '⠤', '(': '⠐⠣', ')': '⠐⠜', '"': '⠐⠦', "'": '⠐⠄'
  };

  const convertToBraille = () => {
    setIsConverting(true);
    
    setTimeout(() => {
      // Convert to Unicode Braille
      const brailleText = inputText.toLowerCase().split('').map(char => 
        brailleMap[char] || char
      ).join('');
      
      // Generate BRF format (simplified)
      const brfText = brailleText.replace(/⠁/g, 'A').replace(/⠃/g, 'B').replace(/⠉/g, 'C')
        .replace(/⠙/g, 'D').replace(/⠑/g, 'E').replace(/⠋/g, 'F').replace(/⠛/g, 'G')
        .replace(/⠓/g, 'H').replace(/⠊/g, 'I').replace(/⠚/g, 'J').replace(/⠅/g, 'K')
        .replace(/⠇/g, 'L').replace(/⠍/g, 'M').replace(/⠝/g, 'N').replace(/⠕/g, 'O')
        .replace(/⠏/g, 'P').replace(/⠟/g, 'Q').replace(/⠗/g, 'R').replace(/⠎/g, 'S')
        .replace(/⠞/g, 'T').replace(/⠥/g, 'U').replace(/⠧/g, 'V').replace(/⠺/g, 'W')
        .replace(/⠭/g, 'X').replace(/⠽/g, 'Y').replace(/⠵/g, 'Z').replace(/⠲/g, '4')
        .replace(/⠂/g, '1');
      
      setBrailleOutput(brailleText);
      setBrfOutput(brfText);
      setIsConverting(false);
    }, 1000);
  };

  const downloadFile = (content, filename, type = 'text/plain') => {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text).then(() => {
      alert('Content copied to clipboard!');
    });
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setInputText(e.target.result);
      };
      reader.readAsText(file);
    }
  };

  const getStats = () => {
    return {
      characters: inputText.length,
      words: inputText.trim() ? inputText.trim().split(/\s+/).length : 0,
      lines: inputText.split('\n').length,
      brailleChars: brailleOutput.length
    };
  };

  const stats = getStats();

  return (
    <div className="text-to-braille">
      <div className="page-header">
        <h1><i className="fas fa-font"></i> Text to Braille Converter</h1>
        <p>Convert any text document to Braille format with various output options</p>
      </div>

      <div className="converter-interface">
        <div className="input-panel">
          <div className="section-header">
            <h3><i className="fas fa-edit"></i> Input Text</h3>
            <div className="text-stats">
              {stats.words} words, {stats.characters} characters
            </div>
          </div>
          
          <textarea 
            placeholder="Type or paste your text here..."
            className="text-input"
            rows="10"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
          />
          
          <div className="input-options">
            <input
              type="file"
              accept=".txt,.doc,.docx"
              onChange={handleFileUpload}
              style={{ display: 'none' }}
              id="file-upload"
            />
            <label htmlFor="file-upload" className="option-btn">
              <i className="fas fa-upload"></i> Upload File
            </label>
            <button className="option-btn" onClick={() => setInputText('')}>
              <i className="fas fa-trash"></i> Clear
            </button>
          </div>
        </div>

        <div className="conversion-settings">
          <h3><i className="fas fa-cog"></i> Conversion Settings</h3>
          
          <div className="setting-group">
            <label>Braille Grade</label>
            <select 
              className="setting-select"
              value={settings.grade}
              onChange={(e) => setSettings({...settings, grade: e.target.value})}
            >
              <option value="grade1">Grade 1 (Uncontracted)</option>
              <option value="grade2">Grade 2 (Contracted)</option>
            </select>
          </div>

          <div className="setting-group">
            <label>Output Format</label>
            <select 
              className="setting-select"
              value={settings.format}
              onChange={(e) => setSettings({...settings, format: e.target.value})}
            >
              <option value="text">Text (.txt)</option>
              <option value="brf">Braille Ready Format (.brf)</option>
              <option value="brl">Braille (.brl)</option>
            </select>
          </div>

          <div className="setting-group">
            <label>Page Layout</label>
            <select 
              className="setting-select"
              value={settings.layout}
              onChange={(e) => setSettings({...settings, layout: e.target.value})}
            >
              <option value="standard">Standard (40x25)</option>
              <option value="compact">Compact (32x25)</option>
              <option value="large">Large Print (25x20)</option>
            </select>
          </div>

          <button 
            className="convert-btn"
            onClick={convertToBraille}
            disabled={!inputText.trim() || isConverting}
          >
            {isConverting ? (
              <>
                <i className="fas fa-spinner fa-spin"></i>
                Converting...
              </>
            ) : (
              <>
                <i className="fas fa-exchange-alt"></i>
                Convert to Braille
              </>
            )}
          </button>
        </div>

        <div className="output-panel">
          <div className="section-header">
            <h3><i className="fas fa-eye"></i> Braille Output</h3>
            <div className="output-stats">
              {stats.brailleChars} Braille characters
            </div>
          </div>

          <div className="output-tabs">
            <div className="tab-buttons">
              <button 
                className={`tab-btn ${activeTab === 'braille' ? 'active' : ''}`}
                onClick={() => setActiveTab('braille')}
              >
                <i className="fas fa-braille"></i> Unicode Braille
              </button>
              <button 
                className={`tab-btn ${activeTab === 'brf' ? 'active' : ''}`}
                onClick={() => setActiveTab('brf')}
              >
                <i className="fas fa-file-alt"></i> BRF Format
              </button>
            </div>

            <div className="tab-content">
              <div className={`tab-pane ${activeTab === 'braille' ? 'active' : ''}`}>
                <div className="braille-output">
                  {brailleOutput || 'Your converted Braille text will appear here...'}
                </div>
              </div>
              <div className={`tab-pane ${activeTab === 'brf' ? 'active' : ''}`}>
                <div className="brf-output">
                  {brfOutput || 'Your BRF format output will appear here...'}
                </div>
              </div>
            </div>
          </div>
          
          {(brailleOutput || brfOutput) && (
            <div className="output-actions">
              <button 
                className="action-btn"
                onClick={() => downloadFile(
                  activeTab === 'braille' ? brailleOutput : brfOutput,
                  `converted_text.${activeTab === 'braille' ? 'txt' : 'brf'}`
                )}
              >
                <i className="fas fa-download"></i> Download
              </button>
              <button 
                className="action-btn"
                onClick={() => copyToClipboard(activeTab === 'braille' ? brailleOutput : brfOutput)}
              >
                <i className="fas fa-copy"></i> Copy
              </button>
              <button 
                className="action-btn"
                onClick={() => window.print()}
              >
                <i className="fas fa-print"></i> Print
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Statistics Section */}
      <div className="stats-section">
        <h3><i className="fas fa-chart-bar"></i> Conversion Statistics</h3>
        <div className="stats-grid">
          <div className="stat-item">
            <div className="stat-label">Words</div>
            <div className="stat-value">{stats.words}</div>
          </div>
          <div className="stat-item">
            <div className="stat-label">Characters</div>
            <div className="stat-value">{stats.characters}</div>
          </div>
          <div className="stat-item">
            <div className="stat-label">Lines</div>
            <div className="stat-value">{stats.lines}</div>
          </div>
          <div className="stat-item">
            <div className="stat-label">Braille Characters</div>
            <div className="stat-value">{stats.brailleChars}</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TextToBraille;

import React, { useState } from 'react';
import './TextToBraille.css';

const TextToBraille = () => {
  const [inputText, setInputText] = useState('');
  const [brailleOutput, setBrailleOutput] = useState('');
  const [isGrade2, setIsGrade2] = useState(false);

  // Simple braille mapping (Grade 1)
  const brailleMap = {
    'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑', 'f': '⠋', 'g': '⠛', 'h': '⠓', 
    'i': '⠊', 'j': '⠚', 'k': '⠅', 'l': '⠇', 'm': '⠍', 'n': '⠝', 'o': '⠕', 'p': '⠏',
    'q': '⠟', 'r': '⠗', 's': '⠎', 't': '⠞', 'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭',
    'y': '⠽', 'z': '⠵', ' ': '⠀', '.': '⠲', ',': '⠂', '?': '⠦', '!': '⠖', ';': '⠆',
    ':': '⠒', '-': '⠤', '\'': '⠄', '"': '⠦', '(': '⠐⠣', ')': '⠐⠜', '1': '⠁', '2': '⠃',
    '3': '⠉', '4': '⠙', '5': '⠑', '6': '⠋', '7': '⠛', '8': '⠓', '9': '⠊', '0': '⠚'
  };

  const convertToBraille = () => {
    if (!inputText.trim()) {
      setBrailleOutput('');
      return;
    }

    const converted = inputText.toLowerCase().split('').map(char => {
      return brailleMap[char] || char;
    }).join('');

    setBrailleOutput(converted);
  };

  const clearAll = () => {
    setInputText('');
    setBrailleOutput('');
  };

  const downloadBraille = () => {
    if (!brailleOutput) return;
    
    const element = document.createElement('a');
    const file = new Blob([brailleOutput], { type: 'text/plain' });
    element.href = URL.createObjectURL(file);
    element.download = 'braille_text.txt';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  const copyToClipboard = () => {
    if (!brailleOutput) return;
    
    navigator.clipboard.writeText(brailleOutput).then(() => {
      // Could add a toast notification here
      console.log('Braille text copied to clipboard');
    });
  };

  return (
    <div className="text-to-braille">
      <div className="converter-header">
        <h2><i className="fas fa-font"></i> Text to Braille Converter</h2>
        <p>Convert any text to Braille notation instantly</p>
      </div>

      <div className="converter-container">
        <div className="input-section">
          <div className="input-header">
            <h3><i className="fas fa-keyboard"></i> Input Text</h3>
            <div className="conversion-options">
              <label className="option">
                <input 
                  type="checkbox" 
                  checked={isGrade2}
                  onChange={(e) => setIsGrade2(e.target.checked)}
                />
                <span>Use Grade 2 Braille (Contracted)</span>
              </label>
            </div>
          </div>
          
          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Type or paste your text here..."
            className="text-input"
            rows="10"
          />
          
          <div className="input-actions">
            <button 
              className="convert-btn"
              onClick={convertToBraille}
              disabled={!inputText.trim()}
            >
              <i className="fas fa-exchange-alt"></i>
              Convert to Braille
            </button>
            <button className="clear-btn" onClick={clearAll}>
              <i className="fas fa-trash"></i>
              Clear All
            </button>
          </div>
        </div>

        <div className="output-section">
          <div className="output-header">
            <h3><i className="fas fa-braille"></i> Braille Output</h3>
            {brailleOutput && (
              <div className="output-actions">
                <button className="copy-btn" onClick={copyToClipboard}>
                  <i className="fas fa-copy"></i>
                  Copy
                </button>
                <button className="download-btn" onClick={downloadBraille}>
                  <i className="fas fa-download"></i>
                  Download
                </button>
              </div>
            )}
          </div>
          
          <div className="braille-display">
            {brailleOutput ? (
              <pre className="braille-text">{brailleOutput}</pre>
            ) : (
              <div className="empty-output">
                <i className="fas fa-braille"></i>
                <p>Converted Braille text will appear here</p>
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="info-section">
        <h3><i className="fas fa-info-circle"></i> About Braille</h3>
        <div className="info-content">
          <div className="info-item">
            <h4>Grade 1 Braille (Uncontracted)</h4>
            <p>Each letter is represented by its own unique pattern of dots. Perfect for beginners and technical content.</p>
          </div>
          <div className="info-item">
            <h4>Grade 2 Braille (Contracted)</h4>
            <p>Uses contractions and abbreviations to save space. Commonly used in books and longer texts.</p>
          </div>
          <div className="info-item">
            <h4>Braille Cell</h4>
            <p>Each character is formed within a cell of six dots, arranged in two columns of three dots each.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TextToBraille;

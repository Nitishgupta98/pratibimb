import React, { useState, useRef } from 'react';
import './BrailleArtEditor.css';

const BrailleArtEditor = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [brailleArt, setBrailleArt] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [dimensions, setDimensions] = useState({ width: 40, height: 25 });
  const [contrast, setContrast] = useState(50);
  const [brightness, setBrightness] = useState(50);
  const fileInputRef = useRef(null);

  const brailleChars = [
    '⠀', '⠁', '⠂', '⠃', '⠄', '⠅', '⠆', '⠇', '⠈', '⠉', '⠊', '⠋', '⠌', '⠍', '⠎', '⠏',
    '⠐', '⠑', '⠒', '⠓', '⠔', '⠕', '⠖', '⠗', '⠘', '⠙', '⠚', '⠛', '⠜', '⠝', '⠞', '⠟',
    '⠠', '⠡', '⠢', '⠣', '⠤', '⠥', '⠦', '⠧', '⠨', '⠩', '⠪', '⠫', '⠬', '⠭', '⠮', '⠯',
    '⠰', '⠱', '⠲', '⠳', '⠴', '⠵', '⠶', '⠷', '⠸', '⠹', '⠺', '⠻', '⠼', '⠽', '⠾', '⠿'
  ];

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setSelectedImage(e.target.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const convertToAsciiArt = async () => {
    if (!selectedImage) return;
    
    setIsProcessing(true);
    
    // Simulate processing time
    setTimeout(() => {
      // Generate mock braille art
      let art = '';
      for (let i = 0; i < dimensions.height; i++) {
        for (let j = 0; j < dimensions.width; j++) {
          // Use random braille characters based on brightness/contrast
          const charIndex = Math.floor(Math.random() * brailleChars.length);
          art += brailleChars[charIndex];
        }
        art += '\n';
      }
      
      setBrailleArt(art);
      setIsProcessing(false);
    }, 2000);
  };

  const downloadArt = () => {
    if (!brailleArt) return;
    
    const element = document.createElement('a');
    const file = new Blob([brailleArt], { type: 'text/plain' });
    element.href = URL.createObjectURL(file);
    element.download = 'braille_art.txt';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  const clearAll = () => {
    setSelectedImage(null);
    setBrailleArt('');
    setDimensions({ width: 40, height: 25 });
    setContrast(50);
    setBrightness(50);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="braille-art-editor">
      <div className="editor-header">
        <h2><i className="fas fa-palette"></i> Braille Art Editor</h2>
        <p>Transform images into beautiful Braille art</p>
      </div>

      <div className="editor-content">
        <div className="upload-section">
          <div className="upload-area">
            <div className="upload-box" onClick={() => fileInputRef.current?.click()}>
              {selectedImage ? (
                <div className="image-preview">
                  <img src={selectedImage} alt="Selected" />
                  <div className="upload-overlay">
                    <i className="fas fa-camera"></i>
                    <span>Click to change image</span>
                  </div>
                </div>
              ) : (
                <div className="upload-placeholder">
                  <i className="fas fa-cloud-upload-alt"></i>
                  <h3>Upload an Image</h3>
                  <p>Support formats: JPG, PNG, GIF</p>
                  <button className="upload-btn">
                    <i className="fas fa-plus"></i> Choose Image
                  </button>
                </div>
              )}
            </div>
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleImageUpload}
              style={{ display: 'none' }}
            />
          </div>

          <div className="settings-panel">
            <h3><i className="fas fa-cog"></i> Conversion Settings</h3>
            
            <div className="setting-group">
              <label>Output Dimensions</label>
              <div className="dimension-inputs">
                <div className="input-field">
                  <label>Width:</label>
                  <input
                    type="number"
                    value={dimensions.width}
                    onChange={(e) => setDimensions(prev => ({ ...prev, width: parseInt(e.target.value) || 40 }))}
                    min="10"
                    max="100"
                  />
                </div>
                <div className="input-field">
                  <label>Height:</label>
                  <input
                    type="number"
                    value={dimensions.height}
                    onChange={(e) => setDimensions(prev => ({ ...prev, height: parseInt(e.target.value) || 25 }))}
                    min="10"
                    max="100"
                  />
                </div>
              </div>
            </div>

            <div className="setting-group">
              <label>Contrast: {contrast}%</label>
              <input
                type="range"
                min="0"
                max="100"
                value={contrast}
                onChange={(e) => setContrast(parseInt(e.target.value))}
                className="slider"
              />
            </div>

            <div className="setting-group">
              <label>Brightness: {brightness}%</label>
              <input
                type="range"
                min="0"
                max="100"
                value={brightness}
                onChange={(e) => setBrightness(parseInt(e.target.value))}
                className="slider"
              />
            </div>

            <div className="action-buttons">
              <button
                className="convert-btn"
                onClick={convertToAsciiArt}
                disabled={!selectedImage || isProcessing}
              >
                <i className={`fas ${isProcessing ? 'fa-spinner fa-spin' : 'fa-magic'}`}></i>
                {isProcessing ? 'Converting...' : 'Convert to Braille Art'}
              </button>
              
              <button className="clear-btn" onClick={clearAll}>
                <i className="fas fa-trash"></i> Clear All
              </button>
            </div>
          </div>
        </div>

        <div className="output-section">
          <div className="output-header">
            <h3><i className="fas fa-braille"></i> Braille Art Output</h3>
            {brailleArt && (
              <button className="download-btn" onClick={downloadArt}>
                <i className="fas fa-download"></i> Download
              </button>
            )}
          </div>
          
          <div className="art-display">
            {brailleArt ? (
              <pre className="braille-output">{brailleArt}</pre>
            ) : (
              <div className="empty-output">
                <i className="fas fa-image"></i>
                <p>Upload an image and click "Convert to Braille Art" to see the result</p>
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="features-info">
        <h3><i className="fas fa-info-circle"></i> How it Works</h3>
        <div className="info-grid">
          <div className="info-item">
            <i className="fas fa-upload"></i>
            <div>
              <h4>1. Upload Image</h4>
              <p>Choose any image file (JPG, PNG, GIF)</p>
            </div>
          </div>
          <div className="info-item">
            <i className="fas fa-sliders-h"></i>
            <div>
              <h4>2. Adjust Settings</h4>
              <p>Fine-tune dimensions, contrast, and brightness</p>
            </div>
          </div>
          <div className="info-item">
            <i className="fas fa-magic"></i>
            <div>
              <h4>3. Convert</h4>
              <p>Transform your image into Braille art</p>
            </div>
          </div>
          <div className="info-item">
            <i className="fas fa-download"></i>
            <div>
              <h4>4. Download</h4>
              <p>Save your Braille art as a text file</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BrailleArtEditor;

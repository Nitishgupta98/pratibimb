import React, { useState } from 'react';
import { convertTextToBraille } from '../../services/api';
import { useConversion } from '../../hooks';
import './ConverterPage.css';

const ConverterPage = () => {
  const [inputText, setInputText] = useState('');
  const [outputBraille, setOutputBraille] = useState('');
  const [outputBrf, setOutputBrf] = useState('');
  const [isConverting, setIsConverting] = useState(false);
  const [error, setError] = useState(null);
  const [conversionStats, setConversionStats] = useState(null);
  
  const { addConversion } = useConversion();

  const handleConvert = async () => {
    if (!inputText.trim()) {
      setError('Please enter some text to convert');
      return;
    }

    setIsConverting(true);
    setError(null);

    try {
      const result = await convertTextToBraille(inputText, {
        braille_settings: {
          preserve_line_breaks: true,
          tab_width: 4
        },
        embosser_settings: {
          line_length: 40,
          page_length: 25,
          include_page_numbers: true
        }
      });

      setOutputBraille(result.braille_unicode || '');
      setOutputBrf(result.embosser_brf || '');
      setConversionStats(result.stats || null);

      // Add to conversion history
      addConversion({
        originalText: inputText,
        brailleUnicode: result.braille_unicode,
        embosserBrf: result.embosser_brf,
        stats: result.stats
      });

      setError(null);
    } catch (err) {
      setError('Conversion failed. Please try again.');
      console.error('Conversion error:', err);
    } finally {
      setIsConverting(false);
    }
  };

  const handleClear = () => {
    setInputText('');
    setOutputBraille('');
    setOutputBrf('');
    setError(null);
    setConversionStats(null);
  };

  const handleCopyBraille = async () => {
    try {
      await navigator.clipboard.writeText(outputBraille);
      // Could add a toast notification here
    } catch (err) {
      console.error('Failed to copy text:', err);
    }
  };

  const handleDownloadBrf = () => {
    if (!outputBrf) return;
    
    const blob = new Blob([outputBrf], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'braille_output.brf';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="converter-page">
      <div className="converter-container">
        <div className="page-header">
          <h1>
            <i className="fas fa-language"></i>
            Text to Braille Converter
          </h1>
          <p>Convert your text to Grade 1 Unicode Braille and embosser-ready BRF format</p>
        </div>

        {error && (
          <div className="alert alert-danger">
            <i className="fas fa-exclamation-triangle"></i>
            {error}
          </div>
        )}

        <div className="converter-grid">
          {/* Input Section */}
          <div className="input-section">
            <div className="section-header">
              <h2>
                <i className="fas fa-edit"></i>
                Input Text
              </h2>
              <div className="text-stats">
                {inputText.length} characters
              </div>
            </div>
            
            <div className="input-controls">
              <textarea
                className="text-input"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder="Enter your text here to convert to Braille..."
                rows={12}
                disabled={isConverting}
              />
              
              <div className="input-actions">
                <button 
                  className="btn btn-primary"
                  onClick={handleConvert}
                  disabled={isConverting || !inputText.trim()}
                >
                  {isConverting ? (
                    <>
                      <div className="spinner"></div>
                      Converting...
                    </>
                  ) : (
                    <>
                      <i className="fas fa-magic"></i>
                      Convert to Braille
                    </>
                  )}
                </button>
                
                <button 
                  className="btn btn-secondary"
                  onClick={handleClear}
                  disabled={isConverting}
                >
                  <i className="fas fa-trash"></i>
                  Clear All
                </button>
              </div>
            </div>
          </div>

          {/* Output Section */}
          <div className="output-section">
            <div className="section-header">
              <h2>
                <i className="fas fa-braille"></i>
                Braille Output
              </h2>
              {conversionStats && (
                <div className="output-stats">
                  {conversionStats.braille_characters} Braille chars
                </div>
              )}
            </div>
            
            <div className="output-tabs">
              <div className="tab-buttons">
                <button className="tab-btn active" data-tab="unicode">
                  <i className="fas fa-font"></i>
                  Unicode Braille
                </button>
                <button className="tab-btn" data-tab="brf">
                  <i className="fas fa-print"></i>
                  BRF Format
                </button>
              </div>
              
              <div className="tab-content">
                <div className="tab-pane active" id="unicode">
                  <textarea
                    className="text-output braille-output"
                    value={outputBraille}
                    readOnly
                    placeholder="Braille output will appear here..."
                    rows={12}
                  />
                  
                  <div className="output-actions">
                    <button 
                      className="btn btn-outline"
                      onClick={handleCopyBraille}
                      disabled={!outputBraille}
                    >
                      <i className="fas fa-copy"></i>
                      Copy Braille
                    </button>
                  </div>
                </div>
                
                <div className="tab-pane" id="brf">
                  <textarea
                    className="text-output brf-output"
                    value={outputBrf}
                    readOnly
                    placeholder="BRF format output will appear here..."
                    rows={12}
                  />
                  
                  <div className="output-actions">
                    <button 
                      className="btn btn-outline"
                      onClick={handleDownloadBrf}
                      disabled={!outputBrf}
                    >
                      <i className="fas fa-download"></i>
                      Download BRF
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Conversion Statistics */}
        {conversionStats && (
          <div className="stats-section">
            <h3>
              <i className="fas fa-chart-bar"></i>
              Conversion Statistics
            </h3>
            
            <div className="stats-grid">
              <div className="stat-item">
                <div className="stat-label">Original Characters</div>
                <div className="stat-value">{conversionStats.original_characters}</div>
              </div>
              
              <div className="stat-item">
                <div className="stat-label">Braille Characters</div>
                <div className="stat-value">{conversionStats.braille_characters}</div>
              </div>
              
              <div className="stat-item">
                <div className="stat-label">Words Converted</div>
                <div className="stat-value">{conversionStats.words_converted}</div>
              </div>
              
              <div className="stat-item">
                <div className="stat-label">Processing Time</div>
                <div className="stat-value">{conversionStats.processing_time_ms}ms</div>
              </div>
              
              {conversionStats.compression_ratio && (
                <div className="stat-item">
                  <div className="stat-label">Compression Ratio</div>
                  <div className="stat-value">{conversionStats.compression_ratio}%</div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ConverterPage;

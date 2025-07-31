import React, { useState, useEffect } from 'react';
import { MODULAR_API_CONFIG, buildModularApiUrl, buildDownloadUrl } from '../modularApiConfig';
import './Results.css';

const Results = ({
  data,
  onGenerateTelugu,
  onGenerateKannada,
  teluguState,
  kannadaState
}) => {
  // --- Language Braille Download UI ---
  const renderLanguageBrailleSection = () => {
    // Only show after main pipeline is complete
    return (
      <div className="language-braille-section">
        <h3>🔤 Generate Braille in Other Languages</h3>
        <div className="language-braille-buttons">
          {/* Telugu Braille */}
          <div className="lang-braille-block">
            <button
              className="download-btn"
              onClick={onGenerateTelugu}
              disabled={teluguState?.status === 'loading'}
              style={{ minWidth: 180 }}
            >
              {teluguState?.status === 'loading' ? 'Generating Telugu Braille...' : 'Generate Telugu Braille'}
            </button>
            {teluguState?.status === 'done' && teluguState.files && teluguState.files.length > 0 && (
              <>
                {/* Download Telugu Transcript */}
                {teluguState.files.find(f => f.name === 'telugu_transcript') && (
                  <a
                    className="download-btn"
                    href={`data:text/plain;charset=utf-8,${encodeURIComponent(
                      teluguState.files.find(f => f.name === 'telugu_transcript').content
                    )}`}
                    download="telugu_transcript.txt"
                    style={{ marginLeft: 8 }}
                  >
                    📥 Download Telugu Transcript
                  </a>
                )}
                {/* Download Telugu Braille */}
                {teluguState.files.find(f => f.name === 'telugu_braille_content') && (
                  <a
                    className="download-btn"
                    href={`data:text/plain;charset=utf-8,${encodeURIComponent(
                      teluguState.files.find(f => f.name === 'telugu_braille_content').content
                    )}`}
                    download="telugu_braille.txt"
                    style={{ marginLeft: 8 }}
                  >
                    📥 Download Telugu Braille
                  </a>
                )}
              </>
            )}
            {teluguState?.status === 'error' && (
              <span className="error-message" style={{ marginLeft: 8 }}>{teluguState.error}</span>
            )}
          </div>
          {/* Kannada Braille */}
          <div className="lang-braille-block">
            <button
              className="download-btn"
              onClick={onGenerateKannada}
              disabled={kannadaState?.status === 'loading'}
              style={{ minWidth: 180 }}
            >
              {kannadaState?.status === 'loading' ? 'Generating Kannada Braille...' : 'Generate Kannada Braille'}
            </button>
            {kannadaState?.status === 'done' && kannadaState.files && kannadaState.files.length > 0 && (
              <>
                {/* Download Kannada Transcript */}
                {kannadaState.files.find(f => f.name === 'kannada_transcript') && (
                  <a
                    className="download-btn"
                    href={`data:text/plain;charset=utf-8,${encodeURIComponent(
                      kannadaState.files.find(f => f.name === 'kannada_transcript').content
                    )}`}
                    download="kannada_transcript.txt"
                    style={{ marginLeft: 8 }}
                  >
                    📥 Download Kannada Transcript
                  </a>
                )}
                {/* Download Kannada Braille */}
                {kannadaState.files.find(f => f.name === 'kannada_braille_content') && (
                  <a
                    className="download-btn"
                    href={`data:text/plain;charset=utf-8,${encodeURIComponent(
                      kannadaState.files.find(f => f.name === 'kannada_braille_content').content
                    )}`}
                    download="kannada_braille.txt"
                    style={{ marginLeft: 8 }}
                  >
                    📥 Download Kannada Braille
                  </a>
                )}
              </>
            )}
            {kannadaState?.status === 'error' && (
              <span className="error-message" style={{ marginLeft: 8 }}>{kannadaState.error}</span>
            )}
          </div>
        </div>
      </div>
    );
  };
  const [reportData, setReportData] = useState(null);
  const [reportLoading, setReportLoading] = useState(true);
  const [reportError, setReportError] = useState(null);

  useEffect(() => {
    // Fetch the latest report data when results are available
    if (data) {
      fetchLatestReportData();
    }
  }, [data]);

  const fetchLatestReportData = async () => {
    setReportLoading(true);
    setReportError(null);
    
    try {
      // For now, just use the provided data directly since we're using the new modular pipeline
      // The modular pipeline returns content directly, so we don't need to fetch additional report data
      setReportData(data);
      setReportLoading(false);
      
    } catch (error) {
      console.error('Error fetching report data:', error);
      setReportError(error.message);
    } finally {
      setReportLoading(false);
    }
  };

  const renderSummaryCards = () => {
    if (!reportData?.summary) return null;
    
    const summaryItems = [
      { key: 'tests_passed', label: 'Tests Passed', className: 'success' },
      { key: 'characters_processed', label: 'Characters Processed' },
      { key: 'pages_generated', label: 'Pages Generated' },
      { key: 'success_rate', label: 'Success Rate' }
    ];

    return (
      <div className="summary-grid">
        {summaryItems.map((item, index) => {
          const value = reportData.summary[item.key] || Object.values(reportData.summary)[index] || '0';
          return (
            <div key={item.key} className={`summary-card ${item.className || ''}`}>
              <h3>{value}</h3>
              <p>{item.label}</p>
            </div>
          );
        })}
      </div>
    );
  };

  const renderProjectFiles = () => {
    if (!reportData?.projectFiles) return null;

    const handleFileDownload = (fileType) => {
      const fileTypeMap = {
        'Input Text File': 'enhanced_transcript',
        'Unicode Braille File': 'braille',
        'Embosser BRF File': 'embosser',
        'Request Log File': 'request_logs'
      };
      
      const downloadType = fileTypeMap[fileType];
      if (downloadType) {
        const downloadUrl = buildDownloadUrl(downloadType);
        window.open(downloadUrl, '_blank');
      }
    };

    return (
      <div className="files-grid">
        {reportData.projectFiles.map((file, index) => (
          <div 
            key={index} 
            className="file-item clickable-file"
            onClick={() => handleFileDownload(file.title)}
            role="button"
            tabIndex={0}
            onKeyPress={(e) => {
              if (e.key === 'Enter' || e.key === ' ') {
                handleFileDownload(file.title);
              }
            }}
          >
            <div className="file-header">
              <div className="file-icon">{file.icon}</div>
              <h3 className="file-title">{file.title}</h3>
            </div>
            <div className="file-description">{file.description}</div>
            <div className="file-meta">
              <span>{file.type}</span>
              <span>{file.format}</span>
            </div>
            <div className="download-indicator">
              <span>📥 Click to Download</span>
            </div>
          </div>
        ))}
      </div>
    );
  };

  const renderTestResults = () => {
    if (!reportData?.testResults) return null;

    return (
      <div className="test-results">
        {reportData.testResults.map((test, index) => (
          <div key={index} className={`test-item ${test.passed ? 'passed' : 'failed'}`}>
            <div className="test-header">
              <div className="test-title">{test.title}</div>
              <div className={`status-badge ${test.passed ? 'passed' : 'failed'}`}>
                {test.status}
              </div>
            </div>
            <div className="test-details">
              <strong>Key Results:</strong> {test.keyResults}
            </div>
          </div>
        ))}
      </div>
    );
  };

  const renderConfiguration = () => {
    if (!reportData?.configuration) return null;

    return (
      <div className="config-grid">
        <div className="config-item">
          <strong>Line Length:</strong> {reportData.configuration.lineLength}<br/>
          <strong>Page Length:</strong> {reportData.configuration.pageLength}<br/>
          <strong>Page Numbers:</strong> {reportData.configuration.pageNumbers}
        </div>
        <div className="config-item">
          <strong>Tab Width:</strong> {reportData.configuration.tabWidth}<br/>
          <strong>Preserve Line Breaks:</strong> {reportData.configuration.preserveLineBreaks}<br/>
          <strong>Skip Carriage Returns:</strong> {reportData.configuration.skipCarriageReturns}
        </div>
      </div>
    );
  };

  const renderConclusion = () => {
    if (!reportData?.conclusion) return null;

    return (
      <div className="conclusion-section">
        <p><strong>{reportData.conclusion.message}</strong></p>
        <p>The embosser-friendly Unicode Braille generation is working perfectly with:</p>
        <ul className="conclusion-points">
          {reportData.conclusion.points.map((point, index) => (
            <li key={index}><strong>{point}</strong></li>
          ))}
        </ul>
      </div>
    );
  };

  if (!data) return null;

  return (
    <div className="results-container">
      <div className="results-header">
        <h2>✅ Processing Complete</h2>
        <p>Your transcript has been processed and converted to Braille-ready format.</p>
      </div>

      <div className="results-content">
        {/* Language Braille Generation Section */}
        {renderLanguageBrailleSection()}
        {/* Download buttons for key result files */}
        <div className="download-section">
          <h3>📥 Download Files</h3>
          <div className="download-buttons">
            {data.merged_transcript_file && (
              <a
                href={buildDownloadUrl('merged_transcript')}
                className="download-btn"
                target="_blank"
                rel="noopener noreferrer"
                download
              >
                🔗 Merged Transcript
              </a>
            )}
            {data.figure_tagged_transcript_file && (
              <a
                href={buildDownloadUrl('figure_tagged_transcript')}
                className="download-btn"
                target="_blank"
                rel="noopener noreferrer"
                download
              >
                🏷️ Figure-Tagged Transcript
              </a>
            )}
            {data.braille_art_file && (
              <a
                href={buildDownloadUrl('braille_art')}
                className="download-btn"
                target="_blank"
                rel="noopener noreferrer"
                download
              >
                ⠃ Braille Art File
              </a>
            )}
            {data.final_braille_transcript_file && (
              <a
                href={buildDownloadUrl('final_braille_transcript')}
                className="download-btn"
                target="_blank"
                rel="noopener noreferrer"
                download
              >
                📄 Final Braille Transcript
              </a>
            )}
          </div>
        </div>

        {/* Text preview for each file (optional, can be removed if not needed) */}
        <div className="text-preview">
          <h3>📝 Text Preview</h3>
          {data.merged_transcript_content && (
            <div className="text-content">
              <h4>Merged Transcript</h4>
              <pre className="text-display">{data.merged_transcript_content}</pre>
            </div>
          )}
          {data.figure_tagged_transcript_content && (
            <div className="text-content">
              <h4>Figure-Tagged Transcript</h4>
              <pre className="text-display">{data.figure_tagged_transcript_content}</pre>
            </div>
          )}
          {data.braille_art_content && (
            <div className="text-content">
              <h4>Braille Art</h4>
              <pre className="text-display">{data.braille_art_content}</pre>
            </div>
          )}
          {data.final_braille_transcript_content && (
            <div className="text-content">
              <h4>Final Braille Transcript</h4>
              <pre className="text-display">{data.final_braille_transcript_content}</pre>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Results;

import React, { useState, useEffect } from 'react';
import { buildApiUrl, buildDownloadUrl, API_CONFIG } from '../config';
import './Results.css';

const Results = ({ data }) => {
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
      const response = await fetch(buildApiUrl(API_CONFIG.endpoints.getLatestReportData));
      
      if (!response.ok) {
        throw new Error('Failed to get latest report data');
      }
      
      const reportData = await response.json();
      setReportData(reportData);
      
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
        'Session Log File': 'log',
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
        {/* Download buttons for files */}
        <div className="download-section">
          <h3>📥 Download Files</h3>
          <div className="download-buttons">
            {data.raw_transcript && (
              <a 
                href={`data:text/plain;charset=utf-8,${encodeURIComponent(data.raw_transcript)}`}
                download="raw_transcript.txt"
                className="download-btn"
              >
                📄 Raw Transcript
              </a>
            )}
            {data.enhanced_text && (
              <a 
                href={`data:text/plain;charset=utf-8,${encodeURIComponent(data.enhanced_text)}`}
                download="enhanced_transcript.txt"
                className="download-btn"
              >
                ✨ Enhanced Transcript
              </a>
            )}
          </div>
        </div>

        {/* Native React Report Rendering */}
        <div className="report-section">
          <h3>📊 Pratibimb Test Report</h3>
          <div className="report-container">
            {reportLoading ? (
              <div className="report-loading">
                <p>🔄 Loading latest test report...</p>
                <div className="loading-spinner"></div>
              </div>
            ) : reportError ? (
              <div className="report-error">
                <p>❌ Failed to load report: {reportError}</p>
                <button onClick={fetchLatestReportData} className="retry-btn">
                  🔄 Retry
                </button>
              </div>
            ) : reportData ? (
              <div className="pratibimb-report">
                {/* Report Header */}
                <div className="report-header">
                  <h1>🔤 Pratibimb Test Report</h1>
                  <div className="report-date">{reportData.timestamp}</div>
                </div>

                {/* Project Files Section */}
                <section>
                  <h2 className="report-section-title">📁 Project Files</h2>
                  {renderProjectFiles()}
                </section>

                {/* Test Overview Section */}
                <section>
                  <h2 className="report-section-title">📊 Test Overview</h2>
                  {renderSummaryCards()}
                </section>

                {/* Test Results Section */}
                <section>
                  <h2 className="report-section-title">🧪 Test Results Summary</h2>
                  {renderTestResults()}
                </section>

                {/* Configuration Section */}
                <section>
                  <h3 className="report-section-title">⚙️ Configuration Used</h3>
                  {renderConfiguration()}
                </section>

                {/* Conclusion Section */}
                <section>
                  <h2 className="report-section-title">🏆 Test Suite Conclusion</h2>
                  {renderConclusion()}
                </section>

                <div className="report-actions" style={{ marginTop: '30px', textAlign: 'center' }}>
                  <button onClick={fetchLatestReportData} className="refresh-btn">
                    🔄 Refresh Report
                  </button>
                </div>
              </div>
            ) : null}
          </div>
        </div>

        {/* Text preview */}
        <div className="text-preview">
          <h3>📝 Text Preview</h3>
          {data.enhanced_text && (
            <div className="text-content">
              <h4>Enhanced Transcript (Braille-Ready)</h4>
              <pre className="text-display">{data.enhanced_text}</pre>
            </div>
          )}
          {data.raw_transcript && (
            <div className="text-content">
              <h4>Raw Transcript</h4>
              <pre className="text-display">{data.raw_transcript}</pre>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Results;

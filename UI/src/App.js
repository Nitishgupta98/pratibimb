import React, { useState, useEffect, useRef } from 'react';
import { Zap } from 'lucide-react';
import Header from './components/Header';
import Footer from './components/Footer';
import YouTubeInput from './components/YouTubeInput';
import FileUpload from './components/FileUpload';
import Results from './components/Results';
import LoadingSpinner from './components/LoadingSpinner';
import { API_CONFIG, buildApiUrl, buildStreamLogsUrl } from './config';
import './App.css';

function App() {
  const [inputMode, setInputMode] = useState('youtube'); // 'youtube' or 'file'
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [progressSteps, setProgressSteps] = useState([]);
  const [displayedSteps, setDisplayedSteps] = useState([]);
  const [animatingStep, setAnimatingStep] = useState(null);
  const progressStepsRef = useRef(null);
  // Ref to track polling state and timeout
  const pollingRef = useRef({ active: false, timeoutId: null });
  const [currentRequestId, setCurrentRequestId] = useState(null);
  
  // YouTube state
  const [youtubeUrl, setYoutubeUrl] = useState('');
  const [isYoutubeValid, setIsYoutubeValid] = useState(false);
  
  // File upload state
  const [selectedFile, setSelectedFile] = useState(null);

  const handleModeToggle = () => {
    setInputMode(inputMode === 'youtube' ? 'file' : 'youtube');
    setResults(null);
    setError(null);
    setProgressSteps([]);
    setDisplayedSteps([]);
    setAnimatingStep(null);
    setCurrentRequestId(null);
  };

  // Poll progress for the latest process (no requestId needed)
  const pollProgress = async () => {
    // Prevent multiple pollers
    if (!pollingRef.current.active) return;
    try {
      const response = await fetch(buildStreamLogsUrl());
      if (response.ok) {
        const progressData = await response.json();
        const newSteps = progressData.progress_steps || [];
        setProgressSteps(newSteps);
        // Stop polling if 12 steps are complete or is_complete is true
        if (newSteps.length >= 12 || progressData.is_complete) {
          pollingRef.current.active = false;
          pollingRef.current.timeoutId = null;
          return;
        }
        // Continue polling every 1s
        pollingRef.current.timeoutId = setTimeout(pollProgress, 1000);
      } else {
        // Retry after 3s on error
        pollingRef.current.timeoutId = setTimeout(pollProgress, 3000);
      }
    } catch (err) {
      console.error('Failed to fetch progress:', err);
      pollingRef.current.timeoutId = setTimeout(pollProgress, 3000);
    }
  };

  // Effect to sync displayedSteps with progressSteps in real-time (no animation, always up-to-date)
  useEffect(() => {
    if (progressSteps.length > displayedSteps.length) {
      const nextStepIndex = displayedSteps.length;
      const nextStep = progressSteps[nextStepIndex];
      
      if (nextStep && !animatingStep) {
        setAnimatingStep(nextStep);
        
        // Add step after a short delay for animation effect
        setTimeout(() => {
          setDisplayedSteps(prev => [...prev, nextStep]);
          setAnimatingStep(null);
        }, 300); // 300ms delay between steps for smooth animation
      }
    }
  }, [progressSteps, displayedSteps, animatingStep]);

  // Effect to auto-scroll to bottom when new steps are added
  useEffect(() => {
    if (progressStepsRef.current) {
      progressStepsRef.current.scrollTop = progressStepsRef.current.scrollHeight;
    }
  }, [displayedSteps, animatingStep]);

  const handleYouTubeUrlChange = (url, isValid) => {
    setYoutubeUrl(url);
    setIsYoutubeValid(isValid);
  };

  const handleFileSelect = (file) => {
    setSelectedFile(file);
  };

  const canGenerate = () => {
    if (inputMode === 'youtube') {
      return isYoutubeValid && !isLoading;
    } else {
      return selectedFile && !isLoading;
    }
  };

  const getTooltipText = () => {
    if (isLoading) {
      return 'Processing your request...';
    }
    if (inputMode === 'youtube' && !isYoutubeValid) {
      return 'Please enter a valid YouTube URL';
    }
    if (inputMode === 'file' && !selectedFile) {
      return 'Please select a video file';
    }
    return '';
  };

  const handleGenerate = async () => {
    if (!canGenerate()) return;

    if (inputMode === 'youtube') {
      // Use the complete process_transcript endpoint for full workflow including Braille conversion
      await handleYouTubeSubmit(youtubeUrl);
    } else {
      await handleFileUpload(selectedFile);
    }
  };

  // COMMENTED OUT: Individual API calls - now using complete process_transcript endpoint
  /*
  const handleYouTubeBrailleGeneration = async (url) => {
    setIsLoading(true);
    setError(null);
    
    try {
      // Step 1: Get raw transcript from YouTube
      const rawResponse = await fetch(`${environment.apiBaseUrl}${environment.endpoints.getRawTranscript}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ youtube_url: url }),
      });

      if (!rawResponse.ok) {
        throw new Error('Failed to get transcript from YouTube video');
      }

      const rawData = await rawResponse.json();
      
      // Step 2: Enhance transcript for Braille
      const enhanceResponse = await fetch(`${environment.apiBaseUrl}${environment.endpoints.getEnhanceTranscript}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ raw_transcript: rawData.raw_transcript }),
      });

      if (!enhanceResponse.ok) {
        throw new Error('Failed to enhance transcript for Braille');
      }

      const enhancedData = await enhanceResponse.json();
      
      // Combine both results
      const combinedResults = {
        raw_transcript: rawData.raw_transcript,
        enhanced_text: enhancedData.enhanced_text,
        raw_transcript_file: rawData.raw_transcript_file,
        enhanced_transcript_file: enhancedData.enhanced_transcript_file
      };
      
      setResults(combinedResults);
    } catch (err) {
      setError(err.message || 'An error occurred while processing the video');
    } finally {
      setIsLoading(false);
    }
  };
  */

  const handleYouTubeSubmit = async (url) => {
    setIsLoading(true);
    setError(null);
    setProgressSteps([]);
    setDisplayedSteps([]);
    setAnimatingStep(null);
    setCurrentRequestId(null);

    // Start polling after 2 seconds, prevent multiple pollers
    if (!pollingRef.current.active) {
      pollingRef.current.active = true;
      pollingRef.current.timeoutId = setTimeout(pollProgress, 2000);
    }

    try {
      const response = await fetch(buildApiUrl(API_CONFIG.endpoints.processTranscript), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ youtube_url: url }),
      });

      if (!response.ok) {
        throw new Error('Failed to process video');
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err.message || 'An error occurred while processing the video');
      // Stop polling on error
      pollingRef.current.active = false;
      if (pollingRef.current.timeoutId) {
        clearTimeout(pollingRef.current.timeoutId);
        pollingRef.current.timeoutId = null;
      }
    } finally {
      setIsLoading(false);
    }
  };
  // Cleanup polling on unmount
  useEffect(() => {
    return () => {
      pollingRef.current.active = false;
      if (pollingRef.current.timeoutId) {
        clearTimeout(pollingRef.current.timeoutId);
        pollingRef.current.timeoutId = null;
      }
    };
  }, []);

  const handleFileUpload = async (file) => {
    setIsLoading(true);
    setError(null);
    
    try {
      // For now, show a message that file upload is not implemented
      // In a real implementation, you would upload the file and process it
      throw new Error('File upload feature is coming soon. Please use YouTube URL for now.');
    } catch (err) {
      setError(err.message || 'An error occurred while processing the file');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <Header />
      
      <main className="main-content">
        <div className="container">
          <div className="hero-section">
            <h1 className="hero-title">
              Pratibimb
              <span className="hero-subtitle">True Reflection of Digital World</span>
            </h1>
            <p className="hero-description">
              Transform YouTube videos into accessible Braille-ready transcripts for visually impaired users. 
              Experience digital content without barriers.
            </p>
          </div>

          <div className="input-section">
            <div className="mode-toggle">
              <button
                className={`toggle-btn ${inputMode === 'youtube' ? 'active' : ''}`}
                onClick={() => setInputMode('youtube')}
              >
                YouTube URL
              </button>
              <button
                className={`toggle-btn ${inputMode === 'file' ? 'active' : ''}`}
                onClick={() => setInputMode('file')}
              >
                Upload Video
              </button>
            </div>

            <div className="input-form">
              {inputMode === 'youtube' ? (
                <YouTubeInput 
                  onSubmit={handleYouTubeSubmit} 
                  isLoading={isLoading}
                  onUrlChange={handleYouTubeUrlChange}
                />
              ) : (
                <FileUpload 
                  onFileUpload={handleFileUpload} 
                  isLoading={isLoading}
                  onFileSelect={handleFileSelect}
                />
              )}
            </div>

            <div className="generate-section">
              <button
                onClick={handleGenerate}
                className={`generate-btn ${canGenerate() ? 'enabled' : 'disabled'} ${isLoading ? 'processing' : ''}`}
                disabled={!canGenerate()}
                data-tooltip={!canGenerate() ? getTooltipText() : ''}
              >
                <Zap size={20} />
                <span>{isLoading ? 'Processing...' : 'Generate Braille'}</span>
              </button>
            </div>

            {/* Real-time Progress Display */}
            {(isLoading || displayedSteps.length > 0) && (
              <div className="progress-section">
                <div className="progress-header">
                  <h3>🔄 Braille Conversion Progress</h3>
                  <div className="progress-counter">
                    {displayedSteps.length} / 12 steps completed
                  </div>
                  {currentRequestId && (
                    <span className="request-id">Request ID: {currentRequestId}</span>
                  )}
                </div>
                <div className="progress-steps" ref={progressStepsRef}>
                  {displayedSteps.map((step, index) => (
                    <div 
                      key={`${step.step}-${index}`}
                      className={`progress-step ${step.status === 'error' ? 'error' : 'completed'} fade-in`}
                    >
                      <div className="step-number">
                        {step.status === 'error' ? '❌' : '✅'} {step.step.toString().padStart(2, '0')}
                      </div>
                      <div className="step-content">
                        <div className="step-message">{step.message}</div>
                        <div className="step-timestamp">
                          {step.timestamp && step.timestamp !== 'Invalid Date' ? step.timestamp : 'Just now'}
                        </div>
                      </div>
                    </div>
                  ))}
                  
                  {/* Show animating step */}
                  {animatingStep && (
                    <div className="progress-step animating">
                      <div className="step-number">
                        ⏳ {animatingStep.step.toString().padStart(2, '0')}
                      </div>
                      <div className="step-content">
                        <div className="step-message">{animatingStep.message}</div>
                        <div className="step-timestamp">Processing...</div>
                      </div>
                    </div>
                  )}
                  
                  {/* Show placeholder for next step when loading */}
                  {isLoading && !animatingStep && displayedSteps.length < 12 && (
                    <div className="progress-step pending pulse">
                      <div className="step-number">⏳ {(displayedSteps.length + 1).toString().padStart(2, '0')}</div>
                      <div className="step-content">
                        <div className="step-message">Processing the request...</div>
                        <div className="step-timestamp">Pending</div>
                      </div>
                    </div>
                  )}
                </div>
                
                {/* Show completion message when all steps are done */}
                {displayedSteps.length >= 12 && !isLoading && (
                  <div className="progress-complete">
                    Braille conversion completed successfully! All files are ready for download.
                  </div>
                )}
                
                {/* Progress bar */}
                <div className="progress-bar-container">
                  <div className="progress-bar">
                    <div 
                      className="progress-fill" 
                      style={{
                        width: `${(progressSteps.length / 12) * 100}%`
                      }}
                    ></div>
                  </div>
                  <span className="progress-text">
                    {progressSteps.length} / 12 steps completed
                  </span>
                </div>
              </div>
            )}

            {isLoading && <LoadingSpinner />}
            
            {error && (
              <div className="error-message">
                <p>{error}</p>
              </div>
            )}

            {results && <Results data={results} />}
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}

export default App;

import React, { useState, useRef } from 'react';
import Header from './components/Header';
import Footer from './components/Footer';
import YouTubeInput from './components/YouTubeInput';
import FileUpload from './components/FileUpload';
import Results from './components/Results';
import LoadingSpinner from './components/LoadingSpinner';
import PipelineProgress from './components/PipelineProgress';
import { pipelineManager } from './services/PipelineManager';
import { buildDownloadUrl, MODULAR_API_CONFIG } from './modularApiConfig';

// (Moved status icons to PipelineProgress component)
import './App.css';

function App() {
  // State for language Braille generation
  const [teluguBraille, setTeluguBraille] = useState({ status: 'idle', files: null, error: null });
  const [kannadaBraille, setKannadaBraille] = useState({ status: 'idle', files: null, error: null });
  const [inputMode, setInputMode] = useState('youtube'); // 'youtube' or 'file'
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  
  // Dynamic progress state
  const [progressSteps, setProgressSteps] = useState([]); // [{step, stepName, status, message, ...}]
  const [isPipelineRunning, setIsPipelineRunning] = useState(false);
  const [stepError, setStepError] = useState(null); // { step, error, message }
  const [downloadableFiles, setDownloadableFiles] = useState([]);
  const pipelineRef = useRef(null);

  // Remove legacy state
  // const [currentStep, setCurrentStep] = useState(null);
  // const [completedSteps, setCompletedSteps] = useState([]);
  
  // YouTube state
  const [youtubeUrl, setYoutubeUrl] = useState('');
  const [isYoutubeValid, setIsYoutubeValid] = useState(false);
  
  // File upload state
  const [selectedFile, setSelectedFile] = useState(null);

  const handleModeToggle = () => {
    setInputMode(inputMode === 'youtube' ? 'file' : 'youtube');
    setResults(null);
    setError(null);
    setDownloadableFiles([]);
    setProgressSteps([]);
    setStepError(null);
  };

  // 10 user-facing steps, each can map to one or more backend API calls
  // Use modularApiConfig.js endpoint keys for robust mapping
  const VISIBLE_STEPS = [
    {
      key: 'download_video',
      label: 'Downloading/accessing video',
      apis: ['validateUrl', 'downloadVideo']
    },
    {
      key: 'audio_transcript',
      label: 'Get audio transcript',
      apis: ['extractAudio']
    },
    {
      key: 'extract_frames',
      label: 'Extracting frames',
      apis: ['extractFrames']
    },
    {
      key: 'deduplicate_frames',
      label: 'Deduplicating frames',
      apis: ['deduplicateFrames']
    },
    {
      key: 'generate_visuals',
      label: 'Generating visual frames',
      apis: ['generateDescriptions']
    },
    {
      key: 'merge_audio_visual',
      label: 'Merge audio-visual transcripts',
      apis: ['mergeAudioVisual']
    },
    {
      key: 'extract_objects_and_tags',
      label: 'Extracting relevant visual objects and insert figure tags',
      apis: ['extractObjects', 'enrichTags']
    },
    {
      key: 'generate_ascii',
      label: 'Generate ASCII art',
      apis: ['generateAscii']
    },
    {
      key: 'generate_braille_art',
      label: 'Generate Braille Art',
      apis: ['generateBraille']
    },
    {
      key: 'generate_braille_text',
      label: 'Generating braille text & combining with braille art',
      apis: ['assembleDocument', 'finalizeOutput']
    }
  ];

  // Helper to initialize step status
  function PipelineStepsInit() {
    return VISIBLE_STEPS.map(() => ({ status: 'pending', error: null }));
  }

  // Use endpoint keys and modularApiConfig for robust API calls
  // Update: For file-based steps, send only minimal payload (YouTube URL),
  // as backend now uses Request_files for all file-based processing.
  const callModularAPI = async (endpointKey, payload) => {
    const endpointPath = MODULAR_API_CONFIG.endpoints[endpointKey];
    if (!endpointPath) {
      throw new Error(`Unknown API endpoint key: ${endpointKey}`);
    }
    // For file-based steps, only send youtube_url or video_title if needed
    let minimalPayload = { ...payload };
    if ([
      'downloadVideo',
      'extractAudio',
      'extractFrames',
      'deduplicateFrames',
      'generateDescriptions'
    ].includes(endpointKey)) {
      // Only send youtube_url and video_title if present
      minimalPayload = {};
      if (payload.youtube_url) minimalPayload.youtube_url = payload.youtube_url;
      if (payload.video_title) minimalPayload.video_title = payload.video_title;
    }
    const response = await fetch(`${MODULAR_API_CONFIG.baseUrl}${endpointPath}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(minimalPayload)
    });
    if (!response.ok) {
      throw new Error(`API call failed: ${response.statusText}`);
    }
    return await response.json();
  };

  // Run pipeline using PipelineManager (dynamic progress)
  const runPipeline = async (url) => {
    setIsPipelineRunning(true);
    setProgressSteps([]);
    setError(null);
    setResults(null);
    setDownloadableFiles([]);
    setStepError(null);
    pipelineRef.current = pipelineManager;
    await pipelineManager.runPipeline(
      url,
      (stepUpdate) => {
        setProgressSteps(prev => {
          // If step already exists, update it; else add new
          const idx = prev.findIndex(s => s.step === stepUpdate.step);
          if (idx !== -1) {
            const updated = [...prev];
            updated[idx] = { ...updated[idx], ...stepUpdate };
            return updated;
          } else {
            return [...prev, stepUpdate];
          }
        });
        if (stepUpdate.status === 'error') {
          setStepError(stepUpdate);
        }
      },
      (finalResult) => {
        setIsPipelineRunning(false);
        if (finalResult.status === 'success') {
          setResults({ message: finalResult.message, status: 'success' });
          setDownloadableFiles(pipelineManager.getDownloadableFiles());
        } else {
          setError(finalResult.message);
        }
      }
    );
  };

  const handleYouTubeUrlChange = (url, isValid) => {
    setYoutubeUrl(url);
    setIsYoutubeValid(isValid);
  };

  const handleFileSelect = (file) => {
    setSelectedFile(file);
  };

  const canGenerate = () => {
    // Disable if pipeline is running or steps are in progress
    if (isPipelineRunning || progressSteps.some(s => s.status === 'processing')) {
      return false;
    }
    if (inputMode === 'youtube') {
      return isYoutubeValid;
    } else {
      return !!selectedFile;
    }
  };

  const handleGenerate = () => {
    if (inputMode === 'youtube') {
      runPipeline(youtubeUrl);
    } else {
      setError('File upload feature is coming soon. Please use YouTube URL for now.');
    }
  };

  // Retry handler for a failed step
  const handleRetryStep = () => {
    if (stepError && typeof stepError.step === 'number') {
      setIsPipelineRunning(true);
      setError(null);
      setResults(null);
      setDownloadableFiles([]);
      setStepError(null);
      setProgressSteps(prev => prev.slice(0, stepError.step - 1));
      pipelineManager.retryFromStep(
        stepError.step,
        (stepUpdate) => {
          setProgressSteps(prev => {
            const idx = prev.findIndex(s => s.step === stepUpdate.step);
            if (idx !== -1) {
              const updated = [...prev];
              updated[idx] = { ...updated[idx], ...stepUpdate };
              return updated;
            } else {
              return [...prev, stepUpdate];
            }
          });
          if (stepUpdate.status === 'error') {
            setStepError(stepUpdate);
          }
        },
        (finalResult) => {
          setIsPipelineRunning(false);
          if (finalResult.status === 'success') {
            setResults({ message: finalResult.message, status: 'success' });
            setDownloadableFiles(pipelineManager.getDownloadableFiles());
          } else {
            setError(finalResult.message);
          }
        }
      );
    }
  };


  // --- Language Braille Generation Handlers ---
  // These are now passed to Results and only shown after pipeline is complete
  const handleGenerateTelugu = async () => {
    setTeluguBraille({ status: 'loading', files: null, error: null });
    try {
      const taggedStep = progressSteps.find(s => s.data && s.data.enriched_transcript);
      const brailleArtStep = progressSteps.find(s => s.data && s.data.braille_art_content);
      if (!taggedStep || !brailleArtStep) throw new Error('Required data missing from pipeline.');
      const response = await fetch(
        `${MODULAR_API_CONFIG.baseUrl}${MODULAR_API_CONFIG.endpoints.brailleInTelugu}`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            transcript_content: taggedStep.data.enriched_transcript,
            braille_art_content: brailleArtStep.data.braille_art_content
          })
        }
      );
      if (!response.ok) throw new Error('Telugu Braille API failed');
      const data = await response.json();
      setTeluguBraille({
        status: 'done',
        files: [
          {
            name: 'Telugu Enhanced Transcript',
            content: data.data?.telugu_braille_content || '',
            type: 'text/plain',
            size: (data.data?.telugu_braille_content || '').length
          }
        ],
        error: null
      });
    } catch (e) {
      setTeluguBraille({ status: 'error', files: null, error: e.message || 'Failed to generate Telugu Braille' });
    }
  };

  const handleGenerateKannada = async () => {
    setKannadaBraille({ status: 'loading', files: null, error: null });
    try {
      const taggedStep = progressSteps.find(s => s.data && s.data.enriched_transcript);
      const brailleArtStep = progressSteps.find(s => s.data && s.data.braille_art_content);
      if (!taggedStep || !brailleArtStep) throw new Error('Required data missing from pipeline.');
      const response = await fetch(
        `${MODULAR_API_CONFIG.baseUrl}${MODULAR_API_CONFIG.endpoints.brailleInKannada}`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            transcript_content: taggedStep.data.enriched_transcript,
            braille_art_content: brailleArtStep.data.braille_art_content
          })
        }
      );
      if (!response.ok) throw new Error('Kannada Braille API failed');
      const data = await response.json();
      setKannadaBraille({
        status: 'done',
        files: [
          {
            name: 'Kannada Enhanced Transcript',
            content: data.data?.kannada_braille_content || '',
            type: 'text/plain',
            size: (data.data?.kannada_braille_content || '').length
          }
        ],
        error: null
      });
    } catch (e) {
      setKannadaBraille({ status: 'error', files: null, error: e.message || 'Failed to generate Kannada Braille' });
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
                className={`toggle-btn${inputMode === 'youtube' ? ' active' : ''}`}
                onClick={() => inputMode !== 'youtube' && handleModeToggle()}
                type="button"
              >
                📺 YouTube URL
              </button>
              <button
                className={`toggle-btn${inputMode === 'file' ? ' active' : ''}`}
                onClick={() => inputMode !== 'file' && handleModeToggle()}
                type="button"
              >
                📄 File Upload
              </button>
            </div>
            {inputMode === 'youtube' ? (
              <YouTubeInput 
                onUrlChange={handleYouTubeUrlChange}
                disabled={isLoading}
              />
            ) : (
              <FileUpload 
                onFileSelect={handleFileSelect}
                selectedFile={selectedFile}
                disabled={isLoading}
              />
            )}
            <div className="generate-section" style={{ justifyContent: 'center', alignItems: 'center', width: '100%', display: 'flex', flexDirection: 'column' }}>
              <button
                className={`generate-btn${canGenerate() ? ' enabled' : ' disabled'}${isPipelineRunning ? ' processing' : ''}`}
                onClick={handleGenerate}
                disabled={!canGenerate()}
                type="button"
                data-tooltip={isPipelineRunning ? 'Processing...' : ''}
                style={{ margin: '0 auto', display: 'block' }}
              >
                ⚡ {isPipelineRunning ? 'Processing...' : 'Generate Braille'}
              </button>
              {isPipelineRunning && (
                <p className="generate-description">
                  Converting your content to Braille format...
                </p>
              )}
            </div>
            {/* Show progress only when pipeline is running and dynamically add steps as APIs progress */}
            {(isPipelineRunning || progressSteps.length > 0) && (
              <div style={{ margin: '2rem 0' }}>
                <PipelineProgress
                  steps={progressSteps}
                  isRunning={isPipelineRunning}
                  onRetry={handleRetryStep}
                  downloadableFiles={downloadableFiles}
                />
              </div>
            )}
            {/* Download Files and Text Preview sections removed as per user request */}
            {isLoading && <LoadingSpinner />}
            {error && (
              <div className="error-message">
                <p>{error}</p>
              </div>
            )}
            {/* Only show Results if present and not empty, and not a removed section */}
            {results && (
              <Results
                data={results}
                onGenerateTelugu={handleGenerateTelugu}
                onGenerateKannada={handleGenerateKannada}
                teluguState={teluguBraille}
                kannadaState={kannadaBraille}
              />
            )}
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}

export default App;

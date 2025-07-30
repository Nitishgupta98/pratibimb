# 🔧 Modular Pipeline API Usage Guide

## Overview
The modular pipeline API provides 13 individual endpoints that break down the full Braille conversion pipeline into discrete, reusable steps. Each endpoint can be called independently for better scalability and debugging.

## 🚀 Running the API Locally

### Option 1: Using start_all_macos.sh (Recommended)
```bash
# This will start both API server (main.py) and UI
./start_all_macos.sh
```
**Note**: The `start_all_macos.sh` script currently starts `main.py` on port 8000, NOT the modular pipeline API.

### Option 2: Running Modular Pipeline API Separately
```bash
# Navigate to API directory
cd API/

# Start modular pipeline API on port 8001
python3 modular_pipeline.py
```

### Option 3: Both APIs Running Simultaneously
```bash
# Terminal 1: Start main API (port 8000)
cd API/
./start_server_macos.sh

# Terminal 2: Start modular pipeline API (port 8001)
cd API/
python3 modular_pipeline.py
```

## 🌐 API Endpoints

### Base URL: `http://localhost:8001`

### Available Endpoints:
1. **POST** `/validate-youtube-url` - Validate YouTube URL
2. **POST** `/download-video` - Download video from YouTube  
3. **POST** `/extract-audio-transcript` - Extract audio transcript
4. **POST** `/extract-video-frames` - Extract video frames
5. **POST** `/deduplicate-frames` - Remove duplicate frames
6. **POST** `/generate-visual-descriptions` - Generate descriptions for frames
7. **POST** `/merge-audio-visual` - Merge audio and visual transcripts
8. **POST** `/extract-visual-objects` - Extract relevant visual objects
9. **POST** `/enrich-with-figure-tags` - Add figure tags to transcript
10. **POST** `/generate-ascii-art` - Generate ASCII art from objects
11. **POST** `/generate-braille-art` - Convert ASCII to Braille art
12. **POST** `/assemble-final-document` - Combine transcript with Braille art
13. **POST** `/finalize-output` - Generate final downloadable files

### Health Check Endpoints:
- **GET** `/` - API information and endpoint list
- **GET** `/health` - Health check
- **GET** `/status` - System status

## 💻 Using the API in Your UI Code

### 1. Update Config for Modular API

```javascript
// In UI/src/config.js
export const MODULAR_API_CONFIG = {
  baseUrl: "http://localhost:8001",
  endpoints: {
    validateUrl: "/validate-youtube-url",
    downloadVideo: "/download-video",
    extractAudio: "/extract-audio-transcript",
    extractFrames: "/extract-video-frames",
    deduplicateFrames: "/deduplicate-frames",
    generateDescriptions: "/generate-visual-descriptions",
    mergeAudioVisual: "/merge-audio-visual",
    extractObjects: "/extract-visual-objects",
    enrichTags: "/enrich-with-figure-tags",
    generateAscii: "/generate-ascii-art",
    generateBraille: "/generate-braille-art",
    assembleDocument: "/assemble-final-document",
    finalizeOutput: "/finalize-output"
  }
};

// Helper function to build modular API URLs
export const buildModularApiUrl = (endpoint) => {
  return `${MODULAR_API_CONFIG.baseUrl}${MODULAR_API_CONFIG.endpoints[endpoint]}`;
};
```

### 2. Example Usage in React Component

```javascript
// Example: Sequential Pipeline Execution
import { MODULAR_API_CONFIG, buildModularApiUrl } from './config';

const ModularPipelineComponent = () => {
  const [currentStep, setCurrentStep] = useState(0);
  const [results, setResults] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);

  const pipelineSteps = [
    { key: 'validateUrl', name: 'Validate YouTube URL', requiresUrl: true },
    { key: 'downloadVideo', name: 'Download Video', requiresUrl: true },
    { key: 'extractAudio', name: 'Extract Audio', requiresUrl: true },
    { key: 'extractFrames', name: 'Extract Frames', requiresUrl: false },
    { key: 'deduplicateFrames', name: 'Deduplicate Frames', requiresUrl: false },
    { key: 'generateDescriptions', name: 'Generate Descriptions', requiresUrl: false },
    { key: 'mergeAudioVisual', name: 'Merge Audio Visual', requiresUrl: false },
    { key: 'extractObjects', name: 'Extract Objects', requiresUrl: false },
    { key: 'enrichTags', name: 'Enrich with Tags', requiresUrl: false },
    { key: 'generateAscii', name: 'Generate ASCII Art', requiresUrl: false },
    { key: 'generateBraille', name: 'Generate Braille Art', requiresUrl: false },
    { key: 'assembleDocument', name: 'Assemble Document', requiresUrl: false },
    { key: 'finalizeOutput', name: 'Finalize Output', requiresUrl: false }
  ];

  const executeStep = async (stepIndex, youtubeUrl) => {
    const step = pipelineSteps[stepIndex];
    setCurrentStep(stepIndex);
    
    try {
      const url = buildModularApiUrl(step.key);
      const body = step.requiresUrl ? { youtube_url: youtubeUrl } : {};
      
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body)
      });

      const result = await response.json();
      
      setResults(prev => [...prev, {
        step: stepIndex + 1,
        name: step.name,
        status: result.status,
        message: result.message,
        data: result.data,
        timestamp: result.timestamp
      }]);

      return result;
    } catch (error) {
      console.error(`Step ${stepIndex + 1} failed:`, error);
      setResults(prev => [...prev, {
        step: stepIndex + 1,
        name: step.name,
        status: 'error',
        message: `Failed: ${error.message}`,
        timestamp: new Date().toISOString()
      }]);
      throw error;
    }
  };

  const runFullPipeline = async (youtubeUrl) => {
    setIsProcessing(true);
    setResults([]);
    setCurrentStep(0);

    try {
      for (let i = 0; i < pipelineSteps.length; i++) {
        const result = await executeStep(i, youtubeUrl);
        
        if (result.status === 'error') {
          break; // Stop on first error
        }
        
        // Add delay between steps for better UX
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
    } catch (error) {
      console.error('Pipeline execution failed:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="modular-pipeline">
      {/* Your UI components here */}
    </div>
  );
};
```

### 3. Individual Step Execution

```javascript
// Example: Execute individual steps
const executeIndividualStep = async (stepKey, youtubeUrl = null) => {
  const url = buildModularApiUrl(stepKey);
  const body = youtubeUrl ? { youtube_url: youtubeUrl } : {};
  
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body)
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    return result;
  } catch (error) {
    console.error(`Failed to execute ${stepKey}:`, error);
    throw error;
  }
};

// Usage examples:
// await executeIndividualStep('validateUrl', 'https://youtube.com/watch?v=...');
// await executeIndividualStep('extractFrames');
// await executeIndividualStep('generateBraille');
```

## 🔄 Dependency Information

### Main.py Dependencies
**NO**, the modular pipeline API does **NOT** depend on `main.py`. They are completely independent:

- **main.py** (port 8000): Original monolithic API with `/full-braille-pipeline` endpoint
- **modular_pipeline.py** (port 8001): New modular API with 13 individual endpoints

### Shared Dependencies
Both APIs share the same core modules:
- `core/youtube_analyzer.py`
- `core/braille_art.py`
- `core/translation_utils.py`
- `config.json`

### File Dependencies Between Steps
The modular pipeline steps have dependencies on files created by previous steps:

```
Step 1: validate-youtube-url → No dependencies
Step 2: download-video → No dependencies
Step 3: extract-audio-transcript → No dependencies
Step 4: extract-video-frames → Requires video file from Step 2
Step 5: deduplicate-frames → Requires frames from Step 4
Step 6: generate-visual-descriptions → Requires frames from Step 5
Step 7: merge-audio-visual → Requires audio (Step 3) + visual (Step 6)
Step 8: extract-visual-objects → Requires audio (Step 3) + visual (Step 6)
Step 9: enrich-with-figure-tags → Requires merged transcript (Step 7) + objects (Step 8)
Step 10: generate-ascii-art → Requires visual objects (Step 8)
Step 11: generate-braille-art → Requires ASCII art (Step 10)
Step 12: assemble-final-document → Requires tagged transcript (Step 9) + braille art (Step 11)
Step 13: finalize-output → Requires all previous outputs
```

## 🛠️ Running Options

### Option A: Traditional Workflow (Current start_all_macos.sh)
```bash
./start_all_macos.sh
# Starts main.py on port 8000 + UI on port 3000
# Uses the monolithic /full-braille-pipeline endpoint
```

### Option B: Modular Workflow
```bash
# Terminal 1: Start modular API
cd API/
python3 modular_pipeline.py

# Terminal 2: Start UI (if needed)
cd UI/
npm start

# Update your UI to use port 8001 instead of 8000
```

### Option C: Both APIs Running
```bash
# Terminal 1: Main API
cd API/
./start_server_macos.sh

# Terminal 2: Modular API  
cd API/
python3 modular_pipeline.py

# Terminal 3: UI
cd UI/
npm start

# Now you have both APIs available:
# - http://localhost:8000 (main.py)
# - http://localhost:8001 (modular_pipeline.py)
# - http://localhost:3000 (UI)
```

## 📋 Testing Individual Endpoints

```bash
# Test API availability
curl -X GET http://localhost:8001/

# Test URL validation
curl -X POST http://localhost:8001/validate-youtube-url \
  -H "Content-Type: application/json" \
  -d '{"youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'

# Test health check
curl -X GET http://localhost:8001/health
```

## 🎯 Recommendations

1. **For Development**: Use the modular API for better debugging and testing
2. **For Production**: Consider running both APIs for compatibility
3. **For UI Integration**: Update your config to support both API endpoints
4. **For Testing**: Use individual endpoints to test specific pipeline steps

The modular API provides much better granular control and is perfect for scenarios where you need to:
- Debug specific pipeline steps
- Implement retry logic for individual steps
- Build custom workflows
- Monitor progress at a more detailed level

// Modular Pipeline API Integration Example
// Add this to your UI/src/config.js or create a new file

// Modular Pipeline API Configuration
export const MODULAR_API_CONFIG = {
  baseUrl: "http://localhost:8001", // Modular pipeline runs on port 8001
  timeout: 300000, // 5 minutes timeout
  endpoints: {
    root: "/",
    health: "/health",
    status: "/status",
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
    assembleDocument: "/generate-braille-text",
    finalizeOutput: "/combine-braille-text-and-art",
    brailleInTelugu: "/braille-in-telugu",
    brailleInKannada: "/braille-in-kannada"
  }
};

// Helper function to build modular API URLs
export const buildModularApiUrl = (endpoint) => {
  const endpointPath = MODULAR_API_CONFIG.endpoints[endpoint];
  if (!endpointPath) {
    throw new Error(`Unknown endpoint: ${endpoint}`);
  }
  return `${MODULAR_API_CONFIG.baseUrl}${endpointPath}`;
};

// Helper function to build download URLs for processed files
export const buildDownloadUrl = (fileType) => {
  const downloadEndpoints = {
    'merged_transcript': '/download/merged-transcript',
    'figure_tagged_transcript': '/download/figure-tagged-transcript',
    'braille_art': '/download/braille-art',
    'final_braille_transcript': '/download/final-transcript',
    'enhanced_transcript': '/download/enhanced-transcript',
    'braille': '/download/braille',
    'embosser': '/download/embosser',
    'request_logs': '/download/request-logs'
  };

  const endpoint = downloadEndpoints[fileType];
  if (!endpoint) {
    throw new Error(`Unknown file type: ${fileType}`);
  }
  return `${MODULAR_API_CONFIG.baseUrl}${endpoint}`;
};

// Pipeline step definitions with metadata
export const PIPELINE_STEPS = [
  {
    id: 1,
    key: 'validateUrl',
    name: 'Validate YouTube URL',
    description: 'Check if the YouTube URL is valid and accessible',
    requiresUrl: true,
    icon: '🔍',
    estimatedTime: '2s'
  },
  {
    id: 2,
    key: 'downloadVideo',
    name: 'Download Video',
    description: 'Download video content from YouTube',
    requiresUrl: true,
    icon: '🔄',
    estimatedTime: '30-60s'
  },
  {
    id: 3,
    key: 'extractAudio',
    name: 'Extract Audio Transcript',
    description: 'Extract and transcribe audio content',
    requiresUrl: true,
    icon: '🔊',
    estimatedTime: '15-30s'
  },
  {
    id: 4,
    key: 'extractFrames',
    name: 'Extract Video Frames',
    description: 'Extract key frames from the video',
    requiresUrl: false,
    icon: '🖼️',
    estimatedTime: '10-20s'
  },
  {
    id: 5,
    key: 'deduplicateFrames',
    name: 'Deduplicate Frames',
    description: 'Remove duplicate and similar frames',
    requiresUrl: false,
    icon: '🧹',
    estimatedTime: '5-10s'
  },
  {
    id: 6,
    key: 'generateDescriptions',
    name: 'Generate Visual Descriptions',
    description: 'Create descriptions for unique frames using AI',
    requiresUrl: false,
    icon: '📝',
    estimatedTime: '30-90s'
  },
  {
    id: 7,
    key: 'mergeAudioVisual',
    name: 'Merge Audio & Visual',
    description: 'Combine audio transcript with visual descriptions',
    requiresUrl: false,
    icon: '🔗',
    estimatedTime: '5s'
  },
  {
    id: 8,
    key: 'extractObjects',
    name: 'Extract Visual Objects',
    description: 'Identify relevant visual elements for Braille art',
    requiresUrl: false,
    icon: '🔍',
    estimatedTime: '10-20s'
  },
  {
    id: 9,
    key: 'enrichTags',
    name: 'Enrich with Figure Tags',
    description: 'Add figure references to the transcript',
    requiresUrl: false,
    icon: '🏷️',
    estimatedTime: '5-10s'
  },
  {
    id: 10,
    key: 'generateAscii',
    name: 'Generate ASCII Art',
    description: 'Create ASCII art representations of visual objects',
    requiresUrl: false,
    icon: '🎨',
    estimatedTime: '60-120s'
  },
  {
    id: 11,
    key: 'generateBraille',
    name: 'Generate Braille Art',
    description: 'Convert ASCII art to Braille format',
    requiresUrl: false,
    icon: '⠃',
    estimatedTime: '10s'
  },
  {
    id: 12,
    key: 'assembleDocument',
    name: 'Assemble Final Document',
    description: 'Combine transcript with Braille art',
    requiresUrl: false,
    icon: '📦',
    estimatedTime: '5s'
  },
  {
    id: 13,
    key: 'finalizeOutput',
    name: 'Finalize Output',
    description: 'Prepare downloadable files',
    requiresUrl: false,
    icon: '✅',
    estimatedTime: '5s'
  }
];

// API Service class for modular pipeline
export class ModularPipelineService {
  constructor() {
    this.baseUrl = MODULAR_API_CONFIG.baseUrl;
    this.timeout = MODULAR_API_CONFIG.timeout;
  }

  async checkHealth() {
    try {
      const response = await fetch(buildModularApiUrl('health'));
      return await response.json();
    } catch (error) {
      throw new Error(`Health check failed: ${error.message}`);
    }
  }

  async executeStep(stepKey, youtubeUrl = null, additionalData = {}) {
    const step = PIPELINE_STEPS.find(s => s.key === stepKey);
    if (!step) {
      throw new Error(`Unknown step: ${stepKey}`);
    }

    const url = buildModularApiUrl(stepKey);
    const body = {
      ...(step.requiresUrl && youtubeUrl ? { youtube_url: youtubeUrl } : {}),
      ...additionalData
    };

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
        signal: AbortSignal.timeout(this.timeout)
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `HTTP ${response.status}: ${response.statusText}`);
      }

      const result = await response.json();
      return {
        ...result,
        stepId: step.id,
        stepName: step.name,
        executedAt: new Date().toISOString()
      };
    } catch (error) {
      if (error.name === 'TimeoutError') {
        throw new Error(`Step ${step.name} timed out after ${this.timeout / 1000} seconds`);
      }
      throw new Error(`Step ${step.name} failed: ${error.message}`);
    }
  }

  async runFullPipeline(youtubeUrl, onStepComplete = null, onStepStart = null) {
    const results = [];
    let currentStep = 0;

    for (const step of PIPELINE_STEPS) {
      currentStep++;
      
      if (onStepStart) {
        onStepStart(step, currentStep, PIPELINE_STEPS.length);
      }

      try {
        const result = await this.executeStep(step.key, youtubeUrl);
        results.push(result);

        if (onStepComplete) {
          onStepComplete(result, currentStep, PIPELINE_STEPS.length);
        }

        // Stop on error
        if (result.status === 'error') {
          break;
        }

        // Add small delay between steps for better UX
        await new Promise(resolve => setTimeout(resolve, 500));

      } catch (error) {
        const errorResult = {
          step: currentStep,
          stepId: step.id,
          stepName: step.name,
          status: 'error',
          message: error.message,
          timestamp: new Date().toISOString(),
          executedAt: new Date().toISOString()
        };
        
        results.push(errorResult);
        
        if (onStepComplete) {
          onStepComplete(errorResult, currentStep, PIPELINE_STEPS.length);
        }
        
        break; // Stop on first error
      }
    }

    return results;
  }

  async getApiInfo() {
    try {
      const response = await fetch(buildModularApiUrl('root'));
      return await response.json();
    } catch (error) {
      throw new Error(`Failed to get API info: ${error.message}`);
    }
  }
}

// Export singleton instance
export const modularPipelineService = new ModularPipelineService();

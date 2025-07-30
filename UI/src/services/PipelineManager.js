// PipelineManager.js - Robust Sequential Pipeline Execution
import { MODULAR_API_CONFIG, PIPELINE_STEPS, buildModularApiUrl } from '../modularApiConfig';

export default class PipelineManager {
  constructor() {
    this.baseUrl = MODULAR_API_CONFIG.baseUrl;
    this.timeout = MODULAR_API_CONFIG.timeout;
    this.stepResults = new Map(); // Store results for each step
    this.stepPayloads = new Map(); // Store payloads for retry functionality
    this.currentStep = 0;
    this.totalSteps = PIPELINE_STEPS.length;
    this.isRunning = false;
    this.youtubeUrl = '';
  }

  // Reset pipeline state
  reset() {
    this.stepResults.clear();
    this.stepPayloads.clear();
    this.currentStep = 0;
    this.isRunning = false;
    this.youtubeUrl = '';
  }

  // Get user-friendly step messages
  getStepMessage(step, phase = 'processing') {
    const messages = {
      validateUrl: {
        processing: '🔍 Validating YouTube URL and checking accessibility...',
        success: '✅ YouTube URL validated successfully!',
        error: '❌ Invalid YouTube URL or video not accessible'
      },
      downloadVideo: {
        processing: '🔄 Downloading video content from YouTube...',
        success: '✅ Video downloaded successfully!',
        error: '❌ Failed to download video content'
      },
      extractAudio: {
        processing: '🔊 Extracting and transcribing audio content...',
        success: '✅ Audio transcript generated successfully!',
        error: '❌ Failed to extract audio transcript'
      },
      extractFrames: {
        processing: '🖼️ Extracting key frames from the video...',
        success: '✅ Video frames extracted successfully!',
        error: '❌ Failed to extract video frames'
      },
      deduplicateFrames: {
        processing: '🧹 Removing duplicate and similar frames...',
        success: '✅ Frames deduplicated successfully!',
        error: '❌ Failed to deduplicate frames'
      },
      generateDescriptions: {
        processing: '📝 Generating AI-powered visual descriptions...',
        success: '✅ Visual descriptions generated successfully!',
        error: '❌ Failed to generate visual descriptions'
      },
      mergeAudioVisual: {
        processing: '🔗 Merging audio transcript with visual descriptions...',
        success: '✅ Audio and visual content merged successfully!',
        error: '❌ Failed to merge audio and visual content'
      },
      extractObjects: {
        processing: '🔍 Extracting relevant visual objects for Braille art...',
        success: '✅ Visual objects extracted successfully!',
        error: '❌ Failed to extract visual objects'
      },
      enrichTags: {
        processing: '🏷️ Adding figure references to the transcript...',
        success: '✅ Figure tags added successfully!',
        error: '❌ Failed to add figure tags'
      },
      generateAscii: {
        processing: '🎨 Creating ASCII art representations...',
        success: '✅ ASCII art generated successfully!',
        error: '❌ Failed to generate ASCII art'
      },
      generateBraille: {
        processing: '⠃ Converting ASCII art to Braille format...',
        success: '✅ Braille art generated successfully!',
        error: '❌ Failed to generate Braille art'
      },
      assembleDocument: {
        processing: '📦 Combining transcript with Braille art...',
        success: '✅ Final document assembled successfully!',
        error: '❌ Failed to assemble final document'
      },
      finalizeOutput: {
        processing: '✅ Preparing downloadable files...',
        success: '🎉 Braille conversion completed successfully!',
        error: '❌ Failed to finalize output'
      }
    };

    return messages[step.key]?.[phase] || `${phase} ${step.name}...`;
  }

  // Execute a single step
  async executeStep(step, onStepUpdate = null) {
    const stepIndex = step.id - 1;
    
    try {
      // Notify step start
      if (onStepUpdate) {
        onStepUpdate({
          step: step.id,
          stepName: step.name,
          status: 'processing',
          message: this.getStepMessage(step, 'processing'),
          progress: Math.round((stepIndex / this.totalSteps) * 100),
          timestamp: new Date().toISOString()
        });
      }

      // Prepare request payload based on step requirements
      const payload = this.prepareStepPayload(step);
      this.stepPayloads.set(step.key, payload);

      // Make API call
      const url = buildModularApiUrl(step.key);
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
        signal: AbortSignal.timeout(this.timeout)
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `HTTP ${response.status}: ${response.statusText}`);
      }

      const result = await response.json();
      
      // Store result for next steps
      this.stepResults.set(step.key, result);
      
      // Notify step success
      if (onStepUpdate) {
        onStepUpdate({
          step: step.id,
          stepName: step.name,
          status: 'success',
          message: this.getStepMessage(step, 'success'),
          progress: Math.round(((stepIndex + 1) / this.totalSteps) * 100),
          timestamp: new Date().toISOString(),
          data: result.data
        });
      }

      return result;

    } catch (error) {
      // Handle different types of errors
      let errorMessage = error.message;
      if (error.name === 'TimeoutError') {
        errorMessage = `Step timed out after ${this.timeout / 1000} seconds`;
      } else if (error.name === 'AbortError') {
        errorMessage = 'Step was cancelled';
      }

      // Notify step error
      if (onStepUpdate) {
        onStepUpdate({
          step: step.id,
          stepName: step.name,
          status: 'error',
          message: this.getStepMessage(step, 'error'),
          error: errorMessage,
          progress: Math.round((stepIndex / this.totalSteps) * 100),
          timestamp: new Date().toISOString(),
          retryable: true
        });
      }

      throw error;
    }
  }

  // Prepare payload for each step based on previous results
  prepareStepPayload(step) {
    const basePayload = {};

    switch (step.key) {
      case 'validateUrl':
      case 'downloadVideo':
      case 'extractAudio':
        return { youtube_url: this.youtubeUrl };

      case 'extractFrames':
        const videoResult = this.stepResults.get('downloadVideo');
        return {
          video_content: videoResult?.data?.video_content || ''
        };

      case 'deduplicateFrames':
        const framesResult = this.stepResults.get('extractFrames');
        return {
          frames_data: framesResult?.data?.frames_data || [],
          ssim_threshold: 0.95
        };

      case 'generateDescriptions':
        const uniqueFramesResult = this.stepResults.get('deduplicateFrames');
        const videoInfo = this.stepResults.get('downloadVideo');
        return {
          frames_data: uniqueFramesResult?.data?.unique_frames || [],
          video_title: videoInfo?.data?.video_title || 'Video Content'
        };

      case 'mergeAudioVisual':
        const audioResult = this.stepResults.get('extractAudio');
        const visualResult = this.stepResults.get('generateDescriptions');
        return {
          audio_transcript: audioResult?.data?.transcript_content || '',
          visual_description: visualResult?.data?.description_content || ''
        };

      case 'extractObjects':
        const audioTranscript = this.stepResults.get('extractAudio');
        const visualDesc = this.stepResults.get('generateDescriptions');
        return {
          audio_transcript: audioTranscript?.data?.transcript_content || '',
          visual_description: visualDesc?.data?.description_content || ''
        };

      case 'enrichTags':
        const mergedResult = this.stepResults.get('mergeAudioVisual');
        const objectsResult = this.stepResults.get('extractObjects');
        return {
          merged_transcript: mergedResult?.data?.merged_transcript || '',
          visual_objects: objectsResult?.data?.visual_objects || []
        };

      case 'generateAscii':
      case 'generateBraille':
        const visualObjectsResult = this.stepResults.get('extractObjects');
        return {
          visual_objects: visualObjectsResult?.data?.visual_objects || []
        };

      case 'assembleDocument':
        const enrichedResult = this.stepResults.get('enrichTags');
        const brailleResult = this.stepResults.get('generateBraille');
        return {
          transcript_content: enrichedResult?.data?.enriched_transcript || '',
          braille_art_content: brailleResult?.data?.braille_art_content || ''
        };

      case 'finalizeOutput':
        const finalDocResult = this.stepResults.get('assembleDocument');
        const asciiResult = this.stepResults.get('generateAscii');
        const brailleArtResult = this.stepResults.get('generateBraille');
        const taggedResult = this.stepResults.get('enrichTags');
        return {
          final_document: finalDocResult?.data?.final_braille_content || '',
          ascii_art: asciiResult?.data?.ascii_art_content || '',
          braille_art: brailleArtResult?.data?.braille_art_content || '',
          tagged_transcript: taggedResult?.data?.enriched_transcript || ''
        };

      default:
        return basePayload;
    }
  }

  // Run full pipeline
  async runPipeline(youtubeUrl, onStepUpdate = null, onComplete = null) {
    this.reset();
    this.youtubeUrl = youtubeUrl;
    this.isRunning = true;

    try {
      for (let i = 0; i < PIPELINE_STEPS.length; i++) {
        if (!this.isRunning) {
          break; // Pipeline was stopped
        }

        const step = PIPELINE_STEPS[i];
        this.currentStep = i + 1;

        await this.executeStep(step, onStepUpdate);

        // Small delay between steps for better UX
        await new Promise(resolve => setTimeout(resolve, 500));
      }

      // Pipeline completed successfully
      if (this.isRunning && onComplete) {
        onComplete({
          status: 'success',
          message: '🎉 Braille conversion pipeline completed successfully!',
          results: this.getAllResults(),
          timestamp: new Date().toISOString()
        });
      }

    } catch (error) {
      if (onComplete) {
        onComplete({
          status: 'error',
          message: `Pipeline failed at step ${this.currentStep}: ${error.message}`,
          error: error.message,
          currentStep: this.currentStep,
          results: this.getAllResults(),
          timestamp: new Date().toISOString()
        });
      }
    } finally {
      this.isRunning = false;
    }
  }

  // Retry from a specific step
  async retryFromStep(stepNumber, onStepUpdate = null, onComplete = null) {
    if (stepNumber < 1 || stepNumber > PIPELINE_STEPS.length) {
      throw new Error(`Invalid step number: ${stepNumber}`);
    }

    this.isRunning = true;
    this.currentStep = stepNumber - 1;

    try {
      for (let i = stepNumber - 1; i < PIPELINE_STEPS.length; i++) {
        if (!this.isRunning) {
          break;
        }

        const step = PIPELINE_STEPS[i];
        this.currentStep = i + 1;

        await this.executeStep(step, onStepUpdate);

        // Small delay between steps
        await new Promise(resolve => setTimeout(resolve, 500));
      }

      // Retry completed successfully
      if (this.isRunning && onComplete) {
        onComplete({
          status: 'success',
          message: '🎉 Pipeline retry completed successfully!',
          results: this.getAllResults(),
          timestamp: new Date().toISOString()
        });
      }

    } catch (error) {
      if (onComplete) {
        onComplete({
          status: 'error',
          message: `Retry failed at step ${this.currentStep}: ${error.message}`,
          error: error.message,
          currentStep: this.currentStep,
          results: this.getAllResults(),
          timestamp: new Date().toISOString()
        });
      }
    } finally {
      this.isRunning = false;
    }
  }

  // Stop pipeline execution
  stop() {
    this.isRunning = false;
  }

  // Get all results
  getAllResults() {
    const results = {};
    this.stepResults.forEach((result, stepKey) => {
      results[stepKey] = result;
    });
    return results;
  }

  // Get downloadable files
  getDownloadableFiles() {
    const finalizeResult = this.stepResults.get('finalizeOutput');
    return finalizeResult?.data?.available_files || [];
  }

  // Check if pipeline is complete
  isComplete() {
    return this.stepResults.size === PIPELINE_STEPS.length && 
           this.stepResults.get('finalizeOutput')?.status === 'success';
  }

  // Health check
  async checkHealth() {
    try {
      const response = await fetch(buildModularApiUrl('health'));
      const result = await response.json();
      return result.status === 'healthy';
    } catch (error) {
      return false;
    }
  }
}

// Export singleton instance
export const pipelineManager = new PipelineManager();

// Configuration for different deployment environments
const config = {
  development: {
    apiBaseUrl: "http://localhost:8000",
  },
  production: {
    // For VM deployment - these will be configured based on actual VM setup
    apiBaseUrl: process.env.REACT_APP_API_URL || "http://localhost:8000",
  },
  vm: {
    // For Windows VM deployment
    apiBaseUrl: process.env.REACT_APP_API_URL || "http://YOUR_VM_IP:8000",
  }
};

// Auto-detect environment
const getEnvironment = () => {
  // Check if we're in development mode
  if (process.env.NODE_ENV === 'development') {
    return 'development';
  }
  
  // Check if REACT_APP_ENVIRONMENT is set
  if (process.env.REACT_APP_ENVIRONMENT) {
    return process.env.REACT_APP_ENVIRONMENT;
  }
  
  // Check if we're running on a VM (can be detected by hostname or custom env var)
  if (process.env.REACT_APP_VM_DEPLOYMENT === 'true') {
    return 'vm';
  }
  
  // Default to production
  return 'production';
};

const currentEnv = getEnvironment();
const currentConfig = config[currentEnv];

// API endpoints
export const API_CONFIG = {
  baseUrl: currentConfig.apiBaseUrl,
  endpoints: {
    processTranscript: "/process_transcript",
    getRawTranscript: "/get_raw_transcript", 
    getEnhanceTranscript: "/get_enhance_transcript",
    getLatestReport: "/api/latest-report",
    getLatestReportData: "/api/latest-report-data",
    downloadFile: "/api/download",
    streamLogs: "/api/stream-logs",
    requestLog: "/api/request-log"
  }
};

// Helper function to build full API URLs
export const buildApiUrl = (endpoint) => {
  return `${API_CONFIG.baseUrl}${endpoint}`;
};

// Helper function to build streaming logs URL
export const buildStreamLogsUrl = (requestId) => {
  return `${API_CONFIG.baseUrl}/api/stream-logs/${requestId}`;
};

// Helper function to build download URL
export const buildDownloadUrl = (fileType) => {
  return `${API_CONFIG.baseUrl}/api/download/${fileType}`;
};

// Debug information
console.log(`🌐 Environment: ${currentEnv}`);
console.log(`🔗 API Base URL: ${API_CONFIG.baseUrl}`);

export default API_CONFIG;

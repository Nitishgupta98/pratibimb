// API Configuration
const API_CONFIG = {
  baseURL: 'https://api.example.com',
  endpoints: {
    pratibimbData: '/pratibimb-data',
    convert: '/api/convert',
    validate: '/api/validate',
    bulkConvert: '/api/bulk-convert',
    status: '/api/status',
    config: '/api/config',
    history: '/api/history',
    logs: '/api/logs',
    download: '/api/download'
  }
};

// Utility function to handle API calls with fallback to local data
const apiCall = async (url, options = {}) => {
  try {
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      ...options
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.warn(`API call failed: ${error.message}. Using fallback data.`);
    throw error;
  }
};

// Main data fetching function with fallback to local JSON
export const fetchPratibimbData = async () => {
  try {
    // Try to fetch from API first
    const apiUrl = `${API_CONFIG.baseURL}${API_CONFIG.endpoints.pratibimbData}`;
    const data = await apiCall(apiUrl);
    console.log('Data loaded from API successfully');
    return data;
  } catch (error) {
    try {
      // Fallback to local JSON file
      console.log('Loading data from local JSON file...');
      const response = await fetch('/db/pratibimb_data_export.json');
      if (!response.ok) {
        throw new Error('Failed to load local data');
      }
      const data = await response.json();
      console.log('Data loaded from local JSON successfully');
      return data;
    } catch (localError) {
      console.error('Failed to load data from both API and local file:', localError);
      // Return minimal structure to prevent app crash
      return {
        carousel_slides: [],
        products: [],
        forum_posts: [],
        community_features: [],
        learning_tools: [],
        recent_activities: [],
        latest_updates: [],
        quick_links: [],
        users: []
      };
    }
  }
};

// Braille conversion API functions
export const convertTextToBraille = async (text, config = {}) => {
  try {
    const apiUrl = `${API_CONFIG.baseURL}${API_CONFIG.endpoints.convert}`;
    return await apiCall(apiUrl, {
      method: 'POST',
      body: JSON.stringify({ text, config })
    });
  } catch (error) {
    console.error('Braille conversion failed:', error);
    throw error;
  }
};

export const validateBrailleContent = async (content, formatType = 'unicode', config = {}) => {
  try {
    const apiUrl = `${API_CONFIG.baseURL}${API_CONFIG.endpoints.validate}`;
    return await apiCall(apiUrl, {
      method: 'POST',
      body: JSON.stringify({ content, format_type: formatType, config })
    });
  } catch (error) {
    console.error('Braille validation failed:', error);
    throw error;
  }
};

export const bulkConvertTexts = async (texts, config = {}) => {
  try {
    const apiUrl = `${API_CONFIG.baseURL}${API_CONFIG.endpoints.bulkConvert}`;
    return await apiCall(apiUrl, {
      method: 'POST',
      body: JSON.stringify({ texts, config })
    });
  } catch (error) {
    console.error('Bulk conversion failed:', error);
    throw error;
  }
};

export const getConversionStatus = async (id) => {
  try {
    const apiUrl = `${API_CONFIG.baseURL}${API_CONFIG.endpoints.status}/${id}`;
    return await apiCall(apiUrl);
  } catch (error) {
    console.error('Failed to get conversion status:', error);
    throw error;
  }
};

export const getApiConfig = async () => {
  try {
    const apiUrl = `${API_CONFIG.baseURL}${API_CONFIG.endpoints.config}`;
    return await apiCall(apiUrl);
  } catch (error) {
    console.error('Failed to get API config:', error);
    throw error;
  }
};

export const getConversionHistory = async () => {
  try {
    const apiUrl = `${API_CONFIG.baseURL}${API_CONFIG.endpoints.history}`;
    return await apiCall(apiUrl);
  } catch (error) {
    console.error('Failed to get conversion history:', error);
    return [];
  }
};

export const getApiLogs = async () => {
  try {
    const apiUrl = `${API_CONFIG.baseURL}${API_CONFIG.endpoints.logs}`;
    return await apiCall(apiUrl);
  } catch (error) {
    console.error('Failed to get API logs:', error);
    return [];
  }
};

export const downloadConversionFile = async (id, format = 'brf') => {
  try {
    const apiUrl = `${API_CONFIG.baseURL}${API_CONFIG.endpoints.download}/${id}?format=${format}`;
    const response = await fetch(apiUrl);
    if (!response.ok) {
      throw new Error(`Download failed: ${response.status}`);
    }
    return response.blob();
  } catch (error) {
    console.error('Failed to download file:', error);
    throw error;
  }
};

// Health check function
export const checkApiHealth = async () => {
  try {
    const response = await fetch(`${API_CONFIG.baseURL}/health`);
    return response.ok;
  } catch (error) {
    return false;
  }
};

export default API_CONFIG;

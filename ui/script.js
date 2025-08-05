// App State
console.log('🔄 Pratibimb Script Loaded - Version 2025-07-12-v2 (All Utils.delay references removed)');
const AppState = {
    currentSection: 'dashboard',
    isProcessing: false,
    currentVideo: null,
    results: {
        original: '',
        braille: '',
        embosser: ''
    }
};

// DOM Elements
const elements = {
    sidebar: document.getElementById('sidebar'),
    mobileMenuToggle: document.getElementById('mobileMenuToggle'),
    menuToggle: document.getElementById('menuToggle'),
    youtubeUrl: document.getElementById('youtubeUrl'),
    convertBtn: document.getElementById('convertBtn'),
    progressContainer: document.getElementById('progressContainer'),
    progressFill: document.getElementById('progressFill'),
    progressText: document.getElementById('progressText'),
    resultsArea: document.getElementById('resultsArea'),
    quickStats: document.getElementById('quickStats'),
    loadingOverlay: document.getElementById('loadingOverlay'),
    toast: document.getElementById('toast'),
    
    // Past conversions
    pastConversionsToggle: document.getElementById('pastConversionsToggle'),
    conversionsList: document.getElementById('conversionsList'),
    toggleIcon: document.getElementById('toggleIcon'),
    
    // Result textareas
    originalText: document.getElementById('originalText'),
    brailleText: document.getElementById('brailleText'),
    embosserText: document.getElementById('embosserText'),
    
    // Stats
    videoDuration: document.getElementById('videoDuration'),
    charCount: document.getElementById('charCount'),
    wordCount: document.getElementById('wordCount'),
    brailleCount: document.getElementById('brailleCount'),
    
    // Options
    includeTimestamps: document.getElementById('includeTimestamps'),
    formatForEmbosser: document.getElementById('formatForEmbosser'),
    languageSelect: document.getElementById('languageSelect')
};

// Utility Functions
const Utils = {
    // Extract YouTube video ID from URL
    extractVideoId(url) {
        const patterns = [
            /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)/,
            /youtube\.com\/v\/([^&\n?#]+)/
        ];
        
        for (const pattern of patterns) {
            const match = url.match(pattern);
            if (match && match[1]) return match[1];
        }
        return null;
    },

    // Validate YouTube URL
    isValidYouTubeUrl(url) {
        return this.extractVideoId(url) !== null;
    },

    // Format relative time
    formatRelativeTime(dateString) {
        const now = new Date();
        const date = new Date(dateString);
        const diffInHours = Math.floor((now - date) / (1000 * 60 * 60));
        
        if (diffInHours < 1) return 'Just now';
        if (diffInHours < 24) return `${diffInHours}h ago`;
        
        const diffInDays = Math.floor(diffInHours / 24);
        if (diffInDays < 7) return `${diffInDays}d ago`;
        
        const diffInWeeks = Math.floor(diffInDays / 7);
        if (diffInWeeks < 4) return `${diffInWeeks}w ago`;
        
        const diffInMonths = Math.floor(diffInDays / 30);
        return `${diffInMonths}mo ago`;
    },

    // Count words in text
    countWords(text) {
        return text.trim().split(/\s+/).filter(word => word.length > 0).length;
    },

    // Show toast notification
    showToast(message, type = 'success', duration = 4000) {
        const toast = elements.toast;
        const icon = toast.querySelector('.toast-icon');
        const messageEl = toast.querySelector('.toast-message');
        
        // Check if toast already has a close button, if not add one
        let closeBtn = toast.querySelector('.toast-close');
        if (!closeBtn) {
            closeBtn = document.createElement('button');
            closeBtn.className = 'toast-close';
            closeBtn.innerHTML = '<i class="fas fa-times"></i>';
            closeBtn.title = 'Close';
            toast.appendChild(closeBtn);
            
            // Add close functionality
            closeBtn.addEventListener('click', () => {
                this.hideToast(toast);
            });
            
            // Double-click for force close
            closeBtn.addEventListener('dblclick', () => {
                // Force immediate cleanup
                toast.style.transform = 'translateX(400px)';
                toast.style.opacity = '0';
                toast.style.visibility = 'hidden';
                toast.classList.remove('show');
                
                if (toast.hideTimeout) {
                    clearTimeout(toast.hideTimeout);
                    delete toast.hideTimeout;
                }
                
                setTimeout(() => {
                    toast.style.transform = '';
                    toast.style.opacity = '';
                    toast.style.visibility = '';
                    toast.className = 'toast';
                }, 100);
            });
        }
        
        // Set content
        messageEl.textContent = message;
        
        // Set icon and style based on type
        if (type === 'success') {
            icon.className = 'toast-icon fas fa-check-circle';
            toast.className = 'toast';
        } else if (type === 'error') {
            icon.className = 'toast-icon fas fa-exclamation-circle';
            toast.className = 'toast error';
        } else if (type === 'info') {
            icon.className = 'toast-icon fas fa-info-circle';
            toast.className = 'toast info';
        } else if (type === 'warning') {
            icon.className = 'toast-icon fas fa-exclamation-triangle';
            toast.className = 'toast warning';
        }
        
        // Show toast
        toast.classList.add('show');
        
        // Clear any existing timeout
        if (toast.hideTimeout) {
            clearTimeout(toast.hideTimeout);
        }
        
        // Hide after specified duration (0 means don't auto-hide)
        if (duration > 0) {
            toast.hideTimeout = setTimeout(() => {
                this.hideToast(toast);
            }, duration);
        }
    },

    // Properly hide toast with animation and cleanup
    hideToast(toast) {
        toast.classList.remove('show');
        
        // Clear any existing timeout
        if (toast.hideTimeout) {
            clearTimeout(toast.hideTimeout);
            delete toast.hideTimeout;
        }
        
        // After animation completes, reset the toast completely
        setTimeout(() => {
            // Force hide by setting transform directly
            toast.style.transform = 'translateX(400px)';
            
            // Reset after a brief delay to ensure it's completely hidden
            setTimeout(() => {
                toast.style.transform = '';
                toast.className = 'toast'; // Reset to default class
            }, 100);
        }, 300); // Match the CSS transition duration
    },

    // Copy text to clipboard
    async copyToClipboard(text) {
        try {
            await navigator.clipboard.writeText(text);
            this.showToast('Copied to clipboard!');
        } catch (err) {
            console.error('Failed to copy text: ', err);
            this.showToast('Failed to copy text', 'error');
        }
    },

    // Download text as file
    downloadText(text, filename) {
        const blob = new Blob([text], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        this.showToast(`Downloaded ${filename}!`);
    },

    // Format duration from seconds
    formatDuration(seconds) {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = Math.floor(seconds % 60);
        
        if (hours > 0) {
            return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        }
        return `${minutes}:${secs.toString().padStart(2, '0')}`;
    },

    // Load past conversions from data.json
    async loadPastConversions() {
        try {
            const response = await fetch('data.json');
            if (!response.ok) throw new Error('Failed to fetch');
            const data = await response.json();
            return data.past_conversions.sort((a, b) => new Date(b.date) - new Date(a.date));
        } catch (error) {
            console.error('Failed to load past conversions from data.json, using fallback data:', error);
            // Fallback data when file can't be loaded (e.g., CORS restrictions)
            return [
                {
                    id: "conv_001",
                    title: "Introduction to Machine Learning",
                    youtube_url: "https://www.youtube.com/watch?v=aircAruvnKk",
                    date: "2025-07-12T14:30:00Z",
                    duration: "19:13",
                    status: "completed",
                    type: "youtube",
                    word_count: 2845,
                    braille_chars: 4267
                },
                {
                    id: "conv_002",
                    title: "Understanding Neural Networks",
                    youtube_url: "https://www.youtube.com/watch?v=bfmFfD2RIcg",
                    date: "2025-07-12T11:15:00Z",
                    duration: "22:07",
                    status: "completed",
                    type: "youtube",
                    word_count: 3124,
                    braille_chars: 4686
                },
                {
                    id: "conv_003",
                    title: "Accessibility in Web Development",
                    youtube_url: "https://www.youtube.com/watch?v=20SHvU2PKsM",
                    date: "2025-07-12T09:45:00Z",
                    duration: "15:30",
                    status: "completed",
                    type: "youtube",
                    word_count: 2156,
                    braille_chars: 3234
                },
                {
                    id: "conv_004",
                    title: "Python Programming Tutorial",
                    youtube_url: "https://www.youtube.com/watch?v=_uQrJ0TkZlc",
                    date: "2025-07-11T16:20:00Z",
                    duration: "28:45",
                    status: "completed",
                    type: "youtube",
                    word_count: 4512,
                    braille_chars: 6768
                },
                {
                    id: "conv_005",
                    title: "Data Science Fundamentals",
                    youtube_url: "https://www.youtube.com/watch?v=ua-CiDNNj30",
                    date: "2025-07-11T13:10:00Z",
                    duration: "32:12",
                    status: "completed",
                    type: "youtube",
                    word_count: 5234,
                    braille_chars: 7851
                }
            ].sort((a, b) => new Date(b.date) - new Date(a.date));
        }
    },

    // API Configuration
    API_BASE_URL: 'http://localhost:8001/api',

    // Call FastAPI backend for conversion
    async callPratibimbAPI(text, config = {}) {
        const response = await fetch(`${this.API_BASE_URL}/convert`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text,
                config: config
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || `API Error: ${response.status}`);
        }

        return await response.json();
    },

    // Get conversion status from API
    async getConversionStatus(conversionId) {
        const response = await fetch(`${this.API_BASE_URL}/status/${conversionId}`);
        if (!response.ok) {
            throw new Error(`Failed to get status: ${response.status}`);
        }
        return await response.json();
    },

    // Get recent logs from API
    async getRecentLogs(lines = 10) {
        try {
            const response = await fetch(`${this.API_BASE_URL}/logs?lines=${lines}`);
            if (!response.ok) {
                throw new Error(`Failed to get logs: ${response.status}`);
            }
            const data = await response.json();
            return data.logs || [];
        } catch (error) {
            console.error('Failed to fetch logs:', error);
            return [];
        }
    }
};

// Braille Conversion Functions
const BrailleConverter = {
    // Basic English to Braille mapping (Grade 1)
    brailleMap: {
        'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑', 'f': '⠋', 'g': '⠛', 'h': '⠓', 'i': '⠊', 'j': '⠚',
        'k': '⠅', 'l': '⠇', 'm': '⠍', 'n': '⠝', 'o': '⠕', 'p': '⠏', 'q': '⠟', 'r': '⠗', 's': '⠎', 't': '⠞',
        'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭', 'y': '⠽', 'z': '⠵',
        '1': '⠼⠁', '2': '⠼⠃', '3': '⠼⠉', '4': '⠼⠙', '5': '⠼⠑', '6': '⠼⠋', '7': '⠼⠛', '8': '⠼⠓', '9': '⠼⠊', '0': '⠼⠚',
        '.': '⠲', ',': '⠂', '?': '⠦', '!': '⠖', ':': '⠒', ';': '⠆', '-': '⠤', '(': '⠐⠣', ')': '⠐⠜',
        '"': '⠐⠦', "'": '⠄', ' ': ' ', '\n': '\n', '\t': '⠀⠀⠀⠀'
    },

    // Convert text to Braille
    textToBraille(text) {
        let result = '';
        let isCapital = false;
        
        for (let char of text) {
            if (char === char.toUpperCase() && char !== char.toLowerCase()) {
                if (!isCapital) {
                    result += '⠠'; // Capital indicator
                    isCapital = true;
                }
            } else {
                isCapital = false;
            }
            
            const lowerChar = char.toLowerCase();
            result += this.brailleMap[lowerChar] || char;
        }
        
        return result;
    },

    // Format for embosser (ASCII Braille)
    formatForEmbosser(brailleText, options = {}) {
        const lineLength = options.lineLength || 40;
        const pageLength = options.pageLength || 25;
        
        // Convert Unicode Braille to ASCII Braille
        const asciiMap = {
            '⠁': 'A', '⠃': 'B', '⠉': 'C', '⠙': 'D', '⠑': 'E', '⠋': 'F', '⠛': 'G', '⠓': 'H', '⠊': 'I', '⠚': 'J',
            '⠅': 'K', '⠇': 'L', '⠍': 'M', '⠝': 'N', '⠕': 'O', '⠏': 'P', '⠟': 'Q', '⠗': 'R', '⠎': 'S', '⠞': 'T',
            '⠥': 'U', '⠧': 'V', '⠺': 'W', '⠭': 'X', '⠽': 'Y', '⠵': 'Z', '⠼': '#', '⠠': ',', '⠲': '.', '⠂': "'",
            '⠦': '?', '⠖': '!', '⠒': ':', '⠆': ';', '⠤': '-', '⠐': '"', '⠣': '<', '⠜': '>', '⠄': "'"
        };
        
        let asciiText = '';
        for (let char of brailleText) {
            asciiText += asciiMap[char] || char;
        }
        
        // Format lines
        const words = asciiText.split(' ');
        const lines = [];
        let currentLine = '';
        
        for (let word of words) {
            if (currentLine.length + word.length + 1 <= lineLength) {
                currentLine += (currentLine ? ' ' : '') + word;
            } else {
                if (currentLine) lines.push(currentLine);
                currentLine = word;
            }
        }
        if (currentLine) lines.push(currentLine);
        
        // Add page breaks
        const pages = [];
        for (let i = 0; i < lines.length; i += pageLength) {
            pages.push(lines.slice(i, i + pageLength).join('\n'));
        }
        
        return pages.join('\n\f'); // Form feed for page breaks
    }
};

// Mock YouTube API functions (replace with actual implementation)
const YouTubeAPI = {
    async getVideoInfo(videoId) {
        // Simulate API delay
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Mock video data
        return {
            title: "Sample Video Title",
            duration: 300, // 5 minutes
            channel: "Sample Channel",
            description: "Sample description"
        };
    },

    async getTranscript(videoId, language = 'en') {
        // Simulate processing delay
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // Mock transcript data
        const mockTranscript = `Hello and welcome to this video. Today we're going to learn about accessibility and Braille conversion. 

Braille is a tactile writing system used by people who are visually impaired. It consists of patterns of raised dots arranged in cells.

Each cell can contain up to six dots, arranged in two columns of three dots each. Different combinations of these dots represent different letters, numbers, and punctuation marks.

The system was invented by Louis Braille in 1824 when he was just 15 years old. It has since become the standard form of written communication for blind and visually impaired people worldwide.

Today, we have technology that can convert regular text into Braille format, making digital content more accessible to everyone.

Thank you for watching this video about Braille accessibility.`;

        return {
            text: mockTranscript,
            timestamps: [
                { start: 0, end: 10, text: "Hello and welcome to this video." },
                { start: 10, end: 25, text: "Today we're going to learn about accessibility and Braille conversion." },
                // ... more timestamps
            ]
        };
    }
};

// Main App Functions
const App = {
    init() {
        this.bindEvents();
        this.updateProgress(0);
        this.loadPastConversions();
    },

    bindEvents() {
        // Mobile menu toggle
        elements.mobileMenuToggle?.addEventListener('click', () => this.toggleSidebar());
        elements.menuToggle?.addEventListener('click', () => this.toggleSidebar());
        
        // Past conversions toggle
        elements.pastConversionsToggle?.addEventListener('click', () => this.togglePastConversions());
        
        // Sidebar navigation
        document.querySelectorAll('.sidebar-menu a').forEach(link => {
            link.addEventListener('click', (e) => this.handleNavClick(e));
        });

        // Convert button
        elements.convertBtn?.addEventListener('click', () => this.handleConversion());
        
        // Shortcuts tooltip functionality
        const shortcutsToggle = document.getElementById('shortcutsToggle');
        const shortcutsTooltip = document.getElementById('shortcutsTooltip');
        
        if (shortcutsToggle && shortcutsTooltip) {
            shortcutsToggle.addEventListener('click', (e) => {
                e.stopPropagation();
                shortcutsTooltip.classList.toggle('show');
            });
            
            // Close tooltip when clicking outside
            document.addEventListener('click', (e) => {
                if (!shortcutsToggle.contains(e.target) && !shortcutsTooltip.contains(e.target)) {
                    shortcutsTooltip.classList.remove('show');
                }
            });
            
            // Close tooltip on Escape
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape') {
                    shortcutsTooltip.classList.remove('show');
                }
            });
        }

        // Tab switching
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.handleTabSwitch(e));
        });

        // Copy and download buttons
        this.bindActionButtons();

        // URL input validation
        elements.youtubeUrl?.addEventListener('input', () => this.validateUrl());

        // Enter key in URL input
        elements.youtubeUrl?.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !elements.convertBtn.disabled) {
                this.handleConversion();
            }
        });
    },

    bindActionButtons() {
        // Copy buttons
        document.getElementById('copyOriginal')?.addEventListener('click', () => {
            Utils.copyToClipboard(AppState.results.original);
        });
        
        document.getElementById('copyBraille')?.addEventListener('click', () => {
            Utils.copyToClipboard(AppState.results.braille);
        });
        
        document.getElementById('copyEmbosser')?.addEventListener('click', () => {
            Utils.copyToClipboard(AppState.results.embosser);
        });

        // Download buttons
        document.getElementById('downloadOriginal')?.addEventListener('click', () => {
            Utils.downloadText(AppState.results.original, 'transcript.txt');
        });
        
        document.getElementById('downloadBraille')?.addEventListener('click', () => {
            Utils.downloadText(AppState.results.braille, 'braille_output.txt');
        });
        
        document.getElementById('downloadEmbosser')?.addEventListener('click', () => {
            Utils.downloadText(AppState.results.embosser, 'embosser_ready.brf');
        });

        // Validate embosser button
        document.getElementById('validateEmbosser')?.addEventListener('click', () => this.validateEmbosser());
    },

    toggleSidebar() {
        const sidebar = elements.sidebar;
        const mainContent = document.querySelector('.main-content');
        
        if (sidebar && mainContent) {
            // Toggle between expanded and collapsed states
            const isExpanded = sidebar.classList.contains('expanded');
            
            if (isExpanded) {
                sidebar.classList.remove('expanded');
                sidebar.classList.add('collapsed');
                mainContent.classList.remove('sidebar-expanded');
            } else {
                sidebar.classList.remove('collapsed');
                sidebar.classList.add('expanded');
                mainContent.classList.add('sidebar-expanded');
            }
        }
    },

    handleNavClick(e) {
        e.preventDefault();
        const href = e.currentTarget.getAttribute('href');
        if (href?.startsWith('#')) {
            const sectionId = href.substring(1);
            App.showSection(sectionId);
            
            // Update active state
            document.querySelectorAll('.sidebar-menu a').forEach(link => {
                link.classList.remove('active');
            });
            e.currentTarget.classList.add('active');

            // Close mobile menu
            elements.sidebar?.classList.remove('open');
        }
    },

    showSection(sectionId) {
        // Hide all sections
        document.querySelectorAll('.content-section').forEach(section => {
            section.classList.remove('active');
        });

        // Show target section
        const targetSection = document.getElementById(sectionId);
        if (targetSection) {
            targetSection.classList.add('active');
            AppState.currentSection = sectionId;
        }
    },

    validateUrl() {
        const url = elements.youtubeUrl?.value.trim();
        const isValid = url && Utils.isValidYouTubeUrl(url);
        
        if (elements.convertBtn) {
            elements.convertBtn.disabled = !isValid || AppState.isProcessing;
        }

        // Visual feedback
        const wrapper = elements.youtubeUrl?.closest('.input-wrapper');
        if (wrapper) {
            if (url && !isValid) {
                wrapper.style.borderColor = '#dc3545';
            } else {
                wrapper.style.borderColor = '';
            }
        }
    },

    async handleConversion() {
        const url = elements.youtubeUrl?.value.trim();
        
        if (!url || !Utils.isValidYouTubeUrl(url)) {
            Utils.showToast('Please enter a valid YouTube URL', 'error');
            return;
        }

        try {
            await this.processVideoWithAPI(url);
        } catch (error) {
            console.error('Conversion error:', error);
            
            // Hide processing modal
            this.hideProcessingModal();
            
            // Show error toast with close button
            Utils.showToast(`An error occurred during conversion: ${error.message}`, 'error', 10000);
            
            this.resetUI();
        } finally {
            // Ensure processing state is always reset
            AppState.isProcessing = false;
            this.updateUIForProcessing(false);
        }
    },

    async processVideoWithAPI(url) {
        AppState.isProcessing = true;
        this.updateUIForProcessing(true);
        this.showProcessingModal();

        try {
            // Step 1: Extract video info (mock for now)
            this.updateProcessingStep('Extracting video information...', 'fab fa-youtube', 'processing');
            
            // Use a direct delay function to avoid Utils object issues
            await new Promise(resolve => setTimeout(resolve, 1000));

            // For demo, we'll use sample text instead of actual YouTube extraction
            const sampleText = `Understanding the Moon's Changing Looks
Have you ever thought about how the Moon appears to change in the night sky? Sometimes it feels like a tiny sliver, other times it feels like a big, bright circle! These changes are not because the Moon is actually changing its shape, but because of how much of its surface is lit up by the Sun as the Moon travels around the Earth.`;

            // Step 2: Call Pratibimb API for conversion
            this.updateProcessingStep('Converting to Braille with Pratibimb...', 'fas fa-cogs', 'processing');
            
            const conversionResult = await Utils.callPratibimbAPI(sampleText, {
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

            // Step 3: Process results
            this.updateProcessingStep('Processing conversion results...', 'fas fa-check-circle', 'processing');
            await new Promise(resolve => setTimeout(resolve, 500));

            // Store results in AppState
            AppState.results = {
                original: conversionResult.original_text,
                braille: conversionResult.braille_unicode,
                embosser: conversionResult.embosser_brf
            };

            // Update stats from API response
            this.updateStats({
                duration: '15:30', // Mock duration
                charCount: conversionResult.stats.original_characters,
                wordCount: conversionResult.stats.original_words,
                brailleCount: conversionResult.stats.braille_characters
            });

            // Step 4: Complete
            this.updateProcessingStep('Conversion completed successfully!', 'fas fa-check-circle', 'completed');
            
            setTimeout(() => {
                this.hideProcessingModal();
                this.showResults();
            }, 1500);

        } catch (error) {
            console.error('Conversion error:', error);
            
            // Update processing step to show error
            this.updateProcessingStep(
                `Process failed: ${error.message}`,
                'fas fa-exclamation-triangle',
                'error'
            );
            
            // Hide modal after showing error for a few seconds
            setTimeout(() => {
                this.hideProcessingModal();
            }, 3000);
            
            // Show error toast with close button
            Utils.showToast(`Conversion failed: ${error.message}`, 'error', 8000);
            
            throw error;
        } finally {
            // Ensure processing state is always reset
            setTimeout(() => {
                AppState.isProcessing = false;
                this.updateUIForProcessing(false);
            }, 100);
        }
    },

    async prepareInputFile(url) {
        // Write the YouTube URL to input_text.txt
        const inputContent = `YouTube URL: ${url}\nPlease convert this YouTube video to Braille format.`;
        
        try {
            // In a real implementation, this would write to the file system
            // For now, we'll simulate this step
            await new Promise(resolve => setTimeout(resolve, 1000));
            console.log('Input file prepared with URL:', url);
        } catch (error) {
            throw new Error('Failed to prepare input file');
        }
    },

    async startPythonProcess() {
        try {
            // In a real implementation, this would execute the Python script
            // For now, we'll simulate the process start
            await new Promise(resolve => setTimeout(resolve, 500));
            console.log('Python process started');
            return { processId: 'mock_process_' + Date.now() };
        } catch (error) {
            throw new Error('Failed to start Python process');
        }
    },

    async monitorLogFile(pythonProcess) {
        const logSteps = [
            { message: 'Initializing Pratibimb processor...', icon: 'fas fa-play-circle', delay: 1000 },
            { message: 'Loading configuration and dependencies...', icon: 'fas fa-cogs', delay: 1500 },
            { message: 'Extracting YouTube video information...', icon: 'fab fa-youtube', delay: 2000 },
            { message: 'Downloading video transcript...', icon: 'fas fa-download', delay: 2500 },
            { message: 'Processing transcript text...', icon: 'fas fa-file-text', delay: 1500 },
            { message: 'Converting text to Braille unicode...', icon: 'fas fa-braille', delay: 3000 },
            { message: 'Formatting for embosser output...', icon: 'fas fa-print', delay: 2000 },
            { message: 'Generating output files...', icon: 'fas fa-file-export', delay: 1500 },
            { message: 'Validating Braille output...', icon: 'fas fa-check-double', delay: 1000 },
            { message: 'Writing conversion report...', icon: 'fas fa-chart-line', delay: 1000 }
        ];

        for (let i = 0; i < logSteps.length; i++) {
            const step = logSteps[i];
            this.updateProcessingStep(step.message, step.icon, 'processing');
            await new Promise(resolve => setTimeout(resolve, step.delay));
        }
    },

    async loadConversionResults() {
        // In a real implementation, this would read the output files
        // For now, we'll simulate loading results
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Mock results based on the input content
        const mockOriginal = `Understanding the Moon's Changing Looks
Have you ever thought about how the Moon appears to change in the night sky? Sometimes it feels like a tiny sliver, other times it feels like a big, bright circle! These changes are not because the Moon is actually changing its shape, but because of how much of its surface is lit up by the Sun as the Moon travels around the Earth.`;

        const mockBraille = BrailleConverter.textToBraille(mockOriginal);
        const mockEmbosser = BrailleConverter.formatForEmbosser(mockBraille);

        AppState.results = {
            original: mockOriginal,
            braille: mockBraille,
            embosser: mockEmbosser
        };

        // Update stats
        this.updateStats({
            duration: '15:30',
            charCount: mockOriginal.length,
            wordCount: Utils.countWords(mockOriginal),
            brailleCount: mockBraille.length
        });
    },

    async processVideo(url) {
        const videoId = Utils.extractVideoId(url);
        if (!videoId) return;

        AppState.isProcessing = true;
        this.updateUIForProcessing(true);

        try {
            // Step 1: Get video info
            this.updateProgress(20, 'Fetching video information...');
            const videoInfo = await YouTubeAPI.getVideoInfo(videoId);
            AppState.currentVideo = videoInfo;

            // Step 2: Get transcript
            this.updateProgress(50, 'Extracting transcript...');
            const transcript = await YouTubeAPI.getTranscript(videoId, elements.languageSelect?.value);

            // Step 3: Convert to Braille
            this.updateProgress(80, 'Converting to Braille...');
            const brailleText = BrailleConverter.textToBraille(transcript.text);
            
            // Step 4: Format for embosser if needed
            let embosserText = '';
            if (elements.formatForEmbosser?.checked) {
                embosserText = BrailleConverter.formatForEmbosser(brailleText);
            }

            this.updateProgress(100, 'Conversion complete!');

            // Store results
            AppState.results = {
                original: transcript.text,
                braille: brailleText,
                embosser: embosserText || brailleText
            };

            // Update UI with results
            await this.displayResults();
            this.updateStats(transcript.text, brailleText, videoInfo);

        } finally {
            AppState.isProcessing = false;
            setTimeout(() => this.updateUIForProcessing(false), 500);
        }
    },

    updateProgress(percentage, text = '') {
        if (elements.progressFill) {
            elements.progressFill.style.width = `${percentage}%`;
        }
        if (elements.progressText && text) {
            elements.progressText.textContent = text;
        }
    },

    updateUIForProcessing(isProcessing) {
        // Show/hide progress
        if (elements.progressContainer) {
            elements.progressContainer.style.display = isProcessing ? 'block' : 'none';
        }

        // Enable/disable convert button
        if (elements.convertBtn) {
            elements.convertBtn.disabled = isProcessing;
            elements.convertBtn.innerHTML = isProcessing 
                ? '<i class="fas fa-spinner fa-spin"></i> Processing...'
                : '<i class="fas fa-magic"></i> Convert to Braille';
        }

        // Show/hide results
        if (!isProcessing) {
            this.updateProgress(0, 'Ready for conversion');
        }
    },

    async displayResults() {
        // Populate textareas
        if (elements.originalText) {
            elements.originalText.value = AppState.results.original;
        }
        if (elements.brailleText) {
            elements.brailleText.value = AppState.results.braille;
        }
        if (elements.embosserText) {
            elements.embosserText.value = AppState.results.embosser;
        }

        // Show results area
        if (elements.resultsArea) {
            elements.resultsArea.style.display = 'block';
        }

        // Show success toast
        Utils.showToast('Video converted to Braille successfully!');
    },

    updateStats(originalText, brailleText, videoInfo) {
        const charCount = originalText.length;
        const wordCount = Utils.countWords(originalText);
        const brailleCount = brailleText.length;
        const duration = Utils.formatDuration(videoInfo.duration);

        // Update stat elements
        if (elements.videoDuration) elements.videoDuration.textContent = duration;
        if (elements.charCount) elements.charCount.textContent = charCount.toLocaleString();
        if (elements.wordCount) elements.wordCount.textContent = wordCount.toLocaleString();
        if (elements.brailleCount) elements.brailleCount.textContent = brailleCount.toLocaleString();

        // Show stats
        if (elements.quickStats) {
            elements.quickStats.style.display = 'block';
        }
    },

    handleTabSwitch(e) {
        const tabBtn = e.currentTarget;
        const tabId = tabBtn.getAttribute('data-tab');

        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        tabBtn.classList.add('active');

        // Update tab panels
        document.querySelectorAll('.tab-panel').forEach(panel => {
            panel.classList.remove('active');
        });
        const targetPanel = document.getElementById(tabId);
        if (targetPanel) {
            targetPanel.classList.add('active');
        }
    },

    validateEmbosser() {
        const embosserText = AppState.results.embosser;
        if (!embosserText) {
            Utils.showToast('No embosser text to validate', 'error');
            return;
        }

        // Mock validation (replace with actual validation logic)
        const issues = [];
        
        // Check line length
        const lines = embosserText.split('\n');
        lines.forEach((line, index) => {
            if (line.length > 40) {
                issues.push(`Line ${index + 1}: Too long (${line.length} characters)`);
            }
        });

        // Check for invalid characters
        const validPattern = /^[A-Z0-9\s.,'"?!:;<>\-#\f]*$/;
        if (!validPattern.test(embosserText)) {
            issues.push('Contains invalid characters for embosser');
        }

        // Show results
        if (issues.length === 0) {
            Utils.showToast('Embosser format is valid!');
        } else {
            Utils.showToast(`Validation issues found: ${issues.length}`, 'error');
            console.log('Validation issues:', issues);
        }
    },

    togglePastConversions() {
        const conversionsList = elements.conversionsList;
        const toggleIcon = elements.toggleIcon;
        
        if (conversionsList?.classList.contains('collapsed')) {
            conversionsList.classList.remove('collapsed');
            toggleIcon?.classList.add('rotated');
        } else {
            conversionsList?.classList.add('collapsed');
            toggleIcon?.classList.remove('rotated');
        }
    },

    async loadPastConversions() {
        const conversions = await Utils.loadPastConversions();
        this.renderPastConversions(conversions);
    },

    renderPastConversions(conversions) {
        const conversionsList = elements.conversionsList;
        if (!conversionsList) return;

        conversionsList.innerHTML = '';

        conversions.forEach(conversion => {
            const card = document.createElement('div');
            card.className = 'conversion-card';
            card.setAttribute('data-id', conversion.id);

            const typeIcon = this.getTypeIcon(conversion.type, conversion.thumbnail);
            const relativeTime = Utils.formatRelativeTime(conversion.date);
            
            card.innerHTML = `
                <div class="conversion-card-header">
                    <span class="conversion-type-icon">${typeIcon}</span>
                    <div class="conversion-title">${conversion.title}</div>
                </div>
                <div class="conversion-meta">
                    <div class="conversion-date">${relativeTime}</div>
                    <div class="conversion-stats">
                        ${conversion.duration ? `
                            <div class="conversion-duration">
                                <i class="fas fa-clock"></i> ${conversion.duration}
                            </div>
                        ` : ''}
                        <span class="stat-badge">${conversion.word_count.toLocaleString()} words</span>
                    </div>
                </div>
            `;

            card.addEventListener('click', () => this.loadConversion(conversion));
            conversionsList.appendChild(card);
        });
    },

    getTypeIcon(type, thumbnail) {
        // Use professional Font Awesome icons instead of emojis
        switch (type) {
            case 'youtube': return '<i class="fab fa-youtube"></i>';
            case 'text': return '<i class="fas fa-file-alt"></i>';
            case 'pdf': return '<i class="fas fa-file-pdf"></i>';
            case 'document': return '<i class="fas fa-file-text"></i>';
            case 'video': return '<i class="fas fa-video"></i>';
            case 'audio': return '<i class="fas fa-volume-up"></i>';
            default: return '<i class="fas fa-file"></i>';
        }
    },

    loadConversion(conversion) {
        // Mock loading a past conversion
        Utils.showToast(`Loading conversion: ${conversion.title}`);
        
        // You would implement actual loading logic here
        console.log('Loading conversion:', conversion);
    },

    resetUI() {
        AppState.isProcessing = false;
        this.updateUIForProcessing(false);
        
        if (elements.resultsArea) {
            elements.resultsArea.style.display = 'none';
        }
        if (elements.quickStats) {
            elements.quickStats.style.display = 'none';
        }
    },

    // Processing Modal Functions
    showProcessingModal() {
        // Create processing modal if it doesn't exist
        let modal = document.getElementById('processingModal');
        if (!modal) {
            modal = this.createProcessingModal();
            document.body.appendChild(modal);
        }
        
        // Reset modal content
        const stepsList = modal.querySelector('.processing-steps');
        stepsList.innerHTML = '';
        
        // Show modal
        modal.style.display = 'flex';
        setTimeout(() => modal.classList.add('show'), 10);
        
        // Auto-close mechanism - force close if modal is stuck for too long
        modal.autoCloseTimeout = setTimeout(() => {
            console.warn('Processing modal auto-closed due to timeout');
            this.hideProcessingModal();
            Utils.showToast('Processing took too long and was automatically closed. Please try again.', 'warning', 8000);
        }, 120000); // 2 minutes timeout
    },

    hideProcessingModal() {
        const modal = document.getElementById('processingModal');
        if (modal) {
            modal.classList.remove('show');
            
            // Clear auto-close timeout
            if (modal.autoCloseTimeout) {
                clearTimeout(modal.autoCloseTimeout);
                delete modal.autoCloseTimeout;
            }
            
            // Clear any existing timeout
            if (modal.hideTimeout) {
                clearTimeout(modal.hideTimeout);
            }
            
            // Hide modal with timeout
            modal.hideTimeout = setTimeout(() => {
                modal.style.display = 'none';
                delete modal.hideTimeout;
            }, 300);
        }
        
        // Also reset processing state to ensure UI is properly reset
        AppState.isProcessing = false;
        this.updateUIForProcessing(false);
    },

    // Force close all modals (useful for stuck modals)
    forceCloseAllModals() {
        const modal = document.getElementById('processingModal');
        if (modal) {
            modal.classList.remove('show');
            modal.style.display = 'none';
            
            // Clear all timeouts
            if (modal.hideTimeout) {
                clearTimeout(modal.hideTimeout);
                delete modal.hideTimeout;
            }
            if (modal.autoCloseTimeout) {
                clearTimeout(modal.autoCloseTimeout);
                delete modal.autoCloseTimeout;
            }
        }
        
        // Also hide any toast notifications using the enhanced cleanup
        Utils.forceHideAllToasts();
        
        // Reset processing state
        AppState.isProcessing = false;
        this.updateUIForProcessing(false);
        
        console.log('All modals force closed');
    },

    createProcessingModal() {
        const modal = document.createElement('div');
        modal.id = 'processingModal';
        modal.className = 'processing-modal';
        modal.innerHTML = `
            <div class="processing-modal-content">
                <div class="processing-header">
                    <div class="processing-title">
                        <i class="fas fa-cogs processing-main-icon"></i>
                        <h3>Converting to Braille</h3>
                    </div>
                    <button class="modal-close-btn" id="processingModalCloseBtn" title="Close">
                        <i class="fas fa-times"></i>
                    </button>
                    <div class="processing-subtitle">
                        Live processing status
                    </div>
                </div>
                <div class="processing-body">
                    <div class="processing-steps" id="processingSteps">
                        <!-- Steps will be added dynamically -->
                    </div>
                </div>
            </div>
        `;
        
        // Add close button functionality
        const closeBtn = modal.querySelector('#processingModalCloseBtn');
        closeBtn.addEventListener('click', () => {
            this.hideProcessingModal();
        });
        
        // Close on overlay click
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                this.hideProcessingModal();
            }
        });
        
        // Close on Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && modal.style.display === 'flex') {
                this.hideProcessingModal();
            }
        });
        
        return modal;
    },

    updateProcessingStep(message, icon, status = 'processing') {
        const modal = document.getElementById('processingModal');
        if (!modal) return;

        const stepsList = modal.querySelector('.processing-steps');
        const timestamp = new Date().toLocaleTimeString();
        
        // Create new step element
        const stepElement = document.createElement('div');
        stepElement.className = `processing-step ${status}`;
        stepElement.innerHTML = `
            <div class="step-icon-container">
                <i class="${icon} step-icon"></i>
                <div class="step-status-indicator ${status}">
                    ${status === 'processing' ? '<i class="fas fa-spinner fa-spin"></i>' : 
                      status === 'completed' ? '<i class="fas fa-check"></i>' : 
                      status === 'error' ? '<i class="fas fa-times"></i>' : ''}
                </div>
            </div>
            <div class="step-content">
                <div class="step-message">${message}</div>
                <div class="step-timestamp">${timestamp}</div>
            </div>
        `;

        // Add step to list
        stepsList.appendChild(stepElement);
        
        // Scroll to bottom
        stepsList.scrollTop = stepsList.scrollHeight;
        
        // Add animation
        setTimeout(() => stepElement.classList.add('visible'), 100);
        
        // Update previous step status if this is a new processing step
        if (status === 'processing') {
            const previousSteps = stepsList.querySelectorAll('.processing-step.processing');
            if (previousSteps.length > 1) {
                const previousStep = previousSteps[previousSteps.length - 2];
                this.markStepAsCompleted(previousStep);
            }
        }
    },

    markStepAsCompleted(stepElement) {
        stepElement.classList.remove('processing');
        stepElement.classList.add('completed');
        const indicator = stepElement.querySelector('.step-status-indicator');
        indicator.className = 'step-status-indicator completed';
        indicator.innerHTML = '<i class="fas fa-check"></i>';
    },

    updateStats(stats) {
        if (elements.videoDuration) elements.videoDuration.textContent = stats.duration;
        if (elements.charCount) elements.charCount.textContent = stats.charCount.toLocaleString();
        if (elements.wordCount) elements.wordCount.textContent = stats.wordCount.toLocaleString();
        if (elements.brailleCount) elements.brailleCount.textContent = stats.brailleCount.toLocaleString();
    },

    showResults() {
        // Populate result textareas
        if (elements.originalText) elements.originalText.value = AppState.results.original;
        if (elements.brailleText) elements.brailleText.value = AppState.results.braille;
        if (elements.embosserText) elements.embosserText.value = AppState.results.embosser;

        // Show results area and stats
        if (elements.resultsArea) elements.resultsArea.style.display = 'block';
        if (elements.quickStats) elements.quickStats.style.display = 'block';

        // Reset UI
        this.updateUIForProcessing(false);
        AppState.isProcessing = false;

        // Show success message
        Utils.showToast('Conversion completed successfully!');
    },

    // Emergency toast cleanup functions
    forceHideAllToasts() {
        const toasts = document.querySelectorAll('.toast');
        toasts.forEach(toast => {
            toast.classList.remove('show');
            toast.style.transform = 'translateX(400px)';
            toast.style.opacity = '0';
            toast.style.visibility = 'hidden';
            
            // Clear any timeouts
            if (toast.hideTimeout) {
                clearTimeout(toast.hideTimeout);
                delete toast.hideTimeout;
            }
            
            // Reset after cleanup
            setTimeout(() => {
                toast.style.transform = '';
                toast.style.opacity = '';
                toast.style.visibility = '';
                toast.className = 'toast';
            }, 500);
        });
    }
};

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Debug: Show Utils object methods to verify delay is not present
    console.log('🔍 Utils object methods:', Object.getOwnPropertyNames(Utils));
    console.log('❌ Utils.delay exists?', typeof Utils.delay !== 'undefined');
    
    App.init();
    console.log('Pratibimb app initialized successfully!');
});

// Global keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Escape key - Close all modals and reset UI
    if (e.key === 'Escape') {
        App.forceCloseAllModals();
    }
    
    // Ctrl/Cmd + R - Emergency reset (prevent default refresh and reset UI)
    if ((e.ctrlKey || e.metaKey) && e.key === 'r' && !e.shiftKey) {
        e.preventDefault();
        App.emergencyReset();
    }
    
    // Ctrl/Cmd + H - Force hide all toasts (for stuck notifications)
    if ((e.ctrlKey || e.metaKey) && e.key === 'h') {
        e.preventDefault();
        Utils.forceHideAllToasts();
    }
    
    // Ctrl/Cmd + Enter - Quick convert if in YouTube input
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        if (document.activeElement === elements.youtubeUrl && !AppState.isProcessing) {
            App.handleConversion();
        }
    }
});

// Emergency reset function for stuck states
App.emergencyReset = function() {
    console.warn('Emergency reset triggered!');
    
    // Force close all modals
    this.forceCloseAllModals();
    
    // Reset all state
    AppState.isProcessing = false;
    AppState.currentVideo = null;
    AppState.results = { original: '', braille: '', embosser: '' };
    
    // Reset UI elements
    this.updateUIForProcessing(false);
    
    // Clear all text areas
    if (elements.youtubeUrl) elements.youtubeUrl.value = '';
    if (elements.originalText) elements.originalText.value = '';
    if (elements.brailleText) elements.brailleText.value = '';
    if (elements.embosserText) elements.embosserText.value = '';
    
    // Hide results areas
    if (elements.resultsArea) elements.resultsArea.style.display = 'none';
    if (elements.quickStats) elements.quickStats.style.display = 'none';
    
    // Show reset confirmation
    Utils.showToast('UI reset successfully! Ready for new conversion.', 'info', 3000);
};

// Handle window resize for responsive design
window.addEventListener('resize', () => {
    if (window.innerWidth > 768) {
        elements.sidebar?.classList.remove('open');
    }
});

// Export for testing (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { App, Utils, BrailleConverter, YouTubeAPI };
}

// Periodic cleanup for stuck toasts (runs every 30 seconds)
setInterval(() => {
    const toasts = document.querySelectorAll('.toast.show');
    toasts.forEach(toast => {
        // If a toast has been showing for more than 30 seconds, force close it
        if (!toast.lastShownTime) {
            toast.lastShownTime = Date.now();
        } else if (Date.now() - toast.lastShownTime > 30000) {
            Utils.hideToast(toast);
        }
    });
}, 30000);

// Update showToast to track when toasts are shown
Utils.showToast = (function(originalShowToast) {
    return function(message, type = 'success', duration = 4000) {
        const result = originalShowToast.call(this, message, type, duration);
        const toast = elements.toast;
        if (toast) {
            toast.lastShownTime = Date.now();
        }
        return result;
    };
})(Utils.showToast);

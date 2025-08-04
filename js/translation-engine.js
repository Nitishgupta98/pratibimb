/**
 * Pratibimb Translation Engine
 * Comprehensive multi-language support system
 */

class TranslationEngine {
    constructor() {
        this.currentLanguage = 'english';
        this.translations = {};
        this.loadedLanguages = new Set();
        this.fallbackLanguage = 'english';
        this.translationCache = new Map();
        
        // Language configuration
        this.languageConfig = {
            'kannada': {
                code: 'kn',
                name: 'ಕನ್ನಡ',
                nativeName: 'ಕನ್ನಡ',
                flag: '🇮🇳',
                direction: 'ltr'
            },
            'telugu': {
                code: 'te',
                name: 'Telugu',
                nativeName: 'తెలుగు',
                flag: '🇮🇳',
                direction: 'ltr'
            },
            'hindi': {
                code: 'hi',
                name: 'Hindi',
                nativeName: 'हिंदी',
                flag: '🇮🇳',
                direction: 'ltr'
            },
            'english': {
                code: 'en',
                name: 'English',
                nativeName: 'English',
                flag: '🇺🇸',
                direction: 'ltr'
            },
            'french': {
                code: 'fr',
                name: 'French',
                nativeName: 'Français',
                flag: '🇫🇷',
                direction: 'ltr'
            },
            'german': {
                code: 'de',
                name: 'German',
                nativeName: 'Deutsch',
                flag: '🇩🇪',
                direction: 'ltr'
            }
        };

        this.init();
    }

    async init() {
        // Load saved language preference
        const savedLanguage = localStorage.getItem('pratibimb_language');
        if (savedLanguage && this.languageConfig[savedLanguage]) {
            this.currentLanguage = savedLanguage;
        }

        // Load default language
        await this.loadLanguage(this.currentLanguage);
        
        // Apply initial translations
        this.applyTranslations();
        
        // Set up event listeners
        this.setupEventListeners();
        
        // Update language selector UI
        this.updateLanguageSelector();
    }

    setupEventListeners() {
        // Language dropdown toggle
        const languageBtn = document.getElementById('languageBtn');
        const languageOptions = document.getElementById('languageOptions');
        
        if (languageBtn && languageOptions) {
            languageBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                const isOpen = languageOptions.style.display === 'block';
                languageOptions.style.display = isOpen ? 'none' : 'block';
            });

            // Close dropdown when clicking outside
            document.addEventListener('click', () => {
                languageOptions.style.display = 'none';
            });

            // Language option selection
            languageOptions.addEventListener('click', (e) => {
                e.stopPropagation();
                const languageOption = e.target.closest('[data-language]');
                if (languageOption) {
                    const selectedLanguage = languageOption.dataset.language;
                    this.changeLanguage(selectedLanguage);
                    languageOptions.style.display = 'none';
                }
            });
        }

        // Handle dynamic content changes
        this.observeContentChanges();
    }

    async loadLanguage(languageCode) {
        if (this.loadedLanguages.has(languageCode)) {
            return this.translations[languageCode];
        }

        try {
            const response = await fetch(`./translations/${languageCode}.json`);
            if (!response.ok) {
                throw new Error(`Failed to load ${languageCode} translations`);
            }
            
            const translations = await response.json();
            this.translations[languageCode] = translations;
            this.loadedLanguages.add(languageCode);
            
            console.log(`✅ Loaded ${languageCode} translations`);
            return translations;
        } catch (error) {
            console.error(`❌ Error loading ${languageCode} translations:`, error);
            
            // Fallback to English if available
            if (languageCode !== this.fallbackLanguage) {
                return await this.loadLanguage(this.fallbackLanguage);
            }
            
            return {};
        }
    }

    async changeLanguage(languageCode) {
        if (!this.languageConfig[languageCode]) {
            console.error(`❌ Unsupported language: ${languageCode}`);
            return;
        }

        // Show loading state
        this.showTranslationLoading();

        try {
            // Load language if not already loaded
            await this.loadLanguage(languageCode);
            
            // Update current language
            const previousLanguage = this.currentLanguage;
            this.currentLanguage = languageCode;
            
            // Save preference
            localStorage.setItem('pratibimb_language', languageCode);
            
            // Apply translations
            this.applyTranslations();
            
            // Update UI elements
            this.updateLanguageSelector();
            this.updateDocumentDirection();
            
            // Trigger custom event for other components
            this.dispatchLanguageChangeEvent(languageCode, previousLanguage);
            
            // Show success notification
            this.showNotification('translation_applied', 'success');
            
            console.log(`🌍 Language changed to: ${this.languageConfig[languageCode].nativeName}`);
            
        } catch (error) {
            console.error('❌ Error changing language:', error);
            this.showNotification('error_occurred', 'error');
        } finally {
            this.hideTranslationLoading();
        }
    }

    applyTranslations() {
        // Translate elements with data-translate attributes
        const translatableElements = document.querySelectorAll('[data-translate]');
        
        translatableElements.forEach(element => {
            const translationKey = element.dataset.translate;
            const translatedText = this.getTranslation(translationKey);
            
            if (translatedText) {
                // Handle different content types
                if (element.tagName === 'INPUT' && (element.type === 'text' || element.type === 'search')) {
                    element.placeholder = translatedText;
                } else if (element.tagName === 'INPUT' && element.type === 'submit') {
                    element.value = translatedText;
                } else {
                    element.textContent = translatedText;
                }
            }
        });

        // Translate elements with data-translate-html for HTML content
        const htmlTranslatableElements = document.querySelectorAll('[data-translate-html]');
        
        htmlTranslatableElements.forEach(element => {
            const translationKey = element.dataset.translateHtml;
            const translatedText = this.getTranslation(translationKey);
            
            if (translatedText) {
                element.innerHTML = translatedText;
            }
        });

        // Update page title if needed
        const titleKey = document.querySelector('meta[name="page-title-key"]');
        if (titleKey) {
            const translatedTitle = this.getTranslation(titleKey.content);
            if (translatedTitle) {
                document.title = `${translatedTitle} - ${this.getTranslation('header.site_title')}`;
            }
        }
    }

    getTranslation(key, params = {}) {
        // Check cache first
        const cacheKey = `${this.currentLanguage}:${key}:${JSON.stringify(params)}`;
        if (this.translationCache.has(cacheKey)) {
            return this.translationCache.get(cacheKey);
        }

        const currentTranslations = this.translations[this.currentLanguage] || {};
        const fallbackTranslations = this.translations[this.fallbackLanguage] || {};
        
        // Navigate through nested object structure
        const getNestedValue = (obj, path) => {
            return path.split('.').reduce((curr, key) => curr && curr[key], obj);
        };

        let translation = getNestedValue(currentTranslations, key) || 
                         getNestedValue(fallbackTranslations, key) || 
                         key;

        // Handle parameter substitution
        if (typeof translation === 'string' && Object.keys(params).length > 0) {
            Object.keys(params).forEach(param => {
                translation = translation.replace(new RegExp(`\\{\\{${param}\\}\\}`, 'g'), params[param]);
            });
        }

        // Cache the result
        this.translationCache.set(cacheKey, translation);
        
        return translation;
    }

    updateLanguageSelector() {
        const languageBtn = document.getElementById('languageBtn');
        if (languageBtn) {
            const currentLangConfig = this.languageConfig[this.currentLanguage];
            const flagSpan = languageBtn.querySelector('.language-flag');
            const nameSpan = languageBtn.querySelector('.language-name');
            
            if (flagSpan) flagSpan.textContent = currentLangConfig.flag;
            if (nameSpan) nameSpan.textContent = currentLangConfig.nativeName;
        }

        // Update active state in dropdown
        const languageOptions = document.querySelectorAll('[data-language]');
        languageOptions.forEach(option => {
            const isActive = option.dataset.language === this.currentLanguage;
            option.classList.toggle('active', isActive);
        });
    }

    updateDocumentDirection() {
        const direction = this.languageConfig[this.currentLanguage].direction;
        document.documentElement.setAttribute('dir', direction);
        document.documentElement.setAttribute('lang', this.languageConfig[this.currentLanguage].code);
    }

    showTranslationLoading() {
        const loadingElement = document.getElementById('translationLoading');
        if (loadingElement) {
            loadingElement.style.display = 'flex';
        }
    }

    hideTranslationLoading() {
        const loadingElement = document.getElementById('translationLoading');
        if (loadingElement) {
            loadingElement.style.display = 'none';
        }
    }

    showNotification(messageKey, type = 'info') {
        const message = this.getTranslation(`notifications.${messageKey}`);
        
        // Create notification element if it doesn't exist
        let notification = document.getElementById('translation-notification');
        if (!notification) {
            notification = document.createElement('div');
            notification.id = 'translation-notification';
            notification.className = 'translation-notification';
            document.body.appendChild(notification);
        }

        notification.className = `translation-notification ${type}`;
        notification.textContent = message;
        notification.style.display = 'block';

        // Auto-hide after 3 seconds
        setTimeout(() => {
            notification.style.display = 'none';
        }, 3000);
    }

    dispatchLanguageChangeEvent(newLanguage, oldLanguage) {
        const event = new CustomEvent('languageChanged', {
            detail: {
                newLanguage,
                oldLanguage,
                config: this.languageConfig[newLanguage]
            }
        });
        
        document.dispatchEvent(event);
    }

    observeContentChanges() {
        // Observe DOM changes to auto-translate new content
        const observer = new MutationObserver((mutations) => {
            let shouldRetranslate = false;
            
            mutations.forEach((mutation) => {
                if (mutation.type === 'childList') {
                    mutation.addedNodes.forEach((node) => {
                        if (node.nodeType === Node.ELEMENT_NODE) {
                            const hasTranslatableContent = node.querySelector('[data-translate], [data-translate-html]') ||
                                                         node.hasAttribute('data-translate') ||
                                                         node.hasAttribute('data-translate-html');
                            
                            if (hasTranslatableContent) {
                                shouldRetranslate = true;
                            }
                        }
                    });
                }
            });
            
            if (shouldRetranslate) {
                // Debounce re-translation
                clearTimeout(this.retranslateTimeout);
                this.retranslateTimeout = setTimeout(() => {
                    this.applyTranslations();
                }, 100);
            }
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    // Utility methods for developers
    getCurrentLanguage() {
        return this.currentLanguage;
    }

    getAvailableLanguages() {
        return Object.keys(this.languageConfig);
    }

    getLanguageConfig(languageCode) {
        return this.languageConfig[languageCode];
    }

    // Method to add translation attributes to elements
    addTranslationAttribute(element, key, isHtml = false) {
        const attribute = isHtml ? 'data-translate-html' : 'data-translate';
        element.setAttribute(attribute, key);
        this.applyTranslations();
    }

    // Method to translate text programmatically
    translate(key, params = {}) {
        return this.getTranslation(key, params);
    }

    // Method to clear translation cache
    clearCache() {
        this.translationCache.clear();
        console.log('🗑️ Translation cache cleared');
    }
}

// Initialize translation engine when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.translationEngine = new TranslationEngine();
    
    // Make it globally accessible for debugging and integration
    window.translate = (key, params) => window.translationEngine.translate(key, params);
    window.changeLanguage = (lang) => window.translationEngine.changeLanguage(lang);
    
    console.log('🌍 Pratibimb Translation Engine initialized');
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TranslationEngine;
}

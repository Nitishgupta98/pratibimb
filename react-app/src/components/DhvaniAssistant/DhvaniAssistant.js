import React, { useState, useRef, useEffect } from 'react';
import './DhvaniAssistant.css';

const DhvaniAssistant = () => {
  const [isListening, setIsListening] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [inputText, setInputText] = useState('');
  const [outputText, setOutputText] = useState('');
  const [brailleOutput, setBrailleOutput] = useState('');
  const [conversation, setConversation] = useState([]);
  const [volume, setVolume] = useState(0.8);
  const [speechRate, setSpeechRate] = useState(1);
  const recognitionRef = useRef(null);
  const synthRef = useRef(null);

  useEffect(() => {
    // Initialize speech recognition
    if ('webkitSpeechRecognition' in window) {
      recognitionRef.current = new window.webkitSpeechRecognition();
      recognitionRef.current.continuous = true;
      recognitionRef.current.interimResults = true;
      recognitionRef.current.lang = 'en-US';

      recognitionRef.current.onresult = (event) => {
        let finalTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          if (event.results[i].isFinal) {
            finalTranscript += event.results[i][0].transcript;
          }
        }
        if (finalTranscript) {
          setInputText(finalTranscript);
        }
      };

      recognitionRef.current.onend = () => {
        setIsListening(false);
      };
    }

    // Initialize speech synthesis
    synthRef.current = window.speechSynthesis;

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
      if (synthRef.current) {
        synthRef.current.cancel();
      }
    };
  }, []);

  const startListening = () => {
    if (recognitionRef.current && !isListening) {
      setIsListening(true);
      recognitionRef.current.start();
    }
  };

  const stopListening = () => {
    if (recognitionRef.current && isListening) {
      setIsListening(false);
      recognitionRef.current.stop();
    }
  };

  const speakText = (text) => {
    if (synthRef.current && text) {
      synthRef.current.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.volume = volume;
      utterance.rate = speechRate;
      utterance.onstart = () => setIsPlaying(true);
      utterance.onend = () => setIsPlaying(false);
      synthRef.current.speak(utterance);
    }
  };

  const stopSpeaking = () => {
    if (synthRef.current) {
      synthRef.current.cancel();
      setIsPlaying(false);
    }
  };

  const convertToBraille = (text) => {
    // Simple braille conversion (placeholder)
    const brailleMap = {
      'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑', 'f': '⠋', 'g': '⠛', 'h': '⠓', 'i': '⠊', 'j': '⠚',
      'k': '⠅', 'l': '⠇', 'm': '⠍', 'n': '⠝', 'o': '⠕', 'p': '⠏', 'q': '⠟', 'r': '⠗', 's': '⠎', 't': '⠞',
      'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭', 'y': '⠽', 'z': '⠵', ' ': '⠀'
    };
    
    return text.toLowerCase().split('').map(char => brailleMap[char] || char).join('');
  };

  const processInput = () => {
    if (!inputText.trim()) return;

    const newMessage = {
      id: Date.now(),
      type: 'user',
      text: inputText,
      timestamp: new Date().toLocaleTimeString()
    };

    // Simulate AI response
    const response = `I understand you said: "${inputText}". How can I help you with accessibility features?`;
    const aiMessage = {
      id: Date.now() + 1,
      type: 'ai',
      text: response,
      timestamp: new Date().toLocaleTimeString()
    };

    setConversation(prev => [...prev, newMessage, aiMessage]);
    setOutputText(response);
    setBrailleOutput(convertToBraille(response));
    setInputText('');
    
    // Auto-speak the response
    speakText(response);
  };

  const clearConversation = () => {
    setConversation([]);
    setOutputText('');
    setBrailleOutput('');
    setInputText('');
  };

  return (
    <div className="dhvani-assistant">
      <div className="assistant-header">
        <h2><i className="fas fa-microphone"></i> Dhvani Voice Assistant</h2>
        <p>Your intelligent voice-powered accessibility companion</p>
      </div>

      <div className="assistant-controls">
        <div className="voice-controls">
          <button 
            className={`voice-btn ${isListening ? 'listening' : ''}`}
            onClick={isListening ? stopListening : startListening}
          >
            <i className={`fas ${isListening ? 'fa-stop' : 'fa-microphone'}`}></i>
            {isListening ? 'Stop Listening' : 'Start Listening'}
          </button>
          
          <button 
            className={`speak-btn ${isPlaying ? 'playing' : ''}`}
            onClick={isPlaying ? stopSpeaking : () => speakText(outputText)}
            disabled={!outputText}
          >
            <i className={`fas ${isPlaying ? 'fa-stop' : 'fa-volume-up'}`}></i>
            {isPlaying ? 'Stop Speaking' : 'Speak Response'}
          </button>
        </div>

        <div className="audio-settings">
          <div className="setting-group">
            <label>Volume: {Math.round(volume * 100)}%</label>
            <input 
              type="range" 
              min="0" 
              max="1" 
              step="0.1" 
              value={volume}
              onChange={(e) => setVolume(parseFloat(e.target.value))}
              className="slider"
            />
          </div>
          <div className="setting-group">
            <label>Speed: {speechRate}x</label>
            <input 
              type="range" 
              min="0.5" 
              max="2" 
              step="0.1" 
              value={speechRate}
              onChange={(e) => setSpeechRate(parseFloat(e.target.value))}
              className="slider"
            />
          </div>
        </div>
      </div>

      <div className="input-section">
        <div className="text-input-group">
          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Type your message or use voice input..."
            className="text-input"
            rows="3"
          />
          <button 
            className="process-btn"
            onClick={processInput}
            disabled={!inputText.trim()}
          >
            <i className="fas fa-paper-plane"></i>
            Process
          </button>
        </div>
      </div>

      <div className="output-section">
        <div className="conversation-area">
          <div className="conversation-header">
            <h3><i className="fas fa-comments"></i> Conversation</h3>
            <button className="clear-btn" onClick={clearConversation}>
              <i className="fas fa-trash"></i> Clear
            </button>
          </div>
          
          <div className="conversation-list">
            {conversation.length === 0 ? (
              <div className="empty-conversation">
                <i className="fas fa-robot"></i>
                <p>Start a conversation by speaking or typing!</p>
              </div>
            ) : (
              conversation.map((message) => (
                <div key={message.id} className={`message ${message.type}`}>
                  <div className="message-content">
                    <div className="message-text">{message.text}</div>
                    <div className="message-time">{message.timestamp}</div>
                  </div>
                  <div className="message-avatar">
                    <i className={`fas ${message.type === 'user' ? 'fa-user' : 'fa-robot'}`}></i>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {outputText && (
          <div className="response-area">
            <div className="response-tabs">
              <div className="tab-content">
                <div className="output-box">
                  <h4><i className="fas fa-comment-alt"></i> Text Response</h4>
                  <div className="output-text">{outputText}</div>
                </div>
                
                <div className="braille-box">
                  <h4><i className="fas fa-braille"></i> Braille Output</h4>
                  <div className="braille-text">{brailleOutput}</div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="features-info">
        <h3><i className="fas fa-star"></i> Features</h3>
        <div className="features-grid">
          <div className="feature-item">
            <i className="fas fa-microphone-alt"></i>
            <span>Voice Recognition</span>
          </div>
          <div className="feature-item">
            <i className="fas fa-volume-up"></i>
            <span>Text-to-Speech</span>
          </div>
          <div className="feature-item">
            <i className="fas fa-braille"></i>
            <span>Braille Conversion</span>
          </div>
          <div className="feature-item">
            <i className="fas fa-language"></i>
            <span>Multi-language Support</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DhvaniAssistant;

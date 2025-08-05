import React, { useState, useEffect } from 'react';
import './LearnBraille.css';

const LearnBraille = () => {
  // State management based on requirements
  const [activeSection, setActiveSection] = useState('audio-learning');
  const [selectedTopic, setSelectedTopic] = useState('Moon Phases');
  const [sessionActive, setSessionActive] = useState(false);
  const [brailleInput, setBrailleInput] = useState('');
  const [isPlaying, setIsPlaying] = useState(false);
  const [progress, setProgress] = useState(0);
  const [sessionHistory, setSessionHistory] = useState([]);
  const [topicInput, setTopicInput] = useState('Moon Phases');

  // Learning tools configuration
  const learningTools = [
    {
      id: 'youtube-braille',
      title: 'YouTube to Braille',
      icon: 'fab fa-youtube',
      description: 'Convert video transcripts to Braille',
      active: false
    },
    {
      id: 'braille-art',
      title: 'Braille Art Editor',
      icon: 'fas fa-palette',
      description: 'Create visual patterns in Braille',
      active: false
    },
    {
      id: 'learn-braille',
      title: 'Learn Braille',
      icon: 'fas fa-graduation-cap',
      description: 'Interactive Braille tutorials',
      active: true
    },
    {
      id: 'text-braille',
      title: 'Text to Braille',
      icon: 'fas fa-file-alt',
      description: 'Convert plain text to Braille',
      active: false
    },
    {
      id: 'dhvani-assistant',
      title: 'Dhvani Assistant',
      icon: 'fas fa-microphone',
      description: 'Voice-powered accessibility',
      active: false
    },
    {
      id: 'braille-service',
      title: 'Braille as a Service',
      icon: 'fas fa-cloud',
      description: 'API for developers',
      active: false
    }
  ];

  // Learning sections for the main content
  const learningSections = [
    {
      id: 'audio-learning',
      title: 'Audio Learning',
      icon: 'fas fa-headphones',
      active: true
    },
    {
      id: 'hands-practice',
      title: 'Hands-on Practice',
      icon: 'fas fa-hands',
      active: false
    },
    {
      id: 'progress-tracking',
      title: 'Progress Tracking',
      icon: 'fas fa-chart-line',
      active: false
    },
    {
      id: 'session-history',
      title: 'Session History',
      icon: 'fas fa-folder',
      active: false
    }
  ];

  // Quick topics
  const quickTopics = ['Moon Phases', 'Solar System', 'Ocean Life', 'Plant Growth'];

  // Virtual braille keyboard layout
  const brailleKeyboard = [
    [
      { char: '⠁', label: '(a)' },
      { char: '⠃', label: '(b)' },
      { char: '⠉', label: '(c)' },
      { char: '⠙', label: '(d)' },
      { char: '⠑', label: '(e)' }
    ],
    [
      { char: '⠊', label: '(i)' },
      { char: '⠚', label: '(j)' },
      { char: '⠅', label: '(k)' },
      { char: '⠇', label: '(l)' },
      { char: '⠍', label: '(m)' }
    ],
    [
      { char: '⠝', label: '(n)' },
      { char: '⠕', label: '(o)' },
      { char: '⠏', label: '(p)' },
      { char: '⠟', label: '(q)' },
      { char: '⠗', label: '(r)' }
    ],
    [
      { char: '⠎', label: '(s)' },
      { char: '⠞', label: '(t)' },
      { char: '⠥', label: '(u)' },
      { char: '⠧', label: '(v)' },
      { char: '⠺', label: '(w)' }
    ],
    [
      { char: '⠭', label: '(x)' },
      { char: '⠽', label: '(y)' },
      { char: '⠵', label: '(z)' },
      { char: '⠀', label: 'Space' },
      { char: 'clear', label: 'Clear' }
    ]
  ];

  // Sample content for topics
  const topicContent = {
    'Moon Phases': `The moon's appearance changes dramatically as it orbits Earth, creating eight distinct phases that have fascinated humanity for millennia. The lunar cycle, also known as the lunation, takes approximately 29.5 days to complete and results from the changing positions of the Moon, Earth, and Sun. The New Moon marks the beginning of the lunar cycle, positioned between Earth and the Sun, making it invisible from our perspective. As the moon moves in its orbit, we begin to see the waxing phases, where the illuminated portion grows larger each night, leading to the spectacular Full Moon phase.`,
    'Solar System': `Our solar system consists of the Sun and all celestial objects that orbit around it, including eight planets, their moons, asteroids, comets, and cosmic dust.`,
    'Ocean Life': `The ocean is home to an incredible diversity of life forms, from microscopic plankton to massive blue whales, each playing a crucial role in marine ecosystems.`,
    'Plant Growth': `Plants grow through the process of photosynthesis, converting sunlight, water, and carbon dioxide into energy and oxygen, supporting all life on Earth.`
  };

  // Functions
  const activateTool = (toolId) => {
    // Tool activation would trigger navigation to different components
    console.log(`Activating tool: ${toolId}`);
  };

  const activateSection = (sectionId) => {
    setActiveSection(sectionId);
  };

  const startSession = () => {
    setSelectedTopic(topicInput);
    setSessionActive(true);
    setProgress(0);
    setBrailleInput('');
  };

  const playContent = () => {
    setIsPlaying(!isPlaying);
    // Audio playback implementation would go here
    if (!isPlaying) {
      // Simulate progress
      const interval = setInterval(() => {
        setProgress(prev => {
          if (prev >= 100) {
            clearInterval(interval);
            setIsPlaying(false);
            return 100;
          }
          return prev + 1;
        });
      }, 100);
    }
  };

  const insertBraille = (char) => {
    if (char === 'clear') {
      setBrailleInput('');
    } else if (char === '⠀') {
      setBrailleInput(prev => prev + ' ');
    } else {
      setBrailleInput(prev => prev + char);
    }
  };

  const clearAllInput = () => {
    setBrailleInput('');
  };

  const completeTyping = () => {
    if (brailleInput.trim()) {
      const newSession = {
        id: Date.now(),
        topic: selectedTopic,
        content: brailleInput,
        date: new Date().toISOString().split('T')[0],
        time: new Date().toLocaleTimeString()
      };
      setSessionHistory(prev => [newSession, ...prev]);
      // Show completion feedback
      alert('Typing session completed and saved to history!');
    }
  };

  const selectQuickTopic = (topic) => {
    setTopicInput(topic);
  };

  return (
    <div className="learn-braille-container">
      <div className="braille-learning-layout">
        {/* Left Sidebar - Learning Tools - COMMENTED OUT TO AVOID DUPLICATION */}
        {/* 
        <div className="learning-sidebar">
          <div className="sidebar-header">
            <h3>
              <i className="fas fa-graduation-cap"></i>
              Learning Tools
            </h3>
          </div>
          
          <div className="learning-tools">
            {learningTools.map(tool => (
              <div 
                key={tool.id}
                className={`learning-tool ${tool.active ? 'active' : ''}`}
                onClick={() => activateTool(tool.id)}
              >
                <div className="tool-icon">
                  <i className={tool.icon}></i>
                </div>
                <div className="tool-content">
                  <div className="tool-title">{tool.title}</div>
                  <div className="tool-description">{tool.description}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
        */}

        {/* Main Content Area */}
        <div className="learning-content">
          {/* Interactive Braille Learning System Header */}
          <div className="section-header">
            <h2>
              <i className="fas fa-graduation-cap"></i>
              Interactive Braille Learning System
            </h2>
            <p>This comprehensive learning tool allows anyone to master Braille through interactive practice sessions. Using our Braille-enabled keyboard interface, students can learn by listening to content and typing in Braille simultaneously.</p>
          </div>

          {/* Learning Section Tabs */}
          <div className="learning-sections">
            {learningSections.map(section => (
              <div
                key={section.id}
                className={`section-tab ${activeSection === section.id ? 'active' : ''}`}
                onClick={() => activateSection(section.id)}
              >
                <i className={section.icon}></i>
                <span>{section.title}</span>
              </div>
            ))}
          </div>

          {/* Audio Learning Section */}
          {activeSection === 'audio-learning' && (
            <div className="content-section active">
              {!sessionActive ? (
                <div className="topic-selection">
                  <div className="select-topic-card">
                    <h3>
                      <i className="fas fa-target"></i>
                      Select Learning Topic
                    </h3>
                    
                    <div className="topic-input-section">
                      <input
                        type="text"
                        value={topicInput}
                        onChange={(e) => setTopicInput(e.target.value)}
                        className="topic-input"
                        placeholder="Enter a topic (e.g., Moon Phases)"
                      />
                      <button onClick={startSession} className="start-session-btn">
                        <i className="fas fa-play"></i>
                        Start Session
                      </button>
                    </div>

                    <div className="quick-topics">
                      <span className="quick-label">Quick Topics:</span>
                      {quickTopics.map(topic => (
                        <button
                          key={topic}
                          onClick={() => selectQuickTopic(topic)}
                          className="quick-topic-btn"
                        >
                          {topic}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              ) : (
                <div className="learning-session">
                  <div className="learning-content-card">
                    <h3>
                      <i className="fas fa-book"></i>
                      Learning Content
                    </h3>
                    
                    <div className="content-display">
                      <h4>{selectedTopic}</h4>
                      <p>{topicContent[selectedTopic] || `Learning content for ${selectedTopic} would be displayed here with detailed information and explanations.`}</p>
                      
                      <div className="audio-controls">
                        <button 
                          onClick={playContent} 
                          className={`play-content-btn ${isPlaying ? 'playing' : ''}`}
                        >
                          <i className={`fas ${isPlaying ? 'fa-pause' : 'fa-play'}`}></i>
                          {isPlaying ? 'Pause' : 'Play'} Content
                        </button>
                        
                        <div className="progress-bar">
                          <div className="progress-fill" style={{width: `${progress}%`}}></div>
                        </div>
                        <span className="progress-text">{progress}%</span>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Hands-on Practice Section */}
          {activeSection === 'hands-practice' && (
            <div className="content-section active">
              <div className="braille-typing-section">
                <h3>
                  <i className="fas fa-keyboard"></i>
                  Braille Typing Practice
                </h3>
                
                <div className="typing-instructions">
                  <div className="instructions-card">
                    <p><strong>Instructions:</strong> Listen to the content above and type what you hear using Braille characters. Use your Braille keyboard or the virtual keys below.</p>
                  </div>
                </div>

                <div className="virtual-keyboard">
                  {brailleKeyboard.map((row, rowIndex) => (
                    <div key={rowIndex} className="keyboard-row">
                      {row.map((key, keyIndex) => (
                        <button
                          key={keyIndex}
                          className={`braille-key ${key.char === 'clear' ? 'clear-key' : ''} ${key.char === '⠀' ? 'space-key' : ''}`}
                          onClick={() => insertBraille(key.char)}
                        >
                          {key.char === 'clear' ? (
                            <>
                              <i className="fas fa-times"></i>
                              <span>Clear</span>
                            </>
                          ) : (
                            <>
                              <span className="braille-char">{key.char}</span>
                              <span className="braille-label">{key.label}</span>
                            </>
                          )}
                        </button>
                      ))}
                    </div>
                  ))}
                </div>

                <div className="braille-input-section">
                  <label htmlFor="brailleInput">Your Braille Input:</label>
                  <textarea
                    id="brailleInput"
                    value={brailleInput}
                    onChange={(e) => setBrailleInput(e.target.value)}
                    className="braille-input-area"
                    placeholder="Type your Braille here as you listen to the content..."
                    rows="8"
                  />
                  
                  <div className="input-controls">
                    <button onClick={completeTyping} className="complete-btn">
                      <i className="fas fa-check"></i>
                      Typing Complete - Review
                    </button>
                    <button onClick={clearAllInput} className="clear-all-btn">
                      <i className="fas fa-trash"></i>
                      Clear All
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Progress Tracking Section */}
          {activeSection === 'progress-tracking' && (
            <div className="content-section active">
              <div className="progress-dashboard">
                <h3>
                  <i className="fas fa-chart-line"></i>
                  Learning Progress & Statistics
                </h3>
                
                <div className="stats-grid">
                  <div className="stat-card">
                    <div className="stat-icon">
                      <i className="fas fa-clock"></i>
                    </div>
                    <div className="stat-content">
                      <div className="stat-value">{sessionHistory.length}</div>
                      <div className="stat-label">Sessions Completed</div>
                    </div>
                  </div>
                  
                  <div className="stat-card">
                    <div className="stat-icon">
                      <i className="fas fa-keyboard"></i>
                    </div>
                    <div className="stat-content">
                      <div className="stat-value">{brailleInput.length}</div>
                      <div className="stat-label">Characters Typed</div>
                    </div>
                  </div>
                  
                  <div className="stat-card">
                    <div className="stat-icon">
                      <i className="fas fa-trophy"></i>
                    </div>
                    <div className="stat-content">
                      <div className="stat-value">{Math.round((sessionHistory.length / 10) * 100)}%</div>
                      <div className="stat-label">Progress</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Session History Section */}
          {activeSection === 'session-history' && (
            <div className="content-section active">
              <div className="session-history">
                <h3>
                  <i className="fas fa-history"></i>
                  Learning Session History
                </h3>
                
                {sessionHistory.length === 0 ? (
                  <div className="no-history">
                    <i className="fas fa-inbox"></i>
                    <p>No learning sessions yet. Complete a typing practice to see your history here.</p>
                  </div>
                ) : (
                  <div className="history-list">
                    {sessionHistory.map(session => (
                      <div key={session.id} className="history-item">
                        <div className="session-info">
                          <h4>{session.topic}</h4>
                          <p className="session-meta">{session.date} at {session.time}</p>
                          <p className="session-preview">{session.content.substring(0, 100)}...</p>
                        </div>
                        <div className="session-actions">
                          <button className="view-btn">
                            <i className="fas fa-eye"></i>
                            View
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default LearnBraille;

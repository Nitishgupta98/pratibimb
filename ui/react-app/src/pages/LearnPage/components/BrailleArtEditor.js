import React, { useState } from 'react';
import './BrailleArtEditor.css';

const BrailleArtEditor = () => {
  const [selectedTopic, setSelectedTopic] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [recentSessions] = useState([]);

  const quickTopics = [
    'Human Heart',
    'Solar System', 
    'Plant Cell',
    'Human Brain',
    'Water Cycle'
  ];

  const handleTopicSelect = (topic) => {
    setSelectedTopic(topic);
  };

  const handleGenerateContent = () => {
    if (!selectedTopic.trim()) {
      alert('Please enter a learning topic first');
      return;
    }
    
    setIsGenerating(true);
    // Simulate content generation
    setTimeout(() => {
      alert(`Generating Braille art content for: ${selectedTopic}`);
      setIsGenerating(false);
    }, 2000);
  };

  return (
    <div className="braille-art-editor">
      <div className="page-header">
        <h1><i className="fas fa-palette"></i> Braille Art Editor</h1>
        <p>Generate tactile visuals in Braille for enhanced learning through touch and cognitive understanding</p>
      </div>

      {/* About This Tool Section */}
      <div className="about-section">
        <div className="info-card">
          <i className="fas fa-info-circle"></i>
          <h3>About This Tool</h3>
          <p>
            The Braille Art Editor is a specialized tool designed to generate visual representations in Braille format 
            that can be printed and tactilely felt. This revolutionary approach allows visually impaired individuals to 
            "visualize" images through touch, significantly enhancing their understanding of technical concepts and 
            various topics beyond just audio learning.
          </p>
        </div>
      </div>

      {/* Feature Badges */}
      <div className="features-row">
        <div className="feature-badge">
          <i className="fas fa-hand-paper"></i>
          <span>Tactile Learning</span>
        </div>
        <div className="feature-badge">
          <i className="fas fa-brain"></i>
          <span>Cognitive Enhancement</span>
        </div>
        <div className="feature-badge">
          <i className="fas fa-eye"></i>
          <span>Visual Concepts</span>
        </div>
        <div className="feature-badge">
          <i className="fas fa-print"></i>
          <span>Printable Format</span>
        </div>
      </div>

      {/* Topic Selection Section */}
      <div className="topic-selection">
        <div className="section-header">
          <h3><i className="fas fa-search"></i> Select Learning Topic</h3>
        </div>
        
        <div className="topic-input-area">
          <input
            type="text"
            value={selectedTopic}
            onChange={(e) => setSelectedTopic(e.target.value)}
            placeholder="Enter a topic (e.g., Human Heart, Solar System, Plant Cell...)"
            className="topic-input"
          />
          <button 
            className="generate-btn"
            onClick={handleGenerateContent}
            disabled={isGenerating}
          >
            <i className="fas fa-magic"></i> 
            {isGenerating ? 'Generating...' : 'Generate Content'}
          </button>
        </div>

        <div className="quick-topics">
          <span className="quick-label">Quick Topics:</span>
          <div className="topic-buttons">
            {quickTopics.map((topic, index) => (
              <button
                key={index}
                className="topic-btn"
                onClick={() => handleTopicSelect(topic)}
              >
                {topic}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Recent Sessions Section */}
      <div className="recent-sessions">
        <div className="section-header">
          <h3><i className="fas fa-history"></i> Recent Sessions</h3>
        </div>
        
        <div className="sessions-content">
          {recentSessions.length === 0 ? (
            <div className="empty-sessions">
              <i className="fas fa-clock"></i>
              <p>No recent sessions yet. Start by generating content for a learning topic above.</p>
            </div>
          ) : (
            <div className="sessions-list">
              {recentSessions.map((session, index) => (
                <div key={index} className="session-item">
                  <div className="session-info">
                    <h4>{session.topic}</h4>
                    <span className="session-date">{session.date}</span>
                  </div>
                  <button className="session-action">
                    <i className="fas fa-download"></i>
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default BrailleArtEditor;

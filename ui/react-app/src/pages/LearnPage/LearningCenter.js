import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import './LearningCenter.css';

// Import the actual components
import YoutubeToBraille from './components/YoutubeToBraille';
import BrailleArtEditor from './components/BrailleArtEditor';
import LearnBraille from './components/LearnBraille';
import TextToBraille from './components/TextToBraille';
import DhvaniAssistant from './components/DhvaniAssistant';
import BrailleAsaService from './components/BrailleAsaService';

// Fallback placeholder component
const PlaceholderComponent = ({ title, description }) => (
  <div className="placeholder-component" style={{ padding: '0.5rem', textAlign: 'center', background: 'white', borderRadius: '8px', margin: '1rem' }}>
    <h2 style={{ color: '#7b2cbf', marginBottom: '1rem' }}>{title}</h2>
    <p style={{ color: '#666', marginBottom: '1rem' }}>{description}</p>
    <div style={{ background: '#f8f9fa', padding: '1rem', borderRadius: '4px', fontSize: '0.9em', color: '#666' }}>
      🚧 This component is being developed. Please check back soon!
    </div>
  </div>
);

const LearningCenter = () => {
  const { section } = useParams();
  const [activeSection, setActiveSection] = useState('overview');

  useEffect(() => {
    if (section) {
      setActiveSection(section);
    }
  }, [section]);

  const learningTools = [
    {
      id: 'youtube-braille',
      title: 'YouTube to Braille',
      icon: 'fab fa-youtube',
      description: 'Convert video transcripts to Braille',
      color: '#FF0000'
    },
    {
      id: 'braille-art',
      title: 'Braille Art Editor',
      icon: 'fas fa-palette',
      description: 'Create artistic Braille patterns',
      color: '#9C27B0'
    },
    {
      id: 'learn-braille',
      title: 'Learn Braille',
      icon: 'fas fa-book-open',
      description: 'Interactive Braille learning system',
      color: '#4CAF50'
    },
    {
      id: 'text-braille',
      title: 'Text to Braille',
      icon: 'fas fa-font',
      description: 'Convert text documents to Braille',
      color: '#2196F3'
    },
    {
      id: 'dhvani',
      title: 'Dhvani Assistant',
      icon: 'fas fa-microphone',
      description: 'Voice-powered accessibility assistant',
      color: '#FF5722'
    },
    {
      id: 'braas',
      title: 'Braille as a Service',
      icon: 'fas fa-cloud',
      description: 'Professional Braille conversion service',
      color: '#607D8B'
    }
  ];

  const renderOverview = () => (
    <div className="overview-section">
      <div className="page-header">
        <h1>
          <i className="fas fa-graduation-cap"></i>
          Learning Center
        </h1>
        <p>Comprehensive tools for Braille learning and conversion</p>
      </div>
      
      <div className="tools-grid">
        {learningTools.map(tool => (
          <div 
            key={tool.id} 
            className="tool-card"
            onClick={() => setActiveSection(tool.id)}
            style={{ '--tool-color': tool.color }}
          >
            <div className="tool-icon">
              <i className={tool.icon}></i>
            </div>
            <h3>{tool.title}</h3>
            <p>{tool.description}</p>
            <button className="tool-button">
              Get Started <i className="fas fa-arrow-right"></i>
            </button>
          </div>
        ))}
      </div>
    </div>
  );

  const renderContent = () => {
    try {
      switch (activeSection) {
        case 'youtube-braille': 
          return <YoutubeToBraille />;
        case 'braille-art': 
          return <BrailleArtEditor />;
        case 'learn-braille': 
          return <LearnBraille />;
        case 'text-braille': 
          return <TextToBraille />;
        case 'dhvani': 
          return <DhvaniAssistant />;
        case 'braas': 
          return <BrailleAsaService />;
        default: 
          return renderOverview();
      }
    } catch (error) {
      console.error('Error rendering component:', error);
      return <PlaceholderComponent title={`Error loading ${activeSection}`} description="There was an issue loading this component. Please try again." />;
    }
  };

  return (
    <div className="learning-center">
      <div className="sidebar-nav">
        <div className="nav-header">
          <h3>
            <i className="fas fa-graduation-cap"></i>
            Learning Center
          </h3>
        </div>
        <nav className="nav-menu">
          <div className="nav-section">
            <div className="nav-section-header">Quick Access</div>
            <button 
              className={`nav-item ${activeSection === 'overview' ? 'active' : ''}`}
              onClick={() => setActiveSection('overview')}
            >
              <i className="fas fa-home"></i>
              <span>Overview</span>
            </button>
          </div>
          
          <div className="nav-section">
            <div className="nav-section-header">Learning Tools</div>
            {learningTools.map(tool => (
              <button 
                key={tool.id}
                className={`nav-item ${activeSection === tool.id ? 'active' : ''}`}
                onClick={() => setActiveSection(tool.id)}
              >
                <i className={tool.icon}></i>
                <span>{tool.title}</span>
              </button>
            ))}
          </div>
        </nav>
      </div>

      <div className="main-content">
        {renderContent()}
      </div>
    </div>
  );
};

export default LearningCenter;

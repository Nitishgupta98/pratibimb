import React from 'react';
import './QuickLinks.css';

const QuickLinks = ({ links = [] }) => {
  const getIconClass = (iconName) => {
    // Map icon names to Font Awesome classes
    const iconMap = {
      'converter': 'fas fa-language',
      'learn': 'fas fa-graduation-cap',
      'marketplace': 'fas fa-store',
      'community': 'fas fa-users',
      'dhvani': 'fas fa-volume-up',
      'documentation': 'fas fa-book',
      'support': 'fas fa-life-ring',
      'settings': 'fas fa-cog',
      'profile': 'fas fa-user',
      'history': 'fas fa-history',
      'upload': 'fas fa-upload',
      'download': 'fas fa-download',
      'default': 'fas fa-link'
    };
    
    return iconMap[iconName] || iconMap.default;
  };

  const getIconColor = (category) => {
    const colorMap = {
      'tools': 'var(--primary-color)',
      'learning': 'var(--success-color)',
      'community': 'var(--warning-color)',
      'support': 'var(--info-color)',
      'settings': 'var(--text-muted)',
      'default': 'var(--primary-color)'
    };
    
    return colorMap[category] || colorMap.default;
  };

  // Default links to show when no custom links are provided
  const defaultLinks = [
    {
      id: 'converter',
      title: 'Text Converter',
      description: 'Convert text to Braille format',
      url: '/converter',
      icon: 'converter',
      category: 'tools'
    },
    {
      id: 'learn',
      title: 'Learning Center',
      description: 'Explore Braille learning resources',
      url: '/learning-center',
      icon: 'learn',
      category: 'learning'
    },
    {
      id: 'marketplace',
      title: 'Accessibility Store',
      description: 'Browse accessibility products',
      url: '/accessibility-store',
      icon: 'marketplace',
      category: 'community'
    },
    {
      id: 'community',
      title: 'Community Hub',
      description: 'Connect with others',
      url: '/community-hub',
      icon: 'community',
      category: 'community'
    },
    {
      id: 'dhvani',
      title: 'Dhvani',
      description: 'Voice and audio tools',
      url: '/dhvani',
      icon: 'dhvani',
      category: 'tools'
    },
    {
      id: 'documentation',
      title: 'Documentation',
      description: 'User guides and help',
      url: '/documentation',
      icon: 'documentation',
      category: 'support'
    }
  ];

  // Use provided links or fall back to default links
  const displayLinks = links.length > 0 ? links : defaultLinks;

  return (
    <div className="quick-links">
      <div className="section-header">
        <h2>
          <i className="fas fa-bolt"></i>
          Quick Links
        </h2>
        <span className="links-count">{displayLinks.length} shortcuts</span>
      </div>
      
      <div className="links-grid">
        {displayLinks.map((link, index) => (
          <a
            key={link.id || index}
            href={link.url || link.link_url || '#'}
            className="quick-link-item"
            target={link.url && link.url.startsWith('http') ? '_blank' : '_self'}
            rel={link.url && link.url.startsWith('http') ? 'noopener noreferrer' : undefined}
          >
            <div className="link-icon" 
                 style={{ backgroundColor: getIconColor(link.category) }}>
              <i className={getIconClass(link.icon || link.name)}></i>
            </div>
            
            <div className="link-content">
              <h3 className="link-title">{link.title || link.name}</h3>
              <p className="link-description">
                {link.description || 'Quick access link'}
              </p>
              
              {link.category && (
                <span className="link-category">
                  {link.category}
                </span>
              )}
            </div>
            
            <div className="link-arrow">
              <i className="fas fa-chevron-right"></i>
            </div>
          </a>
        ))}
      </div>
    </div>
  );
};

export default QuickLinks;

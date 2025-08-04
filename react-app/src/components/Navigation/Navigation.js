import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './Navigation.css';

const Navigation = ({ onTabChange }) => {
  const location = useLocation();
  const navigate = useNavigate();
  
  const tabs = [
    { id: 'dashboard', label: 'Dashboard', icon: 'fas fa-home', path: '/' },
    { id: 'learning-center', label: 'Learning Center', icon: 'fas fa-graduation-cap', path: '/learning-center' },
    { id: 'accessibility-store', label: 'Accessibility Store', icon: 'fas fa-store', path: '/accessibility-store' },
    { id: 'community-hub', label: 'Community Hub', icon: 'fas fa-users', path: '/community-hub' }
  ];

  const handleTabClick = (tab) => {
    navigate(tab.path);
    if (onTabChange) {
      onTabChange(tab.id);
    }
  };

  const isActive = (tabPath) => {
    return location.pathname === tabPath;
  };

  return (
    <nav className="nav-tabs">
      <div className="nav-tabs-container">
        <div className="nav-tabs-list">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              className={`nav-tab ${isActive(tab.path) ? 'active' : ''}`}
              onClick={() => handleTabClick(tab)}
              aria-current={isActive(tab.path) ? 'page' : undefined}
            >
              <i className={tab.icon}></i>
              <span className="tab-label">{tab.label}</span>
            </button>
          ))}
        </div>
      </div>
    </nav>
  );
};

export default Navigation;

import React from 'react';
import './Header.css';

const Header = () => {
  return (
    <header className="header">
      <div className="header-content">
        <div className="header-logo">
          <div className="logo-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M1 12C1 12 5 4 12 4C19 4 23 12 23 12C23 12 19 20 12 20C5 20 1 12 1 12Z" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <circle cx="12" cy="12" r="3" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </div>
          <div className="logo-content">
            <h1 className="logo-title">Pratibimb</h1>
            <p className="logo-subtitle">True Reflection of Digital World</p>
          </div>
        </div>
        <nav className="header-nav">
          <div className="nav-item">
            <svg className="accessibility-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="4" r="2" fill="currentColor"/>
              <path d="M19 13v-2c0-1.1-.9-2-2-2H7c-1.1 0-2 .9-2 2v2m14 0-1.5 3-1.5-3m-9 0 1.5 3 1.5-3m6-6v4c0 1.1-.9 2-2 2s-2-.9-2-2V7" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
            <span>Accessibility First</span>
          </div>
        </nav>
      </div>
    </header>
  );
};

export default Header;

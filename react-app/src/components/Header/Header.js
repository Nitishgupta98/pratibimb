import React from 'react';
import './Header.css';

const Header = ({ userName = "Bhupinder Singh Chawla" }) => {
  return (
    <header className="infosys-header">
      <div className="header-content">
        <div className="header-left">
          <div className="header-title">
            <h1>
              Pratibimb <span className="separator">|</span> True Reflection of Digital World!
            </h1>
          </div>
        </div>
        <div className="header-right">
          <div className="language-selector">
            <button className="language-btn">
              <i className="fas fa-globe"></i> US English <i className="fas fa-chevron-down"></i>
            </button>
          </div>
          <div className="user-info">
            <span className="user-name">{userName}</span>
            <div className="user-avatar">
              <i className="fas fa-user"></i>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;

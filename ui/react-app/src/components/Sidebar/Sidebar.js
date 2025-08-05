import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Sidebar.css';

const Sidebar = () => {
  const navigate = useNavigate();

  const quickAccessItems = [
    {
      id: 1,
      title: "YouTube to Braille Converter",
      icon: "fab fa-youtube",
      color: "#8B63D8",
      path: '/learning-center/youtube-braille'
    },
    {
      id: 2,
      title: "Dhvani (Voice Assistant)",
      icon: "fas fa-microphone",
      color: "#8B63D8",
      path: '/learning-center/dhvani'
    },
    {
      id: 3,
      title: "Braille Art Editor",
      icon: "fas fa-palette",
      color: "#8B63D8",
      path: '/learning-center/braille-art'
    },
    {
      id: 4,
      title: "Learn Braille",
      icon: "fas fa-book-open",
      color: "#8B63D8",
      path: '/learning-center/learn-braille'
    },
    {
      id: 5,
      title: "Braille as a Service",
      icon: "fas fa-cloud",
      color: "#8B63D8",
      path: '/learning-center/braas'
    },
    {
      id: 6,
      title: "Text to Braille Converter",
      icon: "fas fa-font",
      color: "#8B63D8",
      path: '/learning-center/text-braille'
    },
    {
      id: 7,
      title: "Community Hub",
      icon: "fas fa-globe",
      color: "#8B63D8",
      path: '/community-hub'
    }
  ];

  const handleItemClick = (item) => {
    navigate(item.path);
  };

  return (
    <nav className="sidebar">
      <div className="sidebar-content">
        <div className="sidebar-header">
          <h3>
            <i className="fas fa-bolt"></i> 
            Quick Access
          </h3>
        </div>
        
        <div className="quick-access-list">
          {quickAccessItems.map((item) => (
            <button 
              key={item.id} 
              className="quick-access-item"
              onClick={() => handleItemClick(item)}
            >
              <div className="item-icon" style={{ color: item.color }}>
                <i className={item.icon}></i>
              </div>
              <span className="item-title">{item.title}</span>
            </button>
          ))}
        </div>
      </div>
    </nav>
  );
};

export default Sidebar;

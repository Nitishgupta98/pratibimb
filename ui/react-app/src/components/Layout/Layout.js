import React from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import Header from '../Header';
import Navigation from '../Navigation';
import Sidebar from '../Sidebar/Sidebar';
import './Layout.css';

const Layout = () => {
  const location = useLocation();
  
  // Show sidebar only on the Dashboard (home page)
  const showSidebar = location.pathname === '/';

  return (
    <div className="app-layout">
      <Header />
      <Navigation />
      <div className="layout-content">
        {showSidebar && <Sidebar />}
        <main className={`main-content ${!showSidebar ? 'full-width' : ''}`}>
          <div className="content-wrapper">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
};

export default Layout;

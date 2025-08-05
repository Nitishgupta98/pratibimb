import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Layout } from './components';
import { 
  HomePage, 
  ConverterPage, 
  LearnPage, 
  MarketplacePage, 
  CommunityPage, 
  DhvaniPage, 
  DocumentationPage 
} from './pages';
import './styles/globals.css';
import './styles/pages.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<HomePage />} />
            <Route path="learning-center" element={<LearnPage />} />
            <Route path="learning-center/:section" element={<LearnPage />} />
            <Route path="accessibility-store" element={<MarketplacePage />} />
            <Route path="community-hub" element={<CommunityPage />} />
            
            {/* Legacy routes for backward compatibility */}
            <Route path="converter" element={<ConverterPage />} />
            <Route path="learn" element={<LearnPage />} />
            <Route path="marketplace" element={<MarketplacePage />} />
            <Route path="community" element={<CommunityPage />} />
            <Route path="dhvani" element={<DhvaniPage />} />
            <Route path="documentation" element={<DocumentationPage />} />
            
            {/* Catch-all route for 404 */}
            <Route path="*" element={
              <div className="page-placeholder">
                <h1>Page Not Found</h1>
                <p>The page you're looking for doesn't exist.</p>
                <a href="/" className="btn btn-primary">Go Home</a>
              </div>
            } />
          </Route>
        </Routes>
      </div>
    </Router>
  );
}

export default App;

import React from 'react';
import './TrendingUpdates.css';

const TrendingUpdates = ({ updates = [] }) => {
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    });
  };

  const formatTime = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="trending-updates">
      <div className="section-header">
        <h2>
          <i className="fas fa-fire"></i>
          Trending Updates
        </h2>
        <span className="update-count">{updates.length} updates</span>
      </div>
      
      <div className="updates-list">
        {updates.length === 0 ? (
          <div className="empty-state">
            <i className="fas fa-newspaper"></i>
            <p>No updates available</p>
            <small>Check back later for the latest news and updates</small>
          </div>
        ) : (
          updates.map((update, index) => (
            <div key={update.id || index} className="update-item">
              <div className="update-header">
                <div className="update-meta">
                  <span className="update-category">{update.category || 'General'}</span>
                  <span className="update-date">{formatDate(update.created_at || update.date)}</span>
                </div>
                <div className="update-time">
                  {formatTime(update.created_at || update.date)}
                </div>
              </div>
              
              <h3 className="update-title">{update.title}</h3>
              
              <p className="update-description">
                {update.description || update.content}
              </p>
              
              <div className="update-footer">
                <div className="update-stats">
                  {update.views && (
                    <span className="stat">
                      <i className="fas fa-eye"></i>
                      {update.views}
                    </span>
                  )}
                  {update.likes && (
                    <span className="stat">
                      <i className="fas fa-heart"></i>
                      {update.likes}
                    </span>
                  )}
                  {update.comments && (
                    <span className="stat">
                      <i className="fas fa-comments"></i>
                      {update.comments}
                    </span>
                  )}
                </div>
                
                <div className="update-actions">
                  <button className="action-btn" title="Like">
                    <i className="fas fa-heart"></i>
                  </button>
                  <button className="action-btn" title="Share">
                    <i className="fas fa-share"></i>
                  </button>
                  <button className="action-btn" title="Bookmark">
                    <i className="fas fa-bookmark"></i>
                  </button>
                </div>
              </div>
              
              {update.link_url && update.link_url !== '#' && (
                <a 
                  href={update.link_url} 
                  className="read-more-link"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Read Full Article
                  <i className="fas fa-external-link-alt"></i>
                </a>
              )}
            </div>
          ))
        )}
      </div>
      
      {updates.length > 0 && (
        <div className="section-footer">
          <button className="view-all-btn">
            <i className="fas fa-plus"></i>
            View All Updates
          </button>
        </div>
      )}
    </div>
  );
};

export default TrendingUpdates;

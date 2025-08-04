import React from 'react';
import './RecentActivities.css';

const RecentActivities = ({ activities = [] }) => {
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 1) return 'Today';
    if (diffDays === 2) return 'Yesterday';
    if (diffDays < 7) return `${diffDays - 1} days ago`;
    
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric'
    });
  };

  const getActivityIcon = (type) => {
    const iconMap = {
      'conversion': 'fas fa-language',
      'upload': 'fas fa-upload',
      'download': 'fas fa-download',
      'forum_post': 'fas fa-comments',
      'learning': 'fas fa-graduation-cap',
      'marketplace': 'fas fa-shopping-cart',
      'community': 'fas fa-users',
      'default': 'fas fa-bell'
    };
    
    return iconMap[type] || iconMap.default;
  };

  const getActivityColor = (type) => {
    const colorMap = {
      'conversion': 'var(--primary-color)',
      'upload': 'var(--success-color)',
      'download': 'var(--info-color)',
      'forum_post': 'var(--warning-color)',
      'learning': 'var(--primary-light)',
      'marketplace': 'var(--accent-color)',
      'community': 'var(--secondary-color)',
      'default': 'var(--text-muted)'
    };
    
    return colorMap[type] || colorMap.default;
  };

  return (
    <div className="recent-activities">
      <div className="section-header">
        <h2>
          <i className="fas fa-clock"></i>
          Recent Activities
        </h2>
        <span className="activity-count">{activities.length}</span>
      </div>
      
      <div className="activities-list">
        {activities.length === 0 ? (
          <div className="empty-state">
            <i className="fas fa-history"></i>
            <p>No recent activities</p>
            <small>Your recent actions will appear here</small>
          </div>
        ) : (
          activities.map((activity, index) => (
            <div key={activity.id || index} className="activity-item">
              <div className="activity-icon" 
                   style={{ backgroundColor: getActivityColor(activity.activity_type || activity.type) }}>
                <i className={getActivityIcon(activity.activity_type || activity.type)}></i>
              </div>
              
              <div className="activity-content">
                <div className="activity-header">
                  <h4 className="activity-title">
                    {activity.title || activity.description}
                  </h4>
                  <span className="activity-time">
                    {formatDate(activity.created_at || activity.timestamp)}
                  </span>
                </div>
                
                {activity.details && (
                  <p className="activity-details">
                    {activity.details}
                  </p>
                )}
                
                <div className="activity-meta">
                  <span className="activity-type">
                    {activity.activity_type || activity.type || 'Activity'}
                  </span>
                  
                  {activity.status && (
                    <span className={`activity-status status-${activity.status.toLowerCase()}`}>
                      {activity.status}
                    </span>
                  )}
                </div>
              </div>
              
              <div className="activity-actions">
                <button className="activity-action" title="View details">
                  <i className="fas fa-eye"></i>
                </button>
                <button className="activity-action" title="More options">
                  <i className="fas fa-ellipsis-v"></i>
                </button>
              </div>
            </div>
          ))
        )}
      </div>
      
      {activities.length > 0 && (
        <div className="section-footer">
          <button className="view-all-btn">
            <i className="fas fa-history"></i>
            View Activity History
          </button>
        </div>
      )}
    </div>
  );
};

export default RecentActivities;

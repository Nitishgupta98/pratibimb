import React, { useState, useEffect } from 'react';
import { useData } from '../../hooks';
import './HomePage.css';

const HomePage = () => {
  const { data, loading, error } = useData();
  const [currentSlide, setCurrentSlide] = useState(0);
  const [activeTab, setActiveTab] = useState('Recent');

  // Auto-advance carousel
  useEffect(() => {
    if (data?.carousel_slides?.length > 0) {
      const timer = setInterval(() => {
        setCurrentSlide(prev => 
          prev === data.carousel_slides.length - 1 ? 0 : prev + 1
        );
      }, 5000);
      return () => clearInterval(timer);
    }
  }, [data?.carousel_slides?.length]);

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading">
          <div className="spinner"></div>
          <p>Loading Pratibimb data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container">
        <div className="alert alert-danger">
          <h3>Error Loading Data</h3>
          <p>{error}</p>
          <button className="btn btn-primary" onClick={() => window.location.reload()}>
            Retry
          </button>
        </div>
      </div>
    );
  }

  const carouselSlides = data?.carousel_slides || [];
  const forumPosts = data?.forum_posts || [];
  const recentActivities = data?.recent_activities || [];
  const latestUpdates = data?.latest_updates || [];
  
  // Format recent activities with proper time display
  const formatTimeAgo = (timestamp) => {
    const now = new Date();
    const activityTime = new Date(timestamp);
    const diffMs = now - activityTime;
    const diffMins = Math.floor(diffMs / (1000 * 60));
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    
    if (diffMins < 60) {
      return `${diffMins} minute${diffMins !== 1 ? 's' : ''} ago`;
    } else if (diffHours < 24) {
      return `${diffHours} hour${diffHours !== 1 ? 's' : ''} ago`;
    } else {
      return activityTime.toLocaleDateString();
    }
  };

  const nextSlide = () => {
    setCurrentSlide(prev => 
      prev === carouselSlides.length - 1 ? 0 : prev + 1
    );
  };

  const prevSlide = () => {
    setCurrentSlide(prev => 
      prev === 0 ? carouselSlides.length - 1 : prev - 1
    );
  };

  const goToSlide = (index) => {
    setCurrentSlide(index);
  };

  return (
    <div className="home-page">
      <div className="main-content-wrapper">
        {/* Hero Carousel Section */}
        <div className="hero-carousel-section">
          <div className="carousel-header">
            <i className="fas fa-newspaper"></i>
            <h2>Accessibility News & Updates</h2>
          </div>
          <div className="carousel-container">
            <div className="carousel-wrapper">
              <button className="carousel-btn prev-btn" onClick={prevSlide}>
                <i className="fas fa-chevron-left"></i>
              </button>
              
              {carouselSlides.length > 0 && (
                <div className="carousel-slide active">
                  <div 
                    className="slide-content"
                    style={{ background: carouselSlides[currentSlide]?.background_gradient }}
                  >
                    <div className="slide-info">
                      <span className="slide-type">{carouselSlides[currentSlide]?.slide_type}</span>
                      <h3 className="slide-title">{carouselSlides[currentSlide]?.title}</h3>
                      <p className="slide-description">{carouselSlides[currentSlide]?.description}</p>
                      <span className="slide-date">{carouselSlides[currentSlide]?.publish_date}</span>
                    </div>
                  </div>
                </div>
              )}
              
              <button className="carousel-btn next-btn" onClick={nextSlide}>
                <i className="fas fa-chevron-right"></i>
              </button>
            </div>
            
            {carouselSlides.length > 0 && (
              <div className="carousel-indicators">
                {carouselSlides.map((_, index) => (
                  <span 
                    key={index} 
                    className={index === currentSlide ? 'active' : ''}
                    onClick={() => goToSlide(index)}
                  ></span>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Right Sidebar - Latest at Pratibimb */}
        <div className="latest-sidebar">
          <div className="sidebar-header">
            <i className="fas fa-star"></i>
            <h3>Latest at Pratibimb</h3>
          </div>
          <div className="latest-items">
            {latestUpdates.filter(update => update.is_featured).map((update) => (
              <div key={update.id} className="latest-item">
                <h4 className="latest-title">{update.title}</h4>
                <p className="latest-description">{update.description}</p>
                <div className="latest-meta">
                  <span className="latest-date">{update.publish_date}</span>
                  <a href="#" className="latest-link">
                    {update.update_type === 'feature' ? 'Explore →' : 
                     update.update_type === 'tutorial' ? 'Build Now →' : 
                     update.update_type === 'beta' ? 'Join Beta →' : 
                     'Learn More →'}
                  </a>
                </div>
              </div>
            ))}
            <div className="see-all-updates">
              <a href="#" className="see-all-link">
                <i className="fas fa-arrow-right"></i> See All Updates
              </a>
            </div>
          </div>
        </div>
      </div>

      {/* Community Q&A Forum Section */}
      <div className="community-forum-section">
        <div className="forum-header">
          <div className="forum-title">
            <i className="fas fa-comments"></i>
            <h2>Community Q&A Forum</h2>
          </div>
          <button className="post-question-btn">
            <i className="fas fa-plus"></i> Post Question
          </button>
        </div>
        
        <div className="forum-tabs">
          {['Recent', 'Hot', 'Unanswered', 'My Posts'].map(tab => (
            <button 
              key={tab}
              className={`tab-btn ${activeTab === tab ? 'active' : ''}`}
              onClick={() => setActiveTab(tab)}
            >
              {tab}
            </button>
          ))}
        </div>

        <div className="forum-content">
          <div className="forum-posts">
            {forumPosts.map((post) => (
              <div key={post.id} className="forum-post">
                <h4 className="post-title">{post.title}</h4>
                <p className="post-preview">{post.preview}</p>
                <div className="post-meta">
                  <span className="post-category">{post.category_name}</span>
                  <span className="post-stats">
                    👁 {post.view_count} • 💬 {post.reply_count} • 👍 {post.like_count}
                  </span>
                </div>
                <div className="post-author">
                  by @{post.author_username}
                </div>
              </div>
            ))}
            
            {/* Pagination */}
            <div className="pagination">
              <div className="pagination-controls">
                <button className="pagination-btn active">1</button>
                <button className="pagination-btn">2</button>
                <button className="pagination-btn">3</button>
                <span className="pagination-dots">...</span>
                <button className="pagination-btn">8</button>
                <button className="pagination-btn next">❯</button>
              </div>
              <div className="pagination-info">
                Showing 1-10 of 156 posts
              </div>
            </div>
          </div>

          <div className="recent-activity">
            <div className="activity-header">
              <i className="fas fa-clock"></i>
              <h3>Recent Activity</h3>
            </div>
            <div className="activity-items">
              {recentActivities.slice(0, 6).map((activity) => (
                <div key={activity.id} className="activity-item">
                  <span className="activity-user">@{activity.username}</span>
                  <span className="activity-action">{activity.title}</span>
                  <span className="activity-time">{formatTimeAgo(activity.created_at)}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="footer">
        <div className="footer-content">
          <span>Pratibimb v2.1 - Accessibility Innovation Platform | Powered by Infosys | © 2025 All Rights Reserved</span>
        </div>
      </div>
    </div>
  );
};

export default HomePage;

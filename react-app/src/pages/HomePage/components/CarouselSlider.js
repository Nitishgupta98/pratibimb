import React, { useState, useEffect } from 'react';
import './CarouselSlider.css';

const CarouselSlider = ({ slides = [] }) => {
  const [currentSlide, setCurrentSlide] = useState(0);
  const [isAutoPlaying, setIsAutoPlaying] = useState(true);

  // Auto-advance slides
  useEffect(() => {
    if (!isAutoPlaying || slides.length <= 1) return;

    const interval = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % slides.length);
    }, 5000);

    return () => clearInterval(interval);
  }, [currentSlide, isAutoPlaying, slides.length]);

  const goToSlide = (index) => {
    setCurrentSlide(index);
  };

  const goToPrevious = () => {
    setCurrentSlide((prev) => (prev - 1 + slides.length) % slides.length);
  };

  const goToNext = () => {
    setCurrentSlide((prev) => (prev + 1) % slides.length);
  };

  const handleMouseEnter = () => {
    setIsAutoPlaying(false);
  };

  const handleMouseLeave = () => {
    setIsAutoPlaying(true);
  };

  if (!slides || slides.length === 0) {
    return (
      <div className="carousel-container">
        <div className="carousel-empty">
          <i className="fas fa-images"></i>
          <p>No slides available</p>
        </div>
      </div>
    );
  }

  return (
    <div 
      className="carousel-container"
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      <div className="carousel-wrapper">
        <div 
          className="carousel-track"
          style={{ transform: `translateX(-${currentSlide * 100}%)` }}
        >
          {slides.map((slide, index) => (
            <div
              key={slide.id || index}
              className={`carousel-slide ${index === currentSlide ? 'active' : ''}`}
              style={{
                background: slide.background_gradient || 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
              }}
            >
              <div className="slide-content">
                <div className="slide-header">
                  <span className="slide-type">{slide.slide_type || 'News'}</span>
                  <span className="slide-date">
                    {slide.publish_date ? new Date(slide.publish_date).toLocaleDateString() : ''}
                  </span>
                </div>
                
                <h2 className="slide-title">{slide.title}</h2>
                <p className="slide-description">{slide.description}</p>
                
                {slide.link_url && slide.link_url !== '#' && (
                  <div className="slide-actions">
                    <a 
                      href={slide.link_url} 
                      className="slide-link btn btn-primary"
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      Read More
                      <i className="fas fa-arrow-right"></i>
                    </a>
                  </div>
                )}
              </div>
              
              {slide.image_url && (
                <div className="slide-image">
                  <img 
                    src={slide.image_url} 
                    alt={slide.title}
                    loading="lazy"
                  />
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Navigation Controls */}
        {slides.length > 1 && (
          <>
            <button 
              className="carousel-nav prev"
              onClick={goToPrevious}
              aria-label="Previous slide"
            >
              <i className="fas fa-chevron-left"></i>
            </button>
            
            <button 
              className="carousel-nav next"
              onClick={goToNext}
              aria-label="Next slide"
            >
              <i className="fas fa-chevron-right"></i>
            </button>
          </>
        )}

        {/* Indicators */}
        {slides.length > 1 && (
          <div className="carousel-indicators">
            {slides.map((_, index) => (
              <button
                key={index}
                className={`indicator ${index === currentSlide ? 'active' : ''}`}
                onClick={() => goToSlide(index)}
                aria-label={`Go to slide ${index + 1}`}
              />
            ))}
          </div>
        )}

        {/* Play/Pause Control */}
        {slides.length > 1 && (
          <button 
            className="carousel-play-pause"
            onClick={() => setIsAutoPlaying(!isAutoPlaying)}
            aria-label={isAutoPlaying ? 'Pause slideshow' : 'Play slideshow'}
          >
            <i className={`fas ${isAutoPlaying ? 'fa-pause' : 'fa-play'}`}></i>
          </button>
        )}
      </div>
    </div>
  );
};

export default CarouselSlider;

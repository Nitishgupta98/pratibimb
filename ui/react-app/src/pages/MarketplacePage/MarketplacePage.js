import React, { useState, useEffect } from 'react';
import './MarketplacePage.css';

const MarketplacePage = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [viewMode, setViewMode] = useState('grid');
  const [sortBy, setSortBy] = useState('popularity');
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [cart, setCart] = useState([]);
  const [favorites, setFavorites] = useState([]);

  const categories = [
    { id: 'all', name: 'All Products', count: 24 },
    { id: 'software', name: 'Software', count: 8 },
    { id: 'hardware', name: 'Hardware', count: 6 },
    { id: 'services', name: 'Services', count: 5 },
    { id: 'education', name: 'Education', count: 3 },
    { id: 'mobility', name: 'Mobility', count: 2 }
  ];

  const products = [
    {
      id: 'braas',
      title: 'BraaS - Braille as a Service',
      description: 'Professional Braille transcription services with quick turnaround. Convert any text to Grade 1 or Grade 2 Braille with expert accuracy.',
      vendor: 'Divya Jyothi Trust',
      category: 'services',
      price: 10,
      unit: '/page',
      location: 'Mysore, Karnataka',
      rating: 4.8,
      reviews: 156,
      icon: 'fas fa-braille',
      badge: 'Popular',
      features: ['Grade 1 & 2 Braille', 'Quick Turnaround', 'Expert Accuracy', 'Multiple Formats'],
      quantities: ['50 pages', '100 pages', '500 pages']
    },
    {
      id: 'screenreader',
      title: 'Advanced Screen Reader Pro',
      description: 'Powerful screen reading software with AI-enhanced voice synthesis, multi-language support, and advanced navigation features.',
      vendor: 'AccessTech Solutions',
      category: 'software',
      price: 1500,
      unit: '/license',
      location: 'Bangalore, Karnataka',
      rating: 4.5,
      reviews: 89,
      icon: 'fas fa-desktop',
      badge: 'Featured',
      features: ['AI Voice Synthesis', 'Multi-language Support', 'Advanced Navigation', 'OCR Integration'],
      quantities: ['Single License', '3 Licenses', '10 Licenses']
    },
    {
      id: 'brailledisplay',
      title: 'Professional Braille Display 40-Cell',
      description: 'High-quality 40-cell refreshable Braille display with USB and Bluetooth connectivity. Perfect for professional and educational use.',
      vendor: 'BrailleTech India',
      category: 'hardware',
      price: 25000,
      unit: '/unit',
      location: 'Delhi, India',
      rating: 4.7,
      reviews: 34,
      icon: 'fas fa-keyboard',
      badge: 'Premium',
      features: ['40 Cells', 'USB & Bluetooth', 'Cursor Routing', '2 Year Warranty'],
      quantities: ['1 Unit', '2 Units', '5 Units']
    },
    {
      id: 'voiceassistant',
      title: 'Smart Voice Assistant for Accessibility',
      description: 'Customizable voice assistant designed specifically for accessibility needs with smart home integration and daily task management.',
      vendor: 'VoiceTech Solutions',
      category: 'software',
      price: 800,
      unit: '/year',
      location: 'Bangalore, Karnataka',
      rating: 4.3,
      reviews: 67,
      icon: 'fas fa-microphone',
      badge: 'New',
      features: ['Smart Home Control', 'Task Management', 'Voice Customization', 'Accessibility Focus'],
      quantities: ['1 Year', '2 Years', '5 Years']
    },
    {
      id: 'tactilemaps',
      title: 'Tactile Map Creation Kit',
      description: 'Complete kit for creating tactile maps and diagrams with raised materials, perfect for educational institutions and training centers.',
      vendor: 'EduAccess Materials',
      category: 'education',
      price: 300,
      unit: '/kit',
      location: 'Mysore, Karnataka',
      rating: 4.6,
      reviews: 28,
      icon: 'fas fa-map',
      badge: 'Educational',
      features: ['Complete Kit', 'Multiple Materials', 'Educational Guide', 'Reusable'],
      quantities: ['Basic Kit', 'Standard Kit', 'Premium Kit']
    },
    {
      id: 'smartcane',
      title: 'AI-Powered Smart Navigation Cane',
      description: 'Advanced mobility aid with AI-powered obstacle detection, GPS navigation, and smartphone connectivity for enhanced independence.',
      vendor: 'MobilityFirst',
      category: 'mobility',
      price: 12000,
      unit: '/unit',
      location: 'Mumbai, Maharashtra',
      rating: 4.4,
      reviews: 45,
      icon: 'fas fa-walking',
      badge: 'Innovative',
      features: ['AI Obstacle Detection', 'GPS Navigation', 'Smartphone App', 'Rechargeable Battery'],
      quantities: ['1 Unit', '2 Units', '3 Units']
    }
  ];

  const filteredProducts = products.filter(product => {
    const matchesSearch = product.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         product.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || product.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const sortedProducts = [...filteredProducts].sort((a, b) => {
    switch (sortBy) {
      case 'price-low':
        return a.price - b.price;
      case 'price-high':
        return b.price - a.price;
      case 'rating':
        return b.rating - a.rating;
      case 'name':
        return a.title.localeCompare(b.title);
      default: // popularity
        return b.reviews - a.reviews;
    }
  });

  const addToCart = (productId) => {
    if (!cart.includes(productId)) {
      setCart([...cart, productId]);
    }
  };

  const toggleFavorite = (productId) => {
    if (favorites.includes(productId)) {
      setFavorites(favorites.filter(id => id !== productId));
    } else {
      setFavorites([...favorites, productId]);
    }
  };

  const showProductDetails = (productId) => {
    const product = products.find(p => p.id === productId);
    setSelectedProduct(product);
  };

  const closeProductDetails = () => {
    setSelectedProduct(null);
  };

  return (
    <div className="marketplace-page">
      <div className="marketplace-container">
        {/* Sidebar Filters */}
        <div className="marketplace-sidebar">
          <div className="sidebar-content">
            <div className="filter-section">
              <h3 className="filter-title">Categories</h3>
              <ul className="filter-options">
                {categories.map(category => (
                  <li 
                    key={category.id}
                    className={`filter-option ${selectedCategory === category.id ? 'active' : ''}`}
                    onClick={() => setSelectedCategory(category.id)}
                  >
                    <span>{category.name}</span>
                    <span className="filter-count">{category.count}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="filter-section">
              <h3 className="filter-title">Price Range</h3>
              <ul className="filter-options">
                <li className="filter-option">
                  <span>Under ₹1,000</span>
                  <span className="filter-count">8</span>
                </li>
                <li className="filter-option">
                  <span>₹1,000 - ₹5,000</span>
                  <span className="filter-count">6</span>
                </li>
                <li className="filter-option">
                  <span>₹5,000 - ₹15,000</span>
                  <span className="filter-count">4</span>
                </li>
                <li className="filter-option">
                  <span>Above ₹15,000</span>
                  <span className="filter-count">6</span>
                </li>
              </ul>
            </div>

            <div className="filter-section">
              <h3 className="filter-title">Location</h3>
              <ul className="filter-options">
                <li className="filter-option">
                  <span>Bangalore</span>
                  <span className="filter-count">12</span>
                </li>
                <li className="filter-option">
                  <span>Delhi</span>
                  <span className="filter-count">6</span>
                </li>
                <li className="filter-option">
                  <span>Mumbai</span>
                  <span className="filter-count">4</span>
                </li>
                <li className="filter-option">
                  <span>Mysore</span>
                  <span className="filter-count">2</span>
                </li>
              </ul>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="marketplace-main">
          {/* Header */}
          <div className="marketplace-header">
            <div className="marketplace-title">
              <i className="fas fa-store"></i>
              Accessibility Store
            </div>
            <p className="marketplace-subtitle">
              Discover and purchase accessibility products and services from trusted vendors across India
            </p>
            <div className="beckn-badge">
              <i className="fas fa-network-wired"></i>
              Powered by Beckn Protocol
            </div>
            
            {/* Search and Controls */}
            <div className="search-controls">
              <div className="search-wrapper">
                <input
                  type="text"
                  className="search-input"
                  placeholder="Search products, services, vendors..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
                <button className="search-btn">
                  <i className="fas fa-search"></i>
                </button>
              </div>
              
              <div className="view-toggle">
                <button 
                  className={`view-btn ${viewMode === 'grid' ? 'active' : ''}`}
                  onClick={() => setViewMode('grid')}
                >
                  <i className="fas fa-th"></i>
                </button>
                <button 
                  className={`view-btn ${viewMode === 'list' ? 'active' : ''}`}
                  onClick={() => setViewMode('list')}
                >
                  <i className="fas fa-list"></i>
                </button>
              </div>
              
              <select 
                className="sort-select"
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
              >
                <option value="popularity">Most Popular</option>
                <option value="rating">Highest Rated</option>
                <option value="price-low">Price: Low to High</option>
                <option value="price-high">Price: High to Low</option>
                <option value="name">Name A-Z</option>
              </select>
            </div>
          </div>

          {/* Products Grid */}
          <div className="marketplace-content">
            <div className="products-header">
              <div className="products-count">
                Showing <span>{sortedProducts.length}</span> of <span>{products.length}</span> products
              </div>
            </div>

            <div className={`products-grid ${viewMode}`}>
              {sortedProducts.map(product => (
                <div 
                  key={product.id}
                  className="product-card"
                  onClick={() => showProductDetails(product.id)}
                >
                  <div className="product-image">
                    <i className={product.icon}></i>
                    <div className="product-badge">{product.badge}</div>
                  </div>
                  <div className="product-info">
                    <div className="product-vendor">
                      <i className="fas fa-store"></i>
                      {product.vendor}
                    </div>
                    <h3 className="product-title">{product.title}</h3>
                    <p className="product-description">{product.description}</p>
                    <div className="product-location">
                      <i className="fas fa-map-marker-alt"></i>
                      {product.location}
                    </div>
                    <div className="product-rating">
                      <span className="stars">
                        {'★'.repeat(Math.floor(product.rating))}
                        {product.rating % 1 !== 0 && '☆'}
                      </span>
                      <span className="rating-text">{product.rating} ({product.reviews})</span>
                    </div>
                    <div className="product-price">
                      <span className="currency">₹</span>
                      {product.price.toLocaleString()}
                      <span className="unit">{product.unit}</span>
                    </div>
                    <button 
                      className="view-details-btn"
                      onClick={(e) => {
                        e.stopPropagation();
                        showProductDetails(product.id);
                      }}
                    >
                      <i className="fas fa-info-circle"></i> View Details
                    </button>
                    <div className="quantity-selector">
                      <div className="quantity-label">Select quantity:</div>
                      <div className="quantity-options">
                        {product.quantities.map((qty, index) => (
                          <span 
                            key={index}
                            className={`quantity-option ${index === 0 ? 'selected' : ''}`}
                          >
                            {qty}
                          </span>
                        ))}
                      </div>
                    </div>
                    <div className="product-actions">
                      <button 
                        className="add-to-cart"
                        onClick={(e) => {
                          e.stopPropagation();
                          addToCart(product.id);
                        }}
                      >
                        <i className="fas fa-cart-plus"></i>
                        Add to Cart
                      </button>
                      <button 
                        className={`add-to-favorites ${favorites.includes(product.id) ? 'active' : ''}`}
                        onClick={(e) => {
                          e.stopPropagation();
                          toggleFavorite(product.id);
                        }}
                      >
                        <i className="fas fa-heart"></i>
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Product Details Modal */}
      {selectedProduct && (
        <div className="product-details-modal show">
          <div className="product-details-content">
            <div className="product-details-header">
              <h2>{selectedProduct.title}</h2>
              <button 
                className="product-details-close"
                onClick={closeProductDetails}
              >
                <i className="fas fa-times"></i>
              </button>
            </div>
            <div className="product-details-main">
              <div className="product-details-left">
                <div className="product-image-large">
                  <i className={selectedProduct.icon}></i>
                </div>
                <div className="product-vendor-info">
                  <h4>Vendor Information</h4>
                  <p><strong>{selectedProduct.vendor}</strong></p>
                  <p><i className="fas fa-map-marker-alt"></i> {selectedProduct.location}</p>
                  <div className="vendor-rating">
                    <span className="stars">
                      {'★'.repeat(Math.floor(selectedProduct.rating))}
                      {selectedProduct.rating % 1 !== 0 && '☆'}
                    </span>
                    <span>{selectedProduct.rating} ({selectedProduct.reviews} reviews)</span>
                  </div>
                </div>
              </div>
              <div className="product-details-right">
                <div className="product-description-full">
                  <h4>Description</h4>
                  <p>{selectedProduct.description}</p>
                </div>
                <div className="product-features">
                  <h4>Key Features</h4>
                  <ul>
                    {selectedProduct.features.map((feature, index) => (
                      <li key={index}>{feature}</li>
                    ))}
                  </ul>
                </div>
                <div className="product-pricing">
                  <h4>Pricing</h4>
                  <div className="price-display">
                    <span className="currency">₹</span>
                    <span className="price">{selectedProduct.price.toLocaleString()}</span>
                    <span className="unit">{selectedProduct.unit}</span>
                  </div>
                </div>
                <div className="product-actions-modal">
                  <button 
                    className="add-to-cart-modal"
                    onClick={() => addToCart(selectedProduct.id)}
                  >
                    <i className="fas fa-cart-plus"></i>
                    Add to Cart
                  </button>
                  <button 
                    className={`add-to-favorites-modal ${favorites.includes(selectedProduct.id) ? 'active' : ''}`}
                    onClick={() => toggleFavorite(selectedProduct.id)}
                  >
                    <i className="fas fa-heart"></i>
                    {favorites.includes(selectedProduct.id) ? 'Remove from Favorites' : 'Add to Favorites'}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MarketplacePage;

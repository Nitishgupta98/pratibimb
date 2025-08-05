import React, { useState, useEffect } from 'react';
import './BrailleAsaService.css';

const BrailleAsaService = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedLocation, setSelectedLocation] = useState('all');
  const [priceRange, setPriceRange] = useState([0, 5000]);
  const [sortBy, setSortBy] = useState('rating');
  const [cart, setCart] = useState([]);
  const [favorites, setFavorites] = useState([]);
  const [showProductDetails, setShowProductDetails] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [showCart, setShowCart] = useState(false);
  const [showFavorites, setShowFavorites] = useState(false);
  const [toast, setToast] = useState({ show: false, message: '' });

  // Sample products data
  const products = [
    {
      id: 'braas',
      title: 'BraaS - Braille as a Service',
      vendor: 'Divya Jyothi Trust',
      description: 'Professional Braille transcription services with quick turnaround. Convert any text to Grade 1 or Grade 2 Braille with expert accuracy.',
      location: 'Mysore, Karnataka',
      price: 10,
      priceUnit: '/page',
      rating: 4.8,
      reviews: 156,
      category: 'services',
      icon: 'fas fa-braille',
      badge: 'Popular',
      features: [
        'Professional Grade 1 and Grade 2 Braille conversion',
        '24-48 hour turnaround time',
        'Expert quality assurance',
        'Multiple format delivery options',
        'Custom formatting available'
      ]
    },
    {
      id: 'screenreader',
      title: 'Advanced Screen Reader Pro',
      vendor: 'AccessTech Solutions',
      description: 'Powerful screen reading software with AI-enhanced voice synthesis, multi-language support, and advanced navigation features.',
      location: 'Bangalore, Karnataka',
      price: 1500,
      priceUnit: '/license',
      rating: 4.5,
      reviews: 89,
      category: 'software',
      icon: 'fas fa-desktop',
      badge: 'Featured',
      features: [
        'AI-enhanced voice synthesis',
        'Multi-language support',
        'Advanced navigation features',
        'Regular updates included',
        '24/7 customer support'
      ]
    },
    {
      id: 'braille-display',
      title: 'Portable Braille Display',
      vendor: 'TechAccess India',
      description: 'Compact 20-cell Braille display with USB connectivity. Perfect for students and professionals on the go.',
      location: 'Delhi, India',
      price: 25000,
      priceUnit: '/unit',
      rating: 4.6,
      reviews: 45,
      category: 'hardware',
      icon: 'fas fa-keyboard',
      badge: 'New',
      features: [
        '20-cell refreshable Braille display',
        'USB and Bluetooth connectivity',
        'Lightweight and portable design',
        'Compatible with all major screen readers',
        '2-year warranty included'
      ]
    },
    {
      id: 'audio-books',
      title: 'Educational Audio Books Collection',
      vendor: 'Learning Resources Inc',
      description: 'Comprehensive collection of educational audio books for students. Covers curriculum from grades 1-12.',
      location: 'Mumbai, Maharashtra',
      price: 500,
      priceUnit: '/month',
      rating: 4.7,
      reviews: 203,
      category: 'content',
      icon: 'fas fa-headphones',
      badge: 'Best Seller',
      features: [
        'Complete curriculum coverage',
        'High-quality audio narration',
        'Multiple language options',
        'Offline listening capability',
        'Progress tracking included'
      ]
    },
    {
      id: 'magnifier',
      title: 'Digital Magnification Software',
      vendor: 'VisionAid Technologies',
      description: 'Advanced screen magnification software with customizable zoom levels, color filters, and reading modes.',
      location: 'Chennai, Tamil Nadu',
      price: 800,
      priceUnit: '/license',
      rating: 4.4,
      reviews: 67,
      category: 'software',
      icon: 'fas fa-search-plus',
      badge: 'Recommended',
      features: [
        'Up to 16x magnification',
        'Color and contrast enhancement',
        'Multiple reading modes',
        'Customizable settings',
        'Multi-monitor support'
      ]
    },
    {
      id: 'tactile-graphics',
      title: 'Tactile Graphics Printing Service',
      vendor: 'InclusivePrint Solutions',
      description: 'Professional tactile graphics and raised print services for educational materials, maps, and diagrams.',
      location: 'Pune, Maharashtra',
      price: 50,
      priceUnit: '/sheet',
      rating: 4.9,
      reviews: 124,
      category: 'services',
      icon: 'fas fa-print',
      badge: 'Premium',
      features: [
        'High-quality tactile graphics',
        'Educational material specialization',
        'Fast turnaround time',
        'Multiple paper options',
        'Custom design services'
      ]
    }
  ];

  const categories = [
    { value: 'all', label: 'All Categories' },
    { value: 'services', label: 'Services' },
    { value: 'software', label: 'Software' },
    { value: 'hardware', label: 'Hardware' },
    { value: 'content', label: 'Content' }
  ];

  const locations = [
    { value: 'all', label: 'All Locations' },
    { value: 'bangalore', label: 'Bangalore' },
    { value: 'mysore', label: 'Mysore' },
    { value: 'delhi', label: 'Delhi' },
    { value: 'mumbai', label: 'Mumbai' },
    { value: 'chennai', label: 'Chennai' },
    { value: 'pune', label: 'Pune' }
  ];

  // Filter products based on search and filters
  const filteredProducts = products.filter(product => {
    const matchesSearch = product.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         product.vendor.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         product.description.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesCategory = selectedCategory === 'all' || product.category === selectedCategory;
    
    const matchesLocation = selectedLocation === 'all' || 
                           product.location.toLowerCase().includes(selectedLocation.toLowerCase());
    
    const matchesPrice = product.price >= priceRange[0] && product.price <= priceRange[1];

    return matchesSearch && matchesCategory && matchesLocation && matchesPrice;
  });

  // Sort products
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
      default:
        return 0;
    }
  });

  const showToast = (message) => {
    setToast({ show: true, message });
    setTimeout(() => setToast({ show: false, message: '' }), 3000);
  };

  const addToCart = (product) => {
    if (!cart.find(item => item.id === product.id)) {
      setCart([...cart, { ...product, quantity: 1 }]);
      showToast('Item added to cart!');
    } else {
      showToast('Item already in cart!');
    }
  };

  const removeFromCart = (productId) => {
    setCart(cart.filter(item => item.id !== productId));
    showToast('Item removed from cart!');
  };

  const toggleFavorite = (product) => {
    if (favorites.find(item => item.id === product.id)) {
      setFavorites(favorites.filter(item => item.id !== product.id));
      showToast('Removed from favorites');
    } else {
      setFavorites([...favorites, product]);
      showToast('Added to favorites!');
    }
  };

  const openProductDetails = (product) => {
    setSelectedProduct(product);
    setShowProductDetails(true);
  };

  const renderStars = (rating) => {
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 !== 0;
    
    return '★'.repeat(fullStars) + (hasHalfStar ? '☆' : '') + '☆'.repeat(5 - Math.ceil(rating));
  };

  const calculateCartTotal = () => {
    return cart.reduce((total, item) => total + (item.price * item.quantity), 0);
  };

  const renderProductCard = (product) => (
    <div key={product.id} className="product-card" onClick={() => openProductDetails(product)}>
      <div className="product-image">
        <i className={product.icon}></i>
        {product.badge && <div className="product-badge">{product.badge}</div>}
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
          <span className="stars">{renderStars(product.rating)}</span>
          <span className="rating-text">{product.rating} ({product.reviews})</span>
        </div>
        <div className="product-price">
          <span className="currency">₹</span>{product.price.toLocaleString()}<span className="unit">{product.priceUnit}</span>
        </div>
        <div className="product-actions">
          <button 
            className="add-to-cart"
            onClick={(e) => {
              e.stopPropagation();
              addToCart(product);
            }}
          >
            <i className="fas fa-cart-plus"></i>
            Add to Cart
          </button>
          <button 
            className={`add-to-favorites ${favorites.find(item => item.id === product.id) ? 'favorited' : ''}`}
            onClick={(e) => {
              e.stopPropagation();
              toggleFavorite(product);
            }}
          >
            <i className="fas fa-heart"></i>
          </button>
        </div>
      </div>
    </div>
  );

  return (
    <div className="braas-marketplace">
      <div className="marketplace-header">
        <div className="page-title">
          <h1>🛒 BRaaS Marketplace</h1>
          <div className="page-subtitle">
            Braille as a Service - Find assistive technology products and services
          </div>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="search-filters-section">
        <div className="search-bar">
          <div className="search-input-container">
            <i className="fas fa-search"></i>
            <input
              type="text"
              className="search-input"
              placeholder="Search for assistive products, services, or vendors..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
        </div>

        <div className="filters-container">
          <div className="filter-group">
            <label>Category:</label>
            <select 
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
            >
              {categories.map(cat => (
                <option key={cat.value} value={cat.value}>{cat.label}</option>
              ))}
            </select>
          </div>

          <div className="filter-group">
            <label>Location:</label>
            <select 
              value={selectedLocation}
              onChange={(e) => setSelectedLocation(e.target.value)}
            >
              {locations.map(loc => (
                <option key={loc.value} value={loc.value}>{loc.label}</option>
              ))}
            </select>
          </div>

          <div className="filter-group">
            <label>Sort by:</label>
            <select 
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
            >
              <option value="rating">Rating</option>
              <option value="price-low">Price: Low to High</option>
              <option value="price-high">Price: High to Low</option>
              <option value="name">Name A-Z</option>
            </select>
          </div>

          <div className="action-buttons">
            <button className="cart-btn" onClick={() => setShowCart(true)}>
              <i className="fas fa-shopping-cart"></i>
              Cart ({cart.length})
            </button>
            <button className="favorites-btn" onClick={() => setShowFavorites(true)}>
              <i className="fas fa-heart"></i>
              Favorites ({favorites.length})
            </button>
          </div>
        </div>
      </div>

      {/* Products Grid */}
      <div className="products-section">
        <div className="products-header">
          <div className="products-count">
            Showing {sortedProducts.length} of {products.length} products
          </div>
        </div>

        <div className="products-grid">
          {sortedProducts.map(renderProductCard)}
        </div>

        {sortedProducts.length === 0 && (
          <div className="no-products">
            <i className="fas fa-search" style={{fontSize: '3em', color: '#ccc', marginBottom: '20px'}}></i>
            <h3>No products found</h3>
            <p>Try adjusting your search terms or filters</p>
          </div>
        )}
      </div>

      {/* Product Details Modal */}
      {showProductDetails && selectedProduct && (
        <div className="modal show" onClick={() => setShowProductDetails(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2 className="modal-title">Product Details</h2>
              <button className="close-modal" onClick={() => setShowProductDetails(false)}>
                <i className="fas fa-times"></i>
              </button>
            </div>
            <div className="modal-body">
              <div className="product-details">
                <div className="product-details-left">
                  <div className="product-details-image">
                    <i className={selectedProduct.icon}></i>
                  </div>
                </div>
                <div className="product-details-right">
                  <h3 className="product-details-title">{selectedProduct.title}</h3>
                  <div className="product-details-vendor">
                    <i className="fas fa-store"></i>
                    {selectedProduct.vendor}
                  </div>
                  <div className="product-details-rating">
                    <span className="stars">{renderStars(selectedProduct.rating)}</span>
                    <span>{selectedProduct.rating} ({selectedProduct.reviews} reviews)</span>
                  </div>
                  <div className="product-details-price">₹{selectedProduct.price.toLocaleString()}{selectedProduct.priceUnit}</div>
                  <div className="product-details-description">
                    {selectedProduct.description}
                  </div>
                  <div className="product-details-features">
                    <h4>Key Features</h4>
                    <ul>
                      {selectedProduct.features.map((feature, index) => (
                        <li key={index}>{feature}</li>
                      ))}
                    </ul>
                  </div>
                  <div className="product-details-actions">
                    <button className="add-to-cart" onClick={() => addToCart(selectedProduct)}>
                      <i className="fas fa-cart-plus"></i>
                      Add to Cart
                    </button>
                    <button 
                      className={`add-to-favorites ${favorites.find(item => item.id === selectedProduct.id) ? 'favorited' : ''}`}
                      onClick={() => toggleFavorite(selectedProduct)}
                    >
                      <i className="fas fa-heart"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Cart Modal */}
      {showCart && (
        <div className="modal show" onClick={() => setShowCart(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2 className="modal-title">Shopping Cart</h2>
              <button className="close-modal" onClick={() => setShowCart(false)}>
                <i className="fas fa-times"></i>
              </button>
            </div>
            <div className="modal-body">
              {cart.length === 0 ? (
                <p style={{textAlign: 'center', color: '#666', padding: '40px'}}>Your cart is empty</p>
              ) : (
                <>
                  {cart.map(item => (
                    <div key={item.id} className="cart-item">
                      <div className="cart-item-info">
                        <h4>{item.title}</h4>
                        <p>{item.vendor}</p>
                        <div className="cart-item-price">₹{item.price.toLocaleString()}{item.priceUnit}</div>
                      </div>
                      <button className="remove-item" onClick={() => removeFromCart(item.id)}>
                        <i className="fas fa-trash"></i>
                      </button>
                    </div>
                  ))}
                  <div className="cart-total">
                    <div className="total-amount">Total: ₹{calculateCartTotal().toLocaleString()}</div>
                    <button className="checkout-btn">
                      <i className="fas fa-credit-card"></i>
                      Proceed to Checkout
                    </button>
                  </div>
                </>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Favorites Modal */}
      {showFavorites && (
        <div className="modal show" onClick={() => setShowFavorites(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2 className="modal-title">My Favorites</h2>
              <button className="close-modal" onClick={() => setShowFavorites(false)}>
                <i className="fas fa-times"></i>
              </button>
            </div>
            <div className="modal-body">
              {favorites.length === 0 ? (
                <p style={{textAlign: 'center', color: '#666', padding: '40px'}}>No favorites added yet</p>
              ) : (
                favorites.map(item => (
                  <div key={item.id} className="favorite-item" onClick={() => openProductDetails(item)}>
                    <div className="favorite-item-info">
                      <h4>{item.title}</h4>
                      <p>{item.vendor}</p>
                      <div className="favorite-item-price">₹{item.price.toLocaleString()}{item.priceUnit}</div>
                    </div>
                    <button 
                      className="remove-favorite" 
                      onClick={(e) => {
                        e.stopPropagation();
                        toggleFavorite(item);
                      }}
                    >
                      <i className="fas fa-heart-broken"></i>
                    </button>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      )}

      {/* Toast Notification */}
      {toast.show && (
        <div className="toast">
          <div className="toast-content">
            <i className="fas fa-check-circle toast-icon"></i>
            <span>{toast.message}</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default BrailleAsaService;

import React, { useState } from 'react';
import './CommunityPage.css';

const CommunityPage = () => {
  const [selectedProject, setSelectedProject] = useState(null);
  const [showAddProject, setShowAddProject] = useState(false);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  const quickLinks = [
    {
      id: 'latest-projects',
      title: 'Latest Projects',
      icon: 'fas fa-clock',
      href: '#latest'
    },
    {
      id: 'popular-projects',
      title: 'Popular Projects',
      icon: 'fas fa-fire',
      href: '#popular'
    },
    {
      id: 'beginner-friendly',
      title: 'Beginner Friendly',
      icon: 'fas fa-star',
      href: '#beginner'
    },
    {
      id: 'hardware-projects',
      title: 'Hardware Projects',
      icon: 'fas fa-microchip',
      href: '#hardware'
    },
    {
      id: 'software-projects',
      title: 'Software Projects',
      icon: 'fas fa-code',
      href: '#software'
    },
    {
      id: 'mobile-apps',
      title: 'Mobile Apps',
      icon: 'fas fa-mobile-alt',
      href: '#mobile'
    },
    {
      id: 'tutorials',
      title: 'Tutorials & Guides',
      icon: 'fas fa-book',
      href: '#tutorials'
    },
    {
      id: 'community-forum',
      title: 'Community Forum',
      icon: 'fas fa-comments',
      href: '#forum'
    }
  ];

  const projects = [
    {
      id: 'braille-keyboard',
      title: 'Convert Regular Keyboard to Braille-Enabled',
      description: 'Transform any standard keyboard into a braille-accessible device using tactile stickers and simple modifications. Perfect for beginners and cost-effective solution.',
      icon: '⌨️',
      difficulty: 'Easy',
      maker: {
        name: 'Arjun Singh',
        avatar: 'AS',
        location: 'Mumbai, India'
      },
      rating: 4.8,
      tags: ['Hardware', 'Beginner', 'Low Cost'],
      stats: {
        cost: '₹500',
        time: '2 hrs',
        made: '1.2k'
      },
      features: [
        'Tactile braille stickers for keys',
        'Simple installation process',
        'Compatible with any keyboard',
        'Cost-effective solution',
        'No technical expertise required'
      ],
      materials: [
        'Tactile braille stickers (₹200)',
        'Cleaning supplies (₹50)',
        'Installation guide (Free)',
        'Basic tools (₹250)'
      ],
      steps: [
        'Clean the keyboard thoroughly',
        'Plan the braille layout',
        'Apply tactile stickers carefully',
        'Test the tactile feedback',
        'Fine-tune positioning'
      ]
    },
    {
      id: 'audio-reader',
      title: 'DIY Audio Book Reader with Voice Control',
      description: 'Build a portable audio book reader using Raspberry Pi with voice commands, bookmark features, and speed control for enhanced reading experience.',
      icon: '📖',
      difficulty: 'Medium',
      maker: {
        name: 'Priya Kumar',
        avatar: 'PK',
        location: 'Delhi, India'
      },
      rating: 4.6,
      tags: ['Electronics', 'Programming', 'Medium'],
      stats: {
        cost: '₹3500',
        time: '6 hrs',
        made: '850'
      },
      features: [
        'Voice command recognition',
        'Automatic bookmarking',
        'Variable playback speed',
        'Large button interface',
        'Battery powered operation'
      ],
      materials: [
        'Raspberry Pi 4 (₹2000)',
        'MicroSD Card 32GB (₹400)',
        'USB Speaker (₹300)',
        'Microphone Module (₹200)',
        'Push Buttons (₹150)',
        'Enclosure Box (₹300)',
        'Wiring & Connectors (₹150)'
      ],
      steps: [
        'Set up Raspberry Pi OS',
        'Install audio and voice libraries',
        'Wire the hardware components',
        'Program voice recognition',
        'Create user interface',
        'Test and calibrate system'
      ]
    },
    {
      id: 'tactile-map',
      title: 'DIY Tactile Map Creator',
      description: 'Create raised tactile maps using affordable materials like foam board, fabric, and textured elements for educational and navigation purposes.',
      icon: '🗺️',
      difficulty: 'Easy',
      maker: {
        name: 'Ravi Mehta',
        avatar: 'RM',
        location: 'Pune, India'
      },
      rating: 4.7,
      tags: ['Education', 'Craft', 'Easy'],
      stats: {
        cost: '₹800',
        time: '3 hrs',
        made: '650'
      },
      features: [
        'Various texture materials',
        'Layered elevation design',
        'Braille labeling system',
        'Durable construction',
        'Customizable layouts'
      ],
      materials: [
        'Foam Board Sheets (₹300)',
        'Textured Fabrics (₹200)',
        'Adhesive Materials (₹150)',
        'Braille Label Maker (₹150)'
      ],
      steps: [
        'Plan the map layout',
        'Create base layer',
        'Add textured elements',
        'Install braille labels',
        'Test tactile clarity'
      ]
    },
    {
      id: 'smart-cane',
      title: 'Arduino-Based Smart Navigation Cane',
      description: 'Build an intelligent walking cane with ultrasonic sensors, vibration feedback, and obstacle detection to enhance mobility independence.',
      icon: '🦯',
      difficulty: 'Hard',
      maker: {
        name: 'Dr. Anjali Patel',
        avatar: 'AP',
        location: 'Ahmedabad, India'
      },
      rating: 4.9,
      tags: ['Electronics', 'Mobility', 'Advanced'],
      stats: {
        cost: '₹2500',
        time: '8 hrs',
        made: '420'
      },
      features: [
        'Ultrasonic obstacle detection',
        'Vibration feedback system',
        'Adjustable sensitivity',
        'Long battery life',
        'Waterproof design'
      ],
      materials: [
        'Arduino Nano (₹500)',
        'Ultrasonic Sensors HC-SR04 (₹400)',
        'Vibration Motors (₹300)',
        'Battery Pack (₹350)',
        'Aluminum Cane (₹600)',
        'Waterproof Enclosure (₹250)',
        'Wiring Components (₹100)'
      ],
      steps: [
        'Design circuit schematic',
        'Program Arduino controller',
        'Install sensors on cane',
        'Configure vibration feedback',
        'Waterproof electronics',
        'Calibrate detection range',
        'Field testing and adjustment'
      ]
    }
  ];

  const showProjectDetails = (projectId) => {
    const project = projects.find(p => p.id === projectId);
    setSelectedProject(project);
  };

  const closeProjectDetails = () => {
    setSelectedProject(null);
  };

  const toggleAddProject = () => {
    setShowAddProject(!showAddProject);
  };

  const toggleSidebar = () => {
    setSidebarCollapsed(!sidebarCollapsed);
  };

  return (
    <div className="community-page">
      <div className="main-content">
        {/* Quick Links Sidebar */}
        <div className={`quick-links ${sidebarCollapsed ? 'collapsed' : ''}`}>
          <h3>
            <span className="sidebar-text">Quick Links</span>
            <button className="hamburger-toggle" onClick={toggleSidebar}>
              <i className={`fas ${sidebarCollapsed ? 'fa-chevron-right' : 'fa-chevron-left'}`}></i>
            </button>
          </h3>
          {quickLinks.map(link => (
            <a key={link.id} href={link.href} className="quick-link">
              <i className={`quick-link-icon ${link.icon}`}></i>
              <span className="quick-link-text">{link.title}</span>
            </a>
          ))}
        </div>

        {/* Main Content Area */}
        <div className={`content-area ${sidebarCollapsed ? 'expanded' : ''}`}>
          {/* Welcome Section */}
          <div className="welcome-section">
            <h1>
              <i className="fas fa-users"></i>
              Community Hub
            </h1>
            <p>
              Join our vibrant community of makers, developers, and accessibility advocates. 
              Share your DIY projects, learn from others, and contribute to making technology more accessible for everyone.
            </p>
            <div className="community-stats">
              <div className="stat-item">
                <span className="stat-number">2,847</span>
                <span className="stat-label">Community Members</span>
              </div>
              <div className="stat-item">
                <span className="stat-number">156</span>
                <span className="stat-label">Active Projects</span>
              </div>
              <div className="stat-item">
                <span className="stat-number">89</span>
                <span className="stat-label">Contributors</span>
              </div>
              <div className="stat-item">
                <span className="stat-number">340</span>
                <span className="stat-label">Completed Builds</span>
              </div>
            </div>
          </div>

          {/* DIY Projects Section */}
          <div className="projects-section">
            <div className="section-header">
              <h2 className="section-title">DIY Accessibility Projects</h2>
              <button className="add-project-btn" onClick={toggleAddProject}>
                <span>➕</span> Add New Project
              </button>
            </div>

            <div className="projects-grid">
              {projects.map(project => (
                <div 
                  key={project.id}
                  className="project-card"
                  onClick={() => showProjectDetails(project.id)}
                >
                  <div className="project-image">
                    <span className="project-emoji">{project.icon}</span>
                    <div className={`project-difficulty ${project.difficulty.toLowerCase()}`}>
                      {project.difficulty}
                    </div>
                  </div>
                  <div className="project-content">
                    <h3 className="project-title">{project.title}</h3>
                    <p className="project-description">{project.description}</p>
                    <div className="project-meta">
                      <div className="project-maker">
                        <div className="maker-avatar">{project.maker.avatar}</div>
                        <span>{project.maker.name} • {project.maker.location}</span>
                      </div>
                      <div className="project-rating">
                        <span className="stars">
                          {'★'.repeat(Math.floor(project.rating))}
                          {project.rating % 1 !== 0 && '☆'}
                        </span>
                        <span>({project.rating})</span>
                      </div>
                    </div>
                    <div className="project-tags">
                      {project.tags.map((tag, index) => (
                        <span key={index} className="project-tag">{tag}</span>
                      ))}
                    </div>
                    <div className="project-stats">
                      <div className="stat">
                        <span className="stat-number">{project.stats.cost}</span>
                        <span>Est. Cost</span>
                      </div>
                      <div className="stat">
                        <span className="stat-number">{project.stats.time}</span>
                        <span>Time Needed</span>
                      </div>
                      <div className="stat">
                        <span className="stat-number">{project.stats.made}</span>
                        <span>Made This</span>
                      </div>
                    </div>
                    <button className="view-project-btn">View Project</button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Project Details Modal */}
      {selectedProject && (
        <div className="modal show">
          <div className="modal-content">
            <div className="modal-header">
              <h2 className="modal-title">{selectedProject.title}</h2>
              <button className="close-modal" onClick={closeProjectDetails}>
                <i className="fas fa-times"></i>
              </button>
            </div>
            <div className="modal-body">
              <div className="project-overview">
                <div className="project-icon-large">
                  <span>{selectedProject.icon}</span>
                </div>
                <div className="project-meta-detailed">
                  <div className="difficulty-badge">
                    <span className={`difficulty ${selectedProject.difficulty.toLowerCase()}`}>
                      {selectedProject.difficulty}
                    </span>
                  </div>
                  <div className="maker-info">
                    <div className="maker-avatar-large">{selectedProject.maker.avatar}</div>
                    <div>
                      <strong>{selectedProject.maker.name}</strong>
                      <p>{selectedProject.maker.location}</p>
                    </div>
                  </div>
                  <div className="project-rating-large">
                    <span className="stars">
                      {'★'.repeat(Math.floor(selectedProject.rating))}
                      {selectedProject.rating % 1 !== 0 && '☆'}
                    </span>
                    <span>({selectedProject.rating})</span>
                  </div>
                </div>
              </div>

              <div className="info-section">
                <h3 className="info-title">
                  <i className="fas fa-info-circle"></i>
                  Project Description
                </h3>
                <p className="info-content">{selectedProject.description}</p>
              </div>

              <div className="info-section">
                <h3 className="info-title">
                  <i className="fas fa-star"></i>
                  Key Features
                </h3>
                <ul className="info-list">
                  {selectedProject.features.map((feature, index) => (
                    <li key={index}>{feature}</li>
                  ))}
                </ul>
              </div>

              <div className="info-section">
                <h3 className="info-title">
                  <i className="fas fa-shopping-cart"></i>
                  Materials Needed
                </h3>
                <ul className="info-list">
                  {selectedProject.materials.map((material, index) => (
                    <li key={index}>{material}</li>
                  ))}
                </ul>
              </div>

              <div className="info-section">
                <h3 className="info-title">
                  <i className="fas fa-list-ol"></i>
                  Build Steps
                </h3>
                <ol className="info-list numbered">
                  {selectedProject.steps.map((step, index) => (
                    <li key={index}>{step}</li>
                  ))}
                </ol>
              </div>

              <div className="modal-actions">
                <button className="btn-primary">
                  <i className="fas fa-heart"></i>
                  Save Project
                </button>
                <button className="btn-secondary">
                  <i className="fas fa-share"></i>
                  Share
                </button>
                <button className="btn-accent">
                  <i className="fas fa-comments"></i>
                  Join Discussion
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Add Project Modal */}
      {showAddProject && (
        <div className="modal show">
          <div className="modal-content">
            <div className="modal-header">
              <h2 className="modal-title">Add New Project</h2>
              <button className="close-modal" onClick={toggleAddProject}>
                <i className="fas fa-times"></i>
              </button>
            </div>
            <div className="modal-body">
              <form className="add-project-form">
                <div className="form-group">
                  <label htmlFor="project-title">Project Title</label>
                  <input 
                    type="text" 
                    id="project-title"
                    placeholder="Enter your project title"
                    required
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="project-description">Description</label>
                  <textarea 
                    id="project-description"
                    rows="4"
                    placeholder="Describe your project and its accessibility benefits"
                    required
                  ></textarea>
                </div>
                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="project-difficulty">Difficulty Level</label>
                    <select id="project-difficulty" required>
                      <option value="">Select difficulty</option>
                      <option value="easy">Easy</option>
                      <option value="medium">Medium</option>
                      <option value="hard">Hard</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label htmlFor="project-cost">Estimated Cost (₹)</label>
                    <input 
                      type="number" 
                      id="project-cost"
                      placeholder="0"
                      min="0"
                    />
                  </div>
                </div>
                <div className="form-group">
                  <label htmlFor="project-tags">Tags (comma separated)</label>
                  <input 
                    type="text" 
                    id="project-tags"
                    placeholder="e.g., Hardware, Beginner, Low Cost"
                  />
                </div>
                <div className="form-actions">
                  <button type="submit" className="btn-primary">
                    <i className="fas fa-plus"></i>
                    Add Project
                  </button>
                  <button type="button" className="btn-secondary" onClick={toggleAddProject}>
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CommunityPage;

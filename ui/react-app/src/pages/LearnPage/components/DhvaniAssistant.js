import React, { useState } from 'react';
import './DhvaniAssistant.css';

const DhvaniAssistant = () => {
  const [activeTab, setActiveTab] = useState('opensource');
  const [cart, setCart] = useState([]);
  const [selectedTarget, setSelectedTarget] = useState('');
  const [selectedStudents, setSelectedStudents] = useState([]);
  const [showAssignModal, setShowAssignModal] = useState(false);
  const [currentDeviceToAssign, setCurrentDeviceToAssign] = useState(null);
  const [message, setMessage] = useState({ type: '', text: '', show: false });

  // Open Source Audiobooks Data
  const openSourceAudiobooks = [
    {
      id: 'great-gatsby',
      title: 'The Great Gatsby',
      author: 'F. Scott Fitzgerald',
      duration: '4h 32m',
      cover: '📚',
      type: 'audio',
      source: 'opensource'
    },
    {
      id: 'pride-prejudice',
      title: 'Pride and Prejudice',
      author: 'Jane Austen',
      duration: '11h 5m',
      cover: '📚',
      type: 'audio',
      source: 'opensource'
    },
    {
      id: 'alice-wonderland',
      title: 'Alice\'s Adventures in Wonderland',
      author: 'Lewis Carroll',
      duration: '2h 45m',
      cover: '📘',
      type: 'audio',
      source: 'opensource'
    },
    {
      id: 'sherlock-holmes',
      title: 'The Adventures of Sherlock Holmes',
      author: 'Arthur Conan Doyle',
      duration: '8h 20m',
      cover: '📕',
      type: 'audio',
      source: 'opensource'
    },
    {
      id: 'frankenstein',
      title: 'Frankenstein',
      author: 'Mary Shelley',
      duration: '6h 15m',
      cover: '📗',
      type: 'audio',
      source: 'opensource'
    },
    {
      id: 'time-machine',
      title: 'The Time Machine',
      author: 'H.G. Wells',
      duration: '3h 12m',
      cover: '📙',
      type: 'audio',
      source: 'opensource'
    }
  ];

  // Local Audio Files Data
  const localAudioFiles = [
    {
      id: 'math-basics',
      title: 'Mathematics Fundamentals',
      author: 'Dr. Learning Series',
      duration: '4h 25m',
      cover: '📐',
      type: 'audio'
    },
    {
      id: 'science-experiments',
      title: 'Science Experiments for Kids',
      author: 'Young Scientists',
      duration: '3h 15m',
      cover: '🔬',
      type: 'transcript'
    },
    {
      id: 'history-india',
      title: 'History of India',
      author: 'Historical Chronicles',
      duration: '5h 40m',
      cover: '🏛️',
      type: 'transcript'
    },
    {
      id: 'english-classics',
      title: 'English Literature Classics',
      author: 'Classic Authors',
      duration: '6h 10m',
      cover: '🎭',
      type: 'audio'
    },
    {
      id: 'geography',
      title: 'Geography Lessons',
      author: 'World Knowledge Series',
      duration: '2h 55m',
      cover: '🌍',
      type: 'transcript'
    }
  ];

  // Devices Data
  const devices = [
    {
      id: '001',
      model: 'DH-Pro-2024',
      status: 'assigned',
      student: {
        name: 'Arjun Sharma',
        age: 12,
        grade: '7th Standard',
        language: 'Hindi/English',
        school: 'Delhi Public School',
        deviceAge: '6 months'
      }
    },
    {
      id: '002',
      model: 'DH-Pro-2024',
      status: 'assigned',
      student: {
        name: 'Priya Patel',
        age: 10,
        grade: '5th Standard',
        language: 'Gujarati/Hindi',
        school: 'Delhi Public School',
        deviceAge: '3 months'
      }
    },
    {
      id: '003',
      model: 'DH-Standard-2024',
      status: 'unassigned'
    },
    {
      id: '004',
      model: 'DH-Standard-2024',
      status: 'unassigned'
    },
    {
      id: '005',
      model: 'DH-Pro-2024',
      status: 'assigned',
      student: {
        name: 'Rahul Kumar',
        age: 14,
        grade: '9th Standard',
        language: 'Hindi/English',
        school: 'Delhi Public School',
        deviceAge: '1 year'
      }
    },
    {
      id: '006',
      model: 'DH-Lite-2024',
      status: 'unassigned'
    }
  ];

  // Students Data
  const students = [
    { id: 1, name: 'Arjun Sharma', grade: '7th', device: '001' },
    { id: 2, name: 'Priya Patel', grade: '5th', device: '002' },
    { id: 3, name: 'Rahul Kumar', grade: '9th', device: '005' },
    { id: 4, name: 'Anita Singh', grade: '6th', device: null },
    { id: 5, name: 'Karan Mehta', grade: '8th', device: null }
  ];

  const showMessage = (type, text) => {
    setMessage({ type, text, show: true });
    setTimeout(() => {
      setMessage({ type: '', text: '', show: false });
    }, 5000);
  };

  const playAudio = (audiobook) => {
    showMessage('success', `Playing "${audiobook.title}" by ${audiobook.author}`);
  };

  const addToCart = (audiobook) => {
    if (!cart.find(item => item.id === audiobook.id)) {
      setCart([...cart, audiobook]);
      showMessage('success', `"${audiobook.title}" added to cart successfully!`);
    } else {
      showMessage('error', `"${audiobook.title}" is already in cart.`);
    }
  };

  const removeFromCart = (id) => {
    setCart(cart.filter(item => item.id !== id));
    showMessage('success', 'Item removed from cart.');
  };

  const clearCart = () => {
    setCart([]);
    showMessage('success', 'Cart cleared successfully.');
  };

  const assignDevice = (deviceId) => {
    setCurrentDeviceToAssign(deviceId);
    setShowAssignModal(true);
  };

  const confirmAssignment = () => {
    const selectedStudent = document.querySelector('input[name="assignStudent"]:checked');
    if (selectedStudent) {
      showMessage('success', `Device #${currentDeviceToAssign} assigned successfully to selected student.`);
      setShowAssignModal(false);
    } else {
      showMessage('error', 'Please select a student to assign the device to.');
    }
  };

  const reassignDevice = (deviceId) => {
    if (window.confirm(`Are you sure you want to reassign Device #${deviceId}? This will unassign it from the current student.`)) {
      showMessage('success', `Device #${deviceId} is now available for reassignment.`);
    }
  };

  const pushContentToDevice = (deviceId) => {
    if (cart.length === 0) {
      showMessage('error', 'Please add content to cart before pushing.');
      return;
    }
    
    const confirmed = window.confirm(`Push ${cart.length} content item(s) to Device #${deviceId}?`);
    if (confirmed) {
      showMessage('success', `Content pushed successfully to Device #${deviceId}!`);
      setCart([]);
    }
  };

  const pushContentToDevices = () => {
    if (!selectedTarget) return;
    
    let targetMessage = '';
    if (selectedTarget === 'all') {
      targetMessage = 'all students in the school';
    } else if (selectedTarget === 'selected') {
      targetMessage = `${selectedStudents.length} selected student(s)`;
    } else {
      targetMessage = 'the selected device';
    }
    
    const confirmed = window.confirm(`Push ${cart.length} content item(s) to ${targetMessage}?`);
    if (confirmed) {
      showMessage('success', `Content pushed successfully to ${targetMessage}! Students will receive notifications on their devices.`);
      setCart([]);
      setSelectedTarget('');
      setSelectedStudents([]);
    }
  };

  const handleStudentSelection = (studentId, checked) => {
    if (checked) {
      setSelectedStudents([...selectedStudents, studentId]);
    } else {
      setSelectedStudents(selectedStudents.filter(id => id !== studentId));
    }
  };

  const renderOpenSourceAudiobooks = () => (
    <div className="content-section">
      <div className="audiobooks-grid">
        {openSourceAudiobooks.map(audiobook => (
          <div key={audiobook.id} className="audiobook-card">
            <div className="audiobook-header">
              <div className="audiobook-cover">{audiobook.cover}</div>
              <div className="audiobook-info">
                <div className="audiobook-title">{audiobook.title}</div>
                <div className="audiobook-author">{audiobook.author}</div>
              </div>
            </div>
            <div className="audiobook-meta">
              <div className="audiobook-duration">
                <i className="fas fa-clock"></i> {audiobook.duration}
              </div>
              <button 
                className="play-btn"
                onClick={() => playAudio(audiobook)}
              >
                <i className="fas fa-play"></i> Play
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderLocalAudioFiles = () => (
    <div className="content-section">
      <div className="section-header">
        <h3>📚 Local Audio Files & Transcripts</h3>
        <p>Available content for distribution to student devices</p>
      </div>
      <div className="audiobooks-grid">
        {localAudioFiles.map(audiobook => (
          <div key={audiobook.id} className="audiobook-card">
            <div className="audiobook-header">
              <div className="audiobook-cover">{audiobook.cover}</div>
              <div className="audiobook-info">
                <div className="audiobook-title">{audiobook.title}</div>
                <div className="audiobook-author">{audiobook.author}</div>
              </div>
            </div>
            <div className="audiobook-meta">
              <div className="audiobook-duration">
                <i className="fas fa-clock"></i> {audiobook.duration}
              </div>
              <button 
                className="add-btn"
                onClick={() => addToCart(audiobook)}
              >
                <i className="fas fa-plus"></i> Add to Cart
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderDeviceManagement = () => (
    <div className="content-section">
      <div className="section-header">
        <h3>📱 Device Management</h3>
        <p>Manage Dhvani devices and student assignments</p>
      </div>
      <div className="device-grid">
        {devices.map(device => (
          <div key={device.id} className={`device-card ${device.status}`}>
            <div className="device-header">
              <div className="device-info">
                <h3>Dhvani Device #{device.id}</h3>
                <div className="device-model">Model: {device.model}</div>
              </div>
              <div className={`device-status ${device.status}`}>
                {device.status === 'assigned' ? 'Assigned' : 'Unassigned'}
              </div>
            </div>
            
            {device.status === 'assigned' ? (
              <div className="student-info">
                <h4>📚 Student Information</h4>
                <div className="student-details">
                  <div className="detail-item">Name: <span className="detail-value">{device.student.name}</span></div>
                  <div className="detail-item">Age: <span className="detail-value">{device.student.age} years</span></div>
                  <div className="detail-item">Grade: <span className="detail-value">{device.student.grade}</span></div>
                  <div className="detail-item">Language: <span className="detail-value">{device.student.language}</span></div>
                  <div className="detail-item">School: <span className="detail-value">{device.student.school}</span></div>
                  <div className="detail-item">Device Age: <span className="detail-value">{device.student.deviceAge}</span></div>
                </div>
              </div>
            ) : (
              <div className="student-info">
                <h4>📋 Available for Assignment</h4>
                <p style={{color: '#666', fontSize: '0.9em', margin: '10px 0'}}>
                  This device is ready to be assigned to a student. Click below to assign it to an eligible student.
                </p>
              </div>
            )}
            
            <div className="device-actions">
              {device.status === 'assigned' ? (
                <>
                  <button 
                    className="btn btn-success"
                    onClick={() => pushContentToDevice(device.id)}
                  >
                    <i className="fas fa-upload"></i> Push Content
                  </button>
                  <button 
                    className="btn btn-warning"
                    onClick={() => reassignDevice(device.id)}
                  >
                    <i className="fas fa-user-edit"></i> Reassign
                  </button>
                </>
              ) : (
                <button 
                  className="btn btn-primary"
                  onClick={() => assignDevice(device.id)}
                >
                  <i className="fas fa-user-plus"></i> Assign Device
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderContentPush = () => (
    <div className="content-section">
      <div className="content-cart">
        <div className="cart-header">
          <div className="cart-title">
            <i className="fas fa-shopping-cart"></i>
            Content Cart ({cart.length})
          </div>
          {cart.length > 0 && (
            <button className="clear-cart" onClick={clearCart}>
              <i className="fas fa-trash"></i> Clear Cart
            </button>
          )}
        </div>
        
        <div className="cart-content">
          {cart.length === 0 ? (
            <div style={{textAlign: 'center', color: '#666', padding: '20px'}}>
              <i className="fas fa-shopping-cart" style={{fontSize: '2em', marginBottom: '10px', opacity: 0.5}}></i>
              <p>Your cart is empty. Add content from the Local Audio Files tab.</p>
            </div>
          ) : (
            cart.map(item => (
              <div key={item.id} className="content-item">
                <div className="content-info">
                  <div className="content-name">{item.title}</div>
                  <div className="content-type">Type: {item.type}</div>
                </div>
                <button 
                  className="remove-item"
                  onClick={() => removeFromCart(item.id)}
                >
                  <i className="fas fa-times"></i>
                </button>
              </div>
            ))
          )}
        </div>
      </div>

      {cart.length > 0 && (
        <div className="push-section">
          <div className="target-selection">
            <h4>🎯 Select Push Target</h4>
            <div className="target-options">
              <div className="target-option">
                <input
                  type="radio"
                  id="pushAll"
                  name="pushTarget"
                  value="all"
                  checked={selectedTarget === 'all'}
                  onChange={(e) => setSelectedTarget(e.target.value)}
                />
                <label htmlFor="pushAll">Push to all students in school</label>
              </div>
              <div className="target-option">
                <input
                  type="radio"
                  id="pushSelected"
                  name="pushTarget"
                  value="selected"
                  checked={selectedTarget === 'selected'}
                  onChange={(e) => setSelectedTarget(e.target.value)}
                />
                <label htmlFor="pushSelected">Push to selected students</label>
              </div>
            </div>

            {selectedTarget === 'selected' && (
              <div className="student-selector active">
                <h5>Select Students:</h5>
                <div className="student-list">
                  {students.map(student => (
                    <div key={student.id} className="student-checkbox">
                      <input
                        type="checkbox"
                        id={`student-${student.id}`}
                        checked={selectedStudents.includes(student.id)}
                        onChange={(e) => handleStudentSelection(student.id, e.target.checked)}
                      />
                      <label htmlFor={`student-${student.id}`}>
                        {student.name} ({student.grade})
                        {student.device && ` - Device #${student.device}`}
                      </label>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          <button 
            className="push-btn"
            disabled={!selectedTarget || (selectedTarget === 'selected' && selectedStudents.length === 0)}
            onClick={pushContentToDevices}
          >
            <i className="fas fa-paper-plane"></i> Push Content
          </button>
        </div>
      )}
    </div>
  );

  return (
    <div className="dhvani-assistant">
      <div className="dhvani-header">
        <div className="page-title">
          <h1><i className="fas fa-microphone"></i> Dhvani Assistant</h1>
          <div className="page-subtitle">
            AI-powered voice assistant for accessibility content delivery and device management
          </div>
        </div>
      </div>

      <div className="dhvani-tabs">
        <button 
          className={`dhvani-tab ${activeTab === 'opensource' ? 'active' : ''}`}
          onClick={() => setActiveTab('opensource')}
        >
          <i className="fas fa-book-open"></i> Open Source Audiobooks
        </button>
        <button 
          className={`dhvani-tab ${activeTab === 'local' ? 'active' : ''}`}
          onClick={() => setActiveTab('local')}
        >
          <i className="fas fa-folder"></i> Local Audio Files
        </button>
        <button 
          className={`dhvani-tab ${activeTab === 'devices' ? 'active' : ''}`}
          onClick={() => setActiveTab('devices')}
        >
          <i className="fas fa-mobile-alt"></i> Device Management
        </button>
        <button 
          className={`dhvani-tab ${activeTab === 'push' ? 'active' : ''}`}
          onClick={() => setActiveTab('push')}
        >
          <i className="fas fa-cloud-upload-alt"></i> Content Push
        </button>
      </div>

      <div className="dhvani-content">
        {activeTab === 'opensource' && renderOpenSourceAudiobooks()}
        {activeTab === 'local' && renderLocalAudioFiles()}
        {activeTab === 'devices' && renderDeviceManagement()}
        {activeTab === 'push' && renderContentPush()}
      </div>

      {/* Message Display */}
      {message.show && (
        <div className={`message ${message.type}`}>
          <div className="message-content">
            <i className={`fas ${message.type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}`}></i>
            <span>{message.text}</span>
          </div>
        </div>
      )}

      {/* Assignment Modal */}
      {showAssignModal && (
        <div className="modal show">
          <div className="modal-content">
            <div className="modal-header">
              <h3 className="modal-title">Assign Device #{currentDeviceToAssign}</h3>
              <button 
                className="close-modal"
                onClick={() => setShowAssignModal(false)}
              >
                ×
              </button>
            </div>
            <div className="modal-body">
              <p>Select a student to assign this device to:</p>
              <div className="student-selection">
                {students.filter(s => !s.device).map(student => (
                  <div key={student.id} className="student-radio">
                    <input
                      type="radio"
                      id={`assign-${student.id}`}
                      name="assignStudent"
                      value={student.id}
                    />
                    <label htmlFor={`assign-${student.id}`}>
                      {student.name} ({student.grade})
                    </label>
                  </div>
                ))}
              </div>
              <div className="modal-actions">
                <button className="btn btn-primary" onClick={confirmAssignment}>
                  Assign Device
                </button>
                <button className="btn btn-secondary" onClick={() => setShowAssignModal(false)}>
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default DhvaniAssistant;

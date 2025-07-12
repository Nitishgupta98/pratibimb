import React, { useState, useRef } from 'react';
import { Upload, File, X } from 'lucide-react';
import './FileUpload.css';

const FileUpload = ({ onFileUpload, isLoading, onFileSelect }) => {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const fileInputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFiles(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFiles(e.target.files[0]);
    }
  };

  const handleFiles = (file) => {
    // Check file type
    const allowedTypes = ['video/mp4', 'video/avi', 'video/mov', 'video/wmv', 'video/webm'];
    if (!allowedTypes.includes(file.type)) {
      alert('Please select a valid video file (MP4, AVI, MOV, WMV, WebM)');
      return;
    }

    // Check file size (max 100MB)
    const maxSize = 100 * 1024 * 1024; // 100MB
    if (file.size > maxSize) {
      alert('File size must be less than 100MB');
      return;
    }

    setSelectedFile(file);
    if (onFileSelect) {
      onFileSelect(file);
    }
  };

  const removeFile = () => {
    setSelectedFile(null);
    if (onFileSelect) {
      onFileSelect(null);
    }
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const openFileDialog = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="file-upload">
      <div
        className={`upload-area ${dragActive ? 'drag-active' : ''} ${selectedFile ? 'has-file' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={openFileDialog}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept="video/*"
          onChange={handleChange}
          style={{ display: 'none' }}
          disabled={isLoading}
        />
        
        {!selectedFile ? (
          <div className="upload-content">
            <Upload size={48} className="upload-icon" />
            <h3>Drop your video file here</h3>
            <p>or click to browse files</p>
            <div className="file-info">
              <p>Supported formats: MP4, AVI, MOV, WMV, WebM</p>
              <p>Maximum size: 100MB</p>
            </div>
          </div>
        ) : (
          <div className="file-preview">
            <div className="file-icon-container">
              <File size={32} />
            </div>
            <div className="file-details">
              <h4>{selectedFile.name}</h4>
              <p>{formatFileSize(selectedFile.size)}</p>
              <p className="file-type">{selectedFile.type}</p>
            </div>
            <button
              type="button"
              className="remove-file"
              onClick={(e) => {
                e.stopPropagation();
                removeFile();
              }}
              disabled={isLoading}
            >
              <X size={20} />
            </button>
          </div>
        )}
      </div>
      
      <div className="upload-notice">
        <p>⚠️ Note: Video file processing is coming soon. Please use YouTube URL for now.</p>
      </div>
    </div>
  );
};

export default FileUpload;

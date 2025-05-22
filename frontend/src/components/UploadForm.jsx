import React, { useState, useRef } from 'react';
import axios from 'axios';

const UploadForm = ({ onUploadSuccess }) => {
  const [files, setFiles] = useState([]);
  const [progress, setProgress] = useState(0);
  const [loading, setLoading] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileChange = (event) => {
    setFiles(Array.from(event.target.files));
  };

  const handleUpload = async () => {
    if (files.length === 0) {
      alert('Please select files to upload');
      return;
    }

    const formData = new FormData();
    files.forEach(file => formData.append('files', file));

    try {
      setLoading(true);
      setProgress(0);

      await axios.post('http://localhost:8000/api/upload/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          setProgress(percentCompleted);
        }
      });

      alert('Files uploaded successfully!');
      setFiles([]);
      setProgress(0);
      if (fileInputRef.current) fileInputRef.current.value = null;

      if (onUploadSuccess) onUploadSuccess();

    } catch (error) {
      console.error('Upload error:', error);
      alert('Upload failed! ' + (error.response?.data?.message || ''));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={containerStyle}>
      <h2 style={titleStyle}>Upload Documents</h2>
      <input
        type="file"
        multiple
        onChange={handleFileChange}
        ref={fileInputRef}
        style={inputStyle}
      />
      <button
        onClick={handleUpload}
        disabled={loading}
        style={buttonStyle}
      >
        {loading ? `Uploading... ${progress}%` : 'Upload'}
      </button>
    </div>
  );
};

const containerStyle = {
  backgroundColor: 'white',
  padding: '16px',
  borderRadius: '8px',
  boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
  maxWidth: '400px',
  margin: '20px auto',
  textAlign: 'center',
};

const titleStyle = {
  fontSize: '20px',
  fontWeight: '600',
  marginBottom: '12px',
};

const inputStyle = {
  marginBottom: '12px',
  width: '100%',
};

const buttonStyle = {
  padding: '10px 20px',
  backgroundColor: '#28a745',
  color: 'white',
  border: 'none',
  borderRadius: '4px',
  cursor: 'pointer',
  fontWeight: '600',
};

export default UploadForm;

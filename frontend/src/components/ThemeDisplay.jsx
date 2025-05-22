import React, { useState, useEffect } from 'react';
import axios from 'axios';

/**
 * Component to display and extract themes from multiple selected PDFs.
 * Fetches the list of uploaded documents on mount,
 * allows multi-selection, sends selected docs to backend for theme extraction,
 * and displays extracted themes along with a synthesized answer.
 */
const ThemeDisplay = () => {
  const [uploadedDocs, setUploadedDocs] = useState([]);      // List of available uploaded PDFs
  const [selectedDocs, setSelectedDocs] = useState([]);      // Currently selected PDFs
  const [themes, setThemes] = useState([]);                  // Extracted themes from backend
  const [synthesizedAnswer, setSynthesizedAnswer] = useState('');  // Synthesized summary from backend
  const [loading, setLoading] = useState(false);             // Loading state during API call
  const [error, setError] = useState(null);                  // Error message if any

  // Load uploaded documents list from backend on first render
  useEffect(() => {
    async function fetchDocuments() {
      try {
        const response = await axios.get('http://localhost:8000/api/documents/list');
        // Extract just filenames to keep it simple
        setUploadedDocs(response.data.map(doc => doc.filename));
      } catch (err) {
        console.error('Could not load documents:', err);
      }
    }
    fetchDocuments();
  }, []);

  // Handle toggling selection of a single document checkbox
  const handleDocSelect = (event) => {
    const doc = event.target.value;
    setSelectedDocs(prevSelected => 
      prevSelected.includes(doc)
        ? prevSelected.filter(d => d !== doc)  // Remove if already selected
        : [...prevSelected, doc]                // Add if not selected
    );
  };

  // Toggle between selecting all documents or deselecting all
  const toggleSelectAll = () => {
    if (selectedDocs.length === uploadedDocs.length) {
      setSelectedDocs([]);
    } else {
      setSelectedDocs([...uploadedDocs]);
    }
  };

  // Send selected documents to backend API to retrieve themes and synthesized answer
  const fetchThemes = async () => {
    if (selectedDocs.length === 0) {
      setError('Please select at least one PDF.');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await axios.post('http://localhost:8000/api/themes/', {
        documents: selectedDocs,
      });

      console.log("API response:", response.data);

      // Assign themes if they are an array, otherwise clear
      setThemes(Array.isArray(response.data.themes) ? response.data.themes : []);

      // Handle synthesizedAnswer: string, or convert to JSON string if object
      if (typeof response.data.synthesizedAnswer === 'string') {
        setSynthesizedAnswer(response.data.synthesizedAnswer);
      } else if (response.data.synthesizedAnswer) {
        setSynthesizedAnswer(JSON.stringify(response.data.synthesizedAnswer));
      } else {
        setSynthesizedAnswer('');
      }
    } catch (err) {
      console.error('Error fetching themes:', err);
      setError('Failed to fetch themes.');
      setThemes([]);
      setSynthesizedAnswer('');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 900, margin: '40px auto', padding: 24 }}>
      <h2>Multi-PDF Theme Extraction</h2>

      <button onClick={toggleSelectAll} style={{ marginBottom: 15 }}>
        {selectedDocs.length === uploadedDocs.length ? 'Deselect All' : 'Select All'}
      </button>

      <div style={{ marginBottom: 20 }}>
        <h4>Select one or more PDFs (multiple selection allowed):</h4>
        {uploadedDocs.length === 0 && <p>No documents uploaded yet.</p>}
        {uploadedDocs.map(doc => (
          <div key={doc}>
            <label>
              <input
                type="checkbox"
                value={doc}
                checked={selectedDocs.includes(doc)}
                onChange={handleDocSelect}
              />
              {doc}
            </label>
          </div>
        ))}
      </div>

      <button onClick={fetchThemes} disabled={loading}>
        {loading ? 'Analyzing...' : 'Extract Themes'}
      </button>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {!loading && !error && themes.length > 0 && (
        <>
          <section style={{ marginTop: 20 }}>
            <h3>Analyzed Documents</h3>
            <p>{selectedDocs.join(', ')}</p>
          </section>

          <section style={{ marginTop: 20 }}>
            <h3>Synthesized Answer</h3>
            <p>
              {synthesizedAnswer.length > 0
                ? synthesizedAnswer
                : 'No synthesized answer available.'}
            </p>
          </section>

          <section style={{ marginTop: 20 }}>
            <h3>Extracted Themes</h3>
            {themes.map((theme, index) => (
              <div key={index} style={{ marginBottom: 12 }}>
                <strong>Theme {index + 1}:</strong>{' '}
                {typeof theme === 'string' ? theme : JSON.stringify(theme)}
              </div>
            ))}
          </section>
        </>
      )}

      {loading && (
        <div style={{ marginTop: 20 }}>
          <p>Analyzing documents... please wait.</p>
        </div>
      )}
    </div>
  );
};

export default ThemeDisplay;

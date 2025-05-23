import React, { useState } from 'react';
import axios from 'axios';

/**
 * Component to display a list of uploaded documents with delete functionality.
 * Props:
 * - documents: Array of document objects { id, filename, ... }
 * - selectedDocumentId: ID of the currently selected document
 * - onSelectDocument: Callback function triggered when a document is selected
 * - onDocumentsChange: Callback to update the document list after changes (e.g. delete)
 */
const DocumentList = ({ documents, selectedDocumentId, onSelectDocument, onDocumentsChange }) => {
  // Track which document is currently being deleted (for loading state)
  const [deletingId, setDeletingId] = useState(null);

  /**
   * Handles the delete button click for a document.
   * Shows confirmation dialog, then sends delete request to backend.
   * Refreshes the document list after successful deletion.
   * @param {string} id - The document's ID
   * @param {string} filename - The document's filename (used for deletion endpoint)
   */
  const handleDeleteClick = async (id, filename) => {
    // Ask for user confirmation before deleting
    const confirmDelete = window.confirm(`Are you sure you want to delete "${filename}"?`);
    if (!confirmDelete) return;

    // Set loading state for the deleting document
    setDeletingId(id);

    try {
      // Call API to delete the document by filename (encoded for URL safety)
      await axios.delete(`/api/documents/delete/${encodeURIComponent(filename)}`);

      // After deletion, fetch the updated list of documents
      const response = await axios.get('/api/documents/list');

      // Map the returned documents to include an 'id' field for React keys, using filename
      const updatedDocs = response.data.map(doc => ({
        id: doc.filename,
        ...doc,
      }));

      // Notify parent component about updated documents list
      onDocumentsChange(updatedDocs);

    } catch (error) {
      // Log error and notify the user if deletion fails
      console.error('Error deleting document:', error);
      alert('Failed to delete document.');
    } finally {
      // Clear loading state
      setDeletingId(null);
    }
  };

  return (
    <div style={containerStyle}>
      <h2 style={titleStyle}>Uploaded Documents</h2>
      {documents.length === 0 ? (
        <p>No documents uploaded.</p>
      ) : (
        <ul style={listStyle}>
          {documents.map(doc => (
            <li
              key={doc.id}
              style={{
                marginBottom: 6,
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                cursor: onSelectDocument ? 'pointer' : 'default',
                fontWeight: doc.id === selectedDocumentId ? 'bold' : 'normal',
                color: doc.id === selectedDocumentId ? '#28a745' : 'black',
              }}
              onClick={() => onSelectDocument && onSelectDocument(doc.id)}
            >
              <span>{doc.filename}</span>
              <button
                onClick={e => {
                  e.stopPropagation(); // Prevent triggering parent onClick
                  if (!deletingId) handleDeleteClick(doc.id, doc.filename);
                }}
                disabled={deletingId === doc.id}
                style={buttonStyle}
                title={deletingId === doc.id ? 'Deleting...' : 'Delete'}
              >
                {deletingId === doc.id ? 'Deleting...' : 'Delete'}
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

// Styles for the container holding the document list
const containerStyle = {
  backgroundColor: 'white',
  padding: 16,
  borderRadius: 8,
  boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
  maxWidth: 400,
  margin: '20px auto',
};

// Heading style for the document list title
const titleStyle = {
  fontSize: 20,
  fontWeight: 600,
  marginBottom: 12,
};

// Style for the unordered list containing document items
const listStyle = {
  listStyleType: 'disc',
  paddingLeft: 20,
  marginBottom: 0,
};

// Style for delete buttons
const buttonStyle = {
  marginLeft: 12,
  backgroundColor: '#dc3545',
  color: 'white',
  border: 'none',
  borderRadius: 4,
  padding: '2px 8px',
  cursor: 'pointer',
};

export default DocumentList;

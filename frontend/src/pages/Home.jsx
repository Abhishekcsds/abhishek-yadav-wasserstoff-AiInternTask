import React, { useState, useEffect } from 'react';
import UploadForm from '../components/UploadForm.jsx';
import DocumentList from '../components/DocumentList.jsx';
import Chatinterface from '../components/Chatinterface.jsx';
import ThemeDisplay from '../components/ThemeDisplay.jsx';

const Home = () => {
  const [documents, setDocuments] = useState([]);
  const [selectedDocumentId, setSelectedDocumentId] = useState(null);

  // Function to fetch documents from backend API
  const fetchDocuments = () => {
    fetch('/api/documents/list')

      .then(res => res.json())
      .then(data => setDocuments(data))
      .catch(err => {
        console.error('Failed to fetch documents:', err);
        setDocuments([]);
      });
  };

  // Fetch documents once component mounts
  useEffect(() => {
    fetchDocuments();
  }, []);

  return (
    <div className="p-6 max-w-6xl mx-auto space-y-8">
      <h1 className="text-3xl font-bold text-center">Document Research & Theme Chatbot</h1>

      {/* Upload new documents and refresh list on success */}
      <UploadForm onUploadSuccess={fetchDocuments} />

      {/* List documents with ability to select and delete */}
      <DocumentList
        documents={documents}
        selectedDocumentId={selectedDocumentId}
        onSelectDocument={setSelectedDocumentId}
        onDocumentsChange={setDocuments}  // Allows DocumentList to update documents after deletion
      />

      
      {/* Show overall theme display */}
      <ThemeDisplay />

      {/* Chat interface related to selected document */}
      <Chatinterface selectedDocumentId={selectedDocumentId} />

    </div>
  );
};

export default Home;

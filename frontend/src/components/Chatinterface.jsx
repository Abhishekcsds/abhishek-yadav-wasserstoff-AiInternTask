// import React, { useState, useEffect } from 'react';
// import axios from 'axios';

// const Chatinterface = () => {
//   // State to hold the user's question input
//   const [query, setQuery] = useState('');
//   // Stores the responses returned from the backend query
//   const [responses, setResponses] = useState([]);
//   // Flag to indicate if the request is loading
//   const [loading, setLoading] = useState(false);
//   // List of available documents fetched from the server
//   const [documents, setDocuments] = useState([]);
//   // Currently selected document filename
//   const [selectedDoc, setSelectedDoc] = useState('');

//   // Fetch list of documents on component mount
//   useEffect(() => {
//     const fetchDocuments = async () => {
//       try {
//         const res = await axios.get('http://localhost:8000/api/documents/list');
//         const docs = res.data || [];
//         setDocuments(docs);
//         if (docs.length > 0) setSelectedDoc(docs[0].filename);
//       } catch (error) {
//         console.error('Error fetching documents:', error);
//         alert('Failed to load documents. Please ensure the server is running.');
//       }
//     };

//     fetchDocuments();
//   }, []);

//   // Clear previous responses when the selected document changes
//   useEffect(() => {
//     setResponses([]);
//   }, [selectedDoc]);

//   /**
//    * Format citation strings for display
//    * Extracts page and paragraph numbers if present, otherwise returns original string.
//    * Returns empty string for 'N/A' or falsy values.
//    */
//   const formatCitation = (citation) => {
//     if (!citation || citation.toLowerCase() === 'n/a') return '';

//     const pageMatch = citation.match(/page\s*(\d+)/i);
//     const paraMatch = citation.match(/para(?:graph)?\s*(\d+)/i);

//     const pagePart = pageMatch ? `Page ${pageMatch[1]}` : '';
//     const paraPart = paraMatch ? `Para ${paraMatch[1]}` : '';

//     if (pagePart && paraPart) return `${pagePart}, ${paraPart}`;
//     if (pagePart) return pagePart;
//     if (paraPart) return paraPart;
//     return citation;
//   };

//   // Handle user submitting a query
//   const handleSubmit = async () => {
//     if (!query.trim()) {
//       alert('Please enter a question before submitting.');
//       return;
//     }
//     if (!selectedDoc) {
//       alert('Select a document to query.');
//       return;
//     }

//     setLoading(true);
//     setResponses([]);

//     // Debug log for submission info
//     console.log('Sending query:', query, 'for document:', selectedDoc);

//     try {
//       const res = await axios.post('http://localhost:8000/api/query/', {
//         query,
//         doc_id: selectedDoc,
//       });

//       const data = res.data;

//       // Handle different possible response formats from backend
//       if (Array.isArray(data?.answer?.responses)) {
//         setResponses(data.answer.responses);
//       } else if (Array.isArray(data?.responses)) {
//         setResponses(data.responses);
//       } else if (data?.answer && typeof data.answer === 'string') {
//         setResponses([{ answer: data.answer, citation: 'N/A', doc_id: 'N/A' }]);
//       } else {
//         setResponses([]);
//         alert('No valid response received from the server.');
//       }
//     } catch (error) {
//       console.error('Error during query:', error);
//       alert('Query failed. Please verify server connectivity.');
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div style={styles.container}>
//       <h2 style={styles.header}>Ask a Question</h2>

//       <label style={styles.label} htmlFor="document-select">Select Document:</label>
//       <select
//         id="document-select"
//         value={selectedDoc}
//         onChange={(e) => setSelectedDoc(e.target.value)}
//         style={styles.select}
//       >
//         {documents.map((doc) => (
//           <option key={doc.filename} value={doc.filename}>
//             {doc.filename}
//           </option>
//         ))}
//       </select>

//       <input
//         type="text"
//         value={query}
//         onChange={(e) => setQuery(e.target.value)}
//         placeholder="Type your question here..."
//         style={styles.input}
//         onKeyDown={(e) => e.key === 'Enter' && handleSubmit()}
//         disabled={loading}
//       />

//       <button
//         onClick={handleSubmit}
//         disabled={loading}
//         style={{
//           ...styles.button,
//           backgroundColor: loading ? '#6c757d' : '#28a745',
//           cursor: loading ? 'not-allowed' : 'pointer',
//         }}
//       >
//         {loading ? 'Loading...' : 'Ask'}
//       </button>

//       {responses.length > 0 ? (
//         <table style={styles.table}>
//           <thead>
//             <tr>
//               <th style={styles.th}>Document ID</th>
//               <th style={styles.th}>Extracted Answer</th>
//               <th style={styles.th}>Citation</th>
//             </tr>
//           </thead>
//           <tbody>
//             {responses.map((res, idx) => (
//               <tr key={idx} style={idx % 2 === 0 ? styles.evenRow : styles.oddRow}>
//                 <td style={styles.td}>{res.doc_id || 'N/A'}</td>
//                 <td style={styles.td}>{res.answer || 'N/A'}</td>
//                 <td style={styles.td}>{formatCitation(res.citation)}</td>
//               </tr>
//             ))}
//           </tbody>
//         </table>
//       ) : (
//         !loading && <p style={{ fontStyle: 'italic', marginTop: 20 }}>No answers yet.</p>
//       )}
//     </div>
//   );
// };

// // Inline CSS styles for the component
// const styles = {
//   container: {
//     backgroundColor: '#fff',
//     padding: 16,
//     borderRadius: 8,
//     boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
//     maxWidth: 800,
//     margin: '20px auto',
//     fontFamily: 'Arial, sans-serif',
//   },
//   header: {
//     fontSize: 22,
//     fontWeight: 600,
//     marginBottom: 12,
//   },
//   label: {
//     display: 'block',
//     marginBottom: 8,
//     fontWeight: 'bold',
//   },
//   select: {
//     width: '100%',
//     padding: 10,
//     fontSize: 16,
//     borderRadius: 6,
//     border: '1px solid #ccc',
//     marginBottom: 16,
//   },
//   input: {
//     width: '100%',
//     padding: 12,
//     fontSize: 16,
//     borderRadius: 6,
//     border: '1px solid #ccc',
//     marginBottom: 12,
//     boxSizing: 'border-box',
//   },
//   button: {
//     padding: '12px 20px',
//     color: '#fff',
//     borderRadius: 6,
//     border: 'none',
//     fontWeight: 600,
//     display: 'inline-block',
//   },
//   table: {
//     width: '100%',
//     borderCollapse: 'collapse',
//     marginTop: 20,
//   },
//   th: {
//     borderBottom: '2px solid #333',
//     padding: 10,
//     textAlign: 'left',
//     backgroundColor: '#f2f2f2',
//   },
//   td: {
//     padding: 10,
//     verticalAlign: 'top',
//     borderBottom: '1px solid #ccc',
//   },
//   evenRow: {
//     backgroundColor: '#f9f9f9',
//   },
//   oddRow: {
//     backgroundColor: '#fff',
//   },
// };

// export default Chatinterface;


import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Chatinterface = () => {
  const [query, setQuery] = useState('');
  const [responses, setResponses] = useState([]);
  const [loading, setLoading] = useState(false);
  const [documents, setDocuments] = useState([]);
  const [selectedDoc, setSelectedDoc] = useState('');

  useEffect(() => {
    const fetchDocuments = async () => {
      try {
        const res = await axios.get('http://localhost:8000/api/documents/list');
        const docs = res.data || [];
        setDocuments(docs);
        if (docs.length > 0) setSelectedDoc(docs[0].filename);
      } catch (error) {
        console.error('Error fetching documents:', error);
        alert('Failed to load documents. Please ensure the server is running.');
      }
    };

    fetchDocuments();
  }, []);

  useEffect(() => {
    setResponses([]);
  }, [selectedDoc]);

  const formatCitation = (citation) => {
    if (!citation || citation.toLowerCase() === 'n/a') return '';

    const pageMatch = citation.match(/page\s*(\d+)/i);
    const paraMatch = citation.match(/para(?:graph)?\s*(\d+)/i);

    const pagePart = pageMatch ? `Page ${pageMatch[1]}` : '';
    const paraPart = paraMatch ? `Para ${paraMatch[1]}` : '';

    if (pagePart && paraPart) return `${pagePart}, ${paraPart}`;
    if (pagePart) return pagePart;
    if (paraPart) return paraPart;
    return citation;
  };

  const handleSubmit = async () => {
    if (!query.trim()) {
      alert('Please enter a question before submitting.');
      return;
    }
    if (!selectedDoc) {
      alert('Select a document to query.');
      return;
    }

    setLoading(true);
    setResponses([]);

    try {
      const res = await axios.post('http://localhost:8000/api/query/', {
        query,
        doc_id: selectedDoc,
      });

      const data = res.data;

      if (Array.isArray(data?.answer?.responses)) {
        setResponses(data.answer.responses);
      } else if (Array.isArray(data?.responses)) {
        setResponses(data.responses);
      } else if (data?.answer && typeof data.answer === 'object') {
        setResponses([
          {
            answer: data.answer.result || JSON.stringify(data.answer),
            citation: data.answer.citation || 'N/A',
            doc_id: selectedDoc,
          },
        ]);
      } else if (typeof data?.answer === 'string') {
        setResponses([{ answer: data.answer, citation: 'N/A', doc_id: selectedDoc }]);
      } else {
        setResponses([]);
        alert('No valid response received from the server.');
      }
    } catch (error) {
      console.error('Error during query:', error);
      alert('Query failed. Please verify server connectivity.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.header}>Ask a Question</h2>

      <label style={styles.label} htmlFor="document-select">Select Document:</label>
      <select
        id="document-select"
        value={selectedDoc}
        onChange={(e) => setSelectedDoc(e.target.value)}
        style={styles.select}
      >
        {documents.map((doc) => (
          <option key={doc.filename} value={doc.filename}>
            {doc.filename}
          </option>
        ))}
      </select>

      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Type your question here..."
        style={styles.input}
        onKeyDown={(e) => e.key === 'Enter' && handleSubmit()}
        disabled={loading}
      />

      <button
        onClick={handleSubmit}
        disabled={loading}
        style={{
          ...styles.button,
          backgroundColor: loading ? '#6c757d' : '#28a745',
          cursor: loading ? 'not-allowed' : 'pointer',
        }}
      >
        {loading ? 'Loading...' : 'Ask'}
      </button>

      {responses.length > 0 ? (
        <table style={styles.table}>
          <thead>
            <tr>
              <th style={styles.th}>Document ID</th>
              <th style={styles.th}>Extracted Answer</th>
              <th style={styles.th}>Citation</th>
            </tr>
          </thead>
          <tbody>
            {responses.map((res, idx) => (
              <tr key={idx} style={idx % 2 === 0 ? styles.evenRow : styles.oddRow}>
                <td style={styles.td}>{res.doc_id || 'N/A'}</td>
                <td style={styles.td}>
                  {typeof res.answer === 'object'
                    ? JSON.stringify(res.answer)
                    : res.answer || 'N/A'}
                </td>
                <td style={styles.td}>{formatCitation(res.citation)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        !loading && <p style={{ fontStyle: 'italic', marginTop: 20 }}>No answers yet.</p>
      )}
    </div>
  );
};

const styles = {
  container: {
    backgroundColor: '#fff',
    padding: 16,
    borderRadius: 8,
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
    maxWidth: 800,
    margin: '20px auto',
    fontFamily: 'Arial, sans-serif',
  },
  header: {
    fontSize: 22,
    fontWeight: 600,
    marginBottom: 12,
  },
  label: {
    display: 'block',
    marginBottom: 8,
    fontWeight: 'bold',
  },
  select: {
    width: '100%',
    padding: 10,
    fontSize: 16,
    borderRadius: 6,
    border: '1px solid #ccc',
    marginBottom: 16,
  },
  input: {
    width: '100%',
    padding: 12,
    fontSize: 16,
    borderRadius: 6,
    border: '1px solid #ccc',
    marginBottom: 12,
    boxSizing: 'border-box',
  },
  button: {
    padding: '12px 20px',
    color: '#fff',
    borderRadius: 6,
    border: 'none',
    fontWeight: 600,
    display: 'inline-block',
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse',
    marginTop: 20,
  },
  th: {
    borderBottom: '2px solid #333',
    padding: 10,
    textAlign: 'left',
    backgroundColor: '#f2f2f2',
  },
  td: {
    padding: 10,
    verticalAlign: 'top',
    borderBottom: '1px solid #ccc',
  },
  evenRow: {
    backgroundColor: '#f9f9f9',
  },
  oddRow: {
    backgroundColor: '#fff',
  },
};

export default Chatinterface;

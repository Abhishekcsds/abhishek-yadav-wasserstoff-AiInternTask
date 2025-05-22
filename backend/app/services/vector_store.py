

# import os
# from langchain.vectorstores import Chroma
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.schema import Document
# from app.core.config import settings

# # Ensure vector DB directory exists
# os.makedirs(settings.CHROMA_DB_DIR, exist_ok=True)

# # Instantiate embeddings once globally
# _embeddings = HuggingFaceEmbeddings()

# def get_vectorstore():
#     return Chroma(
#         persist_directory=settings.CHROMA_DB_DIR,
#         embedding_function=_embeddings
#     )

# def store_to_vector_db(doc_id: str, content: str):
#     """Split content, embed it, and store in vector DB with doc_id metadata."""
#     vectorstore = get_vectorstore()

#     text_splitter = RecursiveCharacterTextSplitter(
#         chunk_size=settings.CHUNK_SIZE,
#         chunk_overlap=settings.CHUNK_OVERLAP
#     )
#     chunks = text_splitter.split_text(content)
    
#     documents = [
#         Document(page_content=chunk, metadata={"doc_id": doc_id})
#         for chunk in chunks
#     ]

#     # Append new docs with metadata
#     vectorstore.add_documents(documents)
#     vectorstore.persist()

# def query_vector_db(query: str, doc_id: str, k: int = 5):
#     """Query the vector DB filtering by doc_id metadata to restrict results."""
#     vectorstore = get_vectorstore()
    
#     # Use filter to restrict results by doc_id
#     results = vectorstore.similarity_search(
#         query,
#         k=k,
#         filter={"doc_id": doc_id}
#     )
    
#     return results


import os
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from app.core.config import settings

# Create the directory for the vector database if it doesn't exist yet
os.makedirs(settings.CHROMA_DB_DIR, exist_ok=True)

# Initialize the embedding model once to reuse globally
_embeddings = HuggingFaceEmbeddings()

def get_vectorstore():
    """
    Return a Chroma vector store instance using the persisted directory and embeddings.
    """
    return Chroma(
        persist_directory=settings.CHROMA_DB_DIR,
        embedding_function=_embeddings
    )

def store_to_vector_db(doc_id: str, content: str):
    """
    Process and store document content in vector database with associated doc_id metadata.

    Args:
        doc_id (str): Identifier for the document.
        content (str): Full text content to split, embed, and store.
    """
    vectorstore = get_vectorstore()

    # Split the content into smaller overlapping chunks to improve embedding quality
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP
    )
    chunks = text_splitter.split_text(content)
    
    # Create Document objects with chunked text and metadata
    documents = [
        Document(page_content=chunk, metadata={"doc_id": doc_id})
        for chunk in chunks
    ]

    # Add the documents into the vector store and save changes to disk
    vectorstore.add_documents(documents)
    vectorstore.persist()

def query_vector_db(query: str, doc_id: str, k: int = 5):
    """
    Search the vector database for most similar chunks to the query, filtered by document ID.

    Args:
        query (str): The search query string.
        doc_id (str): Document ID to filter search results.
        k (int): Number of top results to return (default 5).

    Returns:
        List of matching Document objects.
    """
    vectorstore = get_vectorstore()
    
    # Perform similarity search with a metadata filter for the specified document ID
    results = vectorstore.similarity_search(
        query,
        k=k,
        filter={"doc_id": doc_id}
    )
    
    return results

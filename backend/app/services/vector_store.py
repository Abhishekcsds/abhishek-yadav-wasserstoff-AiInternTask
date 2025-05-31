


# import os
# from langchain.vectorstores import Chroma
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.schema import Document
# from app.core.config import settings
# from app.services.groq_embeddings import get_groq_embeddings

# # Ensure the vector DB directory exists
# os.makedirs(settings.CHROMA_DB_DIR, exist_ok=True)

# # ✅ Lazy load embedding function inside get_vectorstore()
# def get_vectorstore():
#     """
#     Return a Chroma vector store instance using the persisted directory and embeddings.
#     Lazily loads the embedding model to reduce memory footprint.
#     """
#     embeddings = get_groq_embeddings()
#     return Chroma(
#         persist_directory=settings.CHROMA_DB_DIR,
#         embedding_function=embeddings
#     )

# def store_to_vector_db(doc_id: str, content: str):
#     """
#     Process and store document content in vector database with associated doc_id metadata.
#     """
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

#     vectorstore.add_documents(documents)
#     vectorstore.persist()

# def query_vector_db(query: str, doc_id: str, k: int = 5):
#     """
#     Search the vector database for most similar chunks to the query, filtered by document ID.
#     """
#     vectorstore = get_vectorstore()

#     results = vectorstore.similarity_search(
#         query,
#         k=k,
#         filter={"doc_id": doc_id}
#     )

#     return results




import os
import asyncio
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from app.core.config import settings
from app.services.groq_embeddings import get_groq_embeddings

# Ensure vector DB directory exists
os.makedirs(settings.CHROMA_DB_DIR, exist_ok=True)

# Lazy-load embedding model
def get_vectorstore():
    """
    Return a Chroma vector store using persisted directory and Groq embeddings.
    """
    embeddings = get_groq_embeddings()
    return Chroma(
        persist_directory=settings.CHROMA_DB_DIR,
        embedding_function=embeddings
    )

# ✅ Made async for proper background execution
async def store_to_vector_db(doc_id: str, content: str):
    """
    Split and store document content in Chroma vector DB with doc_id metadata.
    """
    vectorstore = get_vectorstore()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP
    )
    chunks = text_splitter.split_text(content)

    documents = [
        Document(page_content=chunk, metadata={"doc_id": doc_id})
        for chunk in chunks
    ]

    print(f"[DEBUG] Storing {len(documents)} chunks for doc_id: {doc_id}")
    vectorstore.add_documents(documents)
    vectorstore.persist()
    await asyncio.sleep(0)  # Yield control back to event loop

def query_vector_db(query: str, doc_id: str, k: int = 5):
    """
    Search the vector database for top-k chunks matching the query.
    """
    vectorstore = get_vectorstore()

    results = vectorstore.similarity_search(
        query,
        k=k,
        filter={"doc_id": doc_id}
    )

    return results


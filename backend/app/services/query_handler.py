

# from langchain.chains import RetrievalQA
# from langchain_community.vectorstores import Chroma
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_groq.chat_models import ChatGroq
# from app.core.config import settings


# # Initialize the LLM once with minimal temperature (already done well)
# llm = ChatGroq(
#     api_key=settings.GROQ_API_KEY,
#     model="llama3-8b-8192",
#     temperature=0
# )

# # Cache the vectorstore and embeddings globally
# _vectorstore = None
# _embeddings = HuggingFaceEmbeddings()  # Instantiate once to avoid repetitive overhead

# def get_vectorstore():
#     global _vectorstore
#     if _vectorstore is None:
#         _vectorstore = Chroma(
#             persist_directory=settings.CHROMA_DB_DIR,
#             embedding_function=_embeddings
#         )
#     return _vectorstore

# # Pre-initialize the retriever and chain (so you avoid rebuilding them for every query)
# _retriever = None
# _qa_chain = None

# def init_chain():
#     global _retriever, _qa_chain
#     vectorstore = get_vectorstore()
#     if _retriever is None:
#         _retriever = vectorstore.as_retriever(
#             search_type="similarity",
#             search_kwargs={"k": 3}
#         )
#     if _qa_chain is None:
#         _qa_chain = RetrievalQA.from_chain_type(
#             llm=llm,
#             retriever=_retriever,
#             return_source_documents=False
#         )




# def handle_query(query: str, doc_id: str = None):
#     try:
#         init_chain()
        
#         # If doc_id is provided, create a filtered retriever for that doc only
#         if doc_id:
#             # Create a filtered retriever
#             filtered_retriever = _retriever  # default retriever
            
#             # Re-create retriever with metadata filter for doc_id
#             filtered_retriever = _retriever.vectorstore.as_retriever(
#                 search_type="similarity",
#                 search_kwargs={"k": 3},
#                 # This filter depends on your metadata schema
#                 # For example, if you store filename in metadata field 'doc_id':
#                 filter={"doc_id": doc_id}
#             )
            
#             # Build a new QA chain with the filtered retriever
#             qa_chain = RetrievalQA.from_chain_type(
#                 llm=llm,
#                 retriever=filtered_retriever,
#                 return_source_documents=False
#             )
            
#             # Run query with filtered retriever
#             result = qa_chain.run(query)
#         else:
#             # No doc_id, use global chain without filtering
#             result = _qa_chain.run(query)

#         return {
#             "responses": [
#                 {
#                     "doc_id": doc_id or "N/A",
#                     "answer": result,
#                     "citation": "Generated from retrieved documents"
#                 }
#             ]
#         }
#     except Exception as e:
#         return {"error": str(e)}


from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq.chat_models import ChatGroq
from app.core.config import settings

# Initialize Groq LLM with low temperature for deterministic results
llm = ChatGroq(
    api_key=settings.GROQ_API_KEY,
    model="llama3-8b-8192",
    temperature=0
)

# Cache the vectorstore and embeddings globally to avoid repeated instantiations
_vectorstore = None
_embeddings = HuggingFaceEmbeddings()

def get_vectorstore():
    global _vectorstore
    if _vectorstore is None:
        _vectorstore = Chroma(
            persist_directory=settings.CHROMA_DB_DIR,
            embedding_function=_embeddings
        )
    return _vectorstore

# Global retriever and QA chain initialized once for efficiency
_retriever = None
_qa_chain = None

def init_chain():
    global _retriever, _qa_chain
    vectorstore = get_vectorstore()

    if _retriever is None:
        _retriever = vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )

    if _qa_chain is None:
        _qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=_retriever,
            return_source_documents=False
        )

async def handle_query(query: str, doc_id: str = None):
    try:
        init_chain()

        if doc_id:
            filtered_retriever = _retriever.vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 3},
                filter={"doc_id": doc_id}  # adjust metadata key if needed
            )
            qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                retriever=filtered_retriever,
                return_source_documents=False
            )
            result = await qa_chain.acall(query)
        else:
            result = await _qa_chain.acall(query)

        return {
            "responses": [
                {
                    "doc_id": doc_id or "N/A",
                    "answer": result,
                    "citation": "Generated from retrieved documents"
                }
            ]
        }
    except Exception as e:
        return {"error": str(e)}

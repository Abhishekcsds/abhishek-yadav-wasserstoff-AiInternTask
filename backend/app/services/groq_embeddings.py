
# import os
# import requests
# from dotenv import load_dotenv
# from langchain.embeddings.base import Embeddings

# load_dotenv()  # Load env variables from .env automatically

# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# GROQ_EMBEDDING_ENDPOINT = "https://api.groq.ai/v1/embeddings"  # Confirm with Groq docs if URL differs

# class GroqEmbeddings(Embeddings):
#     def __init__(self):
#         if not GROQ_API_KEY:
#             raise ValueError("GROQ_API_KEY is not set in environment variables.")
#         self.api_key = GROQ_API_KEY

#     def embed_documents(self, texts):
#         return [self._embed_text(text) for text in texts]

#     def embed_query(self, text):
#         return self._embed_text(text)

#     def _embed_text(self, text):
#         headers = {
#             "Authorization": f"Bearer {self.api_key}",
#             "Content-Type": "application/json",
#         }
#         payload = {
#             "input": text,
#             "model": "groq-embedding-1",  # Use your actual Groq embedding model name
#         }

#         response = requests.post(GROQ_EMBEDDING_ENDPOINT, json=payload, headers=headers)
#         if response.status_code != 200:
#             raise Exception(f"Groq API error {response.status_code}: {response.text}")

#         data = response.json()
#         # Adjust based on Groq API's actual response format
#         # Example assumes: { "embedding": [float, float, ...] }
#         embedding_vector = data.get("embedding")
#         if embedding_vector is None:
#             # fallback if embedding is nested under 'data'
#             embedding_vector = data.get("data", [{}])[0].get("embedding")
#         if embedding_vector is None:
#             raise Exception(f"Unexpected response from Groq API: {data}")

#         return embedding_vector


import os
import requests
from dotenv import load_dotenv
from langchain.embeddings.base import Embeddings

# Load environment variables from a .env file automatically
load_dotenv()

# Retrieve Groq API key from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Groq embeddings API endpoint (verify with Groq documentation for accuracy)
GROQ_EMBEDDING_ENDPOINT = "https://api.groq.ai/v1/embeddings"

class GroqEmbeddings(Embeddings):
    """
    Custom embedding class to integrate Groq's embedding API
    with LangChain's Embeddings interface.
    """
    def __init__(self):
        # Ensure the API key is available on initialization
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not found in environment variables.")
        self.api_key = GROQ_API_KEY

    def embed_documents(self, texts):
        """
        Generate embeddings for a list of documents.
        Calls the private _embed_text method for each text.
        """
        return [self._embed_text(text) for text in texts]

    def embed_query(self, text):
        """
        Generate embedding vector for a single query string.
        """
        return self._embed_text(text)

    def _embed_text(self, text):
        """
        Internal helper function that calls Groq's API to
        obtain embedding vector for the given text input.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "input": text,
            "model": "groq-embedding-1",  # Replace with actual Groq model identifier if needed
        }

        # Make POST request to Groq embeddings endpoint
        response = requests.post(GROQ_EMBEDDING_ENDPOINT, json=payload, headers=headers)

        # Raise exception if response status is not successful
        if response.status_code != 200:
            raise Exception(f"Groq API returned error {response.status_code}: {response.text}")

        # Parse JSON response
        data = response.json()

        # Attempt to extract embedding vector from response
        embedding_vector = data.get("embedding")

        # Fallback: sometimes embedding might be nested under 'data' key
        if embedding_vector is None:
            embedding_vector = data.get("data", [{}])[0].get("embedding")

        # Raise error if embedding vector still not found
        if embedding_vector is None:
            raise Exception(f"Unexpected Groq API response structure: {data}")

        return embedding_vector

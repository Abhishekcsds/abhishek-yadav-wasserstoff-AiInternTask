# from pydantic import BaseModel

# class QueryRequest(BaseModel):
#     query: str
#     top_k: int = 5


from pydantic import BaseModel

class QueryRequest(BaseModel):
    """
    Schema for incoming query requests.
    
    Attributes:
        query (str): The user's query string.
        top_k (int): Number of top results to return (default is 5).
    """
    query: str
    top_k: int = 5

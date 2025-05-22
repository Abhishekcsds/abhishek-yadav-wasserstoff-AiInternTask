# from pydantic_settings import BaseSettings


# class Settings(BaseSettings):
#     GROQ_API_KEY: str
#     CHROMA_DB_DIR: str = "./data/chroma"
#     OCR_LANG: str = "eng"
#     CHUNK_SIZE: int = 1000
#     CHUNK_OVERLAP: int = 200

#     class Config:
#         env_file = ".env"

# settings = Settings()
# #


from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables or .env file.
    """
    GROQ_API_KEY: str  # API key for Groq service
    CHROMA_DB_DIR: str = "./data/chroma"  # Directory path for Chroma vector database storage
    OCR_LANG: str = "eng"  # Language code used by Tesseract OCR
    CHUNK_SIZE: int = 1000  # Size of text chunks for processing
    CHUNK_OVERLAP: int = 200  # Overlap size between text chunks

    class Config:
        # Specifies the env file to load settings from
        env_file = ".env"

# Instantiate the settings object to access configuration values
settings = Settings()

# from fastapi import APIRouter
# from app.routes.document_routes import router as document_router

# router = APIRouter()
# router.include_router(document_router)
# Import FastAPI's APIRouter and the document routes router



from fastapi import APIRouter
from app.routes.document_routes import router as document_router

# Create a main API router and include the document routes under it
router = APIRouter()
router.include_router(document_router)





# from fastapi import FastAPI
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import FileResponse, Response
# from pathlib import Path

# # Import your API router
# from app.api.routes import router as api_router

# app = FastAPI()

# build_dir = Path(__file__).resolve().parent.parent / "build"

# print(f"build_dir resolved to: {build_dir}")
# print(f"Does build_dir exist? {build_dir.exists()}")
# print(f"Does index.html exist? {(build_dir / 'index.html').exists()}")
# if build_dir.exists():
#     print(f"Contents of build_dir: {[p.name for p in build_dir.iterdir()]}")

# # Mount your API router under /api prefix
# app.include_router(api_router, prefix="/api")

# if build_dir.exists() and (build_dir / "index.html").exists():
#     app.mount("/static", StaticFiles(directory=build_dir / "static"), name="static")

#     @app.get("/", include_in_schema=False)
#     async def serve_root():
#         return FileResponse(build_dir / "index.html")

#     @app.get("/{full_path:path}", include_in_schema=False)
#     async def serve_spa(full_path: str):
#         target_file = build_dir / full_path
#         if target_file.exists() and target_file.is_file():
#             return FileResponse(target_file)
#         return FileResponse(build_dir / "index.html")

# else:
#     @app.get("/", include_in_schema=False)
#     async def missing_build():
#         return Response(
#             content="Frontend build files not found. Please build your React app and copy it to the backend/build folder.",
#             media_type="text/plain",
#             status_code=500,
#         )


from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
from pathlib import Path

from app.api.routes import router as api_router

app = FastAPI()

build_dir = Path(__file__).resolve().parent.parent / "build"

# API router
app.include_router(api_router, prefix="/api")

if build_dir.exists() and (build_dir / "index.html").exists():
    app.mount("/static", StaticFiles(directory=build_dir / "static"), name="static")

    @app.get("/", include_in_schema=False)
    async def serve_root():
        return FileResponse(build_dir / "index.html")

    # Catch-all route to serve index.html for client-side routing (supporting all HTTP methods)
    @app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"], include_in_schema=False)
    async def serve_spa(request: Request, full_path: str):
        target_file = build_dir / full_path
        if target_file.exists() and target_file.is_file():
            return FileResponse(target_file)
        return FileResponse(build_dir / "index.html")

else:
    @app.get("/", include_in_schema=False)
    async def missing_build():
        return Response(
            content="Frontend build files not found. Please build your React app and copy it to the backend/build folder.",
            media_type="text/plain",
            status_code=500,
        )

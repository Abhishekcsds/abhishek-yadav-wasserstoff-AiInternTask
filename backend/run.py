# import os
# import uvicorn

# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 10000))
#     uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)


import os
import uvicorn
from pathlib import Path

if __name__ == "__main__":
    # Set default port to 8000 if not defined
    port = int(os.environ.get("PORT", 8000))

    # Ensure you're using correct app path (adjust if needed)
    uvicorn.run(
        "app.main:app",  # Python path to your FastAPI instance
        host="0.0.0.0",
        port=port,
        reload=True,  # Set to True in development for auto-reload
    )

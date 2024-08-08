from fastapi import FastAPI
from app.api.router import router as api_router
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import init_db

app = FastAPI()

# Initialize the database (create tables if not already created)
init_db()

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (adjust as needed)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Include the API router
app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

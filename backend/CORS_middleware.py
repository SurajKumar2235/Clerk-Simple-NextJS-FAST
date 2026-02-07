from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
load_dotenv()

def setup_cors(app):
    '''
    This function is used to set up CORS middleware for the FastAPI application.
    It is used to allow requests from the frontend to the backend.
    '''
    origins = os.getenv("ALLOWED_HOST")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


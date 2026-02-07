from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
import logging
import sys


from prometheus_fastapi_instrumentator import Instrumentator

from core.database import engine
from models import User
from models.user import Base # We need Base from somewhere to create tables. models/__init__ exposes User, but Base is in models/user (via core/database base class) or just core/database?
# Actually Base is in core/database.py and models inherit from it.
# To create tables, we need to import the models so they are registered with Base metadata.
# Importing models.User does that.
from core.database import Base 

from dependencies.credits import consume_credit
from dependencies.auth import get_current_user
from backend.CORS_middleware import setup_cors

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    logger.info("Creating database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created.")
    yield
    # Shutdown

app = FastAPI(lifespan=lifespan)
setup_cors(app)

# Setup Prometheus
Instrumentator().instrument(app).expose(app)

@app.get("/public")
def public():
    logger.info("Public endpoint accessed")
    return {"message": "public endpoint works"}

@app.get("/protected")
def protected(user: User = Depends(get_current_user)):
    logger.info(f"Protected endpoint accessed by user: {user.email}")
    return {
        "message": "Protected endpoint works",
        "user": user.email,
        "credits": user.credits,
        "role": user.role
    }

@app.post("/generate-ai", dependencies=[Depends(consume_credit(cost=5))])
def generate_ai(user: User = Depends(get_current_user)):
    logger.info(f"Consuming 5 credits for AI generation. User: {user.email}")
    return {
        "message": "AI Generation Successful",
        "remaining_credits": user.credits # Note: This will be the value *after* deduction
    }

@app.post("/failing-endpoint", dependencies=[Depends(consume_credit(cost=2))])
def failing_endpoint():
    logger.info("This endpoint will fail and should refund credits")
    raise HTTPException(status_code=400, detail="Something went wrong, refunding credits")


# dependencies/auth.py
import requests
from jose import jwt
from fastapi import Request, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import os
from dotenv import load_dotenv
from core.database import get_db
from models import User

load_dotenv()

CLERK_JWKS_URL = os.getenv("CLERK_JWKS_URL")

# Fetch JWKS once (or cache appropriately)
if CLERK_JWKS_URL:
    try:
        jwks = requests.get(CLERK_JWKS_URL).json()
    except Exception as e:
        print(f"Failed to fetch JWKS: {e}")
        jwks = {}
else:
    jwks = {}


def verify_clerk_token(token: str):
    try:
        payload = jwt.decode(
            token,
            jwks,
            algorithms=["RS256"],
            options={"verify_aud": True},  # set False if audience check fails unexpectedly
        )
        return payload
    except Exception as e:
        print(f"Token verification failed: {e}")
        raise HTTPException(status_code=401, detail="Invalid Clerk token")


async def get_current_user(request: Request, db: AsyncSession = Depends(get_db)):
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        raise HTTPException(status_code=401, detail="Missing token")

    try:
        token = auth_header.split(" ")[1]
    except IndexError:
        raise HTTPException(status_code=401, detail="Invalid token format")

    payload = verify_clerk_token(token)
    clerk_id = payload.get("sub")
    email = payload.get("email") # Note: Clerk JWT structure varies, might be in 'email_addresses' or custom claims

    if not clerk_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    # Check if user exists in DB
    result = await db.execute(select(User).filter(User.clerk_id == clerk_id))
    user = result.scalars().first()

    if not user:
        # Create new user
        user = User(
            clerk_id=clerk_id,
            email=email, # Might be None if not provided in JWT
            role="user",
            credits=10
        )
        db.add(user)
        # We need to commit here to get the User object fully persisted
        # But since we are in a dependency, we should be careful about transaction scope.
        # For creation, immediate commit is usually fine.
        await db.commit()
        await db.refresh(user)

    return user

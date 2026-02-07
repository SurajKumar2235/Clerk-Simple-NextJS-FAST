# clerk_auth.py

import requests
from jose import jwt
from fastapi import Request, HTTPException
import os
from dotenv import load_dotenv
load_dotenv()

CLERK_JWKS_URL = os.getenv("CLERK_JWKS_URL")
CLERK_AUDIENCE = os.getenv("CLERK_AUDIENCE")

jwks = requests.get(CLERK_JWKS_URL).json()


def verify_clerk_token(token: str):
    try:
        payload = jwt.decode(
            token,
            jwks,
            algorithms=["RS256"],
            options={"verify_aud": True},  # set True if using audience
        )
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Clerk token")


async def clerk_auth_middleware(request: Request):
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        raise HTTPException(status_code=401, detail="Missing token")

    token = auth_header.split(" ")[1]
    user = verify_clerk_token(token)

    return user

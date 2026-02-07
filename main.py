from fastapi import FastAPI, Depends
from clerk_auth import clerk_auth_middleware
from CORS_middleware import setup_cors
app = FastAPI()
setup_cors(app)


@app.get("/public")
def public():
    return {"message": "public endpoint works"}


@app.get("/protected")
def protected(user=Depends(clerk_auth_middleware)):
    return {
        "message": "Protected endpoint works",
        "clerk_user": user["sub"]
    }

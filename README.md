```markdown
# Setup and Installation

## 1. Backend Setup (FastAPI)
1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```
2. **Install `uv` (Fast Python package installer):**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
3. **Create and activate a virtual environment:**
   ```bash
   uv venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```
4. **Install dependencies:**
   ```bash
   uv pip install fastapi uvicorn python-jose[cryptography] requests python-dotenv
   ```
5. **Configure Environment Variables:**
   Create a `.env` file:
   ```env
   CLERK_API_URL=https://api.clerk.dev/v1
   CLERK_SECRET_KEY=sk_test_...
   CLERK_JWKS_URL=https://jwt.clerk.com/.well-known/jwks.json
   ```
6. **Run the server:**
   ```bash
   uvicorn main:app --reload
   ```

## 2. Frontend Setup (Next.js)
1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```
2. **Install dependencies:**
   ```bash
   npm install @clerk/nextjs
   ```
3. **Configure Environment Variables:**
   Create a `.env.local` file:
   ```env
   NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
   CLERK_SECRET_KEY=sk_test_...
   NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
   NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
   ```
4. **Run the development server:**
   ```bash
   npm run dev
   ```

## 3. Communication Flow
- **Frontend:** Use the `useAuth()` or `useToken()` hook from `@clerk/nextjs` to retrieve the JWT.
- **Headers:** Pass the token in the `Authorization: Bearer <token>` header for all API requests.
- **Backend:** The FastAPI middleware intercepts the request, fetches Clerk's JWKS, and validates the token before proceeding to the route handler.
```

from fastapi import FastAPI, Depends, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from typing import Optional
from dotenv import load_dotenv
from jose import ExpiredSignatureError, JWTError

from models import ChatRequest, ChatResponse
from agent import process_agent_message
from services.auth_service import JWKSFetchError, verify_supabase_jwt

# Load Environment Variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")

if not SUPABASE_URL:
    print("WARNING: SUPABASE_URL missing. Mocking auth locally.")

app = FastAPI(title="Agentic Auth Management backend")

# Configure CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer(auto_error=False)

def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Security(security)):
    """
    Validates the Supabase JWT token and extracts the user ID.
    This ensures that the LLM tools strictly act on the authenticated user.
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token.",
        )

    auth_scheme = (credentials.scheme or "").lower()
    if auth_scheme != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme. Expected Bearer token.",
        )

    token = (credentials.credentials or "").strip()
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token.",
        )

    if not SUPABASE_URL:
        # Fallback for local testing without Supabase configured yet
        return "test_user_123"
        
    try:
        payload = verify_supabase_jwt(token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials (no sub in token)",
            )
        return user_id
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed: token has expired",
        )
    except JWKSFetchError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}",
        )
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}",
        )

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/agent/chat", response_model=ChatResponse)
async def agent_chat(request: ChatRequest, user_id: str = Depends(get_current_user)):
    """
    Main endpoint for the Agentic AI.
    It takes the user's prompt, passes it to the Gemini Agent (which has tools tied specifically to `user_id`),
    and returns the final response.
    """
    try:
        # Ensure we pass the user_id securely to the agent context
        agent_response = await process_agent_message(
            user_input=request.message,
            user_id=user_id,
            history=request.history
        )
        return ChatResponse(response=agent_response, success=True)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent error: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

from fastapi import FastAPI, Depends, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import jwt
import os
from dotenv import load_dotenv

from models import ChatRequest, ChatResponse
from agent import process_agent_message

# Load Environment Variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET") # Or Supabase JWT secret from settings

if not SUPABASE_URL or not SUPABASE_JWT_SECRET:
    print("WARNING: Supabase credentials missing. Mocking auth locally.")

app = FastAPI(title="Agentic Auth Management backend")

# Configure CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Validates the Supabase JWT token and extracts the user ID.
    This ensures that the LLM tools strictly act on the authenticated user.
    """
    token = credentials.credentials
    if not SUPABASE_JWT_SECRET:
        # Fallback for local testing without Supabase configured yet
        return "test_user_123"
        
    try:
        # Decode the JWT securely
        payload = jwt.decode(
            token, 
            SUPABASE_JWT_SECRET, 
            algorithms=["HS256"], 
            options={"verify_aud": False} # Supabase aud can vary (authenticated)
        )
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials (no sub in token)",
            )
        return user_id
    except jwt.PyJWTError as e:
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

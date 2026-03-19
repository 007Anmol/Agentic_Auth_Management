import os
import google.generativeai as genai
from tools import get_user_tools

# Initialize Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
else:
    print("WARNING: GOOGLE_API_KEY environment variable not set.")

MASTER_PROMPT = """You are a highly capable AI backend agent.
Your goal is to assist the user by using the provided tools to interact with their account data.
You already have access to their secure context (you do not need to ask for their ID).
Always try to be helpful and concise."""

async def process_agent_message(user_input: str, user_id: str, history: list) -> str:
    """
    Initializes a Gemini chat session with tools dynamically bound to the provided user_id.
    This prevents IDOR vulnerabilities (Prompt Injection into user_id fields).
    """
    # 1. Dynamically generate tools that implicitly use `user_id` without LLM needing to provide it
    secure_tools = get_user_tools(user_id)
    
    # 2. Initialize the model with these secure tools
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash", # Updated to use standard 1.5 flash
        tools=secure_tools,
        system_instruction=MASTER_PROMPT
    )
    
    # 3. Handle history format from client (Optional implementation depending on frontend schema)
    # The frontend might send an array of {"role": "user"/"model", "parts": ["..."]}
    formatted_history = []
    for msg in history:
        # format according to genai structure if needed
        # this is a basic mapping, may need to be adjusted based on exact frontend history schema
        role = "user" if msg.get("role") == "user" else "model"
        formatted_history.append({"role": role, "parts": [msg.get("content", "")]})
    
    # Start chat
    chat = model.start_chat(history=formatted_history, enable_automatic_function_calling=True)
    
    try:
        # Send message and auto-execute functions
        # The `enable_automatic_function_calling=True` simplifies the executor loop entirely
        # The SDK will automatically call our python functions and send the results back to the LLM!
        response = chat.send_message(user_input)
        
        return response.text
    except Exception as e:
        print(f"Agent Execution Error: {e}")
        raise e

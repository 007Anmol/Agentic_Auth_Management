import os
from typing import Any, Dict, List, Optional

import google.generativeai as genai

from tools import get_user_tools


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
else:
    print("WARNING: GOOGLE_API_KEY environment variable not set.")


MASTER_PROMPT = """You are a highly capable AI backend agent.
Your goal is to assist the authenticated user with their account.
Use the provided tools when account-specific data is needed.
Never assume access to another user's account context.
Keep responses concise and actionable."""


def _format_history(history: Optional[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    if not history:
        return []

    formatted_history: List[Dict[str, Any]] = []
    for msg in history:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        if role not in {"user", "model"}:
            role = "user" if role == "assistant" else "model"
        formatted_history.append({"role": role, "parts": [str(content)]})

    return formatted_history


def generate_llm_response(
    user_input: str,
    user_id: str,
    history: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """Generate a Gemini response with authenticated user-aware tools."""
    secure_tools = get_user_tools(user_id)

    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        tools=secure_tools,
        system_instruction=MASTER_PROMPT,
    )

    chat = model.start_chat(
        history=_format_history(history),
        enable_automatic_function_calling=True,
    )

    response = chat.send_message(user_input)
    if getattr(response, "text", None):
        return response.text
    return "I could not generate a response right now."

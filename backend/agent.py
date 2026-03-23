from services.llm_service import generate_llm_response

async def process_agent_message(user_input: str, user_id: str, history: list) -> str:
    """
    Backward-compatible async wrapper used by the API route.
    Delegates LLM execution to the service layer.
    """
    return generate_llm_response(
        user_input=user_input,
        user_id=user_id,
        history=history,
    )

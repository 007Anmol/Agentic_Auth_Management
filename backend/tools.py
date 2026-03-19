def get_user_tools(user_id: str):
    """
    Returns a list of functions that the LLM can call.
    By doing this inside a closure, the tools inherently know the `user_id` context
    without needing the LLM to pass it. This eliminates the risk of prompt injection
    allowing one user to access another user's data (IDOR).
    """

    def check_status() -> dict:
        """Call this to check the current user's account status."""
        print(f"[TOOL EXECUTED] check_status on behalf of user: {user_id}")
        
        # TODO: Implement actual Supabase DB interaction here using the service role client
        # example: 
        # from main import supabase
        # response = supabase.table("users").select("status").eq("id", user_id).execute()
        
        return {"success": True, "status": "active", "account_tier": "premium"}

    def update_db(settings: dict) -> dict:
        """
        Call this to update the current user's profile or account data.
        Pass the parameters as a dictionary in `settings`.
        """
        print(f"[TOOL EXECUTED] update_db on behalf of user: {user_id} with data {settings}")
        
        if not settings:
            return {"success": False, "error": "No data provided"}
            
        # TODO: Implement actual Supabase DB update
        # response = supabase.table("users").update(settings).eq("id", user_id).execute()
        
        return {"success": True, "updated": True, "applied_settings": settings}
        
    def fetch_recent_activity() -> str:
        """Call this to summarize the user's recent account activity."""
        print(f"[TOOL EXECUTED] fetch_recent_activity on behalf of user: {user_id}")
        return "No recent flags. Last login was today. DB was updated 5 minutes ago."

    # Return the callable bound functions directly.
    return [check_status, update_db, fetch_recent_activity]

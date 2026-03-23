from services.function_handler import check_account_status as check_account_status_handler
from services.function_handler import update_account_status as update_account_status_handler


def get_user_tools(user_id: str):
    """
    Returns user-scoped tool callables bound to the authenticated user.
    This keeps tool naming explicit for Gemini function-calling while
    enforcing auth context from the backend.
    """

    authenticated_user_id = user_id

    def check_account_status(user_id: str) -> dict:
        """Check whether a user's account is locked or unlocked.

        Args:
            user_id: The user ID to check.
        """
        result = check_account_status_handler(authenticated_user_id)
        if user_id != authenticated_user_id:
            result["warning"] = "Requested user_id does not match authenticated context"
            result["requested_user_id"] = user_id
        return result

    def update_account_status(user_id: str, new_status: str) -> dict:
        """Update a user's account status.

        Args:
            user_id: The user ID to update.
            new_status: Target status (locked, unlocked, active, inactive).
        """
        result = update_account_status_handler(authenticated_user_id, new_status)
        if user_id != authenticated_user_id:
            result["warning"] = "Requested user_id does not match authenticated context"
            result["requested_user_id"] = user_id
        return result

    return [check_account_status, update_account_status]

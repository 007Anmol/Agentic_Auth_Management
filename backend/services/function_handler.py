from typing import Dict

from services.supabase_service import get_supabase_client


def check_account_status(user_id: str) -> Dict[str, object]:
    """Read account status for a specific user from the users table."""
    client = get_supabase_client()
    if client is None:
        return {
            "success": False,
            "error": "Supabase client not configured",
            "user_id": user_id,
        }

    try:
        response = (
            client.table("users")
            .select("id, status")
            .eq("id", user_id)
            .limit(1)
            .execute()
        )
        rows = response.data or []
        if not rows:
            return {
                "success": False,
                "error": "User not found",
                "user_id": user_id,
            }

        row = rows[0]
        status = row.get("status", "unknown")
        return {
            "success": True,
            "user_id": row.get("id", user_id),
            "status": status,
            "is_locked": str(status).lower() == "locked",
        }
    except Exception as exc:
        return {
            "success": False,
            "error": f"Failed to check account status: {exc}",
            "user_id": user_id,
        }


def update_account_status(user_id: str, new_status: str) -> Dict[str, object]:
    """Update account status for a specific user in the users table."""
    client = get_supabase_client()
    if client is None:
        return {
            "success": False,
            "error": "Supabase client not configured",
            "user_id": user_id,
        }

    normalized_status = (new_status or "").strip().lower()
    allowed_statuses = {"locked", "unlocked", "active", "inactive"}
    if normalized_status not in allowed_statuses:
        return {
            "success": False,
            "error": f"Invalid status '{new_status}'. Allowed values: {sorted(allowed_statuses)}",
            "user_id": user_id,
        }

    try:
        response = (
            client.table("users")
            .update({"status": normalized_status})
            .eq("id", user_id)
            .execute()
        )
        rows = response.data or []
        if not rows:
            return {
                "success": False,
                "error": "User not found or no rows updated",
                "user_id": user_id,
            }

        updated_row = rows[0]
        return {
            "success": True,
            "user_id": updated_row.get("id", user_id),
            "status": updated_row.get("status", normalized_status),
        }
    except Exception as exc:
        return {
            "success": False,
            "error": f"Failed to update account status: {exc}",
            "user_id": user_id,
        }

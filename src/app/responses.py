from src.app.schemas import Status

activate_bot_resp = {
    201: {
        "description": "Bot has been activated",
        "content": {"application/json": {"example": {"assistant_id": 12, "status": "Activated"}}},
    },
    409: {
        "description": "Bot is already activated",
        "content": {
            "application/json": {
                "example": {"detail": {"status": Status.ERROR, "reason": "Bot with this token is already activated"}}
            }
        },
    },
    422: {
        "description": "Wrong bot token",
        "content": {"application/json": {"example": {"detail": {"status": Status.ERROR, "reason": "Invalid bot token"}}}},
    },
}

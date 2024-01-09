from src.app.schemas import Status

activate_bot_resp = {
    201: {
        "description": "Bot has been activated",
        "content": {"application/json": {"example": {"status": "Activated"}}},
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

delete_bot_resp = {
    201: {
        "description": "Bot has been deleted",
        "content": {"application/json": {"example": {"status": "Deleted"}}},
    },
    422: {
        "description": "Bot with given token doesn't exist",
        "content": {
            "application/json": {"example": {"detail": {"status": Status.ERROR, "reason": "Bot with this token doesn't exist"}}}
        },
    },
}

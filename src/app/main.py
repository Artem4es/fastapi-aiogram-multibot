import logging

import uvicorn
from aiohttp.web_runner import GracefulExit
from fastapi import FastAPI

from src.app.routers import router
from src.app.utils import lifespan, setup_logging
from src.config import Settings

logger = logging.getLogger(__name__)
settings = Settings()


app = FastAPI(debug=settings.fastapi_debug, name=settings.fastapi_name, lifespan=lifespan)
app.include_router(router)


if __name__ == "__main__":
    try:
        setup_logging()
        logger.info("FAST Api app has been started...")

        uvicorn.run(app=app, host=settings.fastapi_host, port=settings.fastapi_port)

    except GracefulExit:
        logger.info("Bot app coroutine has been STOPPED")

    except Exception as e:
        logger.error(e, exc_info=True)
        raise e

    finally:
        logger.info("FAST Api app has been STOPPED.")

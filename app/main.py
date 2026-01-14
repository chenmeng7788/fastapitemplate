from fastapi import FastAPI

from app.api.endpoints import users
from app.core.middlewares import AccessMiddleware
from app.core.project_logging import logger
from config.settings import settings

app = FastAPI(
    title="fast api demo",
    debug=settings.ENVIRONMENT
)



logger.info("url:{}".format(settings.DATABASE_URL))
app.add_middleware(AccessMiddleware)

app.include_router(users.router, prefix="/api/v1", tags=["users"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


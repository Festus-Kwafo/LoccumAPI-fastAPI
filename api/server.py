from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.engine import URL

from api.routes import router as api_router
from api.core import config, tasks
from api.db.tasks import some_engine

from api.models.blog import Base

Base.metadata.create_all(some_engine)

def get_application():
    app = FastAPI(title=config.PROJECT_NAME, version=config.VERSION)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # app.add_event_handler("startup", tasks.create_start_app_handler(app))
    # app.add_event_handler("shutdown", tasks.create_stop_app_handler(app))

    app.include_router(api_router, prefix="/api")

    return app


app = get_application()

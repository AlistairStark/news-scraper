__version__ = "0.1.0"

import logging

from fastapi import FastAPI

from app import settings
from app.controllers.v1 import v1_router

logging.basicConfig(
    # filename="record.log",
    level=logging.INFO,
    format=f"%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
)


app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(v1_router, prefix="/v1")

from app.models import *

import os

import celery
from celery import Celery, signals

celery = Celery(
    __name__,
    broker=os.environ.get("CELERY_BROKER_URL"),
    backend=os.environ.get("CELERY_RESULT_BACKEND"),
)


def init_celery(app):
    celery.conf.update(app.config)
    celery.autodiscover_tasks(["application.worker"], force=True)


@signals.worker_process_init.connect
def init_celery_flask_app(**kw):
    from application import init_app

    flask_app = init_app()
    flask_app.app_context().push()
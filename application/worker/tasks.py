from application import models
from application.worker import celery


@celery.task()
def create_task(task_type):
    print("TEST CELERY TASK", task_type)
    res = models.User.query.all()
    print("RES IOS: ", res)

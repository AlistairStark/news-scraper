from application.worker import celery
from application import init_app
import sys
sys.dont_write_bytecode = True

app = init_app()
app.app_context().push()

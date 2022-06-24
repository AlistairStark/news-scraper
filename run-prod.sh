cd app && alembic upgrade head && cd ..

gunicorn --bind=0.0.0.0:5000 -k uvicorn.workers.UvicornWorker app:app
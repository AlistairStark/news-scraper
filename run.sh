cd application && alembic upgrade head && cd ..

gunicorn \
    --reload \
    --user nobody \
    --group nogroup \
    --workers 4 \
    --max-requests 250 \
    --max-requests-jitter 50 \
    --timeout 600 \
    --bind 0.0.0.0:5000 \
    --limit-request-field_size 100000000 \
    --log-level=INFO \
    --worker-class gevent \
    wsgi:app
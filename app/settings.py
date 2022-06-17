import os
import sys

TOKEN_SECRET = os.environ.get('TOKEN_SECRET', 'totallysecretthing')
PROJECT_NAME = 'Daily Ops'
CREATE_SECRET = os.environ.get("CREATE_SECRET", "test")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DBS = os.getenv("POSTGRES_DBS", "postgres")

def get_db_url():
    if "pytest" in sys.modules:
        return f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres/test"
    return f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres/{POSTGRES_DBS}"
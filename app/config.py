import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    PGHOST = os.getenv("PGHOST", "localhost")
    PGPORT = int(os.getenv("PGPORT", "5433"))
    PGDATABASE = os.getenv("PGDATABASE", "appdb")
    PGUSER = os.getenv("PGUSER", "app")
    PGPASSWORD = os.environ["PGPASSWORD"]
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

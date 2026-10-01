import os
from dotenv import load_dotenv
from flask import Flask

from app.db import get_db_conn, apply_migrations
from app.health import bp as health_bp
from app.visits import create_visits_blueprint

load_dotenv()


def create_app():
    app = Flask(__name__)

    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    db_conn = get_db_conn()
    apply_migrations(db_conn)

    app.register_blueprint(create_visits_blueprint(db_conn, redis_url))
    app.register_blueprint(health_bp)

    return app

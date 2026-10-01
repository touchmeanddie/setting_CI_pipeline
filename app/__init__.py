from flask import Flask, jsonify

from app.config import Config
from app.db import get_db_conn, apply_migrations
from app.visits import create_visits_blueprint


def create_app():
    app = Flask(__name__)

    db_conn = get_db_conn()
    apply_migrations(db_conn)

    app.register_blueprint(
        create_visits_blueprint(db_conn, Config.REDIS_URL)
    )

    @app.route("/health")
    def health():
        return jsonify(status="ну типо ок"), 200

    return app

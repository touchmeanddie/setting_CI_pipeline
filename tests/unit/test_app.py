from flask import Flask
from app.health import health


def test_health_returns_200():
    app = Flask(__name__)
    app.add_url_rule("/health", "health", health)

    client = app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "ну типо ок"

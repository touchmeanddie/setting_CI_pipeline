import pathlib

import pytest
import psycopg
from flask import Flask

from testcontainers.community.postgres import PostgresContainer
from testcontainers.community.redis import RedisContainer

from app.visits import create_visits_blueprint

MIGRATIONS_DIR = (
    pathlib.Path(__file__).resolve().parent.parent.parent / "migrations"
)


@pytest.fixture()
def app_client():
    with PostgresContainer("postgres:16") as pg, \
         RedisContainer("redis:7") as redis_c:

        dsn = pg.get_connection_url().replace(
            "postgresql+psycopg2", "postgresql"
        )
        conn = psycopg.connect(dsn)

        with conn.cursor() as cur:
            for sql_file in sorted(MIGRATIONS_DIR.glob("*.sql")):
                cur.execute(sql_file.read_text(encoding="utf-8"))
            conn.commit()

        redis_url = (
            f"redis://{redis_c.get_container_host_ip()}:"
            f"{redis_c.get_exposed_port(6379)}"
        )

        app = Flask(__name__)
        app.register_blueprint(create_visits_blueprint(conn, redis_url))

        yield app.test_client()

        conn.close()


def test_first_request_uses_database(app_client):
    response = app_client.get('/visits')

    assert response.status_code == 204

    data = response.get_json()
    assert data['source'] == 'db'
    assert data['count'] > 0
    assert 'lastId' in data


def test_second_request_uses_cache(app_client):
    app_client.get('/visits')

    response = app_client.get('/visits')

    assert response.status_code == 200
    assert response.get_json()['source'] == 'cache'

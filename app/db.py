import os
import pathlib
import psycopg

MIGRATIONS_DIR = pathlib.Path(__file__).resolve().parent.parent / "migrations"
MIGRATION_LOCK_KEY = 1234


def get_db_conn():
    return psycopg.connect(
        host=os.getenv("PGHOST", "localhost"),
        port=int(os.getenv("PGPORT", "5432")),
        dbname=os.getenv("PGDATABASE", "appdb"),
        user=os.getenv("PGUSER", "app"),
        password=os.environ["PGPASSWORD", "test"],
    )


def apply_migrations(conn):
    conn.autocommit = False
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT pg_advisory_xact_lock(%s)", (MIGRATION_LOCK_KEY,))

            cur.execute("""
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    version     TEXT PRIMARY KEY,
                    applied_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
            """)
            cur.execute("SELECT version FROM schema_migrations")
            applied = {row[0] for row in cur.fetchall()}

            for sql_file in sorted(MIGRATIONS_DIR.glob("*.sql")):
                version = sql_file.stem
                if version in applied:
                    continue
                cur.execute(sql_file.read_text(encoding="utf-8"))
                cur.execute(
                    "INSERT INTO schema_migrations (version) VALUES (%s)",
                    (version,),
                )
        conn.commit()
    except Exception:
        conn.rollback()
        raise

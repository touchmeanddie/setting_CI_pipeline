import psycopg

try:
    conn = psycopg.connect(
        host="127.0.0.1",
        port=5432,
        dbname="lab3db",
        user="alex",
        password="lansh1234",
        sslmode="disable",
    )
    print("OK:", conn.status)
    conn.close()
except Exception as e:
    print("type:", type(e).__name__)
    print("repr:", repr(e))
    print("args:", e.args)
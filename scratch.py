from app.database import get_connection, init_db

conn = get_connection()
init_db(conn)
print(conn.execute("SELECT COUNT(*) FROM categories").fetchone()[0])

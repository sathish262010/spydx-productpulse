from db.db_config import get_connection


try:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DATABASE();")
    db = cursor.fetchone()
    print("Connected to database:",db[0])
    conn.close()
except Exception as e:
    print("Connection failed:",e)
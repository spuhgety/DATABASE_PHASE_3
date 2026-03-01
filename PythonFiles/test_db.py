from db import get_connection

def main():
    try:
        cnx = get_connection()
        cursor = cnx.cursor(dictionary=True)

        cursor.execute("SELECT DATABASE() AS db;")
        print("Connected to:", cursor.fetchone()['db'])

        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        print("Tables:", tables)

        cursor.close()
        cnx.close()

    except Exception as e:
        print("Error connecting:", e)

if __name__ == "__main__":
    main()

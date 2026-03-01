import mysql.connector

DB_CONFIG = {
    'user': 'root',
    'password': 'Imbadatvalorant!1',
    'host': '127.0.0.1',
    'database': 'valorant_tracker2'
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

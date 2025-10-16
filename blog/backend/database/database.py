import pymysql.cursors
from dotenv import load_dotenv
import logging
import os


load_dotenv()


DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', '3306'))
DB_USER = os.getenv('DB_USER', 'root')
DB_PASS = os.getenv("DB_PASS", '')
DB_NAME = os.getenv("DB_NAME", 'blog')




def create_connection_db():
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            port=DB_PORT,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return connection
    except Exception as e:
        logging.error(f"Error connecting to database: {e}")
        return None
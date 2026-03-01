import MySQLdb
import os
from dotenv import load_dotenv

load_dotenv()

db = MySQLdb.connect(
    host=os.getenv('DB_HOST', '127.0.0.1'),
    user=os.getenv('DB_USER', 'root'),
    passwd=os.getenv('DB_PASSWORD', ''),
    port=int(os.getenv('DB_PORT', 3306))
)

cursor = db.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS food_delivery_db")
print("Database created successfully")
db.close()

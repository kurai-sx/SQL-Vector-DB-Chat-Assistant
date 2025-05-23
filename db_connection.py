import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",    
        user="root",             
        password="PASSWORD",
        database="DATABASE_NAME" 
    )

def run_query(sql):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

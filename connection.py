import mysql.connector
from mysql.connector import Error
import sys
import config
 
 
def connect():
    """ Connect to MySQL database """
    conn = None
    try:
        conn = mysql.connector.connect(host='localhost', user='root',password='cookie123', database='users')
        if conn.is_connected():
            print('Connected to MySQL database')
 
    except Error as e:
        print(e)
 
    finally:
        if conn is not None and conn.is_connected():
            conn.close()
 
 
if __name__ == '__main__':
    connect()
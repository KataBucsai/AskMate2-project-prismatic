import psycopg2
import sys


def handle_database(command):
    try:
        connect_str = "dbname='kata' user='kata' host='localhost' password='berendel'"
        conn = psycopg2.connect(connect_str)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(command)
        if "SELECT" in command:
            table = cursor.fetchall()
            return table
        cursor.close()
        conn.close()
    except Exception as e:
        error_message = "Uh oh, can't connect. Invalid dbname, user or password? \n" + str(e)
        print(error_message)
        sys.exit()



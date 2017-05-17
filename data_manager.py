import base64
import time
from datetime import datetime
import psycopg2
import sys


def handle_database(command):
    try:
        connect_str = "dbname='eros' user='eros' host='localhost' password='titok'"
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


def get_table_from_sql_db(table_name, order_by=['submission_time', 'DESC']): 
    result = handle_database("""SELECT * FROM {} ORDER BY {} {} LIMIT 5;""".format(table_name, order_by[0], order_by[1]))
    return result


def get_record_from_sql_db(table_name, condition):
    result = handle_database("""SELECT * FROM {} WHERE {};""".format(table_name, condition))
    return result


def add_item_to_sql_db(table, request):
    handle_database("""INSERT INTO {} ({}, {}, {}, {}, {}) VALUES ('{}', {}, {}, '{}', '{}');""".format(table, 
         'submission_time', 'view_number', 'vote_number', 'title', 'message',
         str(datetime.now())[:-7], 0, 0, request['new_question_title'], request['new_question_message']))


def add_item_to_answer_db(table, request):
    handle_database("""INSERT INTO {} ({}, {}, {}, {}) VALUES ('{}', {}, {}, '{}');""".format(table, 
         'submission_time', 'vote_number', 'question_id', 'message',
         str(datetime.now())[:-7], 0, request['question_id'], request['new_answer_message']))

def update_record(table_name, set_value, condition):
    handle_database("""UPDATE {} SET {} WHERE {}""".format(table_name, set_value, condition))


def delete_record(table_name, condition):
    handle_database("""DELETE FROM {} WHERE {};""".format(table_name, condition))

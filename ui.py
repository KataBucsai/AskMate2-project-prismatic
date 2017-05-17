from datetime import datetime
import psycopg2
from data_manager import handle_database


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

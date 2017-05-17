import base64
import time
from datetime import datetime
import psycopg2
import sys


def init(command):
    print(command)
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
    result = init("""SELECT * FROM {} ORDER BY {} {} LIMIT 5;""".format(table_name, order_by[0], order_by[1]))
    return result

def get_record_from_sql_db(table_name, condition):
    result = init("""SELECT * FROM {} WHERE {};""".format(table_name, condition))
    return result


# write a @table into a file
#
# @file_name: string
# @table: list of lists of strings
def write_table_to_file(file_name, table, indices):
    table = base64_coder(table, indices)
    with open(file_name, "w") as file:
        for record in table:
            row = ','.join(record)
            file.write(row + "\n")


def get_time_stamp():
    # print(str(int(time.time()))) 
    return str(int(time.time()))


def get_timeform_from_stamp(table):
    for row in table:
        row[1] = datetime.datetime.fromtimestamp(int(row[1])).strftime('%Y-%m-%d %H:%M:%S')
    return table


def add_item_to_sql_db(table, request):
    init("""INSERT INTO {} ({}, {}, {}, {}, {}) VALUES ('{}', {}, {}, '{}', '{}');""".format(table, 
         'submission_time', 'view_number', 'vote_number', 'title', 'message',
         str(datetime.now())[:-7], 0, 0, request['new_question_title'], request['new_question_message']))


def update_record(table_name, set_value, condition):
    init("""UPDATE {} SET {} WHERE {}""".format(table_name, set_value, condition))


def add_item_to_answer_table(table, request):
    max_id = 0
    if len(table) > 0:
        max_id = max(int(i[0]) for i in table)
    table.append([str(max_id+1),
                 get_time_stamp(),
                 '0',
                 request['question_id'],
                 request['new_answer_message'],
                 ''])
    return table


def delete_item_from_table(list_table, question_id):
    for row_id, row_value in enumerate(list_table):
        if row_value[0] == question_id:
            del(list_table[row_id])
            break
    return list_table




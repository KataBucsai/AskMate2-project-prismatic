from datetime import datetime
import psycopg2
from data_manager import handle_database


def get_table_from_sql_db(table_name, order_by=['submission_time', 'DESC']): 
    result = handle_database("""SELECT * FROM {} ORDER BY {} {} LIMIT 5;""".format(table_name, order_by[0], order_by[1]))
    return result


def get_record_from_sql_db(table_name, condition):
    result = handle_database("""SELECT * FROM {} WHERE {};""".format(table_name, condition))
    return result


def get_record_from_tag(table_name, join_text, condition):
    # SELECT tag.name FROM tag JOIN question_tag ON question_tag.tag_id=tag.id WHERE question_tag.question_id=1;
    result = handle_database("""SELECT name FROM {} JOIN {} WHERE {};""".format(table_name, join_text, condition))
    return result


def get_existing_tags():
    result = handle_database("""SELECT name FROM tag;""")
    return result


def get_tag_id_by_name(tag_name):
    result = handle_database("""SELECT id FROM tag WHERE name='{}';""".format(tag_name))
    return result


def add_item_to_sql_db(table, request):
    handle_database("""INSERT INTO {} ({}, {}, {}, {}, {}) VALUES ('{}', {}, {}, '{}', '{}');""".format(table, 
                    'submission_time', 'view_number', 'vote_number', 'title', 'message',
                    str(datetime.now())[:-7], 0, 0, request['new_question_title'], request['new_question_message']))


def add_item_to_answer_db(table, request):
    handle_database("""INSERT INTO {} ({}, {}, {}, {}) VALUES ('{}', {}, {}, '{}');""".format(table,
                    'submission_time', 'vote_number', 'question_id', 'message',
                    str(datetime.now())[:-7], 0, request['question_id'], request['new_answer_message']))


def add_item_to_comment_db(table, request):
    handle_database("""INSERT INTO {} ({}, {}, {}, {}) VALUES ({}, {}, '{}', '{}');""".format(table,
                    'question_id', 'answer_id', 'message', 'submission_time',
                    request['question_id'], 'NULL', request['new_comment_message'], str(datetime.now())[:-7]))


def add_item_to_question_tag(table, question_id, tag_id):
    handle_database("""INSERT INTO {} ({}, {}) VALUES ({}, {});""".format(table,
                    'question_id', 'tag_id',
                    question_id, tag_id))


def add_item_to_tag(table, name):
    handle_database("""INSERT INTO {} ({}) VALUES ('{}');""".format(table,
                    'name',
                    name))


def update_record(table_name, set_value, condition):
    handle_database("""UPDATE {} SET {} WHERE {}""".format(table_name, set_value, condition))


def delete_record(table_name, condition):
    handle_database("""DELETE FROM {} WHERE {};""".format(table_name, condition))


def search_in_db(column, table_name, search_condition):
    result = handle_database("""SELECT {} FROM {} WHERE {};""".format(column, table_name, search_condition))
    return result

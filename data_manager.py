import psycopg2
import sys
import config
import public_config
import private_config


def getDbConfig(settings):
    db_settings = settings['db_settings']

    is_dev = True
    is_test = False
    is_prod = False

    if is_dev:
        return db_settings['dev']
    elif is_test:
        return db_settings['test']
    elif is_prod:
        return db_settings['prod']
    return dict()


def handle_database(command):
    try:
        config_data = getDbConfig(config.getSettings())
        connect_str = "dbname='" + config_data['db_name'] + "' user='" + config_data['user'] + "' host='" + config_data['host'] + "' password='" + config_data['password'] + "'"
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

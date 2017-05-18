import config


private_settings = {
    'db_settings': {
        'dev': {
            'db_name': 'your_db_name',
            'host': 'localhost',
            'user': 'your_username',
            'password': 'secret_password'
        },
        'test': {
            'db_name': '?',
            'host': '?',
            'user': '?',
            'password': '?'
        },
        'prod': {
            'db_name': '?',
            'host': '?',
            'user': '?',
            'password': '?'
        }
    }
}

config.update(private_settings)
import mysql.connector

from config.settings import DB_AUTH_PLUGIN, DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USE_PURE, DB_USER


def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        auth_plugin=DB_AUTH_PLUGIN,
        use_pure=DB_USE_PURE,
    )

import json
import os

import mysql.connector

from config.settings import (
    BASE_DIR,
    DB_AUTH_PLUGIN,
    DB_HOST,
    DB_NAME,
    DB_PASSWORD,
    DB_PORT,
    DB_USE_PURE,
    DB_USER,
)

DB_CONNECTION_FILE = os.path.join(BASE_DIR, "config", "db_connection.json")

_runtime_host = DB_HOST
_runtime_port = DB_PORT
_runtime_name = DB_NAME


def load_connection_settings():
    global _runtime_host, _runtime_port, _runtime_name

    _runtime_host = DB_HOST
    _runtime_port = DB_PORT
    _runtime_name = DB_NAME

    if not os.path.exists(DB_CONNECTION_FILE):
        return get_connection_settings()

    try:
        with open(DB_CONNECTION_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, ValueError, TypeError):
        return get_connection_settings()

    host = str(data.get("host", DB_HOST)).strip() or DB_HOST
    port = data.get("port", DB_PORT)
    name = str(data.get("database", DB_NAME)).strip() or DB_NAME

    try:
        _runtime_port = int(port)
    except (TypeError, ValueError):
        _runtime_port = DB_PORT

    _runtime_host = host
    _runtime_name = name
    return get_connection_settings()


def get_connection_settings():
    return {
        "host": _runtime_host,
        "port": _runtime_port,
        "database": _runtime_name,
    }


def save_connection_settings():
    os.makedirs(os.path.dirname(DB_CONNECTION_FILE), exist_ok=True)
    with open(DB_CONNECTION_FILE, "w", encoding="utf-8") as file:
        json.dump(get_connection_settings(), file, ensure_ascii=False, indent=2)


def update_connection_settings(host, port, database_name, persist=True):
    global _runtime_host, _runtime_port, _runtime_name

    normalized_host = str(host).strip()
    if not normalized_host:
        raise ValueError("IP hoặc host database không được để trống.")

    normalized_name = str(database_name).strip()
    if not normalized_name:
        raise ValueError("Tên database không được để trống.")

    try:
        normalized_port = int(str(port).strip())
    except (TypeError, ValueError):
        raise ValueError("Port database phải là số hợp lệ.")

    if normalized_port <= 0:
        raise ValueError("Port database phải lớn hơn 0.")

    _runtime_host = normalized_host
    _runtime_port = normalized_port
    _runtime_name = normalized_name

    if persist:
        save_connection_settings()

    return get_connection_settings()


def test_connection():
    conn = get_connection()
    conn.close()


def get_connection():
    return mysql.connector.connect(
        host=_runtime_host,
        port=_runtime_port,
        user=DB_USER,
        password=DB_PASSWORD,
        database=_runtime_name,
        auth_plugin=DB_AUTH_PLUGIN,
        use_pure=DB_USE_PURE,
    )


load_connection_settings()

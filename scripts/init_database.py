import argparse
import json
from pathlib import Path
import sys

import mysql.connector
from mysql.connector import Error as MySQLError

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config.settings import BASE_DIR, DB_AUTH_PLUGIN, DB_NAME, DB_PASSWORD, DB_PORT, DB_USE_PURE, DB_USER


SCHEMA_PATH = Path(BASE_DIR) / "config" / "schema.sql"
CONNECTION_FILE = Path(BASE_DIR) / "config" / "db_connection.json"


def build_attempts(host, port, database=None):
    base = {
        "host": host,
        "port": port,
        "user": DB_USER,
        "password": DB_PASSWORD,
    }
    if database:
        base["database"] = database

    attempts = []
    for include_auth_plugin, use_pure in (
        (True, DB_USE_PURE),
        (False, DB_USE_PURE),
        (False, False),
        (False, True),
    ):
        kwargs = dict(base)
        if use_pure is not None:
            kwargs["use_pure"] = use_pure
        if include_auth_plugin and DB_AUTH_PLUGIN:
            kwargs["auth_plugin"] = DB_AUTH_PLUGIN
        attempts.append(kwargs)
    return attempts


def connect_with_fallback(host, port, database=None):
    seen = set()
    last_error = None

    for kwargs in build_attempts(host, port, database):
        key = tuple(sorted(kwargs.items()))
        if key in seen:
            continue
        seen.add(key)

        try:
            return mysql.connector.connect(**kwargs)
        except MySQLError as exc:
            last_error = exc
            error_text = str(exc).lower()
            if "authentication plugin" not in error_text and "not supported" not in error_text:
                raise

    if last_error:
        raise last_error
    raise RuntimeError("Không thể kết nối MySQL.")


def split_sql_script(sql_text):
    statements = []
    current = []

    for line in sql_text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("--"):
            continue
        current.append(line)
        if stripped.endswith(";"):
            statements.append("\n".join(current).strip())
            current = []

    if current:
        statements.append("\n".join(current).strip())

    return statements


def save_runtime_connection(host, port, database_name):
    CONNECTION_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONNECTION_FILE.write_text(
        json.dumps(
            {
                "host": host,
                "port": port,
                "database": database_name,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def apply_schema(host, port):
    schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
    statements = split_sql_script(schema_sql)

    conn = connect_with_fallback(host, port, database=None)
    cursor = conn.cursor()
    try:
        for statement in statements:
            cursor.execute(statement)
        conn.commit()
    finally:
        cursor.close()
        conn.close()

    save_runtime_connection(host, port, DB_NAME)


def main():
    parser = argparse.ArgumentParser(description="Initialize MySQL schema for BCHQSTB.")
    parser.add_argument("--host", required=True)
    parser.add_argument("--port", type=int, default=DB_PORT)
    args = parser.parse_args()

    apply_schema(args.host, args.port)
    print(f"Initialized database '{DB_NAME}' on {args.host}:{args.port}")


if __name__ == "__main__":
    main()
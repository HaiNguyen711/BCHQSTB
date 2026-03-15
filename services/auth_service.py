from passlib.hash import pbkdf2_sha256

from config.database import get_connection


def create_user(username, password, role="staff"):
    username = str(username).strip()
    password = str(password).strip()

    if not username or not password:
        return False, "Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu."

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            return False, "Tên đăng nhập đã tồn tại."

        password_hash = pbkdf2_sha256.hash(password)
        cursor.execute(
            """
            INSERT INTO users (username, password_hash, role)
            VALUES (%s, %s, %s)
            """,
            (username, password_hash, role),
        )
        conn.commit()
        return True, "Tạo tài khoản thành công."
    except Exception as exc:
        if conn is not None:
            conn.rollback()
        return False, f"Lỗi tạo tài khoản: {exc}"
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


def login(username, password):
    username = str(username).strip()
    password = str(password).strip()

    if not username or not password:
        return None, "Vui lòng nhập tên đăng nhập và mật khẩu."

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and pbkdf2_sha256.verify(password, user["password_hash"]):
            return user, None

        return None, "Tên đăng nhập hoặc mật khẩu không đúng."
    except Exception as exc:
        return None, f"Không thể kết nối database: {exc}"
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

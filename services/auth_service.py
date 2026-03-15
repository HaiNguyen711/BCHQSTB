from passlib.hash import pbkdf2_sha256

from config.database import get_connection


def create_user(username, password, role='staff'):
    username = str(username).strip()
    password = str(password).strip()

    if not username or not password:
        return False, 'Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.'

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute('SELECT id FROM users WHERE username = %s', (username,))
        if cursor.fetchone():
            return False, 'Tên đăng nhập đã tồn tại.'

        password_hash = pbkdf2_sha256.hash(password)
        cursor.execute(
            '''
            INSERT INTO users (username, password_hash, role)
            VALUES (%s, %s, %s)
            ''',
            (username, password_hash, role),
        )
        conn.commit()
        return True, 'Tạo tài khoản thành công.'
    except Exception as exc:
        conn.rollback()
        return False, 'Lỗi tạo tài khoản: {}'.format(exc)
    finally:
        cursor.close()
        conn.close()


def login(username, password):
    username = str(username).strip()
    password = str(password).strip()

    if not username or not password:
        return None

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()

        if user and pbkdf2_sha256.verify(password, user['password_hash']):
            return user

        return None
    finally:
        cursor.close()
        conn.close()

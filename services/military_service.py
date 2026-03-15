from services.citizen_service import format_display_date, normalize_text, to_db_date
from config.database import get_connection

STATUS_OPTIONS = [
    ('CHUA_GOI', 'Chưa gọi'),
    ('KHAM_SO_TUYEN', 'Khám sơ tuyển'),
    ('KHAM_SUC_KHOE', 'Khám sức khỏe'),
    ('DU_DIEU_KIEN', 'Đủ điều kiện'),
    ('TAM_HOAN', 'Tạm hoãn'),
    ('MIEN_NVQS', 'Miễn NVQS'),
    ('CHO_NHAP_NGU', 'Chờ nhập ngũ'),
    ('DA_NHAP_NGU', 'Đã nhập ngũ'),
    ('DA_XUAT_NGU', 'Đã xuất ngũ'),
]

STATUS_LABELS = dict(STATUS_OPTIONS)


def ensure_military_records():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            '''
            INSERT INTO military_service (citizen_cccd, service_status)
            SELECT c.cccd, 'CHUA_GOI'
            FROM citizens c
            LEFT JOIN military_service m ON m.citizen_cccd = c.cccd
            WHERE m.citizen_cccd IS NULL
            '''
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def format_military_row(row):
    if not row:
        return None

    row['cccd'] = normalize_text(row.get('cccd'))
    row['full_name'] = normalize_text(row.get('full_name'))
    row['date_of_birth'] = format_display_date(row.get('date_of_birth'))
    row['service_status'] = normalize_text(row.get('service_status')) or 'CHUA_GOI'
    row['service_status_label'] = STATUS_LABELS.get(row['service_status'], row['service_status'])
    row['health_check_date'] = format_display_date(row.get('health_check_date'))
    row['enlistment_date'] = format_display_date(row.get('enlistment_date'))
    row['health_result'] = normalize_text(row.get('health_result'))
    row['unit_name'] = normalize_text(row.get('unit_name'))
    row['position_name'] = normalize_text(row.get('position_name'))
    row['note'] = normalize_text(row.get('note'))
    row['phone'] = normalize_text(row.get('phone'))
    row['ward'] = normalize_text(row.get('ward'))
    return row


def get_all_military_records():
    ensure_military_records()

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            '''
            SELECT
                c.cccd,
                c.full_name,
                c.date_of_birth,
                c.phone,
                c.ward,
                m.service_status,
                m.health_check_date,
                m.health_result,
                m.enlistment_date,
                m.unit_name,
                m.position_name,
                m.note
            FROM citizens c
            LEFT JOIN military_service m ON m.citizen_cccd = c.cccd
            ORDER BY c.full_name ASC
            '''
        )
        rows = cursor.fetchall()
        return [format_military_row(row) for row in rows]
    finally:
        cursor.close()
        conn.close()


def search_military_records(keyword):
    ensure_military_records()

    keyword = normalize_text(keyword)
    if not keyword:
        return get_all_military_records()

    like_value = '%{}%'.format(keyword)

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            '''
            SELECT
                c.cccd,
                c.full_name,
                c.date_of_birth,
                c.phone,
                c.ward,
                m.service_status,
                m.health_check_date,
                m.health_result,
                m.enlistment_date,
                m.unit_name,
                m.position_name,
                m.note
            FROM citizens c
            LEFT JOIN military_service m ON m.citizen_cccd = c.cccd
            WHERE c.full_name LIKE %s
               OR c.cccd LIKE %s
               OR c.phone LIKE %s
               OR m.unit_name LIKE %s
               OR m.position_name LIKE %s
            ORDER BY c.full_name ASC
            ''',
            (like_value, like_value, like_value, like_value, like_value),
        )
        rows = cursor.fetchall()
        return [format_military_row(row) for row in rows]
    finally:
        cursor.close()
        conn.close()


def get_military_record(cccd):
    ensure_military_records()

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            '''
            SELECT
                c.cccd,
                c.full_name,
                c.date_of_birth,
                c.phone,
                c.ward,
                m.service_status,
                m.health_check_date,
                m.health_result,
                m.enlistment_date,
                m.unit_name,
                m.position_name,
                m.note
            FROM citizens c
            LEFT JOIN military_service m ON m.citizen_cccd = c.cccd
            WHERE c.cccd = %s
            LIMIT 1
            ''',
            (cccd,),
        )
        row = cursor.fetchone()
        return format_military_row(row)
    finally:
        cursor.close()
        conn.close()


def save_military_record(data):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        citizen_cccd = normalize_text(data.get('citizen_cccd'))
        if not citizen_cccd:
            return False, 'Thiếu CCCD công dân.'

        payload = {
            'citizen_cccd': citizen_cccd,
            'service_status': normalize_text(data.get('service_status')) or 'CHUA_GOI',
            'health_check_date': to_db_date(data.get('health_check_date'), True),
            'health_result': normalize_text(data.get('health_result')),
            'enlistment_date': to_db_date(data.get('enlistment_date'), True),
            'unit_name': normalize_text(data.get('unit_name')),
            'position_name': normalize_text(data.get('position_name')),
            'note': normalize_text(data.get('note')),
        }

        cursor.execute(
            '''
            INSERT INTO military_service (
                citizen_cccd,
                service_status,
                health_check_date,
                health_result,
                enlistment_date,
                unit_name,
                position_name,
                note
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                service_status = VALUES(service_status),
                health_check_date = VALUES(health_check_date),
                health_result = VALUES(health_result),
                enlistment_date = VALUES(enlistment_date),
                unit_name = VALUES(unit_name),
                position_name = VALUES(position_name),
                note = VALUES(note)
            ''',
            (
                payload['citizen_cccd'],
                payload['service_status'],
                payload['health_check_date'],
                payload['health_result'],
                payload['enlistment_date'],
                payload['unit_name'],
                payload['position_name'],
                payload['note'],
            ),
        )
        conn.commit()
        return True, 'Đã lưu thông tin nhập ngũ.'
    except Exception as exc:
        conn.rollback()
        return False, str(exc)
    finally:
        cursor.close()
        conn.close()

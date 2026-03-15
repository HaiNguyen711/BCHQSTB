from services.citizen_service import format_display_date, normalize_text, to_db_date
from config.database import get_connection

STATUS_OPTIONS = [
    ('CHUA_GOI', 'Chưa gọi'),
    ('KHAM_SO_TUYEN', 'Khám sơ tuyển'),
    ('KHAM_SUC_KHOE', 'Khám sức khỏe'),
    ('DU_DIEU_KIEN', 'Đủ điều kiện'),
    ('CHO_NHAP_NGU', 'Chờ nhập ngũ'),
    ('DA_NHAP_NGU', 'Đã nhập ngũ'),
    ('DA_XUAT_NGU', 'Đã xuất ngũ'),
    ('TAM_HOAN', 'Tạm hoãn'),
    ('MIEN_NVQS', 'Miễn'),
]

STATUS_LABELS = dict(STATUS_OPTIONS)
MAIN_STATUS_FLOW = [
    'CHUA_GOI',
    'KHAM_SO_TUYEN',
    'KHAM_SUC_KHOE',
    'DU_DIEU_KIEN',
    'CHO_NHAP_NGU',
    'DA_NHAP_NGU',
    'DA_XUAT_NGU',
]
SPECIAL_STATUS_CODES = ['TAM_HOAN', 'MIEN_NVQS']


def get_allowed_status_codes(current_status):
    current_status = normalize_text(current_status) or 'CHUA_GOI'

    if current_status == 'MIEN_NVQS':
        return ['MIEN_NVQS']

    if current_status == 'TAM_HOAN':
        return MAIN_STATUS_FLOW + SPECIAL_STATUS_CODES

    if current_status in MAIN_STATUS_FLOW:
        current_index = MAIN_STATUS_FLOW.index(current_status)
        allowed = [current_status]
        if current_index + 1 < len(MAIN_STATUS_FLOW):
            allowed.append(MAIN_STATUS_FLOW[current_index + 1])
        allowed.extend(SPECIAL_STATUS_CODES)
        return allowed

    return ['CHUA_GOI', 'TAM_HOAN', 'MIEN_NVQS']


def is_valid_status_transition(current_status, next_status):
    return normalize_text(next_status) in get_allowed_status_codes(current_status)


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


def get_military_status_counts():
    ensure_military_records()

    counts = {code: 0 for code, _ in STATUS_OPTIONS}
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            '''
            SELECT
                COALESCE(m.service_status, 'CHUA_GOI') AS service_status,
                COUNT(*)
            FROM citizens c
            LEFT JOIN military_service m ON m.citizen_cccd = c.cccd
            GROUP BY COALESCE(m.service_status, 'CHUA_GOI')
            '''
        )
        for status_code, total in cursor.fetchall():
            counts[normalize_text(status_code) or 'CHUA_GOI'] = int(total)
        return counts
    finally:
        cursor.close()
        conn.close()


def get_military_records_limited(limit_per_status=100):
    ensure_military_records()

    try:
        limit_per_status = int(limit_per_status)
    except (TypeError, ValueError):
        limit_per_status = 100

    if limit_per_status <= 0:
        limit_per_status = 100

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        records = []
        for status_code, _ in STATUS_OPTIONS:
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
                WHERE COALESCE(m.service_status, 'CHUA_GOI') = %s
                ORDER BY c.full_name ASC
                LIMIT %s
                ''',
                (status_code, limit_per_status),
            )
            records.extend(format_military_row(row) for row in cursor.fetchall())
        return records
    finally:
        cursor.close()
        conn.close()


def search_military_records(keyword):
    ensure_military_records()

    keyword = normalize_text(keyword)
    if not keyword:
        return get_military_records_limited()

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
            SELECT service_status
            FROM military_service
            WHERE citizen_cccd = %s
            LIMIT 1
            ''',
            (citizen_cccd,),
        )
        current_row = cursor.fetchone()
        current_status = current_row[0] if current_row else 'CHUA_GOI'

        if not is_valid_status_transition(current_status, payload['service_status']):
            allowed_labels = [STATUS_LABELS.get(code, code) for code in get_allowed_status_codes(current_status)]
            return False, 'Chỉ được chuyển sang bước kế tiếp hoặc sang Tạm hoãn/Miễn. Cho phép: {}.'.format(', '.join(allowed_labels))

        if payload['service_status'] in ('TAM_HOAN', 'MIEN_NVQS') and not payload['note']:
            return False, 'Khi chuyển sang Tạm hoãn hoặc Miễn, bắt buộc phải ghi lý do.'

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

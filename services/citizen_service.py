from datetime import date, datetime

from config.database import get_connection
from config.settings import DB_NAME

DISPLAY_DATE_FORMAT = '%d-%m-%Y'
DB_DATE_FORMAT = '%Y-%m-%d'


def normalize_text(value):
    if value is None:
        return ''
    return str(value).strip()


def normalize_int(value):
    raw = normalize_text(value)
    if raw == '':
        return None
    try:
        return int(raw)
    except ValueError:
        return None


def to_db_date(value, allow_empty=False):
    if value in (None, ''):
        if allow_empty:
            return None
        raise ValueError('Ngày sinh không được để trống.')

    if isinstance(value, datetime):
        return value.strftime(DB_DATE_FORMAT)

    if isinstance(value, date):
        return value.strftime(DB_DATE_FORMAT)

    raw_value = normalize_text(value)
    for fmt in (DISPLAY_DATE_FORMAT, DB_DATE_FORMAT):
        try:
            return datetime.strptime(raw_value, fmt).strftime(DB_DATE_FORMAT)
        except ValueError:
            pass

    raise ValueError('Ngày không đúng định dạng. Dùng dd-mm-yyyy.')


def format_display_date(value):
    if not value:
        return ''

    if isinstance(value, datetime):
        return value.strftime(DISPLAY_DATE_FORMAT)

    if isinstance(value, date):
        return value.strftime(DISPLAY_DATE_FORMAT)

    raw_value = normalize_text(value)
    for fmt in (DB_DATE_FORMAT, DISPLAY_DATE_FORMAT):
        try:
            return datetime.strptime(raw_value, fmt).strftime(DISPLAY_DATE_FORMAT)
        except ValueError:
            pass

    return raw_value


def format_citizen_row(row):
    if not row:
        return None

    row['cccd'] = normalize_text(row.get('cccd'))
    row['full_name'] = normalize_text(row.get('full_name'))
    row['date_of_birth'] = format_display_date(row.get('date_of_birth'))
    row['gender'] = normalize_text(row.get('gender'))
    row['phone'] = normalize_text(row.get('phone'))
    row['ward'] = normalize_text(row.get('ward'))
    row['address'] = normalize_text(row.get('address'))
    row['neighborhood'] = normalize_text(row.get('neighborhood'))
    row['education_level'] = normalize_text(row.get('education_level'))
    row['occupation'] = normalize_text(row.get('occupation'))
    row['religion'] = normalize_text(row.get('religion'))
    row['ethnicity'] = normalize_text(row.get('ethnicity'))
    row['photo_path'] = normalize_text(row.get('photo_path'))
    return row


def ensure_background_schema(cursor):
    cursor.execute(
        '''
        SELECT COLUMN_NAME
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'citizen_backgrounds'
        ''',
        (DB_NAME,),
    )
    existing_columns = set()
    for row in cursor.fetchall():
        if isinstance(row, dict):
            existing_columns.add(row.get('COLUMN_NAME', ''))
        else:
            existing_columns.add(row[0])
    required_columns = {
        'father_history_before_1975': 'TEXT NULL',
        'father_history_after_1975': 'TEXT NULL',
        'mother_history_before_1975': 'TEXT NULL',
        'mother_history_after_1975': 'TEXT NULL',
    }

    for column_name, column_definition in required_columns.items():
        if column_name not in existing_columns:
            cursor.execute(
                f'ALTER TABLE citizen_backgrounds ADD COLUMN {column_name} {column_definition}'
            )


def create_citizen(data):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        payload = {
            'cccd': normalize_text(data.get('cccd')),
            'full_name': normalize_text(data.get('full_name')),
            'date_of_birth': to_db_date(data.get('date_of_birth')),
            'gender': normalize_text(data.get('gender')),
            'phone': normalize_text(data.get('phone')),
            'ward': normalize_text(data.get('ward')),
            'address': normalize_text(data.get('address')),
            'neighborhood': normalize_text(data.get('neighborhood')),
            'education_level': normalize_text(data.get('education_level')),
            'occupation': normalize_text(data.get('occupation')),
            'religion': normalize_text(data.get('religion')),
            'ethnicity': normalize_text(data.get('ethnicity')),
        }

        if not payload['cccd'] or not payload['full_name']:
            return False, 'CCCD và họ tên không được để trống.'

        cursor.execute(
            '''
            INSERT INTO citizens (
                cccd,
                full_name,
                date_of_birth,
                gender,
                phone,
                ward,
                address,
                neighborhood,
                education_level,
                occupation,
                religion,
                ethnicity
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''',
            (
                payload['cccd'],
                payload['full_name'],
                payload['date_of_birth'],
                payload['gender'],
                payload['phone'],
                payload['ward'],
                payload['address'],
                payload['neighborhood'],
                payload['education_level'],
                payload['occupation'],
                payload['religion'],
                payload['ethnicity'],
            ),
        )
        conn.commit()
        return True, 'Thêm công dân thành công.'
    except Exception as exc:
        conn.rollback()
        return False, str(exc)
    finally:
        cursor.close()
        conn.close()


def update_citizen(data):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        payload = {
            'cccd': normalize_text(data.get('cccd')),
            'full_name': normalize_text(data.get('full_name')),
            'date_of_birth': to_db_date(data.get('date_of_birth')),
            'gender': normalize_text(data.get('gender')),
            'phone': normalize_text(data.get('phone')),
            'ward': normalize_text(data.get('ward')),
            'address': normalize_text(data.get('address')),
            'neighborhood': normalize_text(data.get('neighborhood')),
            'education_level': normalize_text(data.get('education_level')),
            'occupation': normalize_text(data.get('occupation')),
            'religion': normalize_text(data.get('religion')),
            'ethnicity': normalize_text(data.get('ethnicity')),
        }

        cursor.execute(
            '''
            UPDATE citizens
            SET full_name = %s,
                date_of_birth = %s,
                gender = %s,
                phone = %s,
                ward = %s,
                address = %s,
                neighborhood = %s,
                education_level = %s,
                occupation = %s,
                religion = %s,
                ethnicity = %s
            WHERE cccd = %s
            ''',
            (
                payload['full_name'],
                payload['date_of_birth'],
                payload['gender'],
                payload['phone'],
                payload['ward'],
                payload['address'],
                payload['neighborhood'],
                payload['education_level'],
                payload['occupation'],
                payload['religion'],
                payload['ethnicity'],
                payload['cccd'],
            ),
        )
        conn.commit()
        return True, 'Cập nhật công dân thành công.'
    except Exception as exc:
        conn.rollback()
        return False, str(exc)
    finally:
        cursor.close()
        conn.close()


def delete_citizen(cccd):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('DELETE FROM citizens WHERE cccd = %s', (cccd,))
        conn.commit()
        return True, 'Đã xóa công dân.'
    except Exception as exc:
        conn.rollback()
        return False, str(exc)
    finally:
        cursor.close()
        conn.close()


def get_all_citizens():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            '''
            SELECT
                cccd,
                full_name,
                date_of_birth,
                gender,
                phone,
                ward
            FROM citizens
            ORDER BY full_name ASC
            '''
        )
        rows = cursor.fetchall()
        return [format_citizen_row(row) for row in rows]
    finally:
        cursor.close()
        conn.close()


def search_citizens(keyword):
    keyword = normalize_text(keyword)
    if not keyword:
        return get_all_citizens()

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        like_value = '%{}%'.format(keyword)
        cursor.execute(
            '''
            SELECT
                cccd,
                full_name,
                date_of_birth,
                gender,
                phone,
                ward
            FROM citizens
            WHERE full_name LIKE %s OR cccd LIKE %s OR phone LIKE %s
            ORDER BY full_name ASC
            ''',
            (like_value, like_value, like_value),
        )
        rows = cursor.fetchall()
        return [format_citizen_row(row) for row in rows]
    finally:
        cursor.close()
        conn.close()


def get_citizen(cccd):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute('SELECT * FROM citizens WHERE cccd = %s LIMIT 1', (cccd,))
        row = cursor.fetchone()
        return format_citizen_row(row)
    finally:
        cursor.close()
        conn.close()


def save_background(data):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        ensure_background_schema(cursor)
        payload = {
            'citizen_cccd': normalize_text(data.get('citizen_cccd')),
            'father_name': normalize_text(data.get('father_name')),
            'father_phone': normalize_text(data.get('father_phone')),
            'mother_name': normalize_text(data.get('mother_name')),
            'mother_phone': normalize_text(data.get('mother_phone')),
            'father_history_before_1975': normalize_text(data.get('father_history_before_1975')),
            'father_history_after_1975': normalize_text(data.get('father_history_after_1975')),
            'mother_history_before_1975': normalize_text(data.get('mother_history_before_1975')),
            'mother_history_after_1975': normalize_text(data.get('mother_history_after_1975')),
            'family_status': normalize_text(data.get('family_status')),
            'criminal_record': normalize_text(data.get('criminal_record')),
            'party_union_status': normalize_text(data.get('party_union_status')),
            'notes': normalize_text(data.get('notes')),
        }

        cursor.execute(
            '''
            INSERT INTO citizen_backgrounds (
                citizen_cccd,
                father_name,
                father_phone,
                mother_name,
                mother_phone,
                father_history_before_1975,
                father_history_after_1975,
                mother_history_before_1975,
                mother_history_after_1975,
                family_status,
                criminal_record,
                party_union_status,
                notes
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                father_name = VALUES(father_name),
                father_phone = VALUES(father_phone),
                mother_name = VALUES(mother_name),
                mother_phone = VALUES(mother_phone),
                father_history_before_1975 = VALUES(father_history_before_1975),
                father_history_after_1975 = VALUES(father_history_after_1975),
                mother_history_before_1975 = VALUES(mother_history_before_1975),
                mother_history_after_1975 = VALUES(mother_history_after_1975),
                family_status = VALUES(family_status),
                criminal_record = VALUES(criminal_record),
                party_union_status = VALUES(party_union_status),
                notes = VALUES(notes)
            ''',
            (
                payload['citizen_cccd'],
                payload['father_name'],
                payload['father_phone'],
                payload['mother_name'],
                payload['mother_phone'],
                payload['father_history_before_1975'],
                payload['father_history_after_1975'],
                payload['mother_history_before_1975'],
                payload['mother_history_after_1975'],
                payload['family_status'],
                payload['criminal_record'],
                payload['party_union_status'],
                payload['notes'],
            ),
        )
        conn.commit()
        return True, 'Đã lưu thông tin lý lịch.'
    except Exception as exc:
        conn.rollback()
        return False, str(exc)
    finally:
        cursor.close()
        conn.close()


def get_citizen_background(cccd):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        ensure_background_schema(cursor)
        cursor.execute('SELECT * FROM citizen_backgrounds WHERE citizen_cccd = %s LIMIT 1', (cccd,))
        row = cursor.fetchone()
        if not row:
            return {}
        return row
    finally:
        cursor.close()
        conn.close()


def save_health(data):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        payload = {
            'citizen_cccd': normalize_text(data.get('citizen_cccd')),
            'height': normalize_text(data.get('height')),
            'weight': normalize_text(data.get('weight')),
            'vision': normalize_text(data.get('vision')),
            'blood_pressure': normalize_text(data.get('blood_pressure')),
            'health_type': normalize_text(data.get('health_type')),
        }

        cursor.execute(
            '''
            INSERT INTO citizen_health (
                citizen_cccd,
                height,
                weight,
                vision,
                blood_pressure,
                health_type
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                height = VALUES(height),
                weight = VALUES(weight),
                vision = VALUES(vision),
                blood_pressure = VALUES(blood_pressure),
                health_type = VALUES(health_type)
            ''',
            (
                payload['citizen_cccd'],
                payload['height'],
                payload['weight'],
                payload['vision'],
                payload['blood_pressure'],
                payload['health_type'],
            ),
        )
        conn.commit()
        return True, 'Đã lưu thông tin sức khỏe.'
    except Exception as exc:
        conn.rollback()
        return False, str(exc)
    finally:
        cursor.close()
        conn.close()


def get_citizen_health(cccd):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute('SELECT * FROM citizen_health WHERE citizen_cccd = %s LIMIT 1', (cccd,))
        row = cursor.fetchone()
        if not row:
            return {}
        return row
    finally:
        cursor.close()
        conn.close()


def get_citizen_detail(cccd):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        ensure_background_schema(cursor)
        cursor.execute("SELECT * FROM citizens WHERE cccd = %s", (cccd,))
        citizen = cursor.fetchone()

        if citizen:
            citizen = format_citizen_row(citizen)

        cursor.execute("SELECT * FROM citizen_backgrounds WHERE citizen_cccd = %s", (cccd,))
        background = cursor.fetchone()

        cursor.execute("SELECT * FROM citizen_health WHERE citizen_cccd = %s", (cccd,))
        health = cursor.fetchone()

        return {
            "citizen": citizen or {},
            "background": background or {},
            "health": health or {},
        }
    finally:
        cursor.close()
        conn.close()


def update_citizen_detail(data):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        ensure_background_schema(cursor)
        cccd = normalize_text(data.get("cccd"))

        cursor.execute(
            """
            UPDATE citizens
            SET
                address = %s,
                neighborhood = %s,
                education_level = %s,
                occupation = %s,
                religion = %s,
                ethnicity = %s,
                photo_path = COALESCE(%s, photo_path)
            WHERE cccd = %s
            """,
            (
                normalize_text(data.get("address")),
                normalize_text(data.get("neighborhood")),
                normalize_text(data.get("education_level")),
                normalize_text(data.get("occupation")),
                normalize_text(data.get("religion")),
                normalize_text(data.get("ethnicity")),
                normalize_text(data.get("photo_path")) or None,
                cccd,
            ),
        )

        cursor.execute(
            """
            INSERT INTO citizen_backgrounds (
                citizen_cccd,
                father_name,
                father_phone,
                mother_name,
                mother_phone,
                family_status,
                criminal_record,
                party_union_status,
                birth_registration_place,
                hometown,
                nationality,
                family_permanent_residence,
                current_residence,
                family_component,
                general_education_level,
                training_level,
                training_major,
                party_join_date,
                union_join_date,
                workplace_or_school,
                father_birth_date,
                father_status,
                mother_birth_date,
                mother_status,
                father_history_before_1975,
                father_history_after_1975,
                mother_history_before_1975,
                mother_history_after_1975,
                spouse_info,
                children_info,
                total_male_children,
                total_female_children,
                birth_order
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s,
                %s
            )
            ON DUPLICATE KEY UPDATE
                father_name = VALUES(father_name),
                father_phone = VALUES(father_phone),
                mother_name = VALUES(mother_name),
                mother_phone = VALUES(mother_phone),
                family_status = VALUES(family_status),
                criminal_record = VALUES(criminal_record),
                party_union_status = VALUES(party_union_status),
                birth_registration_place = VALUES(birth_registration_place),
                hometown = VALUES(hometown),
                nationality = VALUES(nationality),
                family_permanent_residence = VALUES(family_permanent_residence),
                current_residence = VALUES(current_residence),
                family_component = VALUES(family_component),
                general_education_level = VALUES(general_education_level),
                training_level = VALUES(training_level),
                training_major = VALUES(training_major),
                party_join_date = VALUES(party_join_date),
                union_join_date = VALUES(union_join_date),
                workplace_or_school = VALUES(workplace_or_school),
                father_birth_date = VALUES(father_birth_date),
                father_status = VALUES(father_status),
                mother_birth_date = VALUES(mother_birth_date),
                mother_status = VALUES(mother_status),
                father_history_before_1975 = VALUES(father_history_before_1975),
                father_history_after_1975 = VALUES(father_history_after_1975),
                mother_history_before_1975 = VALUES(mother_history_before_1975),
                mother_history_after_1975 = VALUES(mother_history_after_1975),
                spouse_info = VALUES(spouse_info),
                children_info = VALUES(children_info),
                total_male_children = VALUES(total_male_children),
                total_female_children = VALUES(total_female_children),
                birth_order = VALUES(birth_order)
            """,
            (
                cccd,
                normalize_text(data.get("father_name")),
                normalize_text(data.get("father_phone")),
                normalize_text(data.get("mother_name")),
                normalize_text(data.get("mother_phone")),
                normalize_text(data.get("family_status")),
                normalize_text(data.get("criminal_record")),
                normalize_text(data.get("party_union_status")),

                normalize_text(data.get("birth_registration_place")),
                normalize_text(data.get("hometown")),
                normalize_text(data.get("nationality")),
                normalize_text(data.get("family_permanent_residence")),
                normalize_text(data.get("current_residence")),
                normalize_text(data.get("family_component")),
                normalize_text(data.get("general_education_level")),
                normalize_text(data.get("training_level")),
                normalize_text(data.get("training_major")),
                normalize_text(data.get("party_join_date")),
                normalize_text(data.get("union_join_date")),
                normalize_text(data.get("workplace_or_school")),

                normalize_text(data.get("father_birth_date")),
                normalize_text(data.get("father_status")),
                normalize_text(data.get("mother_birth_date")),
                normalize_text(data.get("mother_status")),
                normalize_text(data.get("father_history_before_1975")),
                normalize_text(data.get("father_history_after_1975")),
                normalize_text(data.get("mother_history_before_1975")),
                normalize_text(data.get("mother_history_after_1975")),

                normalize_text(data.get("spouse_info")),
                normalize_text(data.get("children_info")),
                normalize_int(data.get("total_male_children")),
                normalize_int(data.get("total_female_children")),
                normalize_text(data.get("birth_order")),
            ),
        )

        cursor.execute(
            """
            INSERT INTO citizen_health (
                citizen_cccd,
                height,
                weight,
                vision,
                blood_pressure,
                health_type
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                height = VALUES(height),
                weight = VALUES(weight),
                vision = VALUES(vision),
                blood_pressure = VALUES(blood_pressure),
                health_type = VALUES(health_type)
            """,
            (
                cccd,
                normalize_text(data.get("height")),
                normalize_text(data.get("weight")),
                normalize_text(data.get("vision")),
                normalize_text(data.get("blood_pressure")),
                normalize_text(data.get("health_type")),
            ),
        )

        conn.commit()
        return True

    except Exception as exc:
        conn.rollback()
        print(exc)
        return False

    finally:
        cursor.close()
        conn.close()

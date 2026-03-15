import json
import zipfile
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET

from config.database import get_connection
from services.citizen_service import ensure_background_schema, normalize_personal_situation_stages

EXCEL_EPOCH = datetime(1899, 12, 30)
XML_NS = {
    'a': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}


def clean_text(value):
    if value is None:
        return ''
    return str(value).replace('\n', ' ').strip()


def is_year_text(value):
    raw = clean_text(value)
    return raw.isdigit() and len(raw) == 4


def excel_serial_to_display_date(value):
    raw = clean_text(value)
    if not raw:
        return ''

    try:
        serial = float(raw)
    except ValueError:
        if is_year_text(raw):
            return f'01-01-{raw}'
        return raw

    date_value = EXCEL_EPOCH + timedelta(days=serial)
    return date_value.strftime('%d-%m-%Y')


def extract_year_from_display_date(date_text):
    raw = clean_text(date_text)
    if not raw:
        return ''
    parts = raw.split('-')
    if len(parts) == 3 and len(parts[-1]) == 4:
        return parts[-1]
    return ''


def read_xlsx_rows(file_path):
    with zipfile.ZipFile(file_path) as workbook_zip:
        shared_strings = []
        if 'xl/sharedStrings.xml' in workbook_zip.namelist():
            shared_root = ET.fromstring(workbook_zip.read('xl/sharedStrings.xml'))
            for item in shared_root.findall('a:si', XML_NS):
                texts = [node.text or '' for node in item.findall('.//a:t', XML_NS)]
                shared_strings.append(''.join(texts))

        workbook_root = ET.fromstring(workbook_zip.read('xl/workbook.xml'))
        rels_root = ET.fromstring(workbook_zip.read('xl/_rels/workbook.xml.rels'))
        rel_map = {rel.attrib['Id']: rel.attrib['Target'] for rel in rels_root}
        first_sheet = workbook_root.find('a:sheets', XML_NS).findall('a:sheet', XML_NS)[0]
        relation_id = first_sheet.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']
        target = rel_map[relation_id]
        if not target.startswith('xl/'):
            target = 'xl/' + target

        sheet_root = ET.fromstring(workbook_zip.read(target))
        sheet_data = sheet_root.find('a:sheetData', XML_NS)

        def get_cell_value(cell):
            cell_type = cell.attrib.get('t')
            value_node = cell.find('a:v', XML_NS)
            if cell_type == 'inlineStr':
                inline_node = cell.find('a:is', XML_NS)
                if inline_node is None:
                    return ''
                texts = [node.text or '' for node in inline_node.findall('.//a:t', XML_NS)]
                return ''.join(texts)
            if value_node is None:
                return ''
            raw_value = value_node.text or ''
            if cell_type == 's':
                index = int(raw_value)
                return shared_strings[index] if 0 <= index < len(shared_strings) else ''
            return raw_value

        rows = []
        for row in sheet_data.findall('a:row', XML_NS):
            rows.append([get_cell_value(cell) for cell in row.findall('a:c', XML_NS)])
        return rows


def make_personal_stages(values, display_birth_date):
    birth_year = extract_year_from_display_date(display_birth_date)
    col_15 = clean_text(values[14] if len(values) > 14 else '')
    col_16 = clean_text(values[15] if len(values) > 15 else '')
    col_17 = clean_text(values[16] if len(values) > 16 else '')
    col_18 = clean_text(values[17] if len(values) > 17 else '')
    col_19 = clean_text(values[18] if len(values) > 18 else '')
    col_20 = clean_text(values[19] if len(values) > 19 else '')
    col_21 = clean_text(values[20] if len(values) > 20 else '')
    col_22 = clean_text(values[21] if len(values) > 21 else '')
    col_23 = clean_text(values[22] if len(values) > 22 else '')
    col_24 = clean_text(values[23] if len(values) > 23 else '')
    col_25 = clean_text(values[24] if len(values) > 24 else '')
    col_26 = clean_text(values[25] if len(values) > 25 else '')

    childhood_from = col_15 if is_year_text(col_15) else birth_year
    childhood_to = col_16 if is_year_text(col_16) else ''
    childhood_content = '' if is_year_text(col_15) else col_15

    stages = [
        {
            'stage': 'Lúc nhỏ',
            'from_year': childhood_from,
            'to_year': childhood_to,
            'content': childhood_content,
        }
    ]

    if col_18 or col_17 or col_16:
        stages.append({
            'stage': 'Cấp 1',
            'from_year': col_16 if is_year_text(col_16) else '',
            'to_year': col_17 if is_year_text(col_17) else '',
            'content': col_18,
        })

    if col_20 or col_19 or col_17:
        stages.append({
            'stage': 'Cấp 2',
            'from_year': col_17 if is_year_text(col_17) else '',
            'to_year': col_19 if is_year_text(col_19) else '',
            'content': col_20,
        })

    if col_22 or col_21 or col_19:
        stages.append({
            'stage': 'Cấp 3',
            'from_year': col_19 if is_year_text(col_19) else '',
            'to_year': col_21 if is_year_text(col_21) else '',
            'content': col_22,
        })

    if col_24 or col_23 or col_21:
        stages.append({
            'stage': 'ĐH-CĐ',
            'from_year': col_21 if is_year_text(col_21) else '',
            'to_year': col_23 if is_year_text(col_23) else '',
            'content': col_24,
        })

    work_content = ' - '.join(part for part in [col_25, col_26] if part)
    if work_content:
        stages.append({
            'stage': 'Đi làm',
            'from_year': '',
            'to_year': '',
            'content': work_content,
        })

    return normalize_personal_situation_stages(stages)


def import_citizens_from_excel(file_path):
    rows = read_xlsx_rows(file_path)
    if len(rows) <= 1:
        return False, 'File Excel không có dữ liệu để import.'

    conn = get_connection()
    cursor = conn.cursor()

    imported_count = 0
    skipped_count = 0

    try:
        ensure_background_schema(cursor)

        for values in rows[1:]:
            cccd = clean_text(values[4] if len(values) > 4 else '')
            full_name = clean_text(values[1] if len(values) > 1 else '')
            if not cccd or not full_name:
                skipped_count += 1
                continue

            display_birth_date = excel_serial_to_display_date(values[3] if len(values) > 3 else '')
            father_birth_year = clean_text(values[27] if len(values) > 27 else '')
            mother_birth_year = clean_text(values[31] if len(values) > 31 else '')
            training_school = clean_text(values[13] if len(values) > 13 else '')
            note_parts = [
                clean_text(values[38] if len(values) > 38 else ''),
                clean_text(values[39] if len(values) > 39 else ''),
            ]

            citizen_payload = (
                cccd,
                full_name,
                display_birth_date,
                '',
                '',
                '',
                clean_text(values[8] if len(values) > 8 else ''),
                '',
                clean_text(values[10] if len(values) > 10 else ''),
                clean_text(values[37] if len(values) > 37 else ''),
                clean_text(values[6] if len(values) > 6 else ''),
                clean_text(values[5] if len(values) > 5 else ''),
            )

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
                VALUES (%s, %s, STR_TO_DATE(NULLIF(%s, ''), '%d-%m-%Y'), %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    full_name = VALUES(full_name),
                    date_of_birth = COALESCE(VALUES(date_of_birth), date_of_birth),
                    address = VALUES(address),
                    education_level = VALUES(education_level),
                    occupation = VALUES(occupation),
                    religion = VALUES(religion),
                    ethnicity = VALUES(ethnicity)
                ''',
                citizen_payload,
            )

            cursor.execute(
                '''
                INSERT INTO citizen_backgrounds (
                    citizen_cccd,
                    hometown,
                    current_residence,
                    family_component,
                    training_level,
                    training_major,
                    workplace_or_school,
                    personal_situation,
                    father_name,
                    father_birth_date,
                    father_occupation,
                    mother_name,
                    mother_birth_date,
                    mother_occupation,
                    notes
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    hometown = VALUES(hometown),
                    current_residence = VALUES(current_residence),
                    family_component = VALUES(family_component),
                    training_level = VALUES(training_level),
                    training_major = VALUES(training_major),
                    workplace_or_school = VALUES(workplace_or_school),
                    personal_situation = VALUES(personal_situation),
                    father_name = VALUES(father_name),
                    father_birth_date = CASE
                        WHEN VALUES(father_birth_date) IS NULL OR VALUES(father_birth_date) = '' THEN father_birth_date
                        ELSE VALUES(father_birth_date)
                    END,
                    father_occupation = VALUES(father_occupation),
                    mother_name = VALUES(mother_name),
                    mother_birth_date = CASE
                        WHEN VALUES(mother_birth_date) IS NULL OR VALUES(mother_birth_date) = '' THEN mother_birth_date
                        ELSE VALUES(mother_birth_date)
                    END,
                    mother_occupation = VALUES(mother_occupation),
                    notes = VALUES(notes)
                ''',
                (
                    cccd,
                    clean_text(values[7] if len(values) > 7 else ''),
                    clean_text(values[8] if len(values) > 8 else ''),
                    clean_text(values[9] if len(values) > 9 else ''),
                    clean_text(values[11] if len(values) > 11 else ''),
                    clean_text(values[12] if len(values) > 12 else ''),
                    training_school,
                    json.dumps(make_personal_stages(values, display_birth_date), ensure_ascii=False),
                    clean_text(values[26] if len(values) > 26 else ''),
                    father_birth_year or None,
                    clean_text(values[29] if len(values) > 29 else ''),
                    clean_text(values[30] if len(values) > 30 else ''),
                    mother_birth_year or None,
                    clean_text(values[33] if len(values) > 33 else ''),
                    ' | '.join(part for part in note_parts if part),
                ),
            )

            imported_count += 1

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
        return True, f'Đã import {imported_count} công dân. Bỏ qua {skipped_count} dòng thiếu CCCD hoặc họ tên.'
    except Exception as exc:
        conn.rollback()
        return False, str(exc)
    finally:
        cursor.close()
        conn.close()

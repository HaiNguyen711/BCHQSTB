from collections import Counter

from config.database import get_connection
from services.citizen_service import extract_neighborhood_from_address
from services.military_service import STATUS_OPTIONS


def _fetch_scalar(cursor, query):
    cursor.execute(query)
    row = cursor.fetchone()
    return int(row[0]) if row and row[0] is not None else 0


def get_dashboard_stats():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        stats = {
            'total_citizens': 0,
            'male_count': 0,
            'female_count': 0,
            'eligible_age_count': 0,
            'military_status_counts': [],
            'neighborhood_counts': [],
        }

        cursor.execute('SELECT COUNT(*) AS total FROM citizens')
        row = cursor.fetchone() or {}
        stats['total_citizens'] = int(row.get('total') or 0)

        cursor.execute(
            '''
            SELECT gender, COUNT(*) AS total
            FROM citizens
            GROUP BY gender
            '''
        )
        for row in cursor.fetchall():
            gender = (row.get('gender') or '').strip().lower()
            total = int(row.get('total') or 0)
            if gender == 'nam':
                stats['male_count'] = total
            elif gender == 'nữ':
                stats['female_count'] = total

        cursor.execute(
            '''
            SELECT COUNT(*) AS total
            FROM citizens
            WHERE date_of_birth IS NOT NULL
              AND TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) BETWEEN 18 AND 27
            '''
        )
        row = cursor.fetchone() or {}
        stats['eligible_age_count'] = int(row.get('total') or 0)

        cursor.execute(
            '''
            SELECT service_status, COUNT(*) AS total
            FROM military_service
            GROUP BY service_status
            '''
        )
        status_totals = {row.get('service_status'): int(row.get('total') or 0) for row in cursor.fetchall()}
        stats['military_status_counts'] = [
            {
                'code': code,
                'label': label,
                'count': status_totals.get(code, 0),
            }
            for code, label in STATUS_OPTIONS
        ]

        cursor.execute(
            '''
            SELECT address, neighborhood
            FROM citizens
            '''
        )
        neighborhood_totals = Counter()
        for row in cursor.fetchall():
            label = extract_neighborhood_from_address(row.get('address'), row.get('neighborhood')) or 'Chưa cập nhật'
            neighborhood_totals[label] += 1

        stats['neighborhood_counts'] = [
            {
                'label': label,
                'count': count,
            }
            for label, count in sorted(neighborhood_totals.items(), key=lambda item: (-item[1], item[0]))
        ]

        return stats
    finally:
        cursor.close()
        conn.close()

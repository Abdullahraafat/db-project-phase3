from db import get_connection


def get_all_gatherings():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT g.gathering_id, g.gathering_name, g.category,
               g.start_datetime, g.end_datetime, v.venue_name
        FROM   GATHERING g
        JOIN   VENUE     v ON g.venue_id = v.venue_id
        ORDER  BY g.start_datetime DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


def add_gathering(gathering_name, category, start_datetime, end_datetime, venue_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO GATHERING (gathering_name, category, start_datetime, end_datetime, venue_id)
           VALUES (?, ?, ?, ?, ?)""",
        (gathering_name, category, start_datetime, end_datetime, venue_id)
    )
    conn.commit()
    conn.close()


def update_gathering(gathering_id, gathering_name, category, start_datetime, end_datetime, venue_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE GATHERING
           SET gathering_name = ?,
               category       = ?,
               start_datetime = ?,
               end_datetime   = ?,
               venue_id       = ?
           WHERE gathering_id = ?""",
        (gathering_name, category, start_datetime, end_datetime, venue_id, gathering_id)
    )
    conn.commit()
    conn.close()


def get_gathering_by_id(gathering_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT gathering_id, gathering_name, category,
                  start_datetime, end_datetime, venue_id
           FROM   GATHERING
           WHERE  gathering_id = ?""",
        (gathering_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return row

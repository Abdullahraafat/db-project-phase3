from db import get_connection


def get_all_venues():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT venue_id, venue_name, location, max_capacity FROM VENUE")
    rows = cursor.fetchall()
    conn.close()
    return rows


def add_venue(venue_name, location, max_capacity):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO VENUE (venue_name, location, max_capacity) VALUES (?, ?, ?)",
        (venue_name, location, max_capacity)
    )
    conn.commit()
    conn.close()


def update_venue(venue_id, venue_name, location, max_capacity):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE VENUE
           SET venue_name   = ?,
               location     = ?,
               max_capacity = ?
           WHERE venue_id   = ?""",
        (venue_name, location, max_capacity, venue_id)
    )
    conn.commit()
    conn.close()


def get_venue_by_id(venue_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT venue_id, venue_name, location, max_capacity FROM VENUE WHERE venue_id = ?",
        (venue_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return row


def get_venues_no_passes_last_month():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT   v.venue_id,
                 v.venue_name,
                 v.location,
                 g.gathering_id,
                 g.gathering_name,
                 g.start_datetime
        FROM     VENUE     v
        JOIN     GATHERING g ON v.venue_id = g.venue_id
        WHERE    MONTH(g.start_datetime) = MONTH(DATEADD(MONTH, -1, GETDATE()))
          AND    YEAR (g.start_datetime) = YEAR (DATEADD(MONTH, -1, GETDATE()))
          AND    g.gathering_id NOT IN (
                     SELECT DISTINCT gec.gathering_id
                     FROM   ENTRY_PASS            ep
                     JOIN   GATHERING_ENTRY_CLASS gec
                            ON ep.gathering_entry_class_id = gec.gathering_entry_class_id
                 )
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

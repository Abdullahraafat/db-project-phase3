from db import get_connection


def get_all_patrons():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT patron_id, patron_name, email, phone FROM PATRON")
    rows = cursor.fetchall()
    conn.close()
    return rows


def add_patron(patron_name, email, phone):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO PATRON (patron_name, email, phone) VALUES (?, ?, ?)",
        (patron_name, email, phone)
    )
    conn.commit()
    conn.close()


def update_patron(patron_id, patron_name, email, phone):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE PATRON
           SET patron_name = ?,
               email       = ?,
               phone       = ?
           WHERE patron_id = ?""",
        (patron_name, email, phone, patron_id)
    )
    conn.commit()
    conn.close()


def get_patron_by_id(patron_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT patron_id, patron_name, email, phone FROM PATRON WHERE patron_id = ?",
        (patron_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return row

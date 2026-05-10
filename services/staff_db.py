from db import get_connection


def get_all_staff():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT staff_id, staff_name, role, email FROM STAFF")
    rows = cursor.fetchall()
    conn.close()
    return rows


def add_staff(staff_name, role, email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO STAFF (staff_name, role, email) VALUES (?, ?, ?)",
        (staff_name, role, email)
    )
    conn.commit()
    conn.close()


def update_staff(staff_id, staff_name, role, email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE STAFF
           SET staff_name = ?,
               role       = ?,
               email      = ?
           WHERE staff_id = ?""",
        (staff_name, role, email, staff_id)
    )
    conn.commit()
    conn.close()


def get_staff_by_id(staff_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT staff_id, staff_name, role, email FROM STAFF WHERE staff_id = ?",
        (staff_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return row

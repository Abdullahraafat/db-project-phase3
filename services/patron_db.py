from db import get_connection


def get_all_Patrons():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT PatronID, FirstName, Email, Phone FROM PATRON")
    rows = cursor.fetchall()
    conn.close()
    return rows


def add_Patron(Patron_name, Email, Phone):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO PATRON (Patron_name, Email, Phone) VALUES (?, ?, ?)",
        (Patron_name, Email, Phone)
    )
    conn.commit()
    conn.close()


def update_Patron(PatronID, Patron_name, Email, Phone):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE PATRON
           SET Patron_name = ?,
               Email       = ?,
               Phone       = ?
           WHERE PatronID = ?""",
        (Patron_name, Email, Phone, PatronID)
    )
    conn.commit()
    conn.close()


def get_Patron_by_id(PatronID):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT PatronID, FirstName, Email, Phone FROM PATRON WHERE PatronID = ?",
        (PatronID,)
    )
    row = cursor.fetchone()
    conn.close()
    return row

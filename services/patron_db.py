from db import get_connection


def get_all_patrons():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT PatronID, FirstName, LastName, Email, Phone FROM dbo.Patron"
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_patron_by_id(patron_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT PatronID, FirstName, LastName, Email, Phone "
        "FROM dbo.Patron WHERE PatronID = ?",
        (patron_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return row



def add_patron(first_name, last_name, email, phone):
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO dbo.Patron (FirstName, LastName, Email, Phone)
        VALUES (?, ?, ?, ?)
        """,
        (first_name, last_name, email, phone)
    )
    conn.commit()
    conn.close()


def add_entry_pass(patron_id, gathering_entry_class_id, seat_number, price_paid):
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO dbo.EntryPass
               (PatronID, GatheringEntryClassID, PassStatus, SeatNumber, PricePaid)
        VALUES (?, ?, 'Purchased', ?, ?)
        """,
        (patron_id, gathering_entry_class_id, seat_number, price_paid)
    )
    conn.commit()
    conn.close()



def cancel_entry_pass(entry_pass_id):
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        DELETE FROM dbo.EntryPass
        WHERE  EntryPassID = ?
          AND  PassStatus  = 'Purchased'
        """,
        (entry_pass_id,)
    )
    conn.commit()
    conn.close()



def get_patrons_no_passes_last_month():
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT  p.PatronID,
                p.FirstName,
                p.LastName,
                p.Email,
                p.Phone,
                p.RegistrationDate
        FROM    dbo.Patron AS p
        WHERE   MONTH(p.RegistrationDate) = MONTH(DATEADD(MONTH, -1, GETDATE()))
          AND   YEAR (p.RegistrationDate) = YEAR (DATEADD(MONTH, -1, GETDATE()))
          AND   p.PatronID NOT IN (
                    SELECT DISTINCT ep.PatronID
                    FROM   dbo.EntryPass AS ep
                    WHERE  MONTH(ep.PurchaseDate) = MONTH(DATEADD(MONTH, -1, GETDATE()))
                      AND  YEAR (ep.PurchaseDate) = YEAR (DATEADD(MONTH, -1, GETDATE()))
                )
        ORDER   BY p.LastName, p.FirstName
        """
    )
    rows = cursor.fetchall()
    conn.close()
    return rows



def get_patron_spending():
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT  p.PatronID,
                p.FirstName,
                p.LastName,
                ISNULL(SUM(ep.PricePaid), 0) AS TotalSpent,
                COUNT(ep.EntryPassID) AS PassCount
        FROM    dbo.Patron    AS p
        LEFT JOIN dbo.EntryPass AS ep ON p.PatronID = ep.PatronID
        GROUP   BY p.PatronID, p.FirstName, p.LastName
        ORDER   BY TotalSpent DESC
        """
    )
    rows = cursor.fetchall()
    conn.close()
    return rows

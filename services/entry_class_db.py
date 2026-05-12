from db import get_connection


def get_all_entry_classes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT EntryClassID, ClassName FROM dbo.EntryClass")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_all_gec_records():
    """Return GatheringEntryClass rows with human-readable names for the dropdown."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT  gec.GatheringEntryClassID,
                g.GatheringName,
                ec.ClassName,
                gec.SetPrice,
                gec.AllocatedSeats
        FROM    dbo.GatheringEntryClass AS gec
        JOIN    dbo.Gathering           AS g  ON gec.GatheringID  = g.GatheringID
        JOIN    dbo.EntryClass          AS ec ON gec.EntryClassID = ec.EntryClassID
        ORDER   BY g.GatheringName, ec.ClassName
        """
    )
    rows = cursor.fetchall()
    conn.close()
    return rows



def add_gathering_entry_class(gathering_id, entry_class_id, price, allocated_seats):
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO dbo.GatheringEntryClass
               (GatheringID, EntryClassID, SetPrice, AllocatedSeats)
        VALUES (?, ?, ?, ?)
        """,
        (gathering_id, entry_class_id, price, allocated_seats)
    )
    conn.commit()
    conn.close()



def update_gathering_entry_class(gec_id, price, allocated_seats):
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE dbo.GatheringEntryClass
        SET    SetPrice       = ?,
               AllocatedSeats = ?
        WHERE  GatheringEntryClassID = ?
        """,
        (price, allocated_seats, gec_id)
    )
    conn.commit()
    conn.close()



def get_most_popular_category():
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT  TOP (1) WITH TIES
                gc.CategoryName,
                COUNT(ep.EntryPassID) AS EntryPassesSold
        FROM    dbo.GatheringCategory  AS gc
        JOIN    dbo.Gathering           AS g   ON gc.CategoryID             = g.CategoryID
        JOIN    dbo.GatheringEntryClass AS gec ON g.GatheringID            = gec.GatheringID
        JOIN    dbo.EntryPass           AS ep  ON gec.GatheringEntryClassID = ep.GatheringEntryClassID
        WHERE   ep.PassStatus IN ('Purchased', 'CheckedIn')
        GROUP   BY gc.CategoryName
        ORDER   BY EntryPassesSold DESC
        """
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_entry_classes_per_gathering():
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT  g.GatheringName,
                ec.ClassName,
                gec.SetPrice,
                gec.AllocatedSeats
        FROM    dbo.Gathering           AS g
        JOIN    dbo.GatheringEntryClass AS gec ON g.GatheringID   = gec.GatheringID
        JOIN    dbo.EntryClass          AS ec  ON gec.EntryClassID = ec.EntryClassID
        ORDER   BY g.GatheringName, ec.ClassName
        """
    )
    rows = cursor.fetchall()
    conn.close()
    return rows

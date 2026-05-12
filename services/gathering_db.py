from db import get_connection


def get_all_gatherings():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT  g.GatheringID, g.GatheringName, gc.CategoryName,
                g.StartDateTime, g.EndDateTime, v.VenueName
        FROM    dbo.Gathering         AS g
        JOIN    dbo.GatheringCategory AS gc ON g.CategoryID = gc.CategoryID
        JOIN    dbo.Venue             AS v  ON g.VenueID    = v.VenueID
        ORDER   BY g.StartDateTime DESC
        """
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_gathering_by_id(gathering_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT  g.GatheringID, g.GatheringName, gc.CategoryName,
                g.StartDateTime, g.EndDateTime, g.VenueID
        FROM    dbo.Gathering         AS g
        JOIN    dbo.GatheringCategory AS gc ON g.CategoryID = gc.CategoryID
        WHERE   g.GatheringID = ?
        """,
        (gathering_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return row


def get_or_create_category(cursor, category_name):
    cursor.execute(
        "SELECT CategoryID FROM dbo.GatheringCategory WHERE CategoryName = ?",
        (category_name,)
    )
    row = cursor.fetchone()
    if row:
        return row.CategoryID

    cursor.execute(
        "INSERT INTO dbo.GatheringCategory (CategoryName) VALUES (?)",
        (category_name,)
    )
    cursor.execute(
        "SELECT CategoryID FROM dbo.GatheringCategory WHERE CategoryName = ?",
        (category_name,)
    )
    row = cursor.fetchone()
    return row.CategoryID



def add_gathering(gathering_name, category, start_datetime, end_datetime, venue_id):
    
    conn = get_connection()
    cursor = conn.cursor()
    category_id = get_or_create_category(cursor, category)
    cursor.execute(
        """
        INSERT INTO dbo.Gathering
               (GatheringName, CategoryID, StartDateTime, EndDateTime, VenueID)
        VALUES (?, ?, ?, ?, ?)
        """,
        (gathering_name, category_id, start_datetime, end_datetime, venue_id)
    )
    conn.commit()
    conn.close()



def update_gathering(gathering_id, gathering_name, category,
                     start_datetime, end_datetime, venue_id):
   
    conn = get_connection()
    cursor = conn.cursor()
    category_id = get_or_create_category(cursor, category)
    cursor.execute(
        """
        UPDATE dbo.Gathering
        SET    GatheringName = ?,
               CategoryID    = ?,
               StartDateTime = ?,
               EndDateTime   = ?,
               VenueID       = ?
        WHERE  GatheringID   = ?
        """,
        (gathering_name, category_id, start_datetime, end_datetime, venue_id, gathering_id)
    )
    conn.commit()
    conn.close()

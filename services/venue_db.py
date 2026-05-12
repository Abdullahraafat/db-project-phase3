from db import get_connection


def get_all_venues():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT VenueID, VenueName, Location, MaxSeatingCapacity FROM dbo.Venue"
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_venue_by_id(venue_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT VenueID, VenueName, Location, MaxSeatingCapacity "
        "FROM dbo.Venue WHERE VenueID = ?",
        (venue_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return row



def add_venue(venue_name, location, max_capacity):
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO dbo.Venue (VenueName, Location, MaxSeatingCapacity)
        VALUES (?, ?, ?)
        """,
        (venue_name, location, max_capacity)
    )
    conn.commit()
    conn.close()



def update_venue(venue_id, venue_name, location, max_capacity):
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE dbo.Venue
        SET    VenueName          = ?,
               Location           = ?,
               MaxSeatingCapacity = ?
        WHERE  VenueID            = ?
        """,
        (venue_name, location, max_capacity, venue_id)
    )
    conn.commit()
    conn.close()


def get_venues_no_passes_last_month():
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT  v.VenueID,
                v.VenueName,
                v.Location,
                g.GatheringID,
                g.GatheringName,
                g.StartDateTime
        FROM    dbo.Venue     AS v
        JOIN    dbo.Gathering AS g ON v.VenueID = g.VenueID
        WHERE   MONTH(g.StartDateTime) = MONTH(DATEADD(MONTH, -1, GETDATE()))
          AND   YEAR (g.StartDateTime) = YEAR (DATEADD(MONTH, -1, GETDATE()))
          AND   g.GatheringID NOT IN (
                    SELECT DISTINCT gec.GatheringID
                    FROM   dbo.EntryPass            AS ep
                    JOIN   dbo.GatheringEntryClass  AS gec
                           ON ep.GatheringEntryClassID = gec.GatheringEntryClassID
                    WHERE  ep.PassStatus IN ('Purchased', 'CheckedIn')
                )
        ORDER   BY v.VenueName, g.StartDateTime
        """
    )
    rows = cursor.fetchall()
    conn.close()
    return rows
from db import get_connection



def get_all_staff():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT StaffID, FirstName, LastName, Email FROM dbo.Staff"
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_all_assignments():
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT  sa.AssignmentID,
                CONCAT(s.FirstName, ' ', s.LastName) AS StaffName,
                g.GatheringName                     AS GatheringName,
                sa.AssignmentRole
        FROM    dbo.StaffAssignment AS sa
        JOIN    dbo.Staff           AS s  ON sa.StaffID     = s.StaffID
        JOIN    dbo.Gathering       AS g  ON sa.GatheringID = g.GatheringID
        ORDER   BY g.StartDateTime, s.LastName
        """
    )
    rows = cursor.fetchall()
    conn.close()
    return rows



def add_staff(first_name, last_name, email):
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO dbo.Staff (FirstName, LastName, Email)
        VALUES (?, ?, ?)
        """,
        (first_name, last_name, email)
    )
    conn.commit()
    conn.close()


def assign_staff_to_gathering(staff_id, gathering_id, role='Coordinator', is_primary=0):
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO dbo.StaffAssignment (StaffID, GatheringID, AssignmentRole, IsPrimary)
        VALUES (?, ?, ?, ?)
        """,
        (staff_id, gathering_id, role, is_primary)
    )
    conn.commit()
    conn.close()


def remove_assignment(assignment_id):
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        DELETE FROM dbo.StaffAssignment
        WHERE  AssignmentID = ?
        """,
        (assignment_id,)
    )
    conn.commit()
    conn.close()



def get_top_coordinator_last_month():
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT  TOP (1) WITH TIES
                CONCAT(s.FirstName, ' ', s.LastName) AS CoordinatorName,
                COUNT(DISTINCT g.GatheringID)        AS GatheringsManaged
        FROM    dbo.Staff           AS s
        JOIN    dbo.StaffAssignment AS sa ON s.StaffID     = sa.StaffID
        JOIN    dbo.Gathering       AS g  ON sa.GatheringID = g.GatheringID
        WHERE   sa.AssignmentRole = 'Coordinator'
          AND   MONTH(g.StartDateTime) = MONTH(GETDATE())
          AND   YEAR (g.StartDateTime) = YEAR(GETDATE())
        GROUP   BY s.StaffID, s.FirstName, s.LastName
        ORDER   BY GatheringsManaged DESC
        """
    )
    row = cursor.fetchone()
    conn.close()
    return row

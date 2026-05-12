from flask import Blueprint, render_template, request, redirect, url_for
import pyodbc

staff_bp = Blueprint('staff', __name__)

def get_db_connection():
    conn_str = (
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=localhost;"
        "Database=PremiumEventVenueDB;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )
    return pyodbc.connect(conn_str)

@staff_bp.route('/staff')
def manage_staff():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT StaffID, FirstName, LastName FROM dbo.Staff")
    staff_list = cursor.fetchall()
    
    cursor.execute("SELECT GatheringID, GatheringName FROM dbo.Gathering")
    events = cursor.fetchall()

    cursor.execute("""
        SELECT sa.AssignmentID, s.FirstName + ' ' + s.LastName, g.GatheringName, sa.AssignmentRole
        FROM dbo.StaffAssignment sa
        JOIN dbo.Staff s ON sa.StaffID = s.StaffID
        JOIN dbo.Gathering g ON sa.GatheringID = g.GatheringID
    """)
    schedule = cursor.fetchall()
    cursor.execute("""
        SELECT TOP (1) WITH TIES
            CONCAT(s.FirstName, ' ', s.LastName) AS CoordinatorName,
            COUNT(DISTINCT g.GatheringID) AS GatheringsManaged
        FROM dbo.Staff AS s
        INNER JOIN dbo.StaffAssignment AS sa ON s.StaffID = sa.StaffID
        INNER JOIN dbo.Gathering AS g ON sa.GatheringID = g.GatheringID
        WHERE sa.AssignmentRole = 'Coordinator'
          AND sa.IsPrimary = 1
        GROUP BY s.StaffID, s.FirstName, s.LastName
        ORDER BY GatheringsManaged DESC
    """)
    top_coord = cursor.fetchone()

    conn.close()
    return render_template('staff_list.html', 
                           staff=staff_list, 
                           gatherings=events, 
                           schedule=schedule, 
                           top_coord=top_coord)

@staff_bp.route('/add-staff', methods=['POST'])
def add_new_staff():
    f_name = request.form.get('first_name')
    l_name = request.form.get('last_name')
    email = request.form.get('email')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO dbo.Staff (FirstName, LastName, Email) VALUES (?, ?, ?)", 
                   (f_name, l_name, email))
    conn.commit()
    conn.close()
    return redirect(url_for('staff.manage_staff'))

@staff_bp.route('/assign-staff', methods=['POST'])
def assign_staff():
    s_id = request.form.get('staff_id')
    g_id = request.form.get('gathering_id')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO dbo.StaffAssignment (GatheringID, StaffID, AssignmentRole, IsPrimary) 
        VALUES (?, ?, 'Coordinator', 0)""", (g_id, s_id))
    conn.commit()
    conn.close()
    return redirect(url_for('staff.manage_staff'))

@staff_bp.route('/remove-assignment/<int:id>', methods=['POST'])
def remove_assignment(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM dbo.StaffAssignment WHERE AssignmentID = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('staff.manage_staff'))

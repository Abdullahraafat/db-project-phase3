from flask import Blueprint, render_template, request, redirect
from db import get_connection

entry_bp = Blueprint('entry_bp', __name__)

# =====================================
# ADD ENTRY CLASS
# =====================================

@entry_bp.route('/add_entry_class', methods=['GET', 'POST'])
def add_entry_class():

    if request.method == 'POST':

        gathering_id = request.form['gathering_id']
        entry_class_id = request.form['entry_class_id']
        price = request.form['price']
        allocated_seats = request.form['allocated_seats']

        conn = get_connection()
        cursor = conn.cursor()

        # UPDATED: Matches new table dbo.GatheringEntryClass and column SetPrice
        sql = """
        INSERT INTO dbo.GatheringEntryClass
        (GatheringID, EntryClassID, SetPrice, AllocatedSeats)
        VALUES (?, ?, ?, ?)
        """

        values = (
            gathering_id,
            entry_class_id,
            price,
            allocated_seats
        )

        try:
            cursor.execute(sql, values)
            conn.commit()
        except Exception as e:
            return f"Error: {e}"
        finally:
            cursor.close()
            conn.close()

        return redirect('/')

    # GET REQUEST PART
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT GatheringID, GatheringName
        FROM dbo.Gathering
    """)
    gatherings = cursor.fetchall()

    cursor.execute("""
        SELECT EntryClassID, ClassName
        FROM dbo.EntryClass
    """)
    entry_classes = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'add_entry_class.html',
        gatherings=gatherings,
        entry_classes=entry_classes
    )


# =====================================
# UPDATE ENTRY CLASS
# =====================================

@entry_bp.route('/update_entry_class', methods=['GET', 'POST'])
def update_entry_class():

    if request.method == 'POST':

        gec_id = request.form['gec_id']
        price = request.form['price']
        allocated_seats = request.form['allocated_seats']

        conn = get_connection()
        cursor = conn.cursor()

        sql = """
        UPDATE dbo.GatheringEntryClass
        SET SetPrice = ?,
            AllocatedSeats = ?
        WHERE GatheringEntryClassID = ?
        """

        values = (
            price,
            allocated_seats,
            gec_id
        )

        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/')

    # GET REQUEST PART
    conn = get_connection()
    cursor = conn.cursor()

    # Fetch the ID along with the Gathering and Class names so the user knows what they are picking
    cursor.execute("""
        SELECT 
            gec.GatheringEntryClassID, 
            g.GatheringName, 
            ec.ClassName
        FROM dbo.GatheringEntryClass gec
        JOIN dbo.Gathering g ON gec.GatheringID = g.GatheringID
        JOIN dbo.EntryClass ec ON gec.EntryClassID = ec.EntryClassID
    """)
    
    gec_records = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return render_template('update_entry_class.html', gec_records=gec_records)


# =====================================
# INQUIRY 1
# =====================================

@entry_bp.route('/inquiry1')
def inquiry1():

    conn = get_connection()
    cursor = conn.cursor()

    # UPDATED: Matches new Inquiry 1 logic from your SQL script
    sql = """
    SELECT TOP (1) WITH TIES
        gc.CategoryName,
        COUNT(ep.EntryPassID) AS EntryPassesSold
    FROM dbo.GatheringCategory AS gc
    INNER JOIN dbo.Gathering AS g
        ON gc.CategoryID = g.CategoryID
    INNER JOIN dbo.GatheringEntryClass AS gec
        ON g.GatheringID = gec.GatheringID
    INNER JOIN dbo.EntryPass AS ep
        ON gec.GatheringEntryClassID = ep.GatheringEntryClassID
    WHERE ep.PassStatus IN ('Purchased', 'CheckedIn')
    GROUP BY gc.CategoryName
    ORDER BY EntryPassesSold DESC
    """

    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template(
        'inquiry1.html',
        result=result
    )


# =====================================
# INQUIRY 5
# =====================================

@entry_bp.route('/inquiry5')
def inquiry5():

    conn = get_connection()
    cursor = conn.cursor()

    # UPDATED: Matches new Inquiry 5 table joins and columns
    sql = """
    SELECT
        g.GatheringName,
        ec.ClassName,
        gec.SetPrice,
        gec.AllocatedSeats
    FROM dbo.Gathering AS g
    INNER JOIN dbo.GatheringEntryClass AS gec
        ON g.GatheringID = gec.GatheringID
    INNER JOIN dbo.EntryClass AS ec
        ON gec.EntryClassID = ec.EntryClassID
    """

    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template(
        'inquiry5.html',
        result=result
    )

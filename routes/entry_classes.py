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

        sql = """
        INSERT INTO GATHERING_ENTRY_CLASS
        (gathering_id, entry_class_id, price, allocated_seats)
        VALUES (%s, %s, %s, %s)
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
        SELECT gathering_id, gathering_name
        FROM GATHERING
    """)
    gatherings = cursor.fetchall()

    cursor.execute("""
        SELECT entry_class_id, class_name
        FROM ENTRY_CLASS
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
        UPDATE GATHERING_ENTRY_CLASS
        SET price = %s,
            allocated_seats = %s
        WHERE gathering_entry_class_id = %s
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

    return render_template('update_entry_class.html')


# =====================================
# INQUIRY 1
# =====================================

@entry_bp.route('/inquiry1')
def inquiry1():

    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    SELECT
        g.category,
        COUNT(ep.entry_pass_id) AS total_passes
    FROM GATHERING g
    JOIN GATHERING_ENTRY_CLASS gec
        ON g.gathering_id = gec.gathering_id
    JOIN ENTRY_PASS ep
        ON gec.gathering_entry_class_id = ep.gathering_entry_class_id
    GROUP BY g.category
    ORDER BY total_passes DESC
    LIMIT 1
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

    sql = """
SELECT
    g.gathering_name,
    ec.class_name,
    gec.price,
    gec.allocated_seats
FROM GATHERING g
JOIN GATHERING_ENTRY_CLASS gec
    ON g.gathering_id = gec.gathering_id
JOIN ENTRY_CLASS ec
    ON gec.entry_class_id = ec.entry_class_id
"""

    cursor.execute(sql)

    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'inquiry5.html',
        result=result
    )
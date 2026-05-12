from flask import Blueprint, render_template, request, redirect
import pyodbc

patrons_bp = Blueprint('patrons', __name__)

# Database Connection
def get_db_connection():

    conn = pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=localhost;'
        'DATABASE=PremiumEventVenueDB;'
        'Trusted_Connection=yes;'
    )

    return conn


# -----------------------------------
# Patron Registration
# -----------------------------------

@patrons_bp.route('/register_patron', methods=['GET', 'POST'])
def register_patron():

    if request.method == 'POST':

        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO Patron
        (FirstName, LastName, Email, Phone)
        VALUES (?, ?, ?, ?)
        """

        cursor.execute(query,
                       (first_name,
                        last_name,
                        email,
                        phone))

        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('patrons/register_patron.html')


# -----------------------------------
# Purchase Entry Pass
# -----------------------------------

@patrons_bp.route('/purchase_pass', methods=['GET', 'POST'])
def purchase_pass():

    if request.method == 'POST':

        patron_id = request.form['patron_id']
        gathering_entry_class_id = request.form['gathering_entry_class_id']
        seat_number = request.form['seat_number']
        price_paid = request.form['price_paid']

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO EntryPass
        (PatronID, GatheringEntryClassID, PassStatus, SeatNumber, PricePaid)
        VALUES (?, ?, 'Purchased', ?, ?)
        """

        cursor.execute(query,
                       (patron_id,
                        gathering_entry_class_id,
                        seat_number,
                        price_paid))

        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('patrons/purchase_pass.html')


# -----------------------------------
# Cancel Pass
# -----------------------------------

@patrons_bp.route('/cancel_pass/<int:entry_pass_id>')
def cancel_pass(entry_pass_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    DELETE FROM EntryPass
    WHERE EntryPassID = ?
    AND PassStatus = 'Purchased'
    """

    cursor.execute(query, (entry_pass_id,))

    conn.commit()
    conn.close()

    return redirect('/')
from flask import Blueprint, render_template, request, redirect, url_for
from services.patron_db import (
    add_patron, add_entry_pass, cancel_entry_pass,
    get_patrons_no_passes_last_month, get_patron_spending,
)

patrons_bp = Blueprint('patrons', __name__)


@patrons_bp.route('/register_patron', methods=['GET', 'POST'])
def register_patron():
    if request.method == 'POST':
        add_patron(
            request.form['first_name'],
            request.form['last_name'],
            request.form['email'],
            request.form.get('phone', ''),
        )
        return redirect(url_for('patrons.register_patron'))
    return render_template('patrons/register_patron.html')


@patrons_bp.route('/purchase_pass', methods=['GET', 'POST'])
def purchase_pass():
    if request.method == 'POST':
        add_entry_pass(
            request.form['patron_id'],
            request.form['gathering_entry_class_id'],
            request.form.get('seat_number', ''),
            request.form['price_paid'],
        )
        return redirect(url_for('patrons.purchase_pass'))
    return render_template('patrons/purchase_pass.html')


@patrons_bp.route('/cancel_pass/<int:entry_pass_id>', methods=['POST'])
def cancel_pass(entry_pass_id):
    cancel_entry_pass(entry_pass_id)
    return redirect(url_for('patrons.purchase_pass'))


@patrons_bp.route('/inquiry4')
def inquiry4():
    patrons = get_patrons_no_passes_last_month()
    return render_template('patrons/inquiry4.html', patrons=patrons)


@patrons_bp.route('/inquiry6')
def inquiry6():
    patrons = get_patron_spending()
    return render_template('patrons/inquiry6.html', patrons=patrons)